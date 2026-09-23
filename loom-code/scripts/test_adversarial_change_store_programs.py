"""Adversarial probe: a change store holds programs the probe cap refuses.

concern: a change that commits runnable programs in its store outside
`evidence/probes/`, so the checker rule `adversarial.proportionate` refuses the
change at finalize-review and the change cannot be attested as it stands.

Graduated from the 2026-09-23 acceptance-testing rename, whose probe ran the
rule against that one change and caught an A/B runner copied into `ab/`. As a
permanent test it asks the same question of every change store at HEAD, using
the rule's own helpers, so the next change that commits a program outside its
probe directory fails here, in the package suite, before finalize-review.

Stores that merged before the rule refused such programs are listed below.
The list may only shrink: a listed store that no longer holds one fails too.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "loom-code/scripts"))

from loom_checker.probes import committed_probe_programs, probe_directory  # noqa: E402

CHANGE_STORE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
MERGED_BEFORE_THE_RULE = {
    "2026-09-14-loom-visualization-description-trigger",
    "2026-09-17-loom-readme-small-fixes",
    "2026-09-22-publication-floor-moves-to-github",
}


def _misplaced_by_store() -> dict[str, list[str]]:
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    found = {}
    for store in sorted((ROOT / "docs/loom").iterdir()):
        if not (store.is_dir() and CHANGE_STORE.match(store.name)):
            continue
        misplaced = [p for p in committed_probe_programs(ROOT, head, store.name)
                     if not p.startswith(probe_directory(store.name))]
        if misplaced:
            found[store.name] = misplaced
    return found


def test_change_stores_hold_no_program_outside_their_probe_directory() -> None:
    """No change store at HEAD, other than the frozen list, holds a misplaced program."""
    found = _misplaced_by_store()
    assert {k: v for k, v in found.items() if k not in MERGED_BEFORE_THE_RULE} == {}
    assert MERGED_BEFORE_THE_RULE <= set(found), "a listed store was cleaned; drop it from the list"
