"""No live repository path may still route to the removed `cot-explain` skill.

`cot-explain` was removed without an alias and replaced by
`loom-visualization` (user-decided 2026-09-14). Historical change records keep
the old name: everything under `docs/` and every `CHANGELOG*.md`. Everything
else — the plugin folders, the root README, `scripts/`, `.github/` and
`loom-code/contract/` — is live and is scanned.

Which files are the repository's own is git's answer, taken from
`repo_files.repository_files`: an ignored file and a linked worktree checked
out inside the tree are not live paths of this repository. `docs/` stays in
this scanner's own `SKIPPED_DIRS` — it is this rule's history exemption, not a
generic ignore name. The loom-code module is reached across trees by sys.path,
as `loom-design/tests/spec/test_write_spec_contract.py` already does.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from repo_files import repository_files  # noqa: E402
OLD_NAME = "cot-" + "explain"

# This rule's own history exemption. The machinery names (`.git`,
# `__pycache__`, …) that used to sit here belong to the file list and are not
# repeated: a second copy of an ignore list is a second thing to drift.
SKIPPED_DIRS = {"docs"}

# Files that name the old skill on purpose: negative assertions, the rename
# map that keeps a frozen baseline readable, and this scanner.
INTENTIONAL = {
    "loom-workflow/tests/scripts/test_no_live_cot_explain_references.py",
    "loom-workflow/tests/scripts/test_loom_visualization_compaction.py",
    "loom-workflow/tests/test_loom_visualization_page_scripts.py",
    "tests/test_loom_skill_description_catalog.py",
}



def _is_live(relative: Path) -> bool:
    if any(part in SKIPPED_DIRS for part in relative.parts[:-1]):
        return False
    return not relative.name.startswith("CHANGELOG")


def find_live_hits(root: Path, allowed: set[str] = frozenset()) -> list[str]:
    """Return `path:line` for every live mention of the old skill name."""
    hits: list[str] = []
    for path in sorted(repository_files(root)):
        relative = path.relative_to(root)
        if not _is_live(relative) or relative.as_posix() in allowed:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if OLD_NAME in line:
                hits.append(f"{relative.as_posix()}:{number}")
    return hits


def test_no_live_path_names_the_removed_skill():
    hits = find_live_hits(REPO_ROOT, INTENTIONAL)
    assert not hits, "live references to the removed skill:\n" + "\n".join(hits)


def test_scanner_flags_a_synthetic_live_hit_and_skips_history(tmp_path):
    live = tmp_path / "loom-workflow" / "skills" / "x" / "SKILL.md"
    live.parent.mkdir(parents=True)
    live.write_text(f"see [{OLD_NAME}](../{OLD_NAME}/SKILL.md)\n", encoding="utf-8")
    history = tmp_path / "docs" / "loom" / "record.md"
    history.parent.mkdir(parents=True)
    history.write_text(OLD_NAME, encoding="utf-8")
    changelog = tmp_path / "loom-workflow" / "CHANGELOG.md"
    changelog.write_text(OLD_NAME, encoding="utf-8")

    assert find_live_hits(tmp_path) == ["loom-workflow/skills/x/SKILL.md:1"]


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _seed_repo(repo: Path) -> Path:
    """A real git repository -- the behaviour under test is git's own."""
    (repo / "loom-workflow" / "skills" / "x").mkdir(parents=True)
    (repo / "loom-workflow" / "skills" / "x" / "SKILL.md").write_text(
        "clean\n", encoding="utf-8"
    )
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")
    return repo


def test_nested_worktree_produces_no_hits(tmp_path):
    """A linked worktree checked out inside the repository is another
    checkout of it; its files are not this repository's live paths."""
    repo = _seed_repo(tmp_path / "repo")
    _git(repo, "worktree", "add", "-q", "-b", "side", str(repo / "wt"))
    (repo / "wt" / "loom-workflow" / "skills" / "x" / "SKILL.md").write_text(
        OLD_NAME, encoding="utf-8"
    )

    assert find_live_hits(repo) == []


def test_own_violation_still_reported(tmp_path):
    """An untracked, unignored file of this repository is still scanned."""
    repo = _seed_repo(tmp_path / "repo")
    (repo / "loom-workflow" / "skills" / "x" / "OTHER.md").write_text(
        OLD_NAME, encoding="utf-8"
    )

    assert find_live_hits(repo) == ["loom-workflow/skills/x/OTHER.md:1"]
