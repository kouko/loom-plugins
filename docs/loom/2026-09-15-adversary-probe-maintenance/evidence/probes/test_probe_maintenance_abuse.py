"""Adversarial probes for `2026-09-15-adversary-probe-maintenance`.

The change lets Build re-dispatch the adversary to update its own stale
programs, and tells the adversary to reuse existing probes and tests first.
These probes try to make that change fail:

* mutation runs of the new pins in `test_build_mechanical_checks.py`: each
  mutation removes or loosens one guard sentence in a scratch copy of the
  changed files and runs the committed test module against it; a mutant the
  module still passes is a vacuous pin;
* readings of the new Build exception that an agent under time pressure
  could exploit (a real defect relabelled "stale", a probe rewritten to
  accept the defect, reuse of the implementer's own tests as the
  adversarial floor, staleness that does not come from a fix).

Probes that hold pass. Probes that land a finding fail on purpose and name
the finding in their assertion message. Everything runs read-only against
committed content; mutations touch only a copy under `tmp_path`.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "loom-code").is_dir() and (candidate / "loom-design").is_dir():
            return candidate
    raise RuntimeError(f"could not locate repo root above {start}")


REPO = _find_repo_root(Path(__file__).parent)
sys.path.insert(0, str(REPO / "loom-code/scripts"))
from prose_pin import has_negation, split_sentences  # noqa: E402

BUILD = "loom-code/skills/build/SKILL.md"
ADVERSARY = "loom-code/agents/adversary.md"
REF = "loom-code/skills/closing-review/references/adversarial.md"
TEST_MODULE = "loom-code/scripts/test_build_mechanical_checks.py"
COPIED = [BUILD, ADVERSARY, REF, TEST_MODULE, "loom-code/scripts/prose_pin.py"]


def _flat(rel: str) -> str:
    text = (REPO / rel).read_text(encoding="utf-8")
    return " ".join(re.sub(r"^> ?", "", text, flags=re.M).split())


def _ws(literal: str) -> re.Pattern[str]:
    """Match `literal` across the line wraps of the source file."""
    return re.compile(r"\s+".join(re.escape(w) for w in literal.split()))


def _scratch(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for rel in COPIED:
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, dest)
    return root


def _run_pins(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(root / TEST_MODULE)],
        cwd=root / "loom-code/scripts",
        capture_output=True,
        text=True,
        timeout=300,
    )


def _mutate(root: Path, rel: str, old: str, new: str) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    mutated, count = _ws(old).subn(new, text)
    assert count == 1, f"mutation anchor not found exactly once in {rel}: {old!r} ({count})"
    path.write_text(mutated, encoding="utf-8")


# (id, file, old text, replacement, whether the pins should kill it)
MUTATIONS = [
    # Controls: guards the pins do cover. A mutant surviving here is a vacuous pin.
    ("drop-fresh-context", BUILD, "agent fresh-context again to update", "agent again to update", True),
    ("drop-handoff-reason", BUILD, "each adversary re-dispatch with its reason, ", "", True),
    ("drop-red-then-reverted", ADVERSARY,
     "Each mutation must turn the probe RED and is then reverted;", "", True),
    ("loosen-ref-reuse-sentence", REF,
     "It reuses a program that covers a case,", "It may write new probes freely,", True),
    # Guards the exception relies on to refuse a defect relabelled as stale.
    ("drop-product-defect-guard", BUILD,
     "fails or needs changing for that reason, rather than for a product defect it correctly caught,",
     "fails for any reason,", True),
    ("drop-build-decides-defect-fix", BUILD,
     "Build decides which case applies from the program's failure and the widened scope, "
     "and fixes a product defect in the product as above.", "", True),
    ("drop-rerun-after-update", BUILD,
     "After the update, Build repeats these end-of-Build checks.", "", True),
    ("orchestrator-may-modify-program", BUILD,
     "Implementers and the orchestrator never edit an adversarial program.",
     "Implementers and the orchestrator never edit an adversarial program. "
     "When time is short, the orchestrator may modify a stale adversarial program itself.", True),
]


def test_pins_scratch_copy_unmutated_passes(tmp_path: Path) -> None:
    """Control: the committed pin module passes on an unmutated scratch copy."""
    result = _run_pins(_scratch(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "mutation_id,rel,old,new,should_kill", MUTATIONS, ids=[m[0] for m in MUTATIONS]
)
def test_pins_guard_mutation_killed(
    tmp_path: Path, mutation_id: str, rel: str, old: str, new: str, should_kill: bool
) -> None:
    """Each guard-removing mutation turns the committed pin module RED."""
    root = _scratch(tmp_path)
    _mutate(root, rel, old, new)
    result = _run_pins(root)
    killed = result.returncode != 0
    assert killed == should_kill, (
        f"FINDING vacuous-pin ({mutation_id}): {rel} mutant survived "
        f"test_build_mechanical_checks.py; the guard is stated but no pin fails when it is "
        f"removed or loosened.\n{result.stdout[-800:]}"
    )


# --- Readings of the exception an agent could exploit -----------------------

_DEFECT_TOKENS = ("product defect", "correctly caught", "real defect")
_KEEP_VERBS = re.compile(r"\b(keeps?|leaves?|reports?|returns?|refuses?|flags?|stops?)\b", re.I)


def _affirms_defect_handling(section: str) -> bool:
    """Some sentence affirmatively tells the updater what to do with a program that
    caught a product defect (keep it RED, report it), without a negation token."""
    for s in split_sentences(section):
        if any(t in s for t in _DEFECT_TOKENS) and _KEEP_VERBS.search(s) and not has_negation(s):
            return True
    return False


def test_defect_handling_helper_synthetic() -> None:
    """Self-test: one affirmative example accepted, one negated example rejected."""
    assert _affirms_defect_handling(
        "When the failing program caught a product defect, keep it as it is and report a finding."
    )
    assert not _affirms_defect_handling(
        "When the failing program caught a product defect, do not keep it and never report it."
    )


def _update_section(rel: str) -> str:
    text = _flat(rel)
    if rel == ADVERSARY:
        return text.split("**Updating your own programs.**", 1)[1].split("## What you return", 1)[0]
    return text.split("## Reuse first, update with evidence", 1)[1].split("## Code", 1)[0]


def test_adversary_update_defect_relabelled_stale_kept_red() -> None:
    """The re-dispatched adversary is told to keep a program that caught a real defect.

    Build alone classifies a failure as stale or as a defect, and the adversary
    receives only the failing output. Unless the adversary's own contract tells it
    to keep a defect-catching program RED and report it, a defect Build mislabels as
    stale is 'updated' into a passing probe; mutation evidence then proves only that
    the new probe is non-vacuous, never that the old case survived.
    """
    held = [rel for rel in (ADVERSARY, REF) if _affirms_defect_handling(_update_section(rel))]
    assert held, (
        "FINDING defect-laundering (exploitable exception): neither adversary.md nor "
        "adversarial.md tells the re-dispatched adversary to keep a program that caught "
        "a product defect and report it; Build's own stale-vs-defect call is unchecked."
    )


def test_adversary_update_old_case_preserved_required() -> None:
    """An update must show the case the stale program checked still fails on the
    behaviour it originally rejected, not only that the rewritten probe can go RED."""
    sections = " ".join(_update_section(rel) for rel in (ADVERSARY, REF))
    preserved = [
        s for s in split_sentences(sections)
        if re.search(r"\b(original|previous|old|same) (case|behaviou?r|assertion|check)\b", s)
        and not has_negation(s)
    ]
    assert preserved, (
        "FINDING loosening-by-modify (exploitable exception): the update rule bans "
        "delete/skip/xfail but lets a 'modified' assertion accept the behaviour the "
        "program used to reject; mutation evidence on the new probe does not detect it."
    )


def _affirms_exclusion(text: str) -> bool:
    for s in split_sentences(text):
        if re.search(r"\b(implementer|this change adds|the change adds|changed paths|written for this change)\b", s) \
                and "reuse" in s.lower() and not has_negation(s) and re.search(r"\b(excludes?|only|outside)\b", s):
            return True
    return False


def test_reuse_exclusion_helper_synthetic() -> None:
    """Self-test: one affirmative exclusion accepted, one negated example rejected."""
    assert _affirms_exclusion(
        "Reuse counts only tests outside the changed paths, so it excludes tests the implementer wrote."
    )
    assert not _affirms_exclusion("Reuse does not exclude tests the implementer wrote.")


def test_adversary_reuse_implementer_tests_excluded_from_floor() -> None:
    """Reuse cannot satisfy the three-case floor with the implementer's own tests.

    'A permanent repository test that already covers a case counts as reuse' and
    'Reused and modified cases count toward the floor' together let the adversary
    name three tests the implementer added in this change (for example the new pins
    in test_build_mechanical_checks.py) and write no adversarial case at all, which
    turns the writer's own tests into the attack arm.
    """
    held = [rel for rel in (ADVERSARY, REF) if _affirms_exclusion(_flat(rel))]
    assert held, (
        "FINDING self-reuse floor (writer-is-judge): the reuse-first rule lets tests "
        "added by this change's implementer count toward the adversarial floor."
    )


def test_build_exception_trunk_sync_staleness_covered() -> None:
    """Staleness that does not come from a Build fix is also routed to the adversary.

    closing-review returns to Build section 3 on `content changed` after sync-trunk to
    re-run the existing programs. A program pinning trunk content or a base commit
    can then fail with no fix having widened scope, and the exception only fires
    'When a fix widens or changes what the change covers': the original deadlock
    (no role may edit the program) returns for that path.
    """
    build = _flat(BUILD)
    exception = next(s for s in split_sentences(build) if "to update its own programs" in s)
    assert re.search(r"sync|trunk|rebase|merge", exception), (
        "FINDING sync-staleness deadlock (unmentioned state): the re-dispatch exception "
        f"covers only a fix that widens scope; sentence: {exception!r}"
    )


def test_cross_docs_roles_consistent_holds() -> None:
    """Held attempt: the four documents agree on who dispatches and who edits."""
    build, adv, ref = _flat(BUILD), _flat(ADVERSARY), _flat(REF)
    closing = _flat("loom-code/skills/closing-review/SKILL.md")
    assert "the adversary never fixes what it breaks" in build
    assert "You fix nothing you attack" in adv
    assert "fixes nothing in the product" in ref
    assert "Closing review dispatches no adversary and creates no adversarial program." in closing
    assert "When Build re-dispatches" in adv and "When Build re-dispatches" in ref
    assert "closing-review" not in _update_section(ADVERSARY)
