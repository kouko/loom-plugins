# concern: the version-bump memory entry must not name loom-code/plugin.json as SSOT; the ship entry must state the before-finalize-review deadline
"""Adversarial probe: claim-content pins for the two new memory concept files.

Pins:
- `version-bump-through-claude-ssot-and-sync-script.md` must NOT name `loom-code/plugin.json` as the SSOT
  (that is the trap this change fixes — the SSOT is `loom-code/.claude-plugin/plugin.json`).
- `ship-does-not-write-memory-after-finalize-review.md` must state the before-finalize-review deadline
  (qualifying lessons discovered at or after Ship ride the next change's branch; Ship must not write
  memory entries after finalize-review has generated the attestation).

Mutation probe: weakening the SSOT claim to `loom-code/plugin.json`, or dropping the before-finalize-review
deadline statement from the ship entry, turns RED.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
STORE = REPO / "docs" / "loom" / "memory"


def _norm(text: str) -> str:
    return " ".join(text.split())


def test_version_bump_entry_names_claude_ssot_not_derived_plugin_json() -> None:
    """The entry must present loom-code/.claude-plugin/plugin.json as SSOT, never loom-code/plugin.json."""
    path = STORE / "version-bump-through-claude-ssot-and-sync-script.md"
    text = path.read_text(encoding="utf-8")
    assert "loom-code/.claude-plugin/plugin.json" in text, (
        "version-bump entry dropped the Claude SSOT path"
    )
    assert "`loom-code/plugin.json` is the single source of truth" not in text
    assert "loom-code/plugin.json` is the SSOT" not in text
    assert "loom-code/plugin.json` is the single source of truth" not in text


def test_ship_entry_states_before_finalize_review_deadline() -> None:
    """The ship entry must state the before-finalize-review deadline."""
    path = STORE / "ship-does-not-write-memory-after-finalize-review.md"
    text = _norm(path.read_text(encoding="utf-8"))
    assert "finalize-review" in text, "ship entry lost its finalize-review reference"
    assert (
        "Ship must not write memory entries after finalize-review" in text
        or "Ship **does not write memory entries** after finalize-review" in text
    ), "ship entry dropped the after-finalize-review prohibition"
    assert (
        "ride the next change's branch" in text
        or "routes qualifying lessons discovered at or after Ship to the next" in text
        or "qualifying lessons discovered at or after Ship are deferred to the next" in text
    ), "ship entry lost the next-change-deferral deadline"
