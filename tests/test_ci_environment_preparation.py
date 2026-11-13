"""CI prepares each test job locally and never ignores setup failures."""

import os
from pathlib import Path
import subprocess

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github/workflows"
PYTHON_JOBS = (
    ("loom-code-ci.yml", "test", "code"),
    ("loom-design-ci.yml", "design", "design"),
    ("loom-workflow-ci.yml", "loom-visualization-page-pytest", "workflow-python"),
)


@pytest.mark.parametrize("filename,job,group", PYTHON_JOBS)
def test_ci_job_dependencies_precede_its_suite(filename, job, group):
    data = yaml.safe_load((WORKFLOWS / filename).read_text())
    steps = data["jobs"][job]["steps"]
    suite_index = next(i for i, step in enumerate(steps)
                       if f"--only {group} " in step.get("run", ""))
    preparation = steps[:suite_index]
    commands = "\n".join(step.get("run", "") for step in preparation)
    assert "--require-hashes -r requirements-package-tests.lock" in commands
    assert "-rs" in steps[suite_index]["run"]
    if group == "code":
        assert "apt-get install --yes zsh" in commands
        assert "uv==" in commands and "uv --version" in commands
        assert "agy --version" in commands
        assert "agy plugin validate" in commands
    if group in ("code", "workflow-python"):
        assert any(step.get("uses", "").startswith("actions/setup-node@")
                   for step in preparation)
    if group == "workflow-python":
        assert "npm ci --prefix loom-workflow/tests/mermaid" in commands
    # Native Actions default success() prevents a failed setup from reaching
    # tests. Refuse overrides that would silently bypass that dependency.
    for step in steps[:suite_index + 1]:
        assert not step.get("continue-on-error")
        assert "if" not in step


def test_ci_dependency_changes_trigger_every_consuming_workflow():
    for filename, _, _ in PYTHON_JOBS:
        data = yaml.safe_load((WORKFLOWS / filename).read_text())
        events = data.get("on", data.get(True))
        for event in ("pull_request", "push"):
            paths = events[event]["paths"]
            assert "requirements-dev.txt" in paths
            assert "requirements-package-tests.lock" in paths


def test_ci_agy_corrupt_download_stops_before_extraction(tmp_path):
    data = yaml.safe_load((WORKFLOWS / "loom-code-ci.yml").read_text())
    command = next(step["run"] for step in data["jobs"]["test"]["steps"]
                   if step.get("name") == "Install Antigravity CLI")
    # Run the actual setup script with a corrupt download and trap extraction.
    # This exercises failure propagation inside the step, not a simulated
    # Actions scheduler or a stand-in for the production agy executable.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, body in {
        "curl": 'while [ "$1" != "--output" ]; do shift; done; shift; printf corrupt > "$1"',
        "tar": 'touch "$RUNNER_TEMP/extracted"',
    }.items():
        path = bin_dir / name
        path.write_text("#!/bin/sh\n" + body + "\n")
        path.chmod(0o755)
    env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}",
               RUNNER_TEMP=str(tmp_path), GITHUB_PATH=str(tmp_path / "github-path"))
    result = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", command],
                            cwd=ROOT, env=env, capture_output=True, text=True)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "FAILED" in result.stdout + result.stderr
    assert not (tmp_path / "extracted").exists()
    assert not (tmp_path / "github-path").exists()
