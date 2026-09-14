"""No live repository path may still route to the removed `cot-explain` skill.

`cot-explain` was removed without an alias and replaced by
`loom-visualization` (user-decided 2026-09-14). Historical change records keep
the old name: everything under `docs/` and every `CHANGELOG*.md`. Everything
else — the plugin folders, the root README, `scripts/`, `.github/` and
`loom-code/contract/` — is live and is scanned.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OLD_NAME = "cot-" + "explain"

SKIPPED_DIRS = {".git", ".pytest_cache", "__pycache__", "node_modules", "docs"}

# Files that name the old skill on purpose: negative assertions, the rename
# map that keeps a frozen baseline readable, and this scanner.
INTENTIONAL = {
    "loom-workflow/scripts/test_no_live_cot_explain_references.py",
    "loom-workflow/scripts/test_loom_visualization_compaction.py",
    "loom-workflow/tests/test_loom_visualization_page_scripts.py",
    "scripts/test_loom_skill_description_catalog.py",
}

# Known pending: task W2-04 renames these (READMEs, plugin keywords, Codex
# longDescription). W2-04 empties this set.
PENDING_W2_04 = {
    "README.md",
    "loom-workflow/README.md",
    "loom-workflow/README.ja.md",
    "loom-workflow/README.zh-TW.md",
    "loom-workflow/.claude-plugin/plugin.json",
    "loom-workflow/.codex-plugin/plugin.json",
}


def _is_live(relative: Path) -> bool:
    if any(part in SKIPPED_DIRS for part in relative.parts[:-1]):
        return False
    return not relative.name.startswith("CHANGELOG")


def find_live_hits(root: Path, allowed: set[str] = frozenset()) -> list[str]:
    """Return `path:line` for every live mention of the old skill name."""
    hits: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
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
    hits = find_live_hits(REPO_ROOT, INTENTIONAL | PENDING_W2_04)
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
