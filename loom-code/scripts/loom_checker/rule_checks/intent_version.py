from __future__ import annotations

from loom_checker.helpers import artifact_path, read_text
from loom_checker.intent_state import STATUS
from pathlib import Path
import hashlib
import re


INTENT_CONFIRMED_SHA_RE = re.compile(r"^intent_confirmed_sha:\s*([0-9a-f]{7,64})\s*$", re.IGNORECASE | re.MULTILINE)
STATUS_LINE_RE = re.compile(r"^status:\s*confirmed\s+\d{4}-\d{2}-\d{2}", re.IGNORECASE | re.MULTILINE)


def _compute_blob_sha_without_status_line(intent_text: str) -> str:
    """Compute blob SHA of intent text WITHOUT the status line (matches spec's confirmed-behavior pattern)."""
    # Remove the status line
    text_without_status = STATUS_LINE_RE.sub("", intent_text, count=1)
    # Also remove the intent_confirmed_sha line if present
    text_without_confirmed = INTENT_CONFIRMED_SHA_RE.sub("", text_without_status, count=1)
    return hashlib.sha1(b"blob " + str(len(text_without_confirmed)).encode() + b"\0" + text_without_confirmed.encode()).hexdigest()


def _get_intent_confirmed_sha_from_intent(intent_text: str) -> str | None:
    """Extract intent_confirmed_sha from intent frontmatter."""
    match = INTENT_CONFIRMED_SHA_RE.search(intent_text)
    if match:
        return match.group(1).lower()
    return None


def _get_intent_confirmed_sha_from_attestation(attestation: dict) -> str | None:
    """Extract intent_confirmed_sha from attestation."""
    val = attestation.get("intent_confirmed_sha")
    if val is not None and isinstance(val, str) and val.strip():
        return val.strip().lower()
    return None


def check_intent_version(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str], 
    attestation: dict
) -> list[tuple[str, str]]:
    """Check that intent Acceptance lines haven't changed since confirmation."""
    rule = "intake.intent-version"
    
    # Get intent file path and read it
    intent_path = artifact_path(manifest, "intent", change_id, repo)
    if not intent_path.is_file():
        return [(rule, f"intent file not found at {intent_path.relative_to(repo)}")]
    
    intent_text = read_text(intent_path)
    
    # Check if intent has been confirmed
    if not STATUS_LINE_RE.search(intent_text):
        # Intent not confirmed - no version to check against
        return []
    
    # Get the recorded intent_confirmed_sha from attestation
    recorded_sha = _get_intent_confirmed_sha_from_attestation(attestation)
    if not recorded_sha:
        # No recorded SHA in attestation - could be an old attestation
        # This is OK for backward compatibility
        return []
    
    # Compute current intent SHA (without status line and confirmed_sha line)
    current_sha = _compute_blob_sha_without_status_line(intent_text).lower()
    
    # Compare
    if current_sha != recorded_sha:
        # Intent has changed since confirmation
        # Find which acceptance lines changed (simplified - just report the mismatch)
        return [
            (rule, 
                f"intent Acceptance lines have changed since confirmation "
                f"(attestation records {recorded_sha[:7]}, current is {current_sha[:7]}). "
                f"Run 'loom confirm-intent' to re-confirm the updated intent.")
        ]
    
    return []