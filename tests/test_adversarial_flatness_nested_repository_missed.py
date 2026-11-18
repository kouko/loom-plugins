# concern: missed violation - a nested folder that is its own git repository passes the flatness check (Acceptance 1)
"""A cloned folder inside a skill subfolder is still a nested folder with files."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
NESTED = "loom-code/skills/x/assets/vendor"


def _flatness_module():
    spec = importlib.util.spec_from_file_location(
        "skill_folder_flatness_under_attack",
        REPO / "tests" / "test_skill_folder_flatness.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), "-c", "user.name=probe",
         "-c", "user.email=probe@example.invalid", *args],
        check=True, capture_output=True,
    )


def _commit_all(root: Path) -> None:
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "fixture")


@pytest.mark.parametrize(
    ("inner_committed", "outer_committed"),
    [(False, False), (True, False), (True, True)],
    ids=["fresh-repository", "cloned-uncommitted", "committed-gitlink"],
)
def test_flatness_nested_git_repository_fails(tmp_path, inner_committed, outer_committed):
    """The check names the folder however git chooses to list it."""
    _git(tmp_path, "init", "-q")
    nested = tmp_path / NESTED
    nested.mkdir(parents=True)
    _git(nested, "init", "-q")
    (nested / "f.md").write_text("x\n", encoding="utf-8")
    if inner_committed:
        _commit_all(nested)
    if outer_committed:
        _commit_all(tmp_path)

    with pytest.raises(AssertionError) as failure:
        _flatness_module().assert_skill_folders_flat(tmp_path)

    assert NESTED in str(failure.value)
