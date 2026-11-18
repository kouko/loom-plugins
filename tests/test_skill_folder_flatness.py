"""Skill folders stay flat, and both checks of that rule actually run.

A skill holds SKILL.md plus single-level subfolders, so a file at
`<plugin>/skills/<skill>/<subfolder>/<nested>/...` breaks the rule. The package
suite catches that here, committed or not, through
`repo_files.repository_files` (tracked plus untracked, non-ignored files). The
loom-workflow plugin hook catches it at write time, but it defers to a
repo-level copy of itself, so this repository must not ship one.

Only a top-level `<plugin>` matches: copies kept deeper, under `docs/`, are
records rather than skills.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import run_package_tests  # noqa: E402,F401  (puts repo_files on sys.path)
from repo_files import repository_files  # noqa: E402

HOOK = REPO / "loom-workflow" / "scripts" / "validate-skill-folder-structure.sh"
NESTED_SKILL_FILE = re.compile(r"^[^/]+/skills/[^/]+/[^/]+/[^/]+/.")


def nested_skill_paths(relative_paths) -> list[str]:
    """The repository-relative paths that break the flat skill-folder rule."""
    return sorted(path for path in relative_paths if NESTED_SKILL_FILE.match(path))


def assert_skill_folders_flat(root: Path) -> None:
    relative_paths = (
        path.relative_to(root).as_posix() for path in repository_files(root)
    )
    violations = nested_skill_paths(relative_paths)
    assert not violations, (
        "skill subfolders must not contain subfolders; move these files up "
        "one level:\n" + "\n".join(violations)
    )


def _git_repo(root: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def _write(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n", encoding="utf-8")


def test_nested_uncommitted_path_fails(tmp_path):
    repo = _git_repo(tmp_path)
    nested = "plugin/skills/x/assets/sub/f.md"
    _write(repo / nested)

    assert nested_skill_paths([nested]) == [nested]
    with pytest.raises(AssertionError) as failure:
        assert_skill_folders_flat(repo)
    assert nested in str(failure.value)


def test_flat_and_ignored_paths_pass(tmp_path):
    repo = _git_repo(tmp_path)
    (repo / ".gitignore").write_text("plugin/skills/x/assets/cache/\n", encoding="utf-8")
    _write(repo / "plugin/skills/x/SKILL.md")
    _write(repo / "plugin/skills/x/assets/f.md")
    _write(repo / "plugin/skills/x/assets/cache/f.md")

    assert_skill_folders_flat(repo)
    assert nested_skill_paths(["docs/loom/change/plugin/skills/x/assets/sub/f.md"]) == []


def test_repository_skill_folders_are_flat():
    assert_skill_folders_flat(REPO)


# A local checkout without jq skips; under CI a missing jq runs and fails.
@pytest.mark.skipif(
    shutil.which("jq") is None and not os.environ.get("CI"),
    reason="hook reads stdin via jq",
)
def test_nested_write_reports_violation(tmp_path):
    skill = tmp_path / "skills" / "x"
    nested = skill / "assets" / "sub" / "f.md"
    _write(skill / "SKILL.md")
    _write(nested)
    event = {"tool_name": "Write", "tool_input": {"file_path": str(nested)}}

    # cwd is this repository, so a repo-level hook copy would make it defer.
    result = subprocess.run(
        ["bash", str(HOOK)], input=json.dumps(event),
        capture_output=True, text=True, cwd=REPO,
    )

    assert result.returncode == 2, result.stderr
    assert "Skill folder structure violation" in result.stderr
    assert "assets/sub" in result.stderr
