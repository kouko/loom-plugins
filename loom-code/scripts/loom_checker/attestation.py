from __future__ import annotations

from loom_checker import selection
from loom_checker.digest import functional_content_digest
from loom_checker.helpers import UsageError
from loom_checker.helpers import git_ok
from loom_checker.probes import command_executes_artifact
from loom_checker.probes import command_names_artifact
from loom_checker.probes import declared_test_command
from loom_checker.probes import missing_adversarial_execution
from loom_checker.reviewers import auto_skipped_steps
from loom_checker.reviewers import required_reviewer_count
from pathlib import Path
import hashlib


ATTESTATION_SCHEMA_V1 = "loom-attestation/v1"
ATTESTATION_SCHEMA = "loom-attestation/v2"


ATTESTATION_KEYS_V1 = {
    "schema", "change_id", "content_digest", "executions", "verdicts", "findings"
}
ATTESTATION_KEYS = ATTESTATION_KEYS_V1 | {"selection"}
KEYS_BY_SCHEMA = {ATTESTATION_SCHEMA_V1: ATTESTATION_KEYS_V1, ATTESTATION_SCHEMA: ATTESTATION_KEYS}


FAILURE_FIELDS = ("step", "rule", "head_sha", "branch", "at")


def _command_digest(command: str) -> str:
    return hashlib.sha256(command.encode("utf-8")).hexdigest()


def selection_evidence(repo: Path, change_id: str, manifest: dict | None = None) -> dict | None:
    """The attestation `selection` the local records support, or None.

    Only a valid confirmation whose source is `user-typed`, recorded on the
    current branch and merge base, binds; anything else is the full process.
    `confirmations` lists only bindings no later cancel withdrew, and
    `prior_failures` lists failures recorded before the newest of them (by
    position in the append-only file, not by timestamp)."""
    events = selection.read_events(repo, change_id)
    if not any(event.get("event") == "confirmation" for event in events):
        return None
    vocabulary = manifest if isinstance(manifest, dict) and manifest.get("step_selection") else None
    try:
        effective = selection.effective_selection(repo, change_id, vocabulary)
        branch, merge_base = selection.current_scope(repo)
        names = [step["name"] for step in selection.step_vocabulary(vocabulary)]
    except UsageError:
        return None
    if not effective["bound"] or effective.get("source") != "user-typed":
        return None
    def in_scope(event: dict) -> bool:
        return event.get("branch") == branch and event.get("merge_base") == merge_base

    proposals = {e.get("id"): e for e in events if in_scope(e) and e.get("event") == "proposal"}
    confirmations = []
    latest = -1
    for index, event in enumerate(events):
        if not in_scope(event):
            continue
        if event.get("event") == "cancel":
            confirmations, latest = [], -1  # withdrawn bindings are not disclosed
            continue
        if event.get("event") != "confirmation" or event.get("source") != "user-typed":
            continue
        proposal = proposals.get(event.get("proposal_id"))
        if (proposal is None or not selection.confirmation_is_valid(event, proposal)
                or not selection.session_matches(event)):
            continue
        confirmations.append({
            "code": proposal["code"], "skip": [n for n in names if n in proposal["skip"]],
            "source": event["source"], "at": event.get("at"),
        })
        latest = index
    prior = [
        {key: failure.get(key) for key in FAILURE_FIELDS}
        for failure in events[:max(latest, 0)]
        if failure.get("event") == "failure"
    ]
    return {"confirmations": confirmations, "skip": effective["skip"],
            "source": "user-typed", "prior_failures": prior}


def validate_attestation(
    repo: Path, head_sha: str, change_id: str, attestation: object,
    manifest: dict | None = None, claimed_selection: bool = False,
) -> list[tuple[str, str]]:
    """Validate generated evidence without executing the recorded programs.

    `claimed_selection` runs the content-level checks only: the attestation's
    own `selection` is taken as a claim and never compared with the local
    selection records, which a fresh checkout (CI) does not have."""
    rule = "push.attestation"
    if not isinstance(attestation, dict) or set(attestation) not in KEYS_BY_SCHEMA.values():
        return [(rule, "attestation has an unknown or incomplete schema")]
    schema = attestation.get("schema")
    if schema not in KEYS_BY_SCHEMA:
        return [(rule, f"unsupported attestation schema {schema!r}")]
    if set(attestation) != KEYS_BY_SCHEMA[schema]:
        return [(rule, "attestation has an unknown or incomplete schema")]
    if attestation.get("change_id") != change_id:
        return [(rule, "attestation change_id does not match its path")]
    expected = functional_content_digest(repo, head_sha, change_id, manifest)
    if expected is None or attestation.get("content_digest") != expected:
        return [(rule, "attestation functional content digest does not match the selected tree")]

    skip: set[str] = set()
    if schema == ATTESTATION_SCHEMA and claimed_selection:
        claim = attestation.get("selection")
        if claim is not None:
            claimed = claim.get("skip") if isinstance(claim, dict) else None
            if not isinstance(claimed, list) or not all(isinstance(s, str) for s in claimed):
                return [(rule, "attestation selection claim is malformed")]
            skip = set(claimed)
    elif schema == ATTESTATION_SCHEMA:
        recorded = selection_evidence(repo, change_id, manifest)
        if attestation.get("selection") != recorded:
            return [(rule, "attestation selection does not match the local selection records")]
        if recorded is not None:
            skip = set(recorded["skip"])
    skip |= auto_skipped_steps(repo, change_id, head_sha)

    executions = attestation.get("executions")
    if not isinstance(executions, list) or (
        not executions and not {"package-tests", "adversarial"} <= skip
    ):
        return [(rule, "attestation records no successful functional executions")]
    package_runs = 0
    adversarial_runs = 0
    for execution in executions:
        if not isinstance(execution, dict):
            return [(rule, "attestation contains a malformed execution")]
        command = execution.get("command")
        if not isinstance(command, str) or not command.strip():
            return [(rule, "attestation execution has no command")]
        if execution.get("command_digest") != _command_digest(command):
            return [(rule, "attestation execution command digest is forged or corrupted")]
        if execution.get("result") != "pass":
            return [(rule, "attestation contains a non-passing execution")]
        if execution.get("kind") == "package-tests":
            package_runs += 1
            declared, _ = declared_test_command(repo)
            if command != declared:
                return [(rule, "package-tests execution does not match the declared package command")]
        elif execution.get("kind") == "adversarial":
            adversarial_runs += 1
            artifact = execution.get("artifact")
            if not isinstance(artifact, str) or not artifact.strip():
                return [(rule, "adversarial execution names no artifact")]
            if not command_names_artifact(command, artifact):
                return [(rule, "adversarial command does not name its artifact")]
            if not command_executes_artifact(command, artifact):
                return [(rule, "adversarial command must execute the artifact directly")]
            if not git_ok(repo, "cat-file", "-e", f"{head_sha}:{artifact}"):
                return [(rule, "adversarial execution names no committed artifact")]
        else:
            return [(rule, "attestation contains an unknown execution kind")]
    if package_runs > 1 or (package_runs == 0 and "package-tests" not in skip):
        return [(rule, "attestation must record exactly one package-tests execution")]
    missing = missing_adversarial_execution(adversarial_runs, skip)
    if missing:
        return [(rule, missing)]

    verdicts = attestation.get("verdicts")
    if not isinstance(verdicts, list) or (not verdicts and "reviewers" not in skip):
        return [(rule, "attestation records no reviewer verdict")]
    reviewers = {str(v.get("reviewer", "")).strip() for v in verdicts if isinstance(v, dict)}
    reviewers.discard("")
    reviewer_floor = 0 if "reviewers" in skip else required_reviewer_count(repo, change_id, head_sha)
    if len(reviewers) < reviewer_floor:
        needed = "two" if reviewer_floor == 2 else "one"
        return [(rule, f"attestation needs {needed} distinct reviewers")]
    for verdict in verdicts:
        if not isinstance(verdict, dict) or verdict.get("verdict") not in {
            "PASS", "PASS_WITH_NOTES"
        }:
            return [(rule, "attestation contains a malformed or non-passing reviewer verdict")]
    if not isinstance(attestation.get("findings"), list):
        return [(rule, "attestation findings must be a list")]
    return []
