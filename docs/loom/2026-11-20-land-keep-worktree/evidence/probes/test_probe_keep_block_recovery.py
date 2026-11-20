"""Near-miss read of ship §5 after `land --accepted-by <name> --keep-worktree`.
# concern: skill-text recovery path that destroys a worktree the maintainer asked to keep

Run from the repo root:

    python3 -m pytest docs/loom/2026-11-20-land-keep-worktree/evidence/probes/test_probe_keep_block_recovery.py

With `--keep-worktree`, land can still print `Merged PR` and then a
`BLOCK land.verify` (the merge happened, verification failed). Ship §5 tells
the agent, with no keep exception, to "resolve the named state and run
`land --cleanup <branch>`" -- which removes the worktree and both branches
the maintainer asked to keep (intent Acceptance 1 and 5). `land --help` says
the opposite ("pass --keep-worktree ... and do not run cleanup"), so an agent
reading the ship station follows the destructive branch.

The probe requires §5 to carry one affirmative sentence for that case: it
names a BLOCK and `--keep-worktree`, and tells the agent to keep, leave, stay
in or preserve the worktree, with no negation token in the sentence.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from prose_pin import has_negation, split_sentences  # noqa: E402

SHIP = REPO_ROOT / "loom-code" / "skills" / "ship" / "SKILL.md"
FLAG = "`--keep-worktree`"
KEEP_VERB = re.compile(r"\b(keep|keeps|leave|leaves|stay|stays|preserve|preserves)\b.*\bworktree\b",
                       re.IGNORECASE)


def _land_section() -> str:
    flat = " ".join(SHIP.read_text(encoding="utf-8").split())
    section = flat[flat.index("## 5. Land after acceptance"):]
    return section[:section.index("## Handoff")]


def _keeps_after_block(text: str) -> bool:
    """Some sentence names a BLOCK and the flag, and affirms keeping the worktree."""
    for sentence in split_sentences(text):
        if "BLOCK" not in sentence or FLAG not in sentence:
            continue
        # The flag's own spelling contains "keep" and "worktree"; it is not the verb.
        rest = sentence.replace(FLAG, " ")
        if KEEP_VERB.search(rest) and not has_negation(sentence):
            return True
    return False


def test_keepmatcher_affirmative_accepted() -> None:
    """Synthetic: an affirmative keep sentence for the BLOCK case is accepted."""
    sample = ("When land with `--keep-worktree` prints `Merged PR` and then a BLOCK, "
              "resolve the named state and keep the worktree for a later `land --cleanup <branch>`.")
    assert _keeps_after_block(sample)


def test_keepmatcher_negated_rejected() -> None:
    """Synthetic: a negated sentence, or one whose only keep is the flag, is rejected."""
    assert not _keeps_after_block(
        "When land with `--keep-worktree` prints a BLOCK, do not keep the worktree.")
    assert not _keeps_after_block(
        "When land with `--keep-worktree` prints a BLOCK, run `land --cleanup <branch>`.")


def test_shipland_keepblock_keepsworktree() -> None:
    """Ship §5 tells the agent to keep the worktree when a keep land merges then BLOCKs."""
    land = _land_section()
    assert "If land prints `Merged PR` and then a BLOCK" in land
    assert _keeps_after_block(land), (
        "ship §5 routes a post-merge BLOCK to `land --cleanup <branch>` with no "
        "`--keep-worktree` exception; the kept worktree would be removed")
