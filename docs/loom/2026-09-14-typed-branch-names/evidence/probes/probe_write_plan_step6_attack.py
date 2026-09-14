"""Adversarial probes: write-plan Step 6 typed-branch prose, read as a hurried agent.

Round 2 (after 5ff81a1b): the branch `<type>` binds the branch prefix and the
PR title (the squash-merge commit); task commits keep their own type.

Run from repo root:
    python3 -m pytest docs/loom/2026-09-14-typed-branch-names/evidence/probes/probe_write_plan_step6_attack.py -q

A passing test is an attack the text survived. A strict xfail is an open
finding: it turns into a failure the moment the text closes it, so the
marker must then be removed.
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
SKILL = REPO / "loom-code/skills/write-plan/SKILL.md"
SHIP = REPO / "loom-code/skills/ship/SKILL.md"
IMPLEMENTER = REPO / "loom-code/agents/implementer.md"
STATION_TEST = REPO / "loom-code/scripts/test_write_plan_station_text.py"

NEGATIONS = {"not", "no", "never", "don't", "do not", "without", "nor", "cannot", "instead of"}
TYPES = {"feat", "fix", "docs", "refactor", "test", "chore", "ci"}


def _step6() -> str:
    text = SKILL.read_text(encoding="utf-8")
    start = text.index("## Step 6 — Commit and hand off")
    end = text.find("\n## ", start + 5)
    return text[start:] if end == -1 else text[start:end]


def _sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", flat) if s.strip()]


def _has_negation(sentence: str) -> bool:
    low = f" {sentence.lower()} "
    return any(re.search(rf"(?<![a-z']){re.escape(tok)}(?![a-z'])", low) for tok in NEGATIONS)


def _affirms(sentence: str, verbs: tuple[str, ...], literal: str) -> bool:
    """True when an affirmative verb precedes `literal` and the sentence has no negation."""
    at = sentence.find(literal)
    if at == -1 or _has_negation(sentence):
        return False
    head = sentence[:at].lower()
    return any(re.search(rf"\b{re.escape(v)}\b", head) for v in verbs)


def _station_bare_re() -> re.Pattern[str]:
    scripts = str(STATION_TEST.parent)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)  # the station test imports its sibling `prose_pin`
    spec = importlib.util.spec_from_file_location("station_text", STATION_TEST)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module._BARE_BRANCH_RE


# --- synthetic self-tests for the prose helper ----------------------------


def test_affirmhelper_affirmativeexample_accepts() -> None:
    """The helper accepts an affirmative sentence that pins the literal."""
    assert _affirms("Write `test(x): RED for foo` as the subject.", ("write",), "`test(")


def test_affirmhelper_negatedexample_rejects() -> None:
    """The helper rejects the same literal inside a negated sentence."""
    assert not _affirms("Do not write `test(x): RED for foo` as the subject.", ("write",), "`test(")


# --- attack 1: hurried reading -- is the rename skippable? -----------------


def test_stepsix_alreadyonbranch_conditionalskipsrename() -> None:
    """Survived-by-design record: the typed-branch rule fires only 'if you are
    still on the trunk'. The intent's Constraints forbid enforcement, so an
    agent already on another branch is left alone by design."""
    assert "if you are still on the trunk" in " ".join(_step6().split())


# --- attack 2: temptation 'it's only docs, the plan commit is docs(loom):' -


def test_stepsix_docstemptation_typefollowschange() -> None:
    """The text ties the type to what the change does, not to the plan commit."""
    assert any(_affirms(s, ("pick",), "to match what the change does") for s in _sentences(_step6()))


# --- attack 3 (re-expressed): implementer RED commits vs branch type -------


def test_stepsix_redcommitonfeatbranch_notcontradicted() -> None:
    """The implementer affirms `test(...)` RED commits; Step 6 must let task
    commits keep their own type and must not bind implementation commits to
    the branch type."""
    implementer_affirms_test_type = any(
        _affirms(s, ("write",), "`test(") for s in _sentences(IMPLEMENTER.read_text(encoding="utf-8"))
    )
    assert implementer_affirms_test_type, "precondition: implementer still affirms `test(...)` commits"
    sentences = _sentences(_step6())
    assert any(_affirms(s, ("keep",), "own Conventional Commits type") for s in sentences), (
        "Step 6 has no affirmative carve-out for task commits"
    )
    assert not any("implementation commits" in s and "same type" in s for s in sentences), (
        "Step 6 still binds implementation commits to the branch type"
    )


# --- attack 4: allowed-type sets disagree ---------------------------------


def test_stepsix_implementertypes_coveredbybranchtypes() -> None:
    """Every implementer commit type is a legal branch type, and vice versa."""
    impl = " ".join(IMPLEMENTER.read_text(encoding="utf-8").split())
    m = re.search(r"`type` ∈ `\{([^}]*)\}", impl)
    assert m, "implementer type set not found"
    impl_types = {t.strip() for t in m.group(1).split(",")}
    pick = [s for s in _sentences(_step6()) if "You pick `<type>`" in s]
    assert pick, "pick sentence not found"
    step6_types = set(re.findall(r"`([a-z]+)`", pick[0]))
    assert impl_types == step6_types == TYPES, (impl_types, step6_types)


# --- attack 5 (re-expressed): this change's own history under the new scope


def test_branchhistory_taskcommits_conventionalallowedtype() -> None:
    """Under the PR-title scope task commits may differ from the branch prefix,
    but each non-`docs(loom):` commit still carries an allowed Conventional type."""
    def git(*a: str) -> str:
        return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True).stdout.strip()

    branch = git("symbolic-ref", "--quiet", "--short", "HEAD")
    if not branch.endswith("/2026-09-14-typed-branch-names"):
        pytest.skip(f"not on the change branch ({branch!r})")
    assert branch.split("/", 1)[0] in TYPES, branch
    # Prefer origin/main: a stale local `main` would pull trunk commits into the range.
    base = git("merge-base", "HEAD", "origin/main") or git("merge-base", "HEAD", "main")
    assert base, "no merge base against origin/main or main"
    # Merge commits (e.g. GitHub update-branch) are not task commits.
    subjects = [s for s in git("log", "--no-merges", "--format=%s", f"{base}..HEAD").splitlines() if s]
    pattern = re.compile(rf"^(?:{'|'.join(sorted(TYPES))})\([a-z0-9-]+\): \S")
    offenders = [s for s in subjects if not pattern.match(s)]
    assert not offenders, f"commits without an allowed Conventional type: {offenders}"


# --- attack 6: one character different -- does the sweep catch it? --------


def test_sweepregex_checkoutbarebranch_caught() -> None:
    """Round-1 dodge: `git checkout -b <change-id>` appended to Step 6 is now
    caught by the station test's bare-branch regex."""
    mutant = _step6() + "\nOr run `git checkout -b " + "<change" + "-id>`.\n"
    assert _station_bare_re().search(mutant)


@pytest.mark.parametrize(
    "spelling",
    [
        "git switch --create <change-id>",
        "git switch -c `<change-id>`",
        "git switch -c '<change-id>'",
        "git checkout -B <change-id>",
        "git worktree add -b <change-id> ../wt",
        "create a branch named `<change-id>`",
    ],
)
def test_sweepregex_barespellingvariant_caught(spelling: str) -> None:
    """Each spelling teaches a bare `<change-id>` branch; the sweep should flag it."""
    assert _station_bare_re().search(spelling.replace("<change-id>", "<change" + "-id>"))


# --- attack 7: PR title type different from the branch prefix? ------------


def test_stepsix_prtitletype_bindstobranchtype() -> None:
    """A hurried reading 'pick any type for the PR title' is refused: the same
    affirmative sentence picks `<type>` for the branch and reuses it in the
    PR title, with no negation that could flip it."""
    hits = [
        s for s in _sentences(_step6())
        if "You pick `<type>`" in s and _affirms(s, ("use",), "same type in the PR title")
    ]
    assert hits, "no single affirmative sentence binds the PR title to the branch `<type>`"


def test_shipstation_squashmerge_claimholds() -> None:
    """Step 6 says the PR title becomes the squash-merge commit; ship merges with `--squash`."""
    assert "gh pr merge <number> --squash" in SHIP.read_text(encoding="utf-8")


def test_shipstation_titleflag_namesbranchtype() -> None:
    """The PR title is written at ship, not write-plan; ship affirms that the
    `<title>` type equals the branch's `<type>/` prefix."""
    text = " ".join(SHIP.read_text(encoding="utf-8").split())
    assert any(
        _affirms(s, ("use", "start", "reuse", "prefix", "equals"), "<type>")
        for s in _sentences(text) if "<title>" in s
    )


def test_affirmhelper_equalsnegated_rejects() -> None:
    """Widening to 'equals' still rejects a negated binding."""
    assert not _affirms(
        "The `<title>` type never equals the branch's `<type>/` prefix.", ("equals",), "<type>"
    )


@pytest.mark.xfail(
    strict=True,
    reason="finding round 2b: ship title rule has no fallback for a branch without a Conventional <type>/ prefix",
)
@pytest.mark.parametrize("branch", ["fix-agy-adapter", "w4-03-push-reason", "feature/2026-09-14-x"])
def test_shipstation_untypedbranch_titlerulehasfallback(branch: str) -> None:
    """Hurried agent on a legacy flat branch (or a non-Conventional prefix):
    'type equals the current branch's `<type>/` prefix' has nothing valid to
    copy. Ship should state what to do when the prefix is absent or not an
    allowed type; otherwise the agent invents a type or ships `feature(...)`."""
    prefix = branch.split("/", 1)[0] if "/" in branch else None
    if prefix in TYPES:
        return
    text = " ".join(SHIP.read_text(encoding="utf-8").split())
    fallback = [
        s for s in _sentences(text)
        if "<title>" in s or "prefix" in s
        if re.search(r"\b(without|lacks|no|not|otherwise|flat|untyped)\b", s)
        and re.search(r"prefix|<type>", s)
    ]
    assert fallback, f"ship gives no title-type rule for branch {branch!r}"
