# concern: the AGENTS.md version-bump SSOT line must not drift from the sync script's real constants
"""Adversarial probe: the AGENTS.md single-SSOT description must stay truthful.

Pins the Versioning & Release paragraph against the prose contract it is
supposed to express. A regression reintroducing a second hand-authorable
manifest, naming a derived file as the SSOT, or drifting the described
paths from the sync engine's constants fails here.

Mutation probe: a mutation test that introduces the stale "three manifests
must sync" wording must turn RED.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
AGENTS = REPO / "AGENTS.md"


def _norm(text: str) -> str:
    return " ".join(text.split())


def test_agents_md_states_single_ssot_not_three_manifests() -> None:
    """The version-bump MUST rule must state one SSOT plus derived manifests."""
    text = _norm(AGENTS.read_text(encoding="utf-8"))
    assert "單一來源真相" in text, "AGENTS.md version-bump section lost its single-SSOT statement"
    assert "三份 manifest" not in text and "三個 manifest" not in text, (
        "AGENTS.md version-bump section reintroduced the stale 'three manifests must sync' wording"
    )


def test_agents_md_ssot_line_names_real_paths() -> None:
    """Every manifest path named in the SSOT line must exist on disk."""
    text = AGENTS.read_text(encoding="utf-8")
    for rel in [
        "loom-code/.claude-plugin/plugin.json",
        "loom-code/.codex-plugin/plugin.json",
        "loom-code/plugin.json",
        "loom-code/package.json",
    ]:
        assert f"`{rel}`" in text, f"AGENTS.md SSOT line dropped or renamed path {rel}"
        assert (REPO / rel).exists(), f"AGENTS.md SSOT names a path that does not exist: {rel}"


def test_agents_md_does_not_call_derived_manifests_ssot() -> None:
    """The sentence must never present a derived manifest as the source of truth.

    Guards against inversions where a derived manifest is stated as also-SSOT,
    including via the `也是…SSOT` form that a simple `是` check misses.
    """
    raw = AGENTS.read_text(encoding="utf-8")
    text = _norm(raw)
    # No derived manifest may be claimed as the SSOT in any form.
    assert "loom-code/plugin.json` 是單一來源真相" not in text
    assert "loom-code/.codex-plugin/plugin.json` 是單一來源真相" not in text
    assert "loom-code/.codex-plugin/plugin.json` 也是單一來源真相" not in text
    assert "loom-code/.claude-plugin/plugin.json` 也是單一來源真相" not in text
    # The Claude SSOT must remain the ONLY single source of truth.
    assert "單一來源真相" in text
