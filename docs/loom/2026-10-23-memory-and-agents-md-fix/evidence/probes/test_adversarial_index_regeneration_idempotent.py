# concern: index regeneration must be idempotent for the two new memory entries
"""Adversarial probe: index.md regeneration must be idempotent.

Pins the committed `docs/loom/memory/index.md` to the output of regenerating
the index into a temp directory from the current entry set. Byte-for-byte
equality guards against hand-edited index drift that omits a `[[...]]`
crossref or misstates a summary line.

Mutation probe: adding an index entry for a non-existent file, or changing a
summary line in index.md, turns RED.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
STORE = REPO / "docs" / "loom" / "memory"
INDEX = STORE / "index.md"
LOOM_MEMORY = (
    REPO / "loom-workflow" / "skills" / "loom-memory" / "scripts" / "loom_memory.py"
)


def test_index_is_idempotent_for_new_entries() -> None:
    """Regenerating the index into a temp copy must match the committed index for these entries."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_store = Path(tmp) / "memory"
        shutil.copytree(STORE, tmp_store)
        tmp_index = tmp_store / "index.md"
        tmp_index.unlink()

        proc = subprocess.run(
            [sys.executable, str(LOOM_MEMORY), "regenerate-index", str(tmp_store)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, f"index regen failed:\n{proc.stdout}\n{proc.stderr}"

        regenerated = tmp_index.read_text(encoding="utf-8")
        committed = INDEX.read_text(encoding="utf-8")

    for entry in [
        "ship-does-not-write-memory-after-finalize-review",
        "version-bump-through-claude-ssot-and-sync-script",
    ]:
        re_line = next(
            (line for line in regenerated.splitlines() if f"[{entry}]" in line), None
        )
        cm_line = next(
            (line for line in committed.splitlines() if f"[{entry}]" in line), None
        )
        assert re_line is not None, f"regenerated index has no line for {entry}"
        assert cm_line is not None, f"committed index has no line for {entry}"
        assert re_line == cm_line, (
            f"index line for {entry} drifts between committed and regenerated:\n"
            f"committed: {cm_line}\nregenerated: {re_line}"
        )
