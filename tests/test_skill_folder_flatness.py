"""Skill folders stay flat.

A skill holds SKILL.md plus single-level subfolders, so a file at
`<plugin>/skills/<skill>/<subfolder>/<nested>/...` breaks the rule. The package
suite catches that here, committed or not, from git's own list: every tracked
path, even one under an ignored folder, plus untracked, non-ignored files, as
long as the path still exists in the working tree. A folder git lists as one
entry, a nested repository, is searched on disk.

A gitlink (a nested repository recorded in git's index) at or under
`<plugin>/skills/<skill>` always fails, with or without its folder: a fresh
clone, which is what CI uses, has none of its content to search.

These pass:
- An uncommitted git-ignored path: it does not enter the repository, and local
  caches such as `__pycache__` would otherwise fail the suite.
- A symlink to a folder: git stores only the link.
- A committed file already deleted from disk: the deletion is the fix, not yet
  committed.

Ignore rules do not apply inside a nested repository, so an ignored file nested
there fails: its files are walked on disk, because git run in a gitlink folder
may answer for the outer repository.

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
SKILL_FOLDER = rf"^(?:{'|'.join(map(re.escape, PLUGIN_NAMES))})/skills/[^/]+"
NESTED_SKILL_FILE = re.compile(rf"{SKILL_FOLDER}/[^/]+/[^/]+/")
AT_OR_UNDER_SKILL = re.compile(rf"{SKILL_FOLDER}(?:/|\Z)")


def nested_skill_paths(relative_paths) -> list[str]:
    """The repository-relative paths that break the flat skill-folder rule."""
    return sorted(path for path in relative_paths if NESTED_SKILL_FILE.match(path))


def files_beneath(folder: Path, root: Path) -> list[str]:
    """Files under `folder`, relative to `root`, outside any `.git`; links not followed.

    This walks the disk because a gitlink folder may have no `.git` of its own,
    and git run there would answer for the outer repository.
    """
    files = []
    for current, folders, names in os.walk(folder):
        folders[:] = [name for name in folders if name != ".git"]
        files += [
            (Path(current) / name).relative_to(root).as_posix()
            for name in names
            if name != ".git"
        ]
    return files


def git_listed_paths(root: Path) -> list[str]:
    """Listed paths still on disk, relative to `root`; real folders end in `/`.

    Git lists a nested repository as the folder itself, so no file path shows it:
    such a folder is followed by the files beneath it.
    """
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others",
         "--exclude-standard", "-z"],
        check=True, capture_output=True,
    ).stdout
    paths = []
    for entry in filter(None, listing.split(b"\0")):
        path = os.fsdecode(entry).rstrip("/")
        full_path = root / path
        if os.path.lexists(full_path):
            is_folder = full_path.is_dir() and not full_path.is_symlink()
            paths.append(f"{path}/" if is_folder else path)
            if is_folder:
                paths += files_beneath(full_path, root)
    return paths


def skill_gitlinks(root: Path) -> list[str]:
    """Gitlinks in git's index at or under a skill folder, each ending in `/`."""
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--stage", "-z"],
        check=True, capture_output=True,
    ).stdout
    gitlinks = []
    for entry in filter(None, listing.split(b"\0")):
        metadata, path = entry.split(b"\t", 1)
        if metadata.startswith(b"160000 ") and AT_OR_UNDER_SKILL.match(os.fsdecode(path)):
            gitlinks.append(f"{os.fsdecode(path)}/")
    return gitlinks


def assert_skill_folders_flat(root: Path) -> None:
    violations = sorted(
        {*nested_skill_paths(git_listed_paths(root)), *skill_gitlinks(root)}
    )
    assert not violations, (
        "skill subfolders must not contain subfolders, and skills must not "
        "contain gitlinks; move these files up one level or remove the "
        "gitlink:\n" + "\n".join(violations)
    )


def _git_repo(root: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def _write(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n", encoding="utf-8")


def _commit_all(root: Path) -> None:
    git = ["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@example.invalid"]
    subprocess.run([*git, "add", "--force", "."], check=True, capture_output=True)
    subprocess.run([*git, "commit", "-q", "-m", "fixture"], check=True)


def _add_gitlink(root: Path, path: str) -> None:
    """Record a gitlink with no folder on disk, as a fresh clone has it."""
    subprocess.run(
        ["git", "-C", str(root), "update-index", "--add", "--cacheinfo",
         f"160000,{'1' * 40},{path}"],
        check=True,
    )


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
        _commit_all(repo)

    assert nested_skill_paths(git_listed_paths(repo)) == [nested]
    with pytest.raises(AssertionError) as failure:
        assert_skill_folders_flat(repo)
    # pytest indents continuation lines, so match a newline name's last line.
    assert nested.splitlines()[-1] in str(failure.value)

    (repo / nested).unlink()
    assert_skill_folders_flat(repo)


@pytest.mark.parametrize("outer_committed", [False, True], ids=["untracked", "gitlink"])
@pytest.mark.parametrize(
    ("repository", "inner_file", "nested"),
    [
        ("loom-code/skills/x/assets/vendor", "f.md", "loom-code/skills/x/assets/vendor"),
        ("loom-code/skills/x/references", "deep/f.md", "loom-code/skills/x/references/deep/f.md"),
        ("loom-code/skills/x", "references/deep/f.md", "loom-code/skills/x/references/deep/f.md"),
    ],
    ids=["repository-is-nested", "repository-at-subfolder", "repository-at-skill"],
)
def test_nested_git_repository_fails(tmp_path, outer_committed, repository, inner_file, nested):
    repo = _git_repo(tmp_path)
    _git_repo(repo / repository)
    _write(repo / repository / inner_file)
    _commit_all(repo / repository)
    if outer_committed:
        _commit_all(repo)

    with pytest.raises(AssertionError) as failure:
        assert_skill_folders_flat(repo)
    assert nested in str(failure.value)


@pytest.mark.parametrize("gitlink", ["loom-code/skills/x/references", "loom-code/skills/x"])
def test_gitlink_without_folder_fails_until_removed(tmp_path, gitlink):
    repo = _git_repo(tmp_path)
    _add_gitlink(repo, gitlink)

    with pytest.raises(AssertionError) as failure:
        assert_skill_folders_flat(repo)
    assert gitlink in str(failure.value)

    subprocess.run(["git", "-C", str(repo), "rm", "-q", "--cached", gitlink], check=True)
    assert_skill_folders_flat(repo)


def test_gitlink_outside_skills_passes(tmp_path):
    repo = _git_repo(tmp_path)
    _add_gitlink(repo, "vendor/skills/x/references")
    _add_gitlink(repo, "loom-code/vendor")

    assert_skill_folders_flat(repo)


def test_flat_ignored_and_non_plugin_paths_pass(tmp_path):
    repo = _git_repo(tmp_path)
    (repo / ".gitignore").write_text("loom-code/skills/x/assets/cache/\n", encoding="utf-8")
    _write(repo / "loom-code/skills/x/SKILL.md")
    _write(repo / "loom-code/skills/x/assets/f.md")
    _write(repo / "loom-code/skills/x/assets/cache/f.md")
    _write(repo / "tests/skills/x/assets/sub/f.md")
    os.symlink("..", repo / "loom-code/skills/x/assets/folder-link")
    _git_repo(repo / "loom-code/skills/y")
    _write(repo / "loom-code/skills/y/references/f.md")
    _commit_all(repo / "loom-code/skills/y")

    assert_skill_folders_flat(repo)
    assert nested_skill_paths(["docs/loom/change/loom-code/skills/x/assets/sub/f.md"]) == []


def test_repository_skill_folders_are_flat():
    assert_skill_folders_flat(REPO)
