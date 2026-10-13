from __future__ import annotations

from loom_checker.helpers import artifact_path, blob_sha, read_text, sha_agrees
from pathlib import Path
import re


# The lines excluded from the pinned identity, mirroring the spec's
# confirmed-behavior pin: the status line is the workflow state, not the
# content the user confirmed, and the pin line itself would make the file
# a hash of itself. Each regex removes its whole line, newline included.
STATUS_LINE = re.compile(rb"^status:.*\n?", re.MULTILINE)
INTENT_CONFIRMED_SHA_LINE = re.compile(rb"^intent_confirmed_sha:.*\n?", re.MULTILINE)
CONFIRMED_STATUS = re.compile(rb"^status:\s*confirmed\s+\d{4}-\d{2}-\d{2}", re.MULTILINE)


def intent_identity(intent_path: Path) -> str:
    """The one blob sha the intent-version check compares against: the
    intent WITHOUT its status line and WITHOUT its `intent_confirmed_sha:`
    line -- the same convention the spec's confirmed-behavior pin follows."""
    raw = intent_path.read_bytes()
    return blob_sha(INTENT_CONFIRMED_SHA_LINE.sub(b"", STATUS_LINE.sub(b"", raw), count=1))


def recompute_command(relative: str) -> str:
    return (
        "recompute it with `git hash-object <(grep -v -e '^status:' -e "
        f"'^intent_confirmed_sha:' {relative})`"
    )


def check_intent_version(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str],
    attestation: dict,
) -> list[tuple[str, str]]:
    """The intent is the text whose confirmation the attestation pins.

    `intent_confirmed_sha` is optional bookkeeping: an attestation produced
    before it existed pins nothing and is not checked, and an intent whose
    status is not `confirmed <date>` has no confirmation to compare with.
    """
    rule = "intake.intent-version"

    intent_path = artifact_path(manifest, "intent", change_id, repo)
    if not intent_path.is_file():
        return []
    if not CONFIRMED_STATUS.search(intent_path.read_bytes()):
        return []

    recorded = attestation.get("intent_confirmed_sha")
    if not isinstance(recorded, str) or not recorded.strip():
        return []

    current = intent_identity(intent_path)
    if not sha_agrees(recorded, current):
        return [(
            rule,
            "the intent has changed since the attestation pinned its "
            f"confirmation (recorded {recorded.strip().lower()[:7]}, current "
            f"{current[:7]}); every Acceptance line of the intent may be "
            f"affected. {recompute_command('docs/loom/intent/' + change_id + '.md')} "
            "and re-confirm the intent before closing review",
        )]
    return []
