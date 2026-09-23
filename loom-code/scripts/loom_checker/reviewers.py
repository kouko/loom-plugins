from __future__ import annotations

from loom_checker.artifact_types import _TEST_NAME_RE
from loom_checker.helpers import TRUNK_BRANCH_NAMES
from loom_checker.helpers import UsageError
from loom_checker.helpers import _is_host_plumbing
from loom_checker.helpers import branch_base
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_text
from loom_checker.helpers import is_program_path
from loom_checker.helpers import tree_programs
from pathlib import Path


_LOW_RISK_DOC_EXTENSIONS = frozenset({".md", ".mdx", ".rst", ".txt"})


_REVIEW_PROTECTED_PARTS = frozenset(
    {"agents", "api", "cli", "commands", "contract", "hooks", "skills", "templates"}
)


_REVIEW_PROTECTED_NAMES = frozenset(
    {"agents.md", "claude.md", "design.md", "kickoff-defaults.md", "principles.md", "skill.md"}
)


# Steps that a narrow delta auto-skips. Intent always stays (cannot be skipped).
_NARROW_AUTO_SKIP_STEPS = frozenset(
    {"spec", "plan", "blind-run", "adversarial"}
)


def _is_test_path(path: Path) -> bool:
    """True for a file the suite collects, or anything under a `tests` tree."""
    return bool(_TEST_NAME_RE.fullmatch(path.name)) or "tests" in {
        part.casefold() for part in path.parts
    }


def reviewer_floor_for_paths(
    paths: set[str], change_id: str, deleted: frozenset[str] | set[str] = frozenset()
) -> int:
    """Return one only for a complete, narrow, mechanically low-risk delta.

    This is a positive allowlist. Anything not recognized here, including a
    mixed delta with one protected path, keeps the default floor of two.

    ``deleted`` is the subset of ``paths`` the delta removes. Adding a test is
    low risk; removing one is the delta that deletes the evidence a later
    reviewer would read, so it keeps the default floor whatever else the
    delta touches.
    """
    if not paths:
        return 2
    for path in deleted:
        if _is_test_path(Path(path)):
            return 2
    intent_path = f"docs/loom/intent/{change_id}.md"
    change_store = f"docs/loom/{change_id}/"
    evidence_store = "docs/loom/evidence/"
    for path in paths:
        pure = Path(path)
        if pure.is_absolute() or ".." in pure.parts:
            return 2
        parts = {part.casefold() for part in pure.parts}
        name = pure.name.casefold()
        if parts.intersection(_REVIEW_PROTECTED_PARTS) or name in _REVIEW_PROTECTED_NAMES:
            return 2
        if path == intent_path or path.startswith(change_store):
            continue
        if path.startswith(evidence_store):
            continue
        if _is_test_path(pure):
            continue
        if (
            pure.suffix.casefold() in _LOW_RISK_DOC_EXTENSIONS
            and not path.startswith("docs/loom/")
        ):
            continue
        return 2
    return 1


def is_narrow_delta(
    paths: set[str], change_id: str, deleted: frozenset[str] | set[str] = frozenset(),
    executable: frozenset[str] | set[str] = frozenset(),
) -> bool:
    """Return True when the diff is narrow enough to auto-skip the steps in
    ``_NARROW_AUTO_SKIP_STEPS``.

    A narrow delta contains only the intent, plan, evidence and low-risk docs
    (`.md`/`.rst`/`.txt` outside `docs/loom/`) — no production code, no
    protected surface, no interface-surface glob, and **no file anything
    executes**, wherever it sits.

    ``adversarial`` is auto-skipped here as well, and the program test is what
    makes that safe: the justification for skipping it is that the delta
    carries no executed behaviour a probe program could make fail, so a delta
    that carries an executed file — a test, a script, a probe program under
    this change's own store, which `finalize-review` runs as a subprocess —
    is not one the justification covers. A delta that removes a test is not
    narrow either: what it changes is what the repository can still check.

    Narrowness is therefore strictly stronger than reviewer floor 1: every
    narrow delta gets floor 1, but a delta that only adds a test file gets
    floor 1 without being narrow.

    ``executable`` carries the paths a caller has already resolved against the
    tree — `helpers.tree_programs` reads git's 100755 mode and a `#!` first
    line, which is how `evidence/probes/run` says it is a program without
    taking a suffix. The name test here is the cheap half of that same
    question, and a caller with a commit in hand passes the other half in;
    `auto_skipped_steps` always does.
    """
    if any(is_program_path(path) or path in executable for path in paths):
        return False
    return reviewer_floor_for_paths(paths, change_id, deleted) == 1


def committed_branch_delta(
    repo: Path, change_id: str, head_sha: str | None = None
) -> tuple[set[str], set[str], set[str]] | None:
    """The committed branch delta as (all paths, removed, added), or None.

    This is the single path source for every rule that reasons about the
    branch's committed content: the reviewer floor, the auto-skip list, and
    anything else that must agree on the same delta. Working-tree and staged
    edits are deliberately excluded — they are not yet part of the change
    that reviewers and finalize-review will see.

    ``None`` means the delta could not be computed at all, which is not the
    same fact as an empty delta and must not be read as one. A checkout that
    holds only the branch — the ordinary CI fetch — resolves no trunk, so
    every caller has to decide for itself what "cannot tell" means for it.

    Working on the trunk is not that case. There the delta is computable and
    empty by construction, which `branch_base` refuses precisely because it
    would pass every recomputed rule; that stays an empty delta here, so the
    rules keep failing closed on it.
    """
    try:
        selected = head_sha or git_text(repo, "rev-parse", "HEAD")
        base = branch_base(repo)
        status = git_text(
            repo, "diff", "--name-status", "--no-renames", base, selected
        )
    except (OSError, UsageError):
        current = git_maybe(repo, "rev-parse", "--abbrev-ref", "HEAD") or ""
        if current in TRUNK_BRANCH_NAMES or current == "HEAD":
            return set(), set(), set()
        return None
    paths: set[str] = set()
    removed: set[str] = set()
    added: set[str] = set()
    for line in status.splitlines():
        code, _, name = line.partition("\t")
        name = name.strip()
        if not name or _is_host_plumbing(name):
            continue
        paths.add(name)
        letter = code.strip().upper()[:1]
        if letter == "D":
            removed.add(name)
        elif letter == "A":
            added.add(name)
    return paths, removed, added


def committed_branch_paths(
    repo: Path, change_id: str, head_sha: str | None = None
) -> set[str]:
    """The committed branch-delta paths; empty when the delta cannot be read."""
    delta = committed_branch_delta(repo, change_id, head_sha)
    return delta[0] if delta else set()


def auto_skipped_steps(
    repo: Path, change_id: str, head_sha: str | None = None
) -> set[str]:
    """Steps the committed delta skips with no typed confirmation.

    Recomputed from the delta itself, so finalize-review, the attestation
    validator and `selection show` all read the same answer without a
    recorded event to consult.

    That recomputation is the reason an unreadable delta returns the whole
    auto-skip set rather than nothing. The set is not a demand, it is the
    list of steps nobody has to account for; answering "nothing was skipped"
    where the delta cannot be read turns a checkout that lacks the trunk —
    a single-branch CI clone validating an attestation finalize already
    wrote — into a refusal of evidence that was correct when it was made.
    An empty but readable delta is a different fact and stays not narrow.

    That permissive answer is only ever correct for a caller re-reading
    evidence that already exists and is bound to the commit's content, which
    is `attestation.validate_attestation` and nothing else. The caller that
    MAKES the evidence, `finalize-review`, refuses an unreadable delta before
    it ever reaches this function: there, "cannot tell" read as "everything
    is skipped" let a change touching production code finalize with no
    adversarial execution at all.
    """
    delta = committed_branch_delta(repo, change_id, head_sha)
    if delta is None:
        return set(_NARROW_AUTO_SKIP_STEPS)
    paths, removed, _added = delta
    selected = head_sha or git_maybe(repo, "rev-parse", "HEAD") or ""
    executable = tree_programs(repo, selected, paths) if selected else set()
    narrow = is_narrow_delta(paths, change_id, removed, executable)
    return set(_NARROW_AUTO_SKIP_STEPS) if narrow else set()


def required_reviewer_count(
    repo: Path, change_id: str, head_sha: str | None = None
) -> int:
    """Compute the reviewer floor from the selected branch delta, failing closed.

    Unlike the auto-skip list this one fails closed on an unreadable delta:
    the reviewer count is checked against verdicts the attestation itself
    records, so demanding two costs an honest change nothing.
    """
    delta = committed_branch_delta(repo, change_id, head_sha)
    if delta is None:
        return 2
    paths, removed, _added = delta
    return reviewer_floor_for_paths(paths, change_id, removed)
