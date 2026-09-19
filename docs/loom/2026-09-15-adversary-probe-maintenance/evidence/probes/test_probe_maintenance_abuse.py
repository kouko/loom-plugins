"""Adversarial probes for `2026-09-15-adversary-probe-maintenance`.

The change lets Build re-dispatch the adversary to update its own stale
programs, and tells the adversary to reuse existing probes and tests first.
These probes try to make that change fail:

* mutation runs of the new pins in `test_build_mechanical_checks.py`: each
  mutation removes, loosens or overrides one guard sentence in a scratch copy
  of the changed files and runs the committed test module against it; a
  mutant the module still passes is a vacuous pin, and a mutant killed only by
  a test other than the pin named for it is a pin that holds by accident;
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
SCRIPTS = "loom-code/scripts"
REFERENCES = "loom-code/skills/closing-review/references"
REF = f"{REFERENCES}/adversarial.md"
TEST_MODULE = f"{SCRIPTS}/test_build_mechanical_checks.py"
MANIFEST = "loom-code/contract/manifest.yaml"


def _reference_docs() -> list[str]:
    """Every document of the reference folder, read from the folder itself.

    The procedure the adversary follows is the shared protocol plus one file
    per artifact kind, and which kinds exist is decided by the routing table
    in the protocol, not by this probe. A hand-written list here went stale
    the day a kind was given its own file: the copy below lost the recipes,
    the pin module could not import, and every mutation case reported a dead
    scratch tree instead of a surviving mutant. Reading the folder keeps the
    copy right for a kind added or retired later.
    """
    folder = REPO / REFERENCES
    return sorted(f"{REFERENCES}/{p.name}" for p in folder.glob("*.md") if p.is_file())


def _recipes() -> list[str]:
    """The reference documents other than the shared protocol."""
    return [rel for rel in _reference_docs() if rel != REF]


def _pin_modules() -> list[str]:
    """The test modules that pin these documents' sentences, same reasoning.

    The pins of the protocol and of each recipe live in that file's own test
    module, and `test_build_mechanical_checks.py` imports them, so a copy
    holding only the named module cannot run at all.
    """
    folder = REPO / SCRIPTS
    return sorted(f"{SCRIPTS}/{p.name}" for p in folder.glob("test_adversary*.py") if p.is_file())


# Modules the scratch copy cannot run, whatever they hold: one reads the
# migration out of git history and the copy has no `.git`, and the other
# copies the whole repository and runs pytest inside that copy. Both are
# still copied, because the modules that do run import them.
UNRUNNABLE_IN_SCRATCH = (
    f"{SCRIPTS}/test_adversary_layout.py",
    f"{SCRIPTS}/test_adversary_routing.py",
)

IMPLEMENTER = "loom-code/agents/implementer.md"

COPIED = [
    BUILD, ADVERSARY, IMPLEMENTER, TEST_MODULE, MANIFEST, f"{SCRIPTS}/prose_pin.py",
    *_reference_docs(), *_pin_modules(),
]


def _raw(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


def _flat(rel: str) -> str:
    return " ".join(re.sub(r"^> ?", "", _raw(rel), flags=re.M).split())


def _procedure() -> str:
    """The whole procedure the adversary contract routes it to, flattened.

    The contract names the shared protocol and tells the adversary to read
    the recipe of every kind the change touched, so a rule of the procedure
    is a rule stated in the protocol or in one of its recipes. Before the
    split every one of these sentences was in the protocol alone, which is
    why the cases below used to read that one file.
    """
    return " ".join(_flat(rel) for rel in _reference_docs())


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


def _pin_targets(root: Path) -> list[str]:
    """The pin modules the scratch copy runs: the named one and every module
    that pins one of these documents, bar the two that need a repository."""
    targets = [TEST_MODULE, *(m for m in _pin_modules() if m not in UNRUNNABLE_IN_SCRATCH)]
    for rel in targets:
        assert (root / rel).is_file(), rel
    return [str(root / rel) for rel in targets]


def _run_pins(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-rf", "-p", "no:cacheprovider", *_pin_targets(root)],
        cwd=root / SCRIPTS,
        capture_output=True,
        text=True,
        timeout=300,
    )


def _mutate(root: Path, rel: str, old: str, new: str) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    mutated, count = _ws(old).subn(lambda _m: new, text)
    assert count == 1, f"mutation anchor not found exactly once in {rel}: {old!r} ({count})"
    path.write_text(mutated, encoding="utf-8")


def _failed_tests(output: str) -> set[str]:
    """Failed cases from pytest's FAILED summary lines, as `module::name[id]`.

    The module is kept because the same test name now lives in several
    modules at once: the protocol's module and each recipe's module both
    carry `test_adversary_probe_maintenance_rule_stated`, so a bare name
    would let a pin in one file be credited with killing a mutation in
    another file's rule.
    """
    found = set()
    for match in re.finditer(r"^FAILED (?P<path>\S+?)::(?P<name>\S+)", output, re.M):
        found.add(f"{Path(match.group('path')).name}::{match.group('name')}")
    return found


def test_failed_tests_parser_synthetic() -> None:
    """Self-test: a full parametrised name is parsed with its module; the same
    name in another module is a different case, and a bare name is neither."""
    out = (
        "FAILED /x/test_build_mechanical_checks.py::test_probe_maintenance_pin_helpers_synthetic"
        "[build-trigger-excludes-caught-defect] - AssertionError\n"
    )
    names = _failed_tests(out)
    assert (
        "test_build_mechanical_checks.py::test_probe_maintenance_pin_helpers_synthetic"
        "[build-trigger-excludes-caught-defect]"
    ) in names
    assert (
        "test_adversary_protocol.py::test_probe_maintenance_pin_helpers_synthetic"
        "[build-trigger-excludes-caught-defect]"
    ) not in names
    assert "test_probe_maintenance_pin_helpers_synthetic[build-trigger-excludes-caught-defect]" not in names


_OVERRIDE_ANCHOR = "Implementers and the orchestrator never edit an adversarial program."

BUILD_MODULE = Path(TEST_MODULE).name


def _holder(anchor: str) -> str:
    """The reference document that states `anchor`: found, never named here.

    A rule of the procedure now sits in the shared protocol or in one kind's
    recipe, and which of them is a fact of the tree. Writing the file name
    into this list instead would make every mutation case go stale the next
    time a rule moves between those files, and would leave a dangling name
    behind the day that kind is retired.
    """
    hits = [rel for rel in _reference_docs() if _ws(anchor).search(_raw(rel))]
    assert len(hits) == 1, f"{anchor!r} is stated in {hits}, not in exactly one document"
    return hits[0]


def _kind_of(rel: str) -> str:
    """The artifact kind a recipe file attacks, from its name."""
    return Path(rel).stem[len("adversarial-"):]


def _pin_doc_key(rel: str) -> str:
    """The key the pin module files that document under."""
    return "ref" if rel == REF else f"ref-{_kind_of(rel)}"


def _pin_module(rel: str) -> str:
    """The module that carries that document's own pins."""
    if rel == REF:
        return "test_adversary_protocol.py"
    return f"test_adversary_recipe_{_kind_of(rel).replace('-', '_')}.py"


_RED_THEN_REVERTED = "Each mutation must turn the probe RED and is then reverted"
_DISCARD_TAIL = "they can destroy uncommitted work."
_FLOOR_SENTENCE = "Reused and modified cases count toward the floor."

# (id, file, old text, replacement, pin test expected to kill it)
MUTATIONS = [
    # Controls: guards the pins do cover. A mutant surviving here is a vacuous pin.
    ("drop-fresh-context", BUILD, "agent fresh-context again to update", "agent again to update",
     f"{BUILD_MODULE}::test_build_redispatches_adversary_for_stale_programs"),
    ("drop-handoff-reason", BUILD, "each adversary re-dispatch with its reason, ", "",
     f"{BUILD_MODULE}::test_build_redispatches_adversary_for_stale_programs"),
    ("drop-red-then-reverted", _holder(_RED_THEN_REVERTED), _RED_THEN_REVERTED, "The report says so;",
     f"{_pin_module(_holder(_RED_THEN_REVERTED))}::test_adversary_probe_maintenance_rule_stated"
     f"[{_pin_doc_key(_holder(_RED_THEN_REVERTED))}-mutation-red-then-reverted]"),
    ("loosen-ref-reuse-sentence", REF,
     "It reuses a program that covers a case,", "It may write new probes freely,",
     f"{_pin_module(REF)}::test_adversary_probe_maintenance_rule_stated[ref-reuse-modify-then-new]"),
    # Guards the exception relies on to refuse a defect relabelled as stale.
    ("drop-product-defect-guard", BUILD,
     "fails, or is unable to run, for that reason, rather than for a product defect it correctly caught.",
     "fails for any reason.",
     f"{BUILD_MODULE}::test_adversary_probe_maintenance_rule_stated"
     "[build-trigger-excludes-caught-defect]"),
    ("drop-build-decides-defect-fix", BUILD,
     "Build decides which case applies from the program's failure and the widened scope, "
     "and fixes a product defect in the product as above.", "",
     f"{BUILD_MODULE}::test_adversary_probe_maintenance_rule_stated[build-decides-and-fixes-defect]"),
    ("drop-rerun-after-update", BUILD,
     "After the update, Build repeats these end-of-Build checks.", "",
     f"{BUILD_MODULE}::test_adversary_probe_maintenance_rule_stated[build-reruns-after-update]"),
    # Added sentences that override a pinned rule without touching its text.
    ("orchestrator-may-modify-program", BUILD, _OVERRIDE_ANCHOR,
     _OVERRIDE_ANCHOR + " When time is short, the orchestrator may modify a stale adversarial program itself.",
     f"{BUILD_MODULE}::test_no_other_role_edits_adversarial_program"),
    ("orchestrator-rewrites-program-modal-free", BUILD, _OVERRIDE_ANCHOR,
     _OVERRIDE_ANCHOR + " When time is short, the orchestrator rewrites a stale adversarial program itself.",
     f"{BUILD_MODULE}::test_no_other_role_edits_adversarial_program"),
    ("added-discard-literal", _holder(_DISCARD_TAIL), _DISCARD_TAIL,
     _DISCARD_TAIL + " Clean up a dirty copy with `git reset --hard` afterwards.",
     f"{BUILD_MODULE}::test_no_added_sentence_overrides_pinned_rules"
     f"[{_pin_doc_key(_holder(_DISCARD_TAIL))}]"),
    ("implementer-pin-counts-floor", _holder(_FLOOR_SENTENCE), _FLOOR_SENTENCE,
     _FLOOR_SENTENCE + " An implementer's pin counts toward the floor.",
     f"{BUILD_MODULE}::test_no_added_sentence_overrides_pinned_rules"
     f"[{_pin_doc_key(_holder(_FLOOR_SENTENCE))}]"),
    ("redispatch-for-caught-defect", BUILD, "After the update, Build repeats these end-of-Build checks.",
     "After the update, Build repeats these end-of-Build checks. "
     "Build re-dispatches the adversary for a program that caught a product defect.",
     f"{BUILD_MODULE}::test_no_added_sentence_overrides_pinned_rules[build]"),
    ("every-failure-stale", BUILD, "After the update, Build repeats these end-of-Build checks.",
     "After the update, Build repeats these end-of-Build checks. "
     "Build treats every failure as stale and re-dispatches the adversary.",
     f"{BUILD_MODULE}::test_no_added_sentence_overrides_pinned_rules[build]"),
]


def test_holder_and_pin_key_helpers_synthetic() -> None:
    """Self-test: a rule is found in exactly one reference document, and that
    document's pin key and pin module follow from its name, not from a list."""
    assert _holder(_FLOOR_SENTENCE) in _reference_docs()
    assert _pin_doc_key(REF) == "ref"
    assert _pin_module(REF) == "test_adversary_protocol.py"
    synthetic = f"{REFERENCES}/adversarial-synthetic-kind.md"
    assert _pin_doc_key(synthetic) == "ref-synthetic-kind"
    assert _pin_module(synthetic) == "test_adversary_recipe_synthetic_kind.py"
    with pytest.raises(AssertionError):
        _holder("a sentence no document of the reference folder states")


def test_pins_scratch_copy_unmutated_passes(tmp_path: Path) -> None:
    """Control: the committed pin module passes on an unmutated scratch copy."""
    result = _run_pins(_scratch(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "mutation_id,rel,old,new,killer", MUTATIONS, ids=[m[0] for m in MUTATIONS]
)
def test_pins_guard_mutation_killed(
    tmp_path: Path, mutation_id: str, rel: str, old: str, new: str, killer: str
) -> None:
    """Each guard-removing mutation turns the committed pin module RED, through the pin named for it."""
    root = _scratch(tmp_path)
    _mutate(root, rel, old, new)
    result = _run_pins(root)
    assert result.returncode != 0, (
        f"FINDING vacuous-pin ({mutation_id}): {rel} mutant survived "
        f"test_build_mechanical_checks.py; the guard is stated but no pin fails when it is "
        f"removed, loosened or overridden.\n{result.stdout[-800:]}"
    )
    failed = _failed_tests(result.stdout)
    assert killer in failed, (
        f"FINDING accidental-kill ({mutation_id}): the mutant was killed, but not by {killer}; "
        f"the pin meant for this guard does not see it. Failed: {sorted(failed)}"
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


_REDISPATCH = re.compile(r"re-dispatch", re.I)


def _update_section(rel: str) -> str:
    """What the document says about updating a stale adversarial program.

    The contract used to carry a heading this split on; the consolidation of
    the rule text retired that heading and left the rules in the contract's
    role and input paragraphs, so the region is now taken from the sentences
    that speak of a re-dispatch. The procedure's region is the section that
    owns the update rules, cut at the next heading of its own file rather
    than at the name of a section that moved to a recipe.
    """
    if rel == ADVERSARY:
        return " ".join(s for s in split_sentences(_flat(rel)) if _REDISPATCH.search(s))
    after = _raw(rel).split("## Reuse first, update with evidence", 1)
    assert len(after) == 2, rel
    return " ".join(re.split(r"^## ", after[1], maxsplit=1, flags=re.M)[0].split())


def test_update_section_helpers_synthetic() -> None:
    """Self-test: the contract's region is the re-dispatch sentences, and the
    procedure's region stops at the next heading of its own file."""
    assert _REDISPATCH.search("When Build re-dispatches it for a widened scope")
    assert not _REDISPATCH.search("Build hands off to closing review.")
    section = _update_section(REF)
    assert "Reuse a program" in section or "It reuses a program" in section
    assert "## Recording" not in section
    contract = _update_section(ADVERSARY)
    assert contract, "the contract says nothing about a re-dispatch"
    assert all(_REDISPATCH.search(s) for s in split_sentences(contract))


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


_BRANCH_TEST = re.compile(
    r"\b(implementer|added or changed on the branch|this change adds|written for this change)", re.I
)
_FLOOR_CREDIT = re.compile(r"\bcounts?\b[^.;]*\btoward the floor\b", re.I)


def _affirms_exclusion(text: str) -> bool:
    """The floor is limited to the adversary's programs and tests outside the branch,
    and branch tests such as an implementer's pin are sent to related coverage only.

    The limit and the related-coverage rule may sit in one sentence or in two; each
    must be affirmative, and no sentence may credit a branch test toward the floor.
    """
    sentences = split_sentences(text)
    limit = any(
        "reuse" in s.lower() and "floor" in s and re.search(r"\bonly\b", s)
        and re.search(r"\boutside (?:this|the) change's branch\b|\boutside the changed paths\b", s)
        and not has_negation(s)
        for s in sentences
    )
    related = any(
        _BRANCH_TEST.search(s) and re.search(r"\b(related coverage|excludes?)\b", s)
        and not has_negation(s) and not _FLOOR_CREDIT.search(s)
        for s in sentences
    )
    credited = any(
        _BRANCH_TEST.search(s) and _FLOOR_CREDIT.search(s) and not has_negation(s)
        for s in sentences
    )
    return limit and related and not credited


def test_reuse_exclusion_helper_synthetic() -> None:
    """Self-test: one affirmative exclusion accepted; negated and floor-crediting examples rejected."""
    assert _affirms_exclusion(
        "Reuse toward the floor counts only your programs and tests unchanged outside this "
        "change's branch. Name an implementer's pin as related coverage only."
    )
    assert not _affirms_exclusion(
        "Reuse toward the floor does not count only tests outside this change's branch. "
        "An implementer's pin is never related coverage only."
    )
    assert not _affirms_exclusion(
        "Reuse toward the floor counts only your programs and tests outside this change's branch. "
        "Name an implementer's pin as related coverage only. An implementer's pin counts toward the floor."
    )
    assert not _affirms_exclusion(
        "Reuse toward the floor counts only your programs and tests outside this change's branch. "
        "Name an implementer's pin as floor coverage."
    )


def test_adversary_reuse_implementer_tests_excluded_from_floor() -> None:
    """Reuse cannot satisfy the three-case floor with the implementer's own tests.

    'A permanent repository test that already covers a case counts as reuse' and
    'Reused and modified cases count toward the floor' together let the adversary
    name three tests the implementer added in this change (for example the new pins
    in test_build_mechanical_checks.py) and write no adversarial case at all, which
    turns the writer's own tests into the attack arm. Both the adversary's own
    contract and the reference it reads must carry the exclusion.
    """
    assert _affirms_exclusion(_procedure()), (
        "FINDING self-reuse floor (writer-is-judge): the reuse-first rule lets tests "
        "added by this change's implementer count toward the adversarial floor; neither "
        "the shared protocol nor any recipe it routes to states the exclusion."
    )
    assert REF in _flat(ADVERSARY), (
        "FINDING unreachable exclusion: the contract does not name the procedure that "
        "states the exclusion, so nothing routes the adversary to it."
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
    build, adv, ref = _flat(BUILD), _flat(ADVERSARY), _procedure()
    closing = _flat("loom-code/skills/closing-review/SKILL.md")
    assert "the adversary never fixes what it breaks" in build
    assert "You fix nothing you attack" in adv
    assert "fixes nothing in the product" in ref
    assert "Closing review dispatches no adversary and creates no adversarial program." in closing
    # Case-insensitively: the contract now carries the re-dispatch inside a
    # sentence rather than opening one with it.
    assert _REDISPATCH.search(adv) and _REDISPATCH.search(ref)
    assert "closing-review" not in _update_section(ADVERSARY)
