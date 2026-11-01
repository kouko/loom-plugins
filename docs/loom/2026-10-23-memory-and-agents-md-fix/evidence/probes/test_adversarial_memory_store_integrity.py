# concern: memory store integrity — concept files, name=stem, index reachability, Related links
"""Adversarial probe: the two new memory concept files must pass the OKF v0.2 profile.

Pins: both files validate via `loom_memory.py validate`; each file's YAML `name`
equals its filename stem; `docs/loom/memory/index.md` lists both files with
reachable links; every `[[...]]` Related link inside both files resolves to a
real file in the store.

Mutation probe: removing an index entry for either file, a name/stem mismatch,
a broken Related link, or an invalid concept file turns RED.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
STORE = REPO / "docs" / "loom" / "memory"
LOOM_MEMORY = REPO / "loom-workflow" / "skills" / "loom-memory" / "scripts" / "loom_memory.py"
ENTRIES = ["ship-does-not-write-memory-after-finalize-review.md",
           "version-bump-through-claude-ssot-and-sync-script.md"]


def test_memory_store_passes_okf_validate() -> None:
    """The whole memory store must validate against OKF v0.2."""
    proc = subprocess.run(
        [sys.executable, str(LOOM_MEMORY), "validate", str(STORE)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_each_concept_has_name_equal_to_filename_stem() -> None:
    """The frontmatter `name` of each new entry must equal its filename stem."""
    for entry in ENTRIES:
        path = STORE / entry
        text = path.read_text(encoding="utf-8")
        stem = entry[:-3] if entry.endswith(".md") else entry
        match = re.search(r"^name: (\S+)$", text, re.M)
        assert match, f"{entry}: no frontmatter `name` field"
        assert match.group(1) == stem, f"{entry}: name {match.group(1)!r} != stem {stem!r}"


def test_index_lists_both_new_entries() -> None:
    """index.md must contain an entry link for each new concept file."""
    index = STORE / "index.md"
    text = index.read_text(encoding="utf-8")
    for entry in ENTRIES:
        assert f"[{entry[:-3]}]({entry})" in text or entry in text, f"index.md missing entry for {entry}"


def test_related_links_resolve_to_real_store_files() -> None:
    """Every `[[...]]` Related link inside both new files must point at a real store file."""
    for entry in ENTRIES:
        text = (STORE / entry).read_text(encoding="utf-8")
        for ref in re.findall(r"\[\[([^\]]+)\]\]", text):
            target = STORE / f"{ref}.md"
            assert target.is_file(), f"{entry}: Related link [[{ref}]] does not resolve to {target}"
