from __future__ import annotations

from loom_checker.digest import functional_content_digest
from loom_checker.helpers import git_ok
from loom_checker.probe_results import Row
from loom_checker.probe_results import claiming_row
from loom_checker.probes import argv_for
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
import posixpath


ATTESTATION_SCHEMA_V1 = "loom-attestation/v1"
ATTESTATION_SCHEMA = "loom-attestation/v2"


ATTESTATION_KEYS_V1 = {
    "schema", "change_id", "content_digest", "executions", "verdicts", "findings"
}
ATTESTATION_KEYS = ATTESTATION_KEYS_V1 | {"selection"}
KEYS_BY_SCHEMA = {ATTESTATION_SCHEMA_V1: ATTESTATION_KEYS_V1, ATTESTATION_SCHEMA: ATTESTATION_KEYS}


def _command_digest(command: str) -> str:
    return hashlib.sha256(command.encode("utf-8")).hexdigest()


ARTIFACT_PATH_FORM = "adversarial artifact must be a plain repository path (no `./`, `..` or `//`)"


def artifact_path_form_failure(artifact: str) -> str | None:
    """Refuse an artifact path whose spelling could leave the change's store:
    `git cat-file` normalises `./a/../b`, so a store `startswith` check alone
    would accept a path that resolves outside it."""
    if (artifact.startswith(("./", "../")) or ".." in artifact.split("/")
            or posixpath.normpath(artifact) != artifact):
        return ARTIFACT_PATH_FORM
    return None


def adversarial_route(command: str, artifact: str, repo: Path) -> tuple[str, Row | None]:
    """How an adversarial argv is decided, as one of:

    - `direct`: a Python/pytest or bash/sh program, or a directly executed
      artifact -- today's rules, no runner evidence;
    - `parsed`: a listed runner row in its accepted form (the row returned);
    - `reviewer`: an argv no row claims, which needs a reviewer confirmation;
    - `unnamed` / `not-executed`: today's refusals of a `direct` argv;
    - `not-accepted`: a row claims it but does not accept it (the row
      returned) -- refused whether or not a confirmation is supplied.
    """
    try:
        argv = argv_for(command)
    except ValueError:
        argv = None
    row = claiming_row(argv) if argv else None
    if row is not None:
        return ("parsed" if row.accepts(argv, artifact, repo) else "not-accepted"), row
    if (argv is None or Path(artifact).suffix.lower() in {".py", ".sh"}
            or command_executes_artifact(command, artifact)):
        if not command_names_artifact(command, artifact):
            return "unnamed", None
        if not command_executes_artifact(command, artifact):
            return "not-executed", None
        return "direct", None
    return "reviewer", None


def _evidence_failure(execution: dict, route: str, reviewers: set[str], digest: str) -> str | None:
    """Recompute what an adversarial execution's `evidence` may say."""
    evidence = execution.get("evidence")
    if route == "direct":
        return None if evidence is None else "a pytest, shell or direct execution carries runner evidence"
    passed = execution.get("passed")
    if route == "parsed" and evidence == "parsed":
        if isinstance(passed, int) and not isinstance(passed, bool) and passed >= 1:
            return None
        return "parsed adversarial evidence shows no passing test"
    if evidence != "reviewer":
        return "adversarial execution records neither a parsed passing result nor a reviewer confirmation"
    confirmation = execution.get("confirmation")
    if (not isinstance(confirmation, dict)
            or set(confirmation) != {"reviewer", "reviewed_sha", "content_digest", "quote"}
            or any(not isinstance(value, str) or not value.strip() for value in confirmation.values())):
        return "adversarial reviewer confirmation is malformed"
    if confirmation["reviewer"].strip() not in reviewers:
        return "adversarial confirmation reviewer is not one of the verdict reviewers"
    if confirmation["content_digest"] != digest:
        return "adversarial confirmation was given for other functional content"
    return None


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
    recorded = attestation.get("verdicts")
    verdict_reviewers = {str(v.get("reviewer", "")).strip() for v in recorded
                         if isinstance(v, dict)} if isinstance(recorded, list) else set()
    verdict_reviewers.discard("")
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
            path_failure = artifact_path_form_failure(artifact)
            if path_failure:
                return [(rule, path_failure)]
            route, row = adversarial_route(command, artifact, repo)
            if route == "unnamed":
                return [(rule, "adversarial command does not name its artifact")]
            if route == "not-executed":
                return [(rule, "adversarial command must execute the artifact directly")]
            if route == "not-accepted":
                return [(rule, f"adversarial command is a {row.name} command but not in its "
                               f"accepted form for its artifact")]
            evidence_failure = _evidence_failure(execution, route, verdict_reviewers, expected)
            if evidence_failure:
                return [(rule, evidence_failure)]
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
