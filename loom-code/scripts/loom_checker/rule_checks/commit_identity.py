from __future__ import annotations

from loom_checker.digest import functional_content_digest
from pathlib import Path


def check_commit_identity(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str],
    attestation: dict,
) -> list[tuple[str, str]]:
    """The tested tree and the reviewed tree carry the same functional content.

    ``tested_commit`` and ``reviewed_commit`` are optional bookkeeping fields:
    an attestation produced before they existed carries neither and is not
    checked. When both are present, their functional-content digests must
    match -- evidence and publication files are already excluded from that
    digest, so an evidence file differing between the two commits does not
    fail the check while a functional change does.
    """
    rule = "intake.commit-identity"

    tested = attestation.get("tested_commit")
    reviewed = attestation.get("reviewed_commit")
    if not tested or not reviewed:
        # Absent bookkeeping: pre-field attestation, or acceptance testing
        # skipped. Nothing to compare.
        return []

    tested_digest = functional_content_digest(repo, str(tested), change_id, manifest)
    reviewed_digest = functional_content_digest(repo, str(reviewed), change_id, manifest)
    if tested_digest is None:
        return [(rule, f"cannot compute functional content digest for tested commit {str(tested)[:7]}")]
    if reviewed_digest is None:
        return [(rule, f"cannot compute functional content digest for reviewed commit {str(reviewed)[:7]}")]
    if tested_digest != reviewed_digest:
        return [(
            rule,
            "functional content differs between the tested commit "
            f"{str(tested)[:7]} and the reviewed commit {str(reviewed)[:7]}; "
            "the acceptance evidence was produced on other code than what is "
            "being reviewed",
        )]
    return []