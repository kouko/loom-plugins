"""An adversarial artifact cannot leave the change's store through path
spelling: finalize-review and the attestation validator both refuse an artifact
that starts with `./` or `../`, has a `..` part, or has any part `normpath`
would change -- `git cat-file` normalises `./a/../b`, so the store
`startswith` check alone would accept a path that resolves outside it.
"""
# concern: A probe path spelled with `..` must not escape the change's store.
from __future__ import annotations

from pathlib import Path

import pytest

from test_selection_finalize import CHANGE
from test_selection_finalize import PASSING
from test_selection_finalize import commit_all
from test_selection_finalize import finalize
from test_selection_finalize import make_repo
from test_selection_finalize import review_input
from test_selection_finalize import validate
from test_selection_finalize import written

from loom_checker.attestation import _command_digest

STORE = f"docs/loom/{CHANGE}/evidence/probes/"
BODY = "# concern: a boundary input the code never rejects\nprint('ran')\n"


def repo_with(tmp_path: Path, package: str, *paths: str) -> Path:
    repo = make_repo(tmp_path, package)
    for path in paths:
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_text(BODY, encoding="utf-8")
    commit_all(repo, "probe programs")
    return repo


def run(repo: Path, tmp_path: Path, artifact: str):
    return finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"python3 {artifact}", "artifact": artifact},
    ]))


@pytest.mark.parametrize("package, artifact", [
    ("python3 -c pass", f"{STORE}probe.py"),
    ("python3 -m pytest tests", "tests/test_graduated_probe.py"),
], ids=["store-artifact", "graduated-suite-artifact"])
def test_store_and_graduated_artifacts_accepted(tmp_path: Path, package: str,
                                                artifact: str) -> None:
    if artifact.startswith("tests/"):
        repo = make_repo(tmp_path, package)
        (repo / "tests").mkdir()
        (repo / artifact).write_text(
            "# concern: a defect now covered on every change\n"
            "def test_graduated() -> None:\n    assert True\n", encoding="utf-8")
        commit_all(repo, "graduated probe")
    else:
        repo = repo_with(tmp_path, package, artifact)
    result = run(repo, tmp_path, artifact)
    assert result.returncode == 0, result.stderr
    assert validate(repo, written(repo)) == []


@pytest.mark.parametrize("escape", [
    f"./{STORE}../../../../../escape.py",
    f"{STORE}../../../../../escape.py",
], ids=["dot-slash-dotdot", "plain-dotdot"])
def test_dotdot_escape_refused_by_finalize_and_validator(tmp_path: Path, escape: str) -> None:
    repo = repo_with(tmp_path, "python3 -c pass", f"{STORE}probe.py", "escape.py")
    result = run(repo, tmp_path, escape)
    assert result.returncode == 1
    assert "plain repository path" in result.stderr

    assert run(repo, tmp_path, f"{STORE}probe.py").returncode == 0
    attestation = written(repo)
    execution = next(e for e in attestation["executions"] if e["kind"] == "adversarial")
    command = f"python3 {escape}"
    execution.update(artifact=escape, command=command, command_digest=_command_digest(command))
    assert any("plain repository path" in reason for _, reason in validate(repo, attestation))
