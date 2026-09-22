"""`pr-floor --body-file <f> --base <sha> --head <sha> [--branch <name>]`.

The CI check on a pull request. It fails only on the PR body's structure
(the nine contextual headings), naming the heading. The verification status
is recomputed at CI depth from git and published to the job summary and a
`::notice` annotation; every status passes, and no status text is ever read
from the body. Reads files and git only; executes nothing from the PR.
"""
from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import read_text
from loom_checker.helpers import repo_root
from loom_checker.helpers import report
from loom_checker.rule_checks.publish import validate_contextual_pr_body
from loom_checker.verification import identify_change
from loom_checker.verification import verification_status
from pathlib import Path
import os
import sys


USAGE = ("usage: loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha> "
         "[--branch <name>]")


def _options(args: list[str]) -> dict[str, str]:
    allowed = {"--body-file", "--base", "--head", "--branch"}
    if len(args) % 2:
        raise UsageError(USAGE)
    options = dict(zip(args[::2], args[1::2]))
    if len(options) != len(args) // 2 or not set(options) <= allowed or not (
        {"--body-file", "--base", "--head"} <= set(options)
    ):
        raise UsageError(USAGE)
    return options


def _escaped(text: str) -> str:
    """Workflow-command data escaping, so PR-controlled text stays one annotation:
    https://github.com/actions/toolkit/blob/main/packages/core/src/command.ts"""
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def cmd_pr_floor(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    options = _options(args)
    fault = validate_contextual_pr_body(read_text(Path(options["--body-file"])))
    if fault:
        out.write(f"::error title=pr-floor::{_escaped(f'PR body {fault}')}\n")
        return report([("ci.pr-floor", f"PR body {fault}")], err)
    repo = repo_root(Path.cwd())
    base, head = options["--base"], options["--head"]
    change_id, error = identify_change(
        repo, base=base, head=head, branch=options.get("--branch")
    )
    if change_id is None:
        status = f"stale (change not identified: {error})"
    else:
        status = verification_status(repo, change_id, depth="ci", base=base, head=head)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(f"verification: {status}\n")
    out.write(f"::notice title=verification::{_escaped(status)}\n")
    return 0
