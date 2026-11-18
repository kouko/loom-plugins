# concern: missed violation - committed nested skill content passes the package-suite flatness check (Acceptance 1)
"""Nested content that git tracks must fail the flatness check."""
from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SKILL = "loom-code/skills/x"  # the check scopes <plugin> to marketplace names


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


def _committed_repo(root: Path, relative: str, symlink: bool) -> Path:
    _git(root, "init", "-q")
    target = root / relative
    target.parent.mkdir(parents=True)
    if symlink:
        os.symlink("missing-target", target)
    else:
        target.write_text("x\n", encoding="utf-8")
    _git(root, "add", "--force", ".")
    _git(root, "commit", "-q", "-m", "fixture")
    return root


@pytest.mark.parametrize(
    ("relative", "symlink"),
    [
        (f"{SKILL}/scripts/node_modules/pkg/index.js", False),
        (f"{SKILL}/scripts/__pycache__/tool.pyc", False),
        (f"{SKILL}/assets/sub/\nleading-newline.md", False),
        (f"{SKILL}/assets/sub/dangling-link", True),
    ],
    ids=["node-modules", "pycache", "leading-newline-name", "dangling-symlink"],
)
def test_flatness_committed_nested_path_fails(tmp_path, relative, symlink):
    """Each tracked nested path is reported, whatever its name or file type."""
    repo = _committed_repo(tmp_path, relative, symlink)

    with pytest.raises(AssertionError) as failure:
        _flatness_module().assert_skill_folders_flat(repo)

    assert "skill subfolders must not contain subfolders" in str(failure.value)
