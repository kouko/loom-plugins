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


def _reject_duplicate_keys(pairs: list[tuple]) -> dict:
    """`object_pairs_hook` that fails a JSON object carrying a repeated key.

    `json.loads` otherwise keeps the LAST of a duplicate key and silently
    drops the rest, so a change a human reviewer would see in the raw text
    (a repeated key hiding an earlier value) would disappear once parsed."""
    seen: dict = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r}")
        seen[key] = value
    return seen


def _json_scalar_equal(a: object, b: object) -> bool:
    """Structural equality that treats `0`/`False` and `3`/`3.0` as distinct.

    Plain `==` on parsed JSON is Python value equality: `0 == False` and
    `3 == 3.0` both hold, so a real behaviour flag flip or an int-to-float
    retype could ride alongside a version bump and read as no change at all.
    Comparing `type(a) is type(b)` first, at every level, is what closes that:
    `bool` and `int` are different types even though `0 == False`."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(
            _json_scalar_equal(a[key], b[key]) for key in a
        )
    if isinstance(a, list):
        return len(a) == len(b) and all(
            _json_scalar_equal(x, y) for x, y in zip(a, b)
        )
    # Identity first, like the container `==` this replaces: `json.loads`
    # returns the same interned object for NaN/Infinity/-Infinity every time
    # it parses that literal, so two separately-parsed NaN values are `is`
    # the same object even though plain `nan == nan` is False by IEEE 754.
    # Never a false match between two DIFFERENT values: the only objects two
    # independent parses can share by identity are singletons this Python
    # already treats as one value everywhere (small ints, True/False/None,
    # interned short strings, and json's own float constants).
    return a is b or a == b


def _is_version_only_json_bump(repo: Path, base: str, selected: str, path: str) -> bool:
    """Whether a `.json` file's only change, on both sides, is its `version` value.

    Recomputed from the two blobs, never inferred from the filename: a newly
    added file (no `base` blob), a file either side fails to parse, a
    duplicate key, or a change to any key other than `version` all answer
    False. `version` itself must be a plain string or number on both sides --
    it is popped unread, so a shape change there (an object, a list) is not
    trusted just because the rest of the file matches. This is what lets a
    manifest version bump join the low-risk paths without trusting that the
    rest of the file, or the value itself, was left alone.

    Known blind spot, found adversarially and left open: any key literally
    named `version` is popped, whatever it means in that file. A schema or
    protocol version (`{"version": "v1", ...}` in a config a service reads,
    for example) is a behaviour switch, not a release number, and this check
    cannot tell the two apart -- the filename would be the only signal, and
    trusting the filename is exactly what this function exists to avoid."""
    before_text = git_maybe(repo, "show", f"{base}:{path}")
    if before_text is None:
        return False  # newly added: nothing to compare against
    after_text = git_maybe(repo, "show", f"{selected}:{path}")
    if after_text is None:
        return False  # deleted on this side: not a bump
    try:
        before = json.loads(before_text, object_pairs_hook=_reject_duplicate_keys)
        after = json.loads(after_text, object_pairs_hook=_reject_duplicate_keys)
    except (ValueError, TypeError):
        return False
    if not isinstance(before, dict) or not isinstance(after, dict):
        return False
    for side in (before, after):
        version = side.get("version")
        if version is not None and (
            isinstance(version, bool) or not isinstance(version, (str, int, float))
        ):
            return False
    before = dict(before)
    after = dict(after)
    before.pop("version", None)
    after.pop("version", None)
    return _json_scalar_equal(before, after)


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
