# concern: the narrow-delta allowlist silently waives the adversarial step for
# deltas that do carry executed behaviour, so a change can lose the step
# without anyone typing a confirmation.
"""Attack `auto_skipped_steps` over real committed deltas.

`auto_skipped_steps` in `loom-code/scripts/loom_checker/reviewers.py` now
waives the adversarial step for any delta `is_narrow_delta` accepts. Its
docstring justifies that with "a narrow delta carries no executed behaviour a
probe program could make fail". These cases build real git branches and ask
the predicate itself, because the delta comes out of
`git diff --name-only --no-renames`, and what a deletion or a rename looks
like there is a property of git, not of the allowlist.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from loom_checker.reviewers import auto_skipped_steps  # noqa: E402

CHANGE_ID = "2026-09-23-adversarial-probes-earn-their-place"


def _run(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    )
    return done.stdout.strip()


def _write(repo: Path, relative: str, text: str) -> None:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _branch_with(trunk: dict[str, str], delta: dict[str, str | None]) -> Path:
    """A repo whose `main` holds `trunk` and whose branch applies `delta`.

    A value of None deletes that path on the branch, so a deletion reaches
    `git diff --name-only` the way a real one does.
    """
    repo = Path(tempfile.mkdtemp())
    _run(repo, "init", "-q", "-b", "main", ".")
    _run(repo, "config", "user.email", "adversary@example.invalid")
    _run(repo, "config", "user.name", "adversary")
    for name, text in trunk.items():
        _write(repo, name, text)
    _run(repo, "add", "-A")
    _run(repo, "commit", "-qm", "trunk")
    _run(repo, "checkout", "-q", "-b", f"feat/{CHANGE_ID}")
    for name, text in delta.items():
        if text is None:
            (repo / name).unlink()
        else:
            _write(repo, name, text)
    _run(repo, "add", "-A")
    _run(repo, "commit", "-qm", "delta")
    return repo


def test_auto_skip_delta_deleting_the_test_suite_keeps_the_adversarial_step() -> None:
    """A delta whose whole content is the removal of the repository's tests
    is not a delta that has nothing left to attack."""
    suite = {
        "loom-code/scripts/test_loom_checker_cli.py": "def test_a():\n    assert True\n",
        "loom-code/scripts/test_probes_language_policy.py": "def test_b():\n    assert True\n",
        "README.md": "# repo\n",
    }
    repo = _branch_with(
        suite,
        {
            "loom-code/scripts/test_loom_checker_cli.py": None,
            "loom-code/scripts/test_probes_language_policy.py": None,
        },
    )
    assert "adversarial" not in auto_skipped_steps(repo, CHANGE_ID)


def test_auto_skip_delta_carrying_an_executed_program_keeps_the_adversarial_step() -> None:
    """The change store admits any file, including a probe program that
    `finalize-review` runs as a subprocess. A delta mixing documentation with
    an executable file the checker itself executes carries executed
    behaviour, which is exactly what the docstring says a narrow delta has
    none of."""
    probe = f"docs/loom/{CHANGE_ID}/evidence/probes/test_abuse.py"
    repo = _branch_with(
        {"README.md": "# repo\n"},
        {
            "README.md": "# repo, reworded\n",
            probe: "# concern: anything\ndef test_x():\n    assert True\n",
        },
    )
    assert "adversarial" not in auto_skipped_steps(repo, CHANGE_ID)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
