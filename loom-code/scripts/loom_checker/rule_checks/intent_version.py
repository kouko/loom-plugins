from __future__ import annotations

from loom_checker.helpers import artifact_path, artifact_text, blob_sha, git_text, sha_agrees
from pathlib import Path
import re


# The lines excluded from the pinned identity, mirroring the spec's
# confirmed-behavior pin: the status line is the workflow state, not the
# content the user confirmed, and the pin line itself would make the file
# a hash of itself. Each regex removes its whole line, newline included.
STATUS_LINE = re.compile(rb"^status:.*\n?", re.MULTILINE)
INTENT_CONFIRMED_SHA_LINE = re.compile(rb"^intent_confirmed_sha:.*\n?", re.MULTILINE)
CONFIRMED_STATUS = re.compile(rb"^status:\s*confirmed\s+\d{4}-\d{2}-\d{2}", re.MULTILINE)
PIN_VALUE = re.compile(rb"^intent_confirmed_sha:[ \t]*([0-9a-f]{7,64})[ \t]*\r?$", re.MULTILINE | re.IGNORECASE)


def intent_identity(intent_path: Path) -> str:
    """The one blob sha the intent-version check compares against: the
    intent WITHOUT its status line and WITHOUT its `intent_confirmed_sha:`
    line -- the same convention the spec's confirmed-behavior pin follows."""
    return _content_identity(intent_path.read_bytes())


def _content_identity(raw: bytes) -> str:
    return blob_sha(INTENT_CONFIRMED_SHA_LINE.sub(b"", STATUS_LINE.sub(b"", raw), count=1))


def recompute_command(relative: str) -> str:
    """A POSIX-safe pipeline: bash process substitution `<(...)` prints
    nothing under a minimal `sh`, so the printed fix has to survive it."""
    return (
        "recompute it with `grep -v -e '^status:' -e '^intent_confirmed_sha:' "
        f"{relative} | git hash-object --stdin`"
    )


def pinned_confirmation(
    manifest, repo: Path, change_id: str, *, commit: str | None = None,
) -> tuple[str, bytes] | None:
    """The selected ancestry's latest canonical confirmation, when pinned."""
    relative = artifact_path(manifest, "intent", change_id, repo).relative_to(repo).as_posix()
    # Full history follows every merge parent despite path simplification;
    # selected ancestry and topological order keep children before parents:
    # https://git-scm.com/docs/git-log . Hash/NUL/subject format codes:
    # https://git-scm.com/docs/pretty-formats (verified 2026-11-02).
    history = git_text(repo, "log", "--full-history", "--topo-order", "--format=%H%x00%s", commit or "HEAD", "--", relative)
    subject = f"docs(loom): intent {change_id} confirmed"
    for entry in history.splitlines():
        sha, _, title = entry.partition("\0")
        if title == subject:
            confirmed = artifact_text(manifest, "intent", change_id, repo, commit=sha)
            raw = (confirmed or "").encode("utf-8", "surrogateescape")
            return (sha, raw) if INTENT_CONFIRMED_SHA_LINE.search(raw) else None
    return None


def check_intent_version(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str],
    attestation: dict, *, commit: str | None = None,
) -> list[tuple[str, str]]:
    """A pinned canonical confirmation is the immutable intent baseline.

    Search only the selected tree's ancestry. A confirmation predating pins
    supplies no new baseline; otherwise retain the existing direct pin checks.
    """
    rule = "intake.intent-version"

    intent_text = artifact_text(manifest, "intent", change_id, repo, commit=commit)
    raw = intent_text.encode("utf-8", "surrogateescape") if intent_text is not None else b""
    relative = artifact_path(manifest, "intent", change_id, repo).relative_to(repo).as_posix()
    confirmation = pinned_confirmation(manifest, repo, change_id, commit=commit)
    if confirmation is not None:
        sha, baseline = confirmation
        pin = PIN_VALUE.search(baseline)
        expected = _content_identity(baseline)
        if pin is None or not sha_agrees(pin.group(1).decode(), expected):
            return [(rule, f"confirmation commit {sha[:7]} has an invalid intent pin; re-confirm the intent")]
        current_pin = PIN_VALUE.search(raw)
        recorded = attestation.get("intent_confirmed_sha")
        if (not CONFIRMED_STATUS.search(raw) or _content_identity(raw) != expected
                or current_pin is None or not sha_agrees(current_pin.group(1).decode(), expected)
                or not isinstance(recorded, str) or not re.fullmatch(r"[0-9a-fA-F]{7,64}", recorded)
                or not sha_agrees(recorded, expected)):
            return [(
                rule,
                f"the intent no longer matches confirmation commit {sha[:7]} "
                f"(confirmed {expected[:7]}, current {_content_identity(raw)[:7]}); "
                "every Acceptance line may be affected. "
                f"{recompute_command(relative)} and re-confirm the intent before closing review",
            )]
        return []
    if intent_text is None:
        return []
    if not CONFIRMED_STATUS.search(raw):
        return []

    recorded = attestation.get("intent_confirmed_sha")
    if not isinstance(recorded, str) or not recorded.strip():
        if "intent_confirmed_sha" in attestation and INTENT_CONFIRMED_SHA_LINE.search(raw):
            return [(rule, "attestation is missing the intent's confirmation pin; re-confirm the intent")]
        return []

    current = _content_identity(raw)
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
