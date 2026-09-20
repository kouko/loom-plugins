from __future__ import annotations

from loom_checker.artifact_types import _TEST_NAME_RE
from loom_checker.helpers import UsageError
from loom_checker.helpers import _is_host_plumbing
from loom_checker.helpers import branch_base
from loom_checker.helpers import git_text
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
    {"spec", "plan", "blind-run"}
)


def reviewer_floor_for_paths(paths: set[str], change_id: str) -> int:
    """Return one only for a complete, narrow, mechanically low-risk delta.

    This is a positive allowlist. Anything not recognized here, including a
    mixed delta with one protected path, keeps the default floor of two.
    The `is_narrow_delta` docstring previously mentioned ``adversarial``,
    but adversarial is not auto-skipped for narrow deltas — only ``spec``,
    ``plan``, and ``blind-run`` are.
    """
    if not paths:
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
        if _TEST_NAME_RE.fullmatch(pure.name) or "tests" in parts:
            continue
        if (
            pure.suffix.casefold() in _LOW_RISK_DOC_EXTENSIONS
            and not path.startswith("docs/loom/")
        ):
            continue
        return 2
    return 1


def is_narrow_delta(paths: set[str], change_id: str) -> bool:
    """Return True when the diff is narrow enough to auto-skip spec/plan/blind-run.

    A narrow delta contains only the intent, plan, evidence, low-risk docs
    (`.md`/`.rst`/`.txt` outside `docs/loom/`), and test files — no production
    code, no protected surface, no interface-surface glob.

    The check reuses the same allowlist as `reviewer_floor_for_paths` so the
    two predicates never disagree: a delta that gets floor 1 is narrow, and a
    narrow delta gets floor 1.

    ``adversarial`` is NOT auto-skipped here — it is a mechanical check that
    must run before closing review regardless of delta width.
    """
    # A narrow delta is exactly one whose reviewer floor is 1. The floor
    # computation is the authoritative allowlist; we delegate to it rather
    # than maintaining a second allowlist that could drift.
    return reviewer_floor_for_paths(paths, change_id) == 1


def required_reviewer_count(
    repo: Path, change_id: str, head_sha: str | None = None
) -> int:
    """Compute the reviewer floor from the selected branch delta, failing closed."""
    try:
        selected = head_sha or git_text(repo, "rev-parse", "HEAD")
        base = branch_base(repo)
        paths = {
            line.strip()
            for line in git_text(
                repo, "diff", "--name-only", "--no-renames", base, selected
            ).splitlines()
            if line.strip() and not _is_host_plumbing(line.strip())
        }
    except (OSError, UsageError):
        return 2
    return reviewer_floor_for_paths(paths, change_id)
