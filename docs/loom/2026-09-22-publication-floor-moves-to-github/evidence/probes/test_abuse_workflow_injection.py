"""Adversarial probe: can PR-controlled text or a PR's own files reach code
or privilege in the PR-floor workflows?

REQ-9 and the Design decision "CI template shape": the caller runs under
`pull_request_target`, reads only files and the event body, executes no PR
code, holds `contents: read`, and no checkout keeps credentials. The attack
reads the three shipped workflow files as data and hunts for the classic
`pull_request_target` holes; then drives `pr-floor` with a hostile branch
name to see whether it can open a second workflow command.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-22-publication-floor-moves-to-github/evidence/probes/test_abuse_workflow_injection.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))

TEMPLATE = ROOT / "loom-code/templates/loom-pr-floor.yml"
CALLER = ROOT / ".github/workflows/loom-pr-floor.yml"
REUSABLE = ROOT / ".github/workflows/loom-pr-floor-reusable.yml"
WORKFLOWS = [TEMPLATE, CALLER, REUSABLE]

EXPRESSION = re.compile(r"\$\{\{(.*?)\}\}", re.DOTALL)


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def triggers(workflow: dict):
    return workflow.get("on", workflow.get(True))


def steps(workflow: dict):
    for job in (workflow.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            yield job, step


def test_workflow_caller_template_identical() -> None:
    """What this repository runs is exactly what adopters copy."""
    assert TEMPLATE.read_bytes() == CALLER.read_bytes()


@pytest.mark.parametrize("path", [TEMPLATE, CALLER])
def test_workflow_caller_trigger_base_only(path: Path) -> None:
    on = triggers(load(path))
    assert set(on) == {"pull_request_target"}, on


@pytest.mark.parametrize("path", WORKFLOWS)
def test_workflow_permissions_read_only(path: Path) -> None:
    workflow = load(path)
    assert workflow.get("permissions") == {"contents": "read"}
    for job in (workflow.get("jobs") or {}).values():
        assert job.get("permissions") in (None, {"contents": "read"}), job
        assert "secrets" not in job, "caller passes secrets to the reusable workflow"


def test_workflow_run_blocks_no_expression() -> None:
    """No `${{ }}` inside any `run:` script: PR text must arrive via env."""
    for _job, step in steps(load(REUSABLE)):
        assert not EXPRESSION.search(str(step.get("run", ""))), step


def test_workflow_checkouts_drop_credentials() -> None:
    checkouts = [s for _j, s in steps(load(REUSABLE))
                 if str(s.get("uses", "")).startswith("actions/checkout")]
    assert len(checkouts) == 2
    for step in checkouts:
        with_ = step.get("with") or {}
        assert with_.get("persist-credentials") is False, step
        assert not with_.get("submodules"), step
        assert not with_.get("lfs"), step


def test_workflow_pr_tree_runs_only_loom_code() -> None:
    """Every step that runs in the PR checkout runs loom's own checker, by an
    absolute path outside the PR tree, and nothing the PR tree names."""
    for _job, step in steps(load(REUSABLE)):
        if "run" not in step:
            continue
        script = step["run"].strip()
        if step.get("working-directory") == "pr":
            assert script.startswith('python3 "$GITHUB_WORKSPACE/loom/loom-code/scripts/loom_checker.py"'), script
        else:
            assert "pr/" not in script, script


def test_workflow_pr_values_arrive_through_env() -> None:
    """PR-controlled context values appear only as `env:` values."""
    pr_controlled = ("github.event.pull_request.body", "github.event.pull_request.head.ref",
                     "github.event.pull_request.title", "github.head_ref")
    for _job, step in steps(load(REUSABLE)):
        for key, value in step.items():
            if key == "env":
                continue
            assert not any(p in str(value) for p in pr_controlled), (key, value)


def test_pr_floor_hostile_branch_single_notice(tmp_path: Path, monkeypatch) -> None:
    """A hostile head ref (`%`, `::`) reaches the status text; the notice must
    stay one workflow command and keep `%` escaped."""
    from loom_checker.command_handlers.pr_floor import cmd_pr_floor
    from loom_checker.rule_checks.publish import CONTEXTUAL_PR_HEADINGS
    from test_verification_status import branch_repo, commit, git

    repo = branch_repo(tmp_path, "wip")  # the hostile ref arrives by --branch, as in CI
    (repo / "src.py").write_text("V = 2\n", encoding="utf-8")
    commit(repo, "work")
    body = tmp_path / "body.md"
    body.write_text("\n".join(f"## {h}\n\nThe {h.lower()} section says something real.\n"
                              for h in CONTEXTUAL_PR_HEADINGS), encoding="utf-8")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.chdir(repo)
    out = io.StringIO()
    code = cmd_pr_floor(["--body-file", str(body), "--base", git(repo, "rev-parse", "main"),
                         "--head", "HEAD", "--branch", "feat/x%0A::error::owned"],
                        out, io.StringIO())
    assert code == 0
    lines = out.getvalue().splitlines()
    assert len(lines) == 1 and lines[0].startswith("::notice title=verification::")
    assert "%0A::error" not in lines[0]  # the runner would decode an unescaped %0A
