from __future__ import annotations

from loom_checker.digest import functional_content_digest
from loom_checker.helpers import git_ok
from loom_checker.probes import command_executes_artifact
from loom_checker.probes import command_names_artifact
from loom_checker.probes import declared_test_command
from loom_checker.probes import missing_adversarial_execution
from loom_checker.reviewers import auto_skipped_steps
from loom_checker.reviewers import required_reviewer_count
from loom_checker.reviewers import outside_verdict_failure
from loom_checker.reviewers import selected_outside_family
from pathlib import Path
import hashlib


ATTESTATION_SCHEMA_V1 = "loom-attestation/v1"
ATTESTATION_SCHEMA = "loom-attestation/v2"


ATTESTATION_KEYS_V1 = {
    "schema", "change_id", "content_digest", "executions", "verdicts", "findings"
}
ATTESTATION_KEYS = ATTESTATION_KEYS_V1 | {"selection"}
KEYS_BY_SCHEMA = {ATTESTATION_SCHEMA_V1: ATTESTATION_KEYS_V1, ATTESTATION_SCHEMA: ATTESTATION_KEYS}


def _command_digest(command: str) -> str:
    return hashlib.sha256(command.encode("utf-8")).hexdigest()


def validate_attestation(
    repo: Path, head_sha: str, change_id: str, attestation: object,
    manifest: dict | None = None,
) -> list[tuple[str, str]]:
    """Validate generated evidence without executing the recorded programs.

    A v2 attestation keeps its `selection` key, and the key must be null: no
    typed confirmation can waive a step any more, so a recorded selection
    matches nothing. Only the automatic narrow-change simplification skips."""
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

    if schema == ATTESTATION_SCHEMA and attestation.get("selection") is not None:
        return [(rule, "attestation records a step selection, which nothing can bind")]
    skip = auto_skipped_steps(repo, change_id, head_sha)

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
    outside_failure = outside_verdict_failure(
        verdicts, selected_outside_family(repo, change_id, head_sha), head_sha,
        repo=repo, change_id=change_id, content_digest=expected, manifest=manifest,
    )
    if outside_failure:
        return [(rule, outside_failure)]
    if not isinstance(attestation.get("findings"), list):
        return [(rule, "attestation findings must be a list")]
    return []
