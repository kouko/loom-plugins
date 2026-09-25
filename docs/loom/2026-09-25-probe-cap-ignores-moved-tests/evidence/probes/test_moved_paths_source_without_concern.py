# concern: the move exemption in the probe cap trusts git's rename pairing
# alone, so a brand-new probe written over a deleted non-probe test (one that
# never carried a `concern:` line) is paired as a "move" and escapes the cap.
"""Attack `_moved_paths` / `graduated_probe_programs` in
`loom-code/scripts/loom_checker/probes.py`.

The exemption is justified as "it is an earlier change's probe, not this
change's output". A source file that carried no `concern:` line was never a
probe, so the file that replaces it under a new name is a new probe program.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

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


PLAIN_TEST = "def test_plain() -> None:\n" + "".join(
    f"    assert {n} + {n} == {2 * n}\n" for n in range(1, 30)
)


def test_moved_paths_source_without_concern_still_counted() -> None:
    """A deleted plain test (no `concern:` line) replaced under a new name by a
    concern-bearing probe that reuses its body is a new probe program, and the
    cap must count it even though git pairs the two as a rename."""
    repo = Path(tempfile.mkdtemp())
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "adversary@example.invalid")
    _git(repo, "config", "user.name", "adversary")
    _write(repo, {
        "scripts/run_package_tests.py": RUNNER.read_text(encoding="utf-8"),
        f"{SUITE}/test_plain.py": PLAIN_TEST,
    })
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "checkout", "-q", "-b", "feature")
    _git(repo, "rm", "-q", f"{SUITE}/test_plain.py")
    new_probe = f"{SUITE}/test_new_probe.py"
    _write(repo, {new_probe: "# concern: a new defect class\n" + PLAIN_TEST
                  + "\n\ndef test_new_case() -> None:\n    assert True\n"})
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "branch")
    head = _git(repo, "rev-parse", "HEAD")
    status = _git(repo, "diff", "--name-status", "-M", "main", head)
    assert status.startswith("R"), status  # git does pair them as a rename
    assert graduated_probe_programs(repo, head, CHANGE_ID) == [new_probe]
