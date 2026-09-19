from __future__ import annotations

from loom_checker.artifact_types import _TEST_NAME_RE
from loom_checker.helpers import UsageError
from loom_checker.helpers import _is_host_plumbing
from loom_checker.helpers import branch_base
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_text
from pathlib import Path
import json


_LOW_RISK_DOC_EXTENSIONS = frozenset({".md", ".mdx", ".rst", ".txt"})


_REVIEW_PROTECTED_PARTS = frozenset(
    {"agents", "api", "cli", "commands", "contract", "hooks", "skills", "templates"}
)


_REVIEW_PROTECTED_NAMES = frozenset(
    {"agents.md", "claude.md", "design.md", "kickoff-defaults.md", "principles.md", "skill.md"}
)


def _is_version_only_json_bump(repo: Path, base: str, selected: str, path: str) -> bool:
    """Whether a `.json` file's only change, on both sides, is its `version` value.

    Recomputed from the two blobs, never inferred from the filename: a newly
    added file (no `base` blob), a file either side fails to parse, or a change
    to any key other than `version` all answer False. This is what lets a
    manifest version bump join the low-risk paths without trusting that the
    rest of the file was left alone."""
    before_text = git_maybe(repo, "show", f"{base}:{path}")
    if before_text is None:
        return False  # newly added: nothing to compare against
    after_text = git_maybe(repo, "show", f"{selected}:{path}")
    if after_text is None:
        return False  # deleted on this side: not a bump
    try:
        before = json.loads(before_text)
        after = json.loads(after_text)
    except (ValueError, TypeError):
        return False
    if not isinstance(before, dict) or not isinstance(after, dict):
        return False
    before = dict(before)
    after = dict(after)
    before.pop("version", None)
    after.pop("version", None)
    return before == after


def reviewer_floor_for_paths(
    paths: set[str],
    change_id: str,
    repo: Path | None = None,
    base: str | None = None,
    selected: str | None = None,
) -> int:
    """Return one only for a complete, narrow, mechanically low-risk delta.

    This is a positive allowlist. Anything not recognized here, including a
    mixed delta with one protected path, keeps the default floor of two.

    `repo`, `base` and `selected` are optional and only used to recompute
    whether a `.json` file's change is version-only (see
    `_is_version_only_json_bump`); a caller that omits them simply does not
    get that one extra low-risk case, matching prior behaviour exactly.
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
        if (
            pure.suffix.casefold() == ".json"
            and repo is not None
            and base is not None
            and selected is not None
            and _is_version_only_json_bump(repo, base, selected, path)
        ):
            continue
        return 2
    return 1


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
    return reviewer_floor_for_paths(paths, change_id, repo=repo, base=base, selected=selected)
