from __future__ import annotations

from loom_checker.digest import functional_content_digest
from loom_checker.attestation import ATTESTATION_SCHEMA_V1, ATTESTATION_SCHEMA
from pathlib import Path


def check_commit_identity(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str],
    attestation: dict,
) -> list[tuple[str, str]]:
    """The tested tree and the reviewed tree carry the same functional content.

    v2 attestations MUST record both ``tested_commit`` and ``reviewed_commit``.
    Missing bookkeeping fields on a v2 attestation is a failure -- the flow
    guarantees the acceptance tester and closing-review supply them. v1
    attestations (which lack these fields entirely) are exempt and skipped.
    When both fields are present, their functional-content digests must match.
    """
    rule = "intake.commit-identity"

    schema = attestation.get("schema")
    tested = attestation.get("tested_commit")
    reviewed = attestation.get("reviewed_commit")

    # v1 attestations predate these fields; skip them entirely.
    if schema == ATTESTATION_SCHEMA_V1:
        return []

    # v2 attestations must have both bookkeeping fields.
    if not tested or not reviewed:
        return [(
            rule,
            "v2 attestation is missing required bookkeeping fields: "
            f"tested_commit={tested!r} reviewed_commit={reviewed!r}; "
            "the acceptance test report and closing review must supply them"
        )]

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