"""A pytest adversarial probe is attested only when its own tests really ran:
the `python -m pytest` form names the artifact as its sole positional, and
finalize-review reads pytest's summary line, refusing a run that deselected
tests, passed none, or printed no summary. The declared package-suite command
keeps its filters.
"""
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

from loom_checker import probes
from loom_checker.attestation import _command_digest

PROBE = f"docs/loom/{CHANGE}/evidence/probes/test_attack.py"
TWO_TESTS = (
    "# concern: a boundary input the code never rejects\n"
    "def test_attack() -> None:\n    assert True\n"
    "def test_kept() -> None:\n    assert True\n"
)


def probe_repo(tmp_path: Path, body: str = TWO_TESTS, package: str = "python3 -c pass") -> Path:
    repo = make_repo(tmp_path, package)
    path = repo / PROBE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    commit_all(repo, "probe")
    return repo


def run(repo: Path, tmp_path: Path, command: str, artifact: str = PROBE, env: dict | None = None):
    return finalize(repo, review_input(tmp_path, PASSING, [
        {"command": command, "artifact": artifact},
    ]), env)


def adversarial(attestation: dict) -> dict:
    return next(run for run in attestation["executions"] if run["kind"] == "adversarial")


def test_sole_artifact_pytest_passing_accepted(tmp_path: Path) -> None:
    repo = probe_repo(tmp_path)
    # Coloured output still yields a readable summary line.
    result = run(repo, tmp_path, f"python3 -m pytest {PROBE}", env={"PY_COLORS": "1"})
    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    assert set(adversarial(attestation)) == {
        "kind", "command", "artifact", "result", "command_digest"}
    assert validate(repo, attestation) == []


def test_config_addopts_deselect_refused(tmp_path: Path) -> None:
    repo = probe_repo(tmp_path)
    (repo / "pytest.ini").write_text("[pytest]\naddopts = -k test_kept\n", encoding="utf-8")
    commit_all(repo, "a config filter deselects the probe's own test")
    result = run(repo, tmp_path, f"python3 -m pytest {PROBE}")
    assert result.returncode == 1
    assert "BLOCK finalize.adversarial" in result.stderr
    assert "deselected" in result.stderr
    assert not (repo / f"docs/loom/{CHANGE}/attestation.json").exists()


def test_second_positional_refused_by_finalize_and_validator(tmp_path: Path) -> None:
    repo = probe_repo(tmp_path)
    (repo / "test_other.py").write_text("def test_other() -> None:\n    assert True\n",
                                        encoding="utf-8")
    commit_all(repo, "another test file")
    command = f"python3 -m pytest {PROBE} test_other.py -k other"
    assert not probes.command_executes_artifact(command, PROBE)
    result = run(repo, tmp_path, command)
    assert result.returncode == 1
    assert "command must execute the artifact directly" in result.stderr

    assert run(repo, tmp_path, f"python3 -m pytest {PROBE}").returncode == 0
    attestation = written(repo)
    adversarial(attestation).update(command=command, command_digest=_command_digest(command))
    assert any("execute the artifact directly" in reason
               for _, reason in validate(repo, attestation))


def test_suite_filter_still_collects_graduated_probe(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, 'python3 -m pytest -m "not slow" tests')
    artifact = "tests/test_graduated_probe.py"
    (repo / "tests").mkdir()
    (repo / artifact).write_text(
        "# concern: a defect now covered on every change\n"
        "def test_graduated() -> None:\n    assert True\n", encoding="utf-8",
    )
    commit_all(repo, "graduate into a filtering pytest suite")
    assert probes.suite_collects(repo, artifact)
    result = run(repo, tmp_path, f"python3 -m pytest {artifact}", artifact)
    assert result.returncode == 0, result.stderr


SKIPPED = ("# concern: x\nimport pytest\n"
           "@pytest.mark.skip\ndef test_attack() -> None:\n    assert True\n")


@pytest.mark.parametrize("body, ini, other, accepted", [
    (TWO_TESTS, "pytest.ini", "test_other.py", True),
    (SKIPPED, "pytest.ini", "test_other.py", False),
    # Same basename elsewhere; the probe's own ini makes its nodeid `test_attack.py`.
    (SKIPPED, f"docs/loom/{CHANGE}/evidence/probes/pytest.ini", "test_attack.py", False),
], ids=["own-pass", "config-added-file-only", "same-basename"])
def test_pass_must_come_from_probe_file(tmp_path: Path, body: str, ini: str, other: str,
                                        accepted: bool) -> None:
    repo = probe_repo(tmp_path, body)
    (repo / ini).write_text(f"[pytest]\naddopts = --import-mode=importlib {other}\n",
                            encoding="utf-8")
    (repo / other).write_text("def test_other() -> None:\n    assert True\n", encoding="utf-8")
    commit_all(repo, "a config positional adds another passing file")
    result = run(repo, tmp_path, f"python3 -m pytest {PROBE}")
    assert (result.returncode == 0) is accepted, result.stderr
    if accepted:
        assert validate(repo, written(repo)) == []
    else:
        assert "no passed test from" in result.stderr


@pytest.mark.parametrize("body, flags, reason", [
    (TWO_TESTS, "-qq ", "summary"),  # -qq prints no summary line
    ("# concern: x\nimport pytest\n"
     "@pytest.mark.skip\ndef test_attack() -> None:\n    assert True\n", "", "no passed test"),
], ids=["no-summary", "zero-passed"])
def test_no_summary_or_zero_passed_refused(tmp_path: Path, body: str, flags: str,
                                           reason: str) -> None:
    repo = probe_repo(tmp_path, body)
    result = run(repo, tmp_path, f"python3 -m pytest {flags}{PROBE}")
    assert result.returncode == 1
    assert "BLOCK finalize.adversarial" in result.stderr
    assert reason in result.stderr
