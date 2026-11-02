from __future__ import annotations

from loom_checker.digest import functional_content_digest
from loom_checker.attestation import ATTESTATION_SCHEMA_V1, ATTESTATION_SCHEMA, ATTESTATION_KEYS_V2_LEGACY
from loom_checker.attestation import NEW_CONFIRMATION_FIELDS
from loom_checker.helpers import artifact_text, git_maybe
from loom_checker.rule_checks.intent_version import pinned_confirmation
from pathlib import Path
import re


def report_tested_commit(report_text: str) -> str | None:
    """The single canonical Tried-on line's commit, never an arbitrary `at`."""
    if len(re.findall(r"^Tried on\b", report_text, re.IGNORECASE | re.MULTILINE)) != 1:
        return None
    matches = re.findall(
        r"^Tried on[^\n]*?\bat\s+([0-9a-f]{7,64})(?=[\s.]|$)",
        report_text, re.IGNORECASE | re.MULTILINE,
    )
    return matches[0].lower() if len(matches) == 1 else None


def check_commit_identity(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str],
    attestation: dict, *, commit: str | None = None,
) -> list[tuple[str, str]]:
    """The tested tree and the reviewed tree carry the same functional content.

    Bookkeeping-v2 records both ``tested_commit`` and ``reviewed_commit``;
    exact historical v1 and seven-key v2 records are exempt. Both commits
    must resolve and carry equal functional content. A selected commit also
    binds that reviewed content to the tree being validated. A report that
    declares Tried-on provenance must agree with the recorded tested commit.
    """
    rule = "intake.commit-identity"

    schema = attestation.get("schema")
    tested = attestation.get("tested_commit")
    reviewed = attestation.get("reviewed_commit")

    # Exact historical shapes predate these fields.
    if schema == ATTESTATION_SCHEMA_V1 or (
        schema == ATTESTATION_SCHEMA and set(attestation) == ATTESTATION_KEYS_V2_LEGACY
    ):
        if pinned_confirmation(manifest, repo, change_id, commit=commit) is not None:
            return [(rule, NEW_CONFIRMATION_FIELDS)]
        return []

    # v2 attestations must have both bookkeeping fields.
    if not tested or not reviewed:
        return [(
            rule,
            "v2 attestation is missing required bookkeeping fields: "
            f"tested_commit={tested!r} reviewed_commit={reviewed!r}; "
            "the acceptance test report and closing review must supply them"
        )]

    resolved = []
    for label, value in (("tested", tested), ("reviewed", reviewed)):
        sha = (git_maybe(repo, "rev-parse", "--verify", f"{value}^{{commit}}")
               if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{7,64}", value) else None)
        if sha is None:
            return [(rule, f"cannot resolve {label} commit {value!r}")]
        resolved.append(sha)
    tested_digest = functional_content_digest(repo, resolved[0], change_id, manifest)
    reviewed_digest = functional_content_digest(repo, resolved[1], change_id, manifest)
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
    if commit is not None:
        selected_digest = functional_content_digest(repo, commit, change_id, manifest)
        if selected_digest is None or reviewed_digest != selected_digest:
            return [(rule, "the reviewed commit does not have the selected tree's functional content")]
    report_text = artifact_text(manifest, "acceptance-test-report", change_id, repo, commit=commit)
    if report_text is not None and re.search(r"^Tried on\b", report_text, re.IGNORECASE | re.MULTILINE):
        declared = report_tested_commit(report_text)
        declared_sha = (git_maybe(repo, "rev-parse", "--verify", f"{declared}^{{commit}}")
                        if declared else None)
        if declared_sha != resolved[0]:
            return [(rule, "acceptance report's Tried-on commit is missing, invalid, or differs from tested_commit")]
    return []
