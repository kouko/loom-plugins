from __future__ import annotations

from loom_checker.helpers import artifact_path, git_maybe, is_real_date, read_text
from loom_checker.intent_state import STATUS
from loom_checker.parsing import LIST_ITEM
from pathlib import Path
import hashlib


def _get_tested_commit_from_attestation(attestation: dict) -> str | None:
    """Extract tested_commit from attestation."""
    val = attestation.get("tested_commit")
    if val is not None and isinstance(val, str) and val.strip():
        return val.strip()
    return None


def _get_reviewed_commit_from_attestation(attestation: dict) -> str | None:
    """Extract reviewed_commit from attestation."""
    val = attestation.get("reviewed_commit")
    if val is not None and isinstance(val, str) and val.strip():
        return val.strip()
    return None


def _get_functional_content_digest(repo: Path, sha: str, change_id: str, manifest: dict | None) -> str | None:
    """Get functional content digest for a given SHA."""
    from loom_checker.digest import functional_content_digest
    return functional_content_digest(repo, sha, change_id, manifest)


def check_commit_identity(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str], 
    attestation: dict
) -> list[tuple[str, str]]:
    """Check that tested_commit and reviewed_commit have matching functional content 
    except for allowed evidence files."""
    rule = "intake.commit-identity"
    
    tested_commit = _get_tested_commit_from_attestation(attestation)
    reviewed_commit = _get_reviewed_commit_from_attestation(attestation)
    
    # If either is missing, we can't check - but this might be OK if acceptance-test was skipped
    # For now, let's require both to be present
    if not tested_commit:
        return [(rule, "attestation missing tested_commit field")]
    if not reviewed_commit:
        return [(rule, "attestation missing reviewed_commit field")]
    
    # Get functional content digests
    tested_digest = _get_functional_content_digest(repo, tested_commit, change_id, manifest)
    reviewed_digest = _get_functional_content_digest(repo, reviewed_commit, change_id, manifest)
    
    if tested_digest is None:
        return [(rule, f"could not compute functional content digest for tested commit {tested_commit}")]
    if reviewed_digest is None:
        return [(rule, f"could not compute functional content digest for reviewed commit {reviewed_commit}")]
    
    # If they match, we're good
    if tested_digest == reviewed_digest:
        return []
    
    # They differ - check if the difference is only in allowed evidence files
    # For now, we'll implement a simple version: if they differ, fail
    # A more sophisticated implementation would check what files changed
    return [(rule, f"functional content differs between tested commit {tested_commit[:7]} and reviewed commit {reviewed_commit[:7]}")]


def acceptance_count(intent_sections: dict[str, str]) -> int:
    """How many things the user said "done means this" about."""
    body = intent_sections.get("Acceptance", "")
    return sum(1 for line in body.splitlines() if LIST_ITEM.match(line))