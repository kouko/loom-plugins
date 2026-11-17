"""Read immutable prerequisite execution provenance from committed history."""
from __future__ import annotations

import json
import re
from pathlib import Path

from loom_checker.helpers import git_maybe


def prerequisite_probe_programs(
    repo: Path, head_sha: str, change_id: str, candidates: set[str],
) -> set[str]:
    """Only pre-intent, validated executions with uninterrupted path identity qualify."""
    # Import locally: attestation validation itself consumes probe discovery.
    from loom_checker.attestation import validate_attestation

    if not candidates:
        return set()
    intent = f"docs/loom/intent/{change_id}.md"
    introductions = git_maybe(repo, "log", "--full-history", "--diff-filter=A",
                              "--format=%H", head_sha, "--", intent)
    if introductions is None or len(introductions.splitlines()) != 1:
        return set()
    introduction = introductions.strip()
    parents = git_maybe(repo, "rev-parse", f"{introduction}^@")
    if not parents:
        return set()
    horizon = parents.splitlines()
    names = git_maybe(repo, "log", "--format=", "--name-only", *horizon,
                     "--", "docs/loom/*/attestation.json")
    if names is None:
        return set()
    proven: set[str] = set()
    for path in sorted(set(names.splitlines())):
        match = re.fullmatch(r"docs/loom/([^/]+)/attestation\.json", path)
        if match is None or match[1] == change_id:
            continue
        revisions = git_maybe(repo, "log", "--format=%H", *horizon, "--", path)
        for revision in (revisions or "").splitlines():
            raw = git_maybe(repo, "show", f"{revision}:{path}")
            try:
                record = json.loads(raw or "")
                if not isinstance(record, dict):
                    continue
                executions = record.get("executions")
                if not isinstance(executions, list):
                    continue
                artifacts = {execution["artifact"] for execution in executions
                             if isinstance(execution, dict)
                             and execution.get("kind") == "adversarial"
                             and execution.get("result") == "pass"
                             and isinstance(execution.get("artifact"), str)}
                artifacts &= candidates - proven
                # No-program records cannot establish provenance and can recurse
                # through stored_probe_programs during attestation validation.
                if not artifacts or any(isinstance(run, dict) and "no_program" in run
                                        for run in executions):
                    continue
                if validate_attestation(repo, revision, match[1], record):
                    continue
            except (ValueError, TypeError, KeyError, AttributeError):
                continue
            for artifact in artifacts - proven:
                old = git_maybe(repo, "ls-tree", revision, "--", artifact)
                current = git_maybe(repo, "ls-tree", head_sha, "--", artifact)
                if not old or old != current or not old.startswith(("100644 blob ", "100755 blob ")):
                    continue
                changes = git_maybe(repo, "log", "--full-history", "--ancestry-path", "--format=%H",
                                    f"{revision}..{head_sha}", "--", artifact)
                # A full-history log also lists merges whose other parent did
                # not yet carry this path. Only actual tree identity changes
                # on evidence-descended history invalidate provenance.
                if changes is not None and all(
                    git_maybe(repo, "ls-tree", commit, "--", artifact) == old
                    for commit in changes.splitlines()
                ):
                    proven.add(artifact)
    return proven
