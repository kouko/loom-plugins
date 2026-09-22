"""Which change a branch carries, and how verified it is.

Neither function refuses: identification returns an error string naming the
fix, and status is a value (`valid`, `valid (skipped: <steps>)`, `absent`,
`stale (<reason>)`) that publish, land, the hook and CI print.

Two depths. `local` runs the full `validate_attestation`, including the
comparison with the local selection records. `ci` runs the content-level
checks only, because a fresh checkout has no selection records; it treats
the attestation's own `selection` as a claim and reports any claimed skip
as `valid (skipped: ...)`, never plain `valid`.
"""

from __future__ import annotations

from loom_checker.attestation import validate_attestation
from loom_checker.helpers import UsageError
from loom_checker.helpers import changed_paths
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_ok
from loom_checker.helpers import git_text
from loom_checker.helpers import glob_to_regex
from loom_checker.helpers import load_manifest
from loom_checker.parsing import parse_document
from pathlib import Path
import json
import re


def _delta(repo: Path, base: str | None, head: str) -> set[str]:
    """The branch delta: the local diff (working tree included) when no base
    is given, else the committed diff base..head."""
    if base is None:
        return changed_paths(repo)
    return {line for line in git_text(repo, "diff", "--name-only", base, head).splitlines()
            if line.strip()}


def _change_ids(manifest: dict, artifact: str, paths: set[str]) -> list[tuple[str, str]]:
    """(change id, path) for every path matching the artifact's template."""
    template = manifest["artifacts"][artifact]["path"]
    pattern = re.compile(
        re.escape(template).replace(re.escape("<change-id>"), r"(?P<change_id>[^/]+)")
    )
    found = []
    for path in sorted(paths):
        match = pattern.fullmatch(path)
        if match:
            found.append((match.group("change_id"), path))
    return found


def _at(repo: Path, head: str, path: str) -> bool:
    return git_ok(repo, "cat-file", "-e", f"{head}:{path}")


def identify_change(
    repo: Path, *, base: str | None = None, head: str = "HEAD",
    branch: str | None = None, manifest: dict | None = None,
) -> tuple[str | None, str | None]:
    """(change id, None), or (None, why it is unidentified and how to fix it).

    The branch name `<type>/<change-id>` wins when that intent exists at
    `head`; else the single intent file in the branch delta. An attestation in
    the delta, when present, must name the same change."""
    manifest = manifest if manifest is not None else load_manifest()
    if branch is None:
        branch = git_maybe(repo, "rev-parse", "--abbrev-ref", "HEAD") or ""
    intent_template = manifest["artifacts"]["intent"]["path"]
    fix = ("rename the branch to <type>/<change-id> or commit the intent "
           f"{intent_template}")
    try:
        delta = _delta(repo, base, head)
    except UsageError as exc:
        return None, f"cannot identify the change on branch {branch!r}: {exc}; {fix}"

    change_id = None
    named = re.fullmatch(r"[^/]+/([^/]+)", branch)
    if named and _at(repo, head, intent_template.replace("<change-id>", named.group(1))):
        change_id = named.group(1)
    else:
        intents = [cid for cid, path in _change_ids(manifest, "intent", delta)
                   if _at(repo, head, path)]
        if len(intents) != 1:
            return None, (
                f"cannot identify the change: branch {branch!r} names no committed intent "
                f"and the branch delta carries {len(intents)} intent files; {fix}"
            )
        change_id = intents[0]

    attested = {cid for cid, _ in _change_ids(manifest, "attestation", delta)}
    if attested and attested != {change_id}:
        return None, (
            f"the branch identifies change {change_id!r} but its attestation names "
            f"{', '.join(sorted(attested))}; {fix}"
        )
    return change_id, None


def verification_status(
    repo: Path, change_id: str, *, depth: str = "local", base: str | None = None,
    head: str = "HEAD", manifest: dict | None = None,
) -> str:
    """`valid`, `valid (skipped: <steps>)`, `absent` or `stale (<reason>)`."""
    if depth not in {"local", "ci"}:
        raise ValueError(f"unknown verification depth {depth!r}")
    manifest = manifest if manifest is not None else load_manifest()
    try:
        head_sha = git_text(repo, "rev-parse", head)
        attestations = _change_ids(manifest, "attestation", _delta(repo, base, head_sha))
    except UsageError as exc:
        return f"stale ({exc})"
    if not attestations:
        return "absent"
    if len(attestations) > 1:
        return f"stale (branch carries {len(attestations)} attestations)"
    attested_id, path = attestations[0]
    if attested_id != change_id:
        return f"stale (attestation belongs to change {attested_id})"
    try:
        payload = json.loads(git_text(repo, "show", f"{head_sha}:{path}"))
    except UsageError:
        return "stale (attestation is not committed at HEAD)"
    except json.JSONDecodeError:
        return "stale (attestation is not readable JSON)"
    failures = validate_attestation(
        repo, head_sha, change_id, payload, manifest, claimed_selection=(depth == "ci")
    )
    if failures:
        return f"stale ({failures[0][1]})"
    selection = payload.get("selection")
    skip = selection.get("skip") if isinstance(selection, dict) else None
    return f"valid (skipped: {', '.join(skip)})" if skip else "valid"


def missing_records(repo: Path, change_id: str, status: str, head: str = "HEAD",
                    manifest: dict | None = None) -> list[str]:
    """Absent records among confirmed intent, plan and attestation."""
    manifest = manifest if manifest is not None else load_manifest()
    missing = []
    intent = manifest["artifacts"]["intent"]["path"].replace("<change-id>", change_id)
    front: dict = {}
    if _at(repo, head, intent):
        front, _sections = parse_document(git_text(repo, "show", f"{head}:{intent}"))
    if not re.fullmatch(r"confirmed \d{4}-\d{2}-\d{2}", front.get("status", "")):
        missing.append("confirmed intent")
    if not _at(repo, head, manifest["artifacts"]["plan"]["path"].replace("<change-id>", change_id)):
        missing.append("plan")
    if status == "absent":
        missing.append("attestation")
    return missing


def missing_clause(missing: list[str]) -> str:
    return f"(missing: {', '.join(missing)})" if missing else ""
