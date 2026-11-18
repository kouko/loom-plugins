"""Skill folders stay flat.

A skill holds SKILL.md plus single-level subfolders, so a file at
`<plugin>/skills/<skill>/<subfolder>/<nested>/...` breaks the rule. The package
suite catches that here, committed or not, from git's own list: every tracked
path, even one under an ignored folder, plus untracked, non-ignored files.

`<plugin>` is a top-level folder named in this repository's marketplace.json:
other folders holding a `skills/` directory, such as test fixtures or records
under `docs/`, are not plugins.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
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
