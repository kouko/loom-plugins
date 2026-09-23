# concern: the five-program cap and the `concern:` requirement are recomputed
# over a subset of the programs a change actually commits and runs, so both
# halves of `adversarial.proportionate` are escaped by where a program is put
# or what it is named.
"""Attack `check_adversarial_proportionate` in
`loom-code/scripts/loom_checker/probes.py`.

The rule counts `*.py` files under `docs/loom/<change-id>/evidence/probes/`
and nothing else, while `finalize-review` accepts any `artifact` that merely
exists in the selected commit. Whether those two agree is a property of git's
tree listing and of the finalize predicates, so the cases below build a real
commit and ask both.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from loom_checker.helpers import git_ok  # noqa: E402
from loom_checker.probes import MAX_PROBE_PROGRAMS  # noqa: E402
from loom_checker.probes import check_adversarial_proportionate  # noqa: E402
from loom_checker.probes import command_executes_artifact  # noqa: E402
from loom_checker.probes import command_names_artifact  # noqa: E402

CHANGE_ID = "2026-09-23-adversarial-probes-earn-their-place"
OVER_THE_CAP = MAX_PROBE_PROGRAMS + 2


def _commit(files: dict[str, str]) -> tuple[Path, str]:
    repo = Path(tempfile.mkdtemp())
    for args in (
        ("init", "-q", "-b", "main", "."),
        ("config", "user.email", "adversary@example.invalid"),
        ("config", "user.name", "adversary"),
    ):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
    for name, text in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "x"], cwd=repo, check=True, capture_output=True)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()
    return repo, head


PROGRAM = "# concern: a stated concern\nprint(1)\n"


def test_cap_programs_beside_the_expected_directory_are_refused() -> None:
    """Seven programs one directory up from `evidence/probes/`. They are over
    the cap, and `finalize-review` would accept and execute every one of
    them, because it only asks whether the artifact exists in the commit."""
    paths = [f"docs/loom/{CHANGE_ID}/probes/p{i}.py" for i in range(OVER_THE_CAP)]
    repo, head = _commit(dict.fromkeys(paths, PROGRAM))
    for path in paths:
        command = f"python3 {path}"
        assert command_names_artifact(command, path)
        assert command_executes_artifact(command, path)
        assert git_ok(repo, "cat-file", "-e", f"{head}:{path}")
    assert check_adversarial_proportionate(repo, head, CHANGE_ID) != []


def test_cap_programs_that_are_not_dot_py_are_refused() -> None:
    """Seven shell programs in the expected directory. The protocol says
    "program", not "Python file", and the listing filters on `.py`, so these
    are neither counted against the cap nor asked for a `concern:` line."""
    paths = [
        f"docs/loom/{CHANGE_ID}/evidence/probes/p{i}.sh" for i in range(OVER_THE_CAP)
    ]
    repo, head = _commit(dict.fromkeys(paths, "#!/bin/sh\nexit 0\n"))
    assert check_adversarial_proportionate(repo, head, CHANGE_ID) != []


def test_cap_programs_inside_the_expected_directory_are_refused() -> None:
    """The control: the same count, spelled the way the protocol asks for, is
    refused. This is what the two cases above escape."""
    paths = [
        f"docs/loom/{CHANGE_ID}/evidence/probes/p{i}.py" for i in range(OVER_THE_CAP)
    ]
    repo, head = _commit(dict.fromkeys(paths, PROGRAM))
    assert check_adversarial_proportionate(repo, head, CHANGE_ID) != []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
