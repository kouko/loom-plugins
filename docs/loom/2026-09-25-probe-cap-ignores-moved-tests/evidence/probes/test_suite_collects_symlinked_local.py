# concern: `suite_collects` decides "skipped by --ignore=" by resolved path,
# but pytest applies --ignore to the path it walks, so a probe committed under
# tests/local/ and reached through a committed symlink is run by the package
# suite while the probe cap counts it as not graduated.
"""Attack `_ignored` / `suite_collects` in
`loom-code/scripts/loom_checker/probes.py`.

Before this change a program under `loom-code/tests/local/` was counted as
graduated. Now it is excluded because the runner passes
`--ignore=<tests/local>`. A committed directory symlink `loom-code/tests/alias
-> local` makes pytest collect the same file as `alias/test_hidden.py`, a path
the ignore does not cover, so the suite runs a probe the cap no longer sees.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from loom_checker.probes import _declared_suite_commands  # noqa: E402
from loom_checker.probes import graduated_probe_programs  # noqa: E402

CHANGE_ID = "2026-09-25-probe-cap-ignores-moved-tests"
SUITE = "loom-code/tests"
RUNNER = REPO_ROOT / "scripts" / "run_package_tests.py"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def _write(repo: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_suite_collects_symlinked_local_alias_counted() -> None:
    """A probe under tests/local/ that the declared suite still collects
    through a symlinked alias directory is graduated and must be counted."""
    repo = Path(tempfile.mkdtemp())
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "adversary@example.invalid")
    _git(repo, "config", "user.name", "adversary")
    _write(repo, {
        "scripts/run_package_tests.py": RUNNER.read_text(encoding="utf-8"),
        f"{SUITE}/test_anchor.py": "def test_anchor() -> None:\n    assert True\n",
    })
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "checkout", "-q", "-b", "feature")
    hidden = f"{SUITE}/local/test_hidden.py"
    _write(repo, {hidden: "# concern: hidden probe\ndef test_hidden() -> None:\n"
                          "    assert True\n"})
    os.symlink("local", repo / SUITE / "alias")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "branch")
    head = _git(repo, "rev-parse", "HEAD")

    collected = ""
    for command in _declared_suite_commands(repo):
        if "pytest" not in command[:4]:
            continue
        args = [a for a in command if a not in {"-n", "auto", "-q"}]
        collected += subprocess.run(
            [*args, "--collect-only", "-q", "-p", "no:xdist", "-p", "no:cacheprovider"],
            cwd=repo, capture_output=True, text=True,
        ).stdout
    assert "alias/test_hidden.py::test_hidden" in collected, collected

    assert hidden in graduated_probe_programs(repo, head, CHANGE_ID)
