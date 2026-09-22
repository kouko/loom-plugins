"""The loom PR-floor CI template and its reusable workflow (plan W2-01; intent Acceptance 9).

The caller template is what adopters copy to `.github/workflows/loom-pr-floor.yml`;
this repository adopts it byte-for-byte. The check context GitHub reports is
`<caller job id> / <reusable job name>`, which must equal the constant the
`github-rules` probe requires.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from loom_checker.command_handlers.github_rules import REQUIRED_CONTEXT  # noqa: E402
from loom_checker.command_handlers.github_rules import TEMPLATE_JOB  # noqa: E402

REPO = HERE.parents[1]
TEMPLATE = REPO / "loom-code" / "templates" / "loom-pr-floor.yml"
ADOPTION = REPO / ".github" / "workflows" / "loom-pr-floor.yml"
REUSABLE = REPO / ".github" / "workflows" / "loom-pr-floor-reusable.yml"
REUSABLE_REF = "kouko/loom-plugins/.github/workflows/loom-pr-floor-reusable.yml@"


def _load(path: Path) -> dict:
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    # YAML 1.1 reads a bare `on:` key as boolean True.
    if True in workflow:
        workflow["on"] = workflow.pop(True)
    return workflow


def _steps(workflow: dict) -> list[dict]:
    return [step for job in workflow["jobs"].values() for step in job.get("steps", [])]


def test_template_uses_pull_request_target_and_context_constant():
    caller = _load(TEMPLATE)
    reusable = _load(REUSABLE)
    assert list(caller["on"]) == ["pull_request_target"]
    assert sorted(caller["on"]["pull_request_target"]["types"]) == sorted(
        ["opened", "edited", "synchronize", "reopened"]
    )
    assert list(caller["jobs"]) == [TEMPLATE_JOB]
    job = caller["jobs"][TEMPLATE_JOB]
    assert job["uses"].startswith(REUSABLE_REF)
    assert job["uses"].removeprefix(REUSABLE_REF) == job["with"]["loom-ref"] == "main"
    assert "pin" in TEMPLATE.read_text(encoding="utf-8").lower()

    assert list(reusable["on"]) == ["workflow_call"]
    assert reusable["on"]["workflow_call"]["inputs"]["loom-ref"]["default"] == "main"
    (reusable_job,) = reusable["jobs"].values()
    assert f"{TEMPLATE_JOB} / {reusable_job['name']}" == REQUIRED_CONTEXT


def test_template_grants_only_contents_read():
    for path in (TEMPLATE, REUSABLE):
        workflow = _load(path)
        assert workflow["permissions"] == {"contents": "read"}, path
        for job in workflow["jobs"].values():
            assert job.get("permissions", {"contents": "read"}) == {"contents": "read"}, path


def test_every_checkout_drops_credentials():
    checkouts = [s for s in _steps(_load(REUSABLE)) if str(s.get("uses", "")).startswith("actions/checkout@")]
    assert len(checkouts) == 2
    for step in checkouts:
        assert step["with"]["persist-credentials"] is False
    head = [s for s in checkouts if "github.event.pull_request.head.sha" in str(s["with"].get("ref"))]
    assert len(head) == 1 and head[0]["with"]["fetch-depth"] == 0
    loom = [s for s in checkouts if s is not head[0]][0]
    assert loom["with"]["repository"] == "kouko/loom-plugins"
    assert "inputs.loom-ref" in loom["with"]["ref"]


def test_no_pr_controlled_text_interpolated_into_a_script():
    tainted = re.compile(
        r"\$\{\{[^}]*github\.event\.pull_request\.(body|title|head\.ref|head\.label)"
    )
    runs = [s["run"] for s in _steps(_load(REUSABLE)) if "run" in s]
    assert runs
    for script in runs:
        assert not tainted.search(script), script
    checker = [r for r in runs if re.search(r"loom_checker\.py\"? pr-floor", r)]
    assert len(checker) == 1
    for flag in ("--body-file", "--base", "--head", "--branch"):
        assert flag in checker[0]


def test_this_repository_adopts_the_template_unchanged():
    assert ADOPTION.read_bytes() == TEMPLATE.read_bytes()


def test_checker_dependency_is_pinned_to_the_lock() -> None:
    lock = (REPO / "requirements-package-tests.lock").read_text(encoding="utf-8")
    pinned = re.search(r"^pyyaml==(\S+)", lock, re.MULTILINE).group(1)
    installs = [step["run"] for step in _steps(_load(REUSABLE))
                if "pip install" in step.get("run", "")]
    assert installs == [f"python3 -m pip install --quiet pyyaml=={pinned}"]
