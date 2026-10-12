# concern: A runner's root pytest target must not graduate a test excluded by pytest configuration.
"""A configured pytest ignore must govern runner-backed probe graduation."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "loom-code/scripts"))

from loom_checker.probes import suite_collects  # noqa: E402


def test_runner_ignored_refused(tmp_path: Path) -> None:
    """Reject a probe that a root-target runner never collects."""
    repo = tmp_path / "repo"
    tests = repo / "tests"
    runner = repo / "scripts/run_package_tests.py"
    tests.mkdir(parents=True)
    runner.parent.mkdir()
    runner.write_text(
        "def loom_family_commands(repo):\n"
        "    return [['python3', '-m', 'pytest', '.']]\n",
        encoding="utf-8",
    )
    (repo / "pytest.ini").write_text(
        "[pytest]\naddopts = -q --ignore=tests/test_ignored.py\n",
        encoding="utf-8",
    )
    (tests / "test_kept.py").write_text(
        "def test_kept():\n    assert True\n", encoding="utf-8",
    )
    (tests / "test_ignored.py").write_text(
        "# concern: excluded from package tests\n"
        "def test_ignored():\n    assert True\n", encoding="utf-8",
    )
    collected = subprocess.run(
        [sys.executable, "-m", "pytest", ".", "--collect-only", "-q"],
        cwd=repo, capture_output=True, text=True, check=True,
    )
    assert "tests/test_kept.py: 1" in collected.stdout
    assert "test_ignored.py::test_ignored" not in collected.stdout
    assert suite_collects(repo, "tests/test_kept.py")
    assert not suite_collects(repo, "tests/test_ignored.py")
