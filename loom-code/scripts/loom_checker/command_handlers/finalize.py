from __future__ import annotations

from loom_checker.attestation import ATTESTATION_SCHEMA
from loom_checker.attestation import _command_digest
from loom_checker.attestation import adversarial_route
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
from loom_checker.probes import declared_test_command
from loom_checker.probes import missing_adversarial_execution
from loom_checker.probes import probe_directory
from loom_checker.probes import runs_pytest
from loom_checker.probes import suite_collection
from loom_checker.reviewers import auto_skipped_steps
from loom_checker.reviewers import committed_branch_delta
from loom_checker.reviewers import required_reviewer_count
from loom_checker.reviewers import attach_outside_receipt
from loom_checker.reviewers import selected_outside_family
from pathlib import Path
import json
import re
import subprocess
import sys
import tempfile


_DURATIONS = (
    (re.compile(r"""(\btime=)(["'])[^"']*\2"""), r"\1\2<duration>\2"),
    (re.compile(r"""(\bduration_ms["']?\s*[:=]\s*)\d+(?:\.\d+)?"""), r"\1<duration>"),
    (re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?\b"), "<duration>"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*(?:ms|seconds?|secs?|s)\b"), "<duration>"),
)


def _without_durations(line: str) -> str:
    """`line` with every duration value replaced by one placeholder: the
    probe's output was quoted from an earlier run, and only timings differ."""
    for pattern, placeholder in _DURATIONS:
        line = pattern.sub(placeholder, line)
    return line


def _quotes_whole_lines(quote: str, output: str, stem: str) -> bool:
    """`quote` is one or more complete, non-blank lines that appear in a row
    in `output` and together name the artifact's file stem. Duration values
    are ignored; every other character, counts included, must match."""
    wanted = [_without_durations(line.strip()) for line in quote.splitlines()]
    if not wanted or any(not line for line in wanted) or stem not in quote:
        return False
    lines = [_without_durations(line.strip()) for line in output.splitlines()]
    return any(lines[start:start + len(wanted)] == wanted
               for start in range(len(lines) - len(wanted) + 1))


_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_PYTEST_SUMMARY = re.compile(
    r"^=*\s*((?:\d+ \w+)(?:, \d+ \w+)*) in \d+(?:\.\d+)?s\b.*$"
)


def _pytest_summary_failure(command: str, output: str) -> str | None:
    """Why a pytest probe that exited 0 is not shown to have run its own
    tests, read from pytest's final summary line (`2 passed, 1 deselected in
    0.01s`): a deselecting filter (argv, config or plugin), no passed test, or
    no summary line at all -- an unreadable run is refused, never attested."""
    lines = [_ANSI.sub("", line).strip() for line in output.splitlines()]
    summary = next((match for line in reversed(lines)
                    if (match := _PYTEST_SUMMARY.match(line))), None)
    if summary is None:
        return (f"`{command}` exited 0, but its output has no pytest summary line "
                f"(such as `1 passed in 0.01s`), so loom cannot tell that the probe's "
                f"tests ran; drop `-qq` or any option that hides the summary")
    counts = {word: int(number) for number, word in
              (part.split(" ", 1) for part in summary.group(1).split(", "))}
    if counts.get("deselected", 0):
        return (f"`{command}` exited 0, but pytest deselected {counts['deselected']} "
                f"test(s) (`{summary.group(1)}`); a filter from the command, config or a "
                f"plugin kept the probe's own tests from running")
    if not counts.get("passed", 0):
        return (f"`{command}` exited 0, but its pytest summary (`{summary.group(1)}`) "
                f"shows no passed test")
    return None


def _runner_evidence(
    repo: Path, change_id: str, head_sha: str, manifest: dict, reviewers: set[str],
    command: str, artifact: str, how: dict, output: str,
) -> tuple[dict, str | None]:
    """The `evidence` fields for a passing non-pytest/shell adversarial run, or
    the reason it is refused: a listed row's own count of passing tests, else
    a verdict reviewer's confirmation bound to this content and this output."""
    row = how["row"]
    if how["route"] == "parsed":
        passed = row.passed(output, artifact)
        if passed is not None and passed >= 1:
            return {"evidence": "parsed", "passed": passed}, None
        if passed == 0:
            return {}, (f"`{command}` exited 0, but its {row.name} output shows no passing, "
                        f"non-skipped test from {artifact} (zero tests, all skipped, or tests "
                        f"from another file); a reviewer confirmation cannot stand in for it")
        reason = f"loom cannot read its {row.name} output"
    else:
        reason = "no listed runner claims it, so loom cannot read its result"
    stem = Path(artifact).stem
    needed = (f"`{command}` exited 0, but {reason}; attesting it needs a reviewer "
              f"confirmation on its adversarial input item, `confirmation: {{reviewer, "
              f"reviewed_sha, quote}}`, from one of this round's verdict reviewers who read "
              f"this run's output at HEAD's content, quoting one or more whole lines of the "
              f"output below that name `{stem}`")
    confirmation = how["confirmation"]
    if confirmation is None:
        return {}, needed
    if (not isinstance(confirmation, dict)
            or any(not isinstance(confirmation.get(key), str) or not confirmation[key].strip()
                   for key in ("reviewer", "reviewed_sha", "quote"))):
        return {}, f"the reviewer confirmation is malformed. {needed}"
    reviewer = confirmation["reviewer"].strip()
    if reviewer not in reviewers:
        return {}, f"the confirmation's reviewer {reviewer!r} gave no verdict this round. {needed}"
    head_digest = functional_content_digest(repo, head_sha, change_id, manifest)
    sha = confirmation["reviewed_sha"].strip()
    resolved = (git_maybe(repo, "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}")
                if re.fullmatch(r"[0-9a-f]{7,64}", sha) else None)
    if (head_digest is None or not resolved
            or functional_content_digest(repo, resolved, change_id, manifest) != head_digest):
        return {}, (f"the confirmation's reviewed_sha {sha} does not have HEAD's functional "
                    f"content, so it confirms another run. {needed}")
    if not _quotes_whole_lines(confirmation["quote"], output, stem):
        return {}, (f"the confirmation's quote is not one or more whole, non-blank lines of "
                    f"this run's output naming `{stem}`. {needed}")
    return {"evidence": "reviewer", "confirmation": {
        "reviewer": reviewer, "reviewed_sha": sha,
        "content_digest": head_digest, "quote": confirmation["quote"],
    }}, None


def cmd_finalize_review(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Run functional verification once and generate content-bound evidence."""
    if not args:
        raise UsageError("finalize-review needs a change-id.")
    change_id, *rest = args
    repo = repo_root(Path.cwd())
    findings = _finalize(repo, change_id, rest, out)
    if findings:
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
    skip = auto_skipped_steps(repo, change_id, head_sha)
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
    verdicts, outside_failure = attach_outside_receipt(
        verdicts, selected_outside_family(repo, change_id, head_sha), head_sha
    )
    if outside_failure:
        return [("finalize.verdicts", outside_failure)]
    if not isinstance(findings, list) or not isinstance(adversarial, list):
        return [("finalize.schema", "findings and adversarial must be lists")]
    missing = missing_adversarial_execution(len(adversarial), skip)
    if missing:
        return [("finalize.adversarial", missing)]
    config_before = git_text(repo, "config", "--list", "--null")
    work: list[tuple[str, str, str, dict]] = []
    if "package-tests" not in skip:
        package_command, source = declared_test_command(repo)
        if package_command is None or package_command.strip().lower() == NO_PACKAGE_TESTS:
            return [("finalize.package-tests", f"no executable package command ({source})")]
        work.append(("package-tests", package_command, "", {}))
    for item in adversarial:
        if not isinstance(item, dict):
            return [("finalize.adversarial", "malformed adversarial input")]
        command = str(item.get("command", "")).strip()
        artifact = str(item.get("artifact", "")).strip()
        if not command or not artifact:
            return [("finalize.adversarial", "adversarial input needs command and artifact")]
        route, row = adversarial_route(command, artifact, repo)
        if route == "unnamed":
            return [("finalize.adversarial", "command must name its artifact argument")]
        if route == "not-executed":
            return [("finalize.adversarial", "command must execute the artifact directly")]
        if route == "not-accepted":
            return [("finalize.adversarial",
                     f"`{command}` is a {row.name} command but not in its accepted form "
                     f"for {artifact}: it must run that one file alone with the runner's "
                     f"machine-readable output and no filter; a reviewer confirmation "
                     f"cannot stand in for it")]
        if not git_ok(repo, "cat-file", "-e", f"{head_sha}:{artifact}"):
            return [("finalize.adversarial", "artifact must exist in the selected commit")]
        if not artifact.startswith(probe_directory(change_id)):
            collected, collection_error = suite_collection(repo, artifact)
            if collected is None:
                return [("finalize.adversarial",
                         f"package suite collection unavailable: {collection_error}")]
            if not collected:
                # A graduated test must be collected by the package suite
                # and counted against the adversarial cap.
                return [("finalize.adversarial",
                         f"adversarial artifact must be committed under "
                         f"{probe_directory(change_id)} or be a program the "
                         f"package suite already runs")]
        work.append(("adversarial", command, artifact,
                     {"route": route, "row": row, "confirmation": item.get("confirmation")}))

    # Every artifact is now in a legal home, so the cap can count them: what
    # finalize-review is about to execute is this change's adversarial output
    # wherever graduation has since moved it.
    proportionate = check_adversarial_proportionate(
        repo, head_sha, change_id,
        [artifact for kind, _command, artifact, _how in work if kind == "adversarial"],
    )
    if proportionate:
        return proportionate

    executions: list[dict] = []
    for kind, command, artifact, how in work:
        try:
            completed = subprocess.run(
                argv_for(command), cwd=str(repo), stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=PROBE_RUN_TIMEOUT,
            )
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            return [(f"finalize.{kind}", f"execution failed: {exc}")]
        output = completed.stdout or ""
        detail = output.strip()
        suffix = f"\n{detail[-4000:]}" if detail else ""
        if completed.returncode != 0:
            return [(
                f"finalize.{kind}",
                f"`{command}` exited {completed.returncode}{suffix}",
            )]
        execution = {
            "kind": kind, "command": command, "artifact": artifact,
            "result": "pass", "command_digest": _command_digest(command),
        }
        if kind == "adversarial" and how["route"] != "direct":
            evidence, failure = _runner_evidence(
                repo, change_id, head_sha, manifest, reviewers, command, artifact,
                how, output,
            )
            if failure:
                return [("finalize.adversarial", f"{failure}{suffix}")]
            execution.update(evidence)
        elif kind == "adversarial" and runs_pytest(command):
            failure = _pytest_summary_failure(command, output)
            if failure:
                return [("finalize.adversarial", f"{failure}{suffix}")]
        executions.append(execution)

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
        "verdicts": verdicts, "findings": findings, "selection": None,
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
