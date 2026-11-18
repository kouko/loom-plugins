"""Skill folders stay flat, and both checks of that rule actually run.

A skill holds SKILL.md plus single-level subfolders, so a file at
`<plugin>/skills/<skill>/<subfolder>/<nested>/...` breaks the rule. The package
suite catches that here, committed or not, from git's own list: every tracked
path, even one under an ignored folder, plus untracked, non-ignored files. The
loom-workflow plugin hook catches it at write time, but it defers to a
repo-level copy of itself, so this repository must not ship one.

`<plugin>` is a top-level folder named in this repository's marketplace.json:
other folders holding a `skills/` directory, such as test fixtures or records
under `docs/`, are not plugins.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
HOOK = REPO / "loom-workflow" / "scripts" / "validate-skill-folder-structure.sh"
PLUGIN_NAMES = [
    plugin["name"]
    for plugin in json.loads(
        (REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )["plugins"]
]
NESTED_SKILL_FILE = re.compile(
    rf"^(?:{'|'.join(map(re.escape, PLUGIN_NAMES))})/skills/[^/]+/[^/]+/[^/]+/.",
    re.DOTALL,
)


def nested_skill_paths(relative_paths) -> list[str]:
    """The repository-relative paths that break the flat skill-folder rule."""
    return sorted(path for path in relative_paths if NESTED_SKILL_FILE.match(path))


def git_listed_paths(root: Path) -> list[str]:
    """Tracked paths plus untracked, non-ignored ones, relative to `root`."""
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others",
         "--exclude-standard", "-z"],
        check=True, capture_output=True,
    ).stdout
    return [os.fsdecode(path) for path in listing.split(b"\0") if path]


def assert_skill_folders_flat(root: Path) -> None:
    violations = nested_skill_paths(git_listed_paths(root))
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


@pytest.mark.parametrize(
    ("nested", "committed"),
    [
        ("loom-code/skills/x/assets/sub/f.md", False),
        ("loom-code/skills/x/scripts/node_modules/f.js", True),
        ("loom-code/skills/x/assets/sub/\nf.md", True),
    ],
    ids=["uncommitted", "force-added-ignored-dir", "newline-leading-name"],
)
def test_nested_path_fails(tmp_path, nested, committed):
    repo = _git_repo(tmp_path)
    _write(repo / nested)
    if committed:
        git = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid"]
        subprocess.run([*git, "add", "--force", "."], check=True)
        subprocess.run([*git, "commit", "-q", "-m", "fixture"], check=True)

    assert nested_skill_paths(git_listed_paths(repo)) == [nested]
    with pytest.raises(AssertionError) as failure:
        assert_skill_folders_flat(repo)
    # pytest indents continuation lines, so match a newline name's last line.
    assert nested.splitlines()[-1] in str(failure.value)


def test_flat_ignored_and_non_plugin_paths_pass(tmp_path):
    repo = _git_repo(tmp_path)
    (repo / ".gitignore").write_text("loom-code/skills/x/assets/cache/\n", encoding="utf-8")
    _write(repo / "loom-code/skills/x/SKILL.md")
    _write(repo / "loom-code/skills/x/assets/f.md")
    _write(repo / "loom-code/skills/x/assets/cache/f.md")
    _write(repo / "tests/skills/x/assets/sub/f.md")

    assert_skill_folders_flat(repo)
    assert nested_skill_paths(["docs/loom/change/loom-code/skills/x/assets/sub/f.md"]) == []


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
