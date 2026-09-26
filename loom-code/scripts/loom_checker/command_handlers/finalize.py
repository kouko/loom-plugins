from __future__ import annotations

from loom_checker import selection
from loom_checker.attestation import ATTESTATION_SCHEMA
from loom_checker.attestation import _command_digest
from loom_checker.attestation import selection_evidence
from loom_checker.digest import functional_content_digest
from loom_checker.helpers import TRUNK_BRANCH_NAMES
from loom_checker.helpers import UsageError
from loom_checker.helpers import artifact_path
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_ok
from loom_checker.helpers import git_text
from loom_checker.helpers import load_manifest
from loom_checker.helpers import read_text
from loom_checker.helpers import repo_root
from loom_checker.helpers import report
from loom_checker.probes import NO_PACKAGE_TESTS
from loom_checker.probes import PROBE_RUN_TIMEOUT
from loom_checker.probes import argv_for
from loom_checker.probes import check_adversarial_proportionate
from loom_checker.probes import command_executes_artifact
from loom_checker.probes import command_names_artifact
from loom_checker.probes import declared_test_command
from loom_checker.probes import missing_adversarial_execution
from loom_checker.probes import probe_directory
from loom_checker.probes import suite_collects
from loom_checker.reviewers import auto_skipped_steps
from loom_checker.reviewers import committed_branch_delta
from loom_checker.reviewers import required_reviewer_count
from pathlib import Path
import json
import subprocess
import sys
import tempfile


# The step a refused finalize rule belongs to. Only these rules (execution
# failures included) record a failure; refusals no step owns, such as a dirty
# tree, a usage error or a malformed input, verify nothing and record none.
STEP_BY_RULE = {
    "finalize.verdicts": "reviewers",
    "finalize.adversarial": "adversarial",
    "adversarial.proportionate": "adversarial",
    "finalize.package-tests": "package-tests",
}


def _record_failure(repo: Path, change_id: str, rule: str) -> None:
    """Append a failure event for a step's rule; a store that cannot be
    written never masks the refusal."""
    if rule not in STEP_BY_RULE:
        return
    try:
        selection.append_event(repo, change_id, {
            "event": "failure", "step": STEP_BY_RULE[rule], "rule": rule,
            "head_sha": git_maybe(repo, "rev-parse", "HEAD"),
            "branch": git_maybe(repo, "rev-parse", "--abbrev-ref", "HEAD"),
            "at": selection.now(),
        })
    except (UsageError, OSError):
        pass


def cmd_finalize_review(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Run functional verification once and generate content-bound evidence."""
    if not args:
        raise UsageError("finalize-review needs a change-id.")
    change_id, *rest = args
    repo = repo_root(Path.cwd())
    findings = _finalize(repo, change_id, rest, out)
    if findings:
        _record_failure(repo, change_id, findings[0][0])
        return report(findings, err)
    return 0


def _finalize(repo: Path, change_id: str, rest: list[str], out) -> list[tuple[str, str]]:
    if len(rest) != 2 or rest[0] != "--input":
        raise UsageError("finalize-review expects `--input <review-input.json>`.")
    input_path = Path(rest[1])
    try:
        review_input = json.loads(read_text(input_path))
    except (OSError, json.JSONDecodeError) as exc:
        raise UsageError(f"cannot read review input: {exc}") from exc
    if not isinstance(review_input, dict):
        raise UsageError("review input must be a JSON object.")
    head_sha = git_text(repo, "rev-parse", "HEAD")
    status_before = git_text(repo, "status", "--porcelain")
    if status_before:
        return [("finalize.clean-tree", "commit functional content before finalizing review")]
    if committed_branch_delta(repo, change_id, head_sha) is None:
        # `auto_skipped_steps` answers "every auto-skippable step is skipped"
        # when the delta cannot be recomputed, and that permissive reading is
        # correct exactly once: in `attestation.py`, re-validating evidence
        # that already exists and is bound to the commit's content. Here the
        # evidence does not exist yet — finalize is making it — so the same
        # answer would let a change that touches production code waive the
        # adversarial step by being finalized in a checkout that cannot see
        # the trunk. Finalize therefore fails closed, and says why.
        return [("finalize.delta",
                 "cannot recompute this branch's committed delta, so which "
                 "steps a narrow change would skip cannot be established; "
                 "finalize review in a checkout that resolves the trunk "
                 f"({', '.join(sorted(TRUNK_BRANCH_NAMES))}), or fetch it")]
    manifest = load_manifest()
    bound = selection_evidence(repo, change_id, manifest)
    skip = (set(bound["skip"]) if bound is not None
            else auto_skipped_steps(repo, change_id, head_sha))
    verdicts = review_input.get("verdicts", [] if "reviewers" in skip else None)
    findings = review_input.get("findings", [])
    adversarial = review_input.get("adversarial", [])
    if not isinstance(verdicts, list) or (not verdicts and "reviewers" not in skip):
        return [("finalize.verdicts", "review input has no verdicts")]
    if any(not isinstance(v, dict) or v.get("verdict") not in {
        "PASS", "PASS_WITH_NOTES"
    } for v in verdicts):
        return [("finalize.verdicts", "every reviewer verdict must pass")]
    reviewers = {str(v.get("reviewer", "")).strip() for v in verdicts}
    reviewers.discard("")
    reviewer_floor = 0 if "reviewers" in skip else required_reviewer_count(repo, change_id, head_sha)
    if len(reviewers) < reviewer_floor:
        needed = "two" if reviewer_floor == 2 else "one"
        return [("finalize.verdicts", f"{needed} distinct reviewers are required")]
    if not isinstance(findings, list) or not isinstance(adversarial, list):
        return [("finalize.schema", "findings and adversarial must be lists")]
    missing = missing_adversarial_execution(len(adversarial), skip)
    if missing:
        return [("finalize.adversarial", missing)]
    config_before = git_text(repo, "config", "--list", "--null")
    work: list[tuple[str, str, str]] = []
    if "package-tests" not in skip:
        package_command, source = declared_test_command(repo)
        if package_command is None or package_command.strip().lower() == NO_PACKAGE_TESTS:
            return [("finalize.package-tests", f"no executable package command ({source})")]
        work.append(("package-tests", package_command, ""))
    for item in adversarial:
        if not isinstance(item, dict):
            return [("finalize.adversarial", "malformed adversarial input")]
        command = str(item.get("command", "")).strip()
        artifact = str(item.get("artifact", "")).strip()
        if not command or not artifact:
            return [("finalize.adversarial", "adversarial input needs command and artifact")]
        if not command_names_artifact(command, artifact):
            return [("finalize.adversarial", "command must name its artifact argument")]
        if not command_executes_artifact(command, artifact):
            return [("finalize.adversarial", "command must execute the artifact directly")]
        if not git_ok(repo, "cat-file", "-e", f"{head_sha}:{artifact}"):
            return [("finalize.adversarial", "artifact must exist in the selected commit")]
        if not artifact.startswith(probe_directory(change_id)) and not suite_collects(repo, artifact):
            # A probe program has two legal homes. In this change's probe
            # directory it is counted by `adversarial.proportionate`, which
            # reads that directory only. Graduated into the package suite it
            # is an ordinary permanent test: the suite runs it on every later
            # change and reviewers read it, so it escapes neither the cap nor
            # review by leaving the store. An artifact in neither home is a
            # program that gets executed and is answerable to nothing.
            return [("finalize.adversarial",
                     f"adversarial artifact must be committed under "
                     f"{probe_directory(change_id)} or be a program the "
                     f"package suite already runs")]
        work.append(("adversarial", command, artifact))

    # Every artifact is now in a legal home, so the cap can count them: what
    # finalize-review is about to execute is this change's adversarial output
    # wherever graduation has since moved it.
    proportionate = check_adversarial_proportionate(
        repo, head_sha, change_id,
        [artifact for kind, _command, artifact in work if kind == "adversarial"],
    )
    if proportionate:
        return proportionate

    executions: list[dict] = []
    for kind, command, artifact in work:
        try:
            completed = subprocess.run(
                argv_for(command), cwd=str(repo), capture_output=True, text=True,
                timeout=PROBE_RUN_TIMEOUT,
            )
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            return [(f"finalize.{kind}", f"execution failed: {exc}")]
        if completed.returncode != 0:
            detail = (completed.stdout + completed.stderr).strip()
            suffix = f"\n{detail[-4000:]}" if detail else ""
            return [(
                f"finalize.{kind}",
                f"`{command}` exited {completed.returncode}{suffix}",
            )]
        executions.append({
            "kind": kind, "command": command, "artifact": artifact,
            "result": "pass", "command_digest": _command_digest(command),
        })

    if git_text(repo, "rev-parse", "HEAD") != head_sha:
        return [("finalize.stable-tree", "HEAD moved during functional verification")]
    if git_text(repo, "status", "--porcelain") != status_before:
        return [("finalize.stable-tree", "working tree or index changed during functional verification")]
    if git_text(repo, "config", "--list", "--null") != config_before:
        return [("finalize.stable-tree", "git configuration changed during functional verification")]

    digest = functional_content_digest(repo, head_sha, change_id, manifest)
    if digest is None:
        return [("finalize.digest", "cannot compute functional content digest")]
    attestation = {
        "schema": ATTESTATION_SCHEMA, "change_id": change_id,
        "content_digest": digest, "executions": executions,
        "verdicts": verdicts, "findings": findings, "selection": bound,
    }
    target = artifact_path(manifest, "attestation", change_id, repo)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=target.parent, prefix=f".{target.name}.", delete=False,
    ) as handle:
        json.dump(attestation, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(target)
    out.write(f"wrote {target.relative_to(repo)} for {digest}\n")
    return []
