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

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from loom_checker.helpers import git_ok  # noqa: E402
from loom_checker.probes import MAX_PROBE_PROGRAMS  # noqa: E402
from loom_checker.probes import check_adversarial_proportionate  # noqa: E402
from loom_checker.probes import command_executes_artifact  # noqa: E402
from loom_checker.probes import command_names_artifact  # noqa: E402
from loom_checker.probes import graduated_probe_programs  # noqa: E402
from loom_checker.probes import suite_collects  # noqa: E402
from loom_checker.reviewers import committed_branch_delta  # noqa: E402

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


RUNNER_SOURCE = REPO_ROOT / "scripts" / "run_package_tests.py"
SUITE = "loom-code/tests"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def _write(repo: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def _probe(index: int) -> str:
    """A concern-bearing probe with enough distinct body that two of them are
    not similar to each other in git's rename sense."""
    body = "".join(f"    assert {index} * {line} == {index * line}\n" for line in range(1, 30))
    return f"# concern: defect class {index}\ndef test_probe_{index}() -> None:\n{body}"


def _branch(base: dict[str, str]) -> Path:
    """A repo whose trunk holds the runner plus `base`, checked out on a
    feature branch with nothing committed on it yet."""
    repo = Path(tempfile.mkdtemp())
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "adversary@example.invalid")
    _git(repo, "config", "user.name", "adversary")
    _write(repo, {
        "scripts/run_package_tests.py": RUNNER_SOURCE.read_text(encoding="utf-8"),
        f"{SUITE}/test_anchor.py": "def test_anchor() -> None:\n    assert True\n",
        **base,
    })
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "checkout", "-q", "-b", "feature")
    return repo


def _commit_branch(repo: Path) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "branch")
    return _git(repo, "rev-parse", "HEAD")


MOVED = MAX_PROBE_PROGRAMS + 1


def test_moved_concern_tests_are_not_counted() -> None:
    """Acceptance 1: a branch that only `git mv`s six concern-bearing tests
    into the suite folder produces no probe program of its own."""
    old = {f"loom-code/scripts/test_probe_{i}.py": _probe(i) for i in range(MOVED)}
    repo = _branch(old)
    for i in range(MOVED):
        _git(repo, "mv", f"loom-code/scripts/test_probe_{i}.py", f"{SUITE}/test_probe_{i}.py")
    head = _commit_branch(repo)
    assert graduated_probe_programs(repo, head, CHANGE_ID) == []
    assert check_adversarial_proportionate(repo, head, CHANGE_ID) == []


def test_moved_and_rewritten_into_a_new_probe_is_counted() -> None:
    """Acceptance 2 negative: a move whose content falls below git's default
    rename similarity (50%) is a removal plus a new probe, and counts."""
    repo = _branch({"loom-code/scripts/test_probe_0.py": _probe(0)})
    _git(repo, "mv", "loom-code/scripts/test_probe_0.py", f"{SUITE}/test_probe_0.py")
    _write(repo, {f"{SUITE}/test_probe_0.py": _probe(99)})
    head = _commit_branch(repo)
    assert graduated_probe_programs(repo, head, CHANGE_ID) == [f"{SUITE}/test_probe_0.py"]


def test_moved_with_a_small_edit_is_still_a_move() -> None:
    """At or above git's default 50% similarity the pair stays a rename."""
    repo = _branch({"loom-code/scripts/test_probe_0.py": _probe(0)})
    _git(repo, "mv", "loom-code/scripts/test_probe_0.py", f"{SUITE}/test_probe_0.py")
    _write(repo, {f"{SUITE}/test_probe_0.py": _probe(0) + "    assert True\n"})
    head = _commit_branch(repo)
    assert graduated_probe_programs(repo, head, CHANGE_ID) == []


def test_new_probes_are_counted_and_over_the_cap_refused() -> None:
    """Acceptance 2 positive: brand-new probes still count, six still refuse."""
    repo = _branch({})
    _write(repo, {f"{SUITE}/test_probe_{i}.py": _probe(i) for i in range(MOVED)})
    head = _commit_branch(repo)
    assert len(graduated_probe_programs(repo, head, CHANGE_ID)) == MOVED
    assert check_adversarial_proportionate(repo, head, CHANGE_ID) != []


def test_a_copied_probe_under_a_new_name_is_counted() -> None:
    """Acceptance 2 boundary: a copy whose original stays on the branch is a
    new program; only a pair whose old path left the branch is a move."""
    repo = _branch({f"{SUITE}/test_probe_0.py": _probe(0)})
    _write(repo, {f"{SUITE}/test_probe_copy.py": _probe(0)})
    head = _commit_branch(repo)
    assert graduated_probe_programs(repo, head, CHANGE_ID) == [f"{SUITE}/test_probe_copy.py"]


def test_a_program_under_tests_local_is_not_graduated() -> None:
    """Acceptance 3: the package suite skips `tests/local/`, so a probe there
    is not in the suite and not counted as graduated into it."""
    repo = _branch({})
    local = f"{SUITE}/local/test_probe_0.py"
    kept = f"{SUITE}/test_probe_1.py"
    _write(repo, {local: _probe(0), kept: _probe(1)})
    head = _commit_branch(repo)
    assert not suite_collects(repo, local)
    assert suite_collects(repo, kept)
    assert graduated_probe_programs(repo, head, CHANGE_ID) == [kept]


def test_the_branch_delta_still_reads_a_move_as_removal_plus_addition() -> None:
    """Acceptance 5: the shared delta keeps `--no-renames` for its other
    callers (reviewer floor, narrow delta, finalize)."""
    repo = _branch({"loom-code/scripts/test_probe_0.py": _probe(0)})
    _git(repo, "mv", "loom-code/scripts/test_probe_0.py", f"{SUITE}/test_probe_0.py")
    head = _commit_branch(repo)
    delta = committed_branch_delta(repo, CHANGE_ID, head)
    assert delta is not None
    _paths, removed, added = delta
    assert removed == {"loom-code/scripts/test_probe_0.py"}
    assert added == {f"{SUITE}/test_probe_0.py"}


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
