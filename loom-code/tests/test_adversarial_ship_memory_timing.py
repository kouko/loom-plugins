# concern: memory-write-timing rule absent, weakened, or reintroducing sibling-plugin internal citations in ship/SKILL.md
"""Adversarial regression pins for the rewritten ship memory-write-timing paragraph (HEAD 48b3161a).

The paragraph was rewritten to cite only public skill names
(`loom-workflow:git-memory`, `loom-workflow:loom-memory`) instead of
sibling-plugin internal `loom-workflow/skills/...SKILL.md:NN-NN` line
ranges — those internal citations broke isolated-install boundary tests
and were removed. Each pin is GREEN on current HEAD and turns RED if its
target defect is reintroduced: paragraph removed, timing rule weakened,
internal file:line citations reintroduced, or a contradiction with
closing-review's Convergence passage introduced.
"""

from pathlib import Path

SHIP = Path(__file__).resolve().parents[1] / "skills" / "ship" / "SKILL.md"
CLOSE_REVIEW = (
    Path(__file__).resolve().parents[1] / "skills" / "closing-review" / "SKILL.md"
)


def _norm(text: str) -> str:
    return " ".join(text.split())


def _ship_norm() -> str:
    return _norm(_ship_text())


def _ship_text() -> str:
    return SHIP.read_text(encoding="utf-8")


def test_ship_memory_write_timing_paragraph_present():
    """The paragraph states Ship does not write memory entries after finalize-review."""
    text = _ship_norm()
    assert "Memory write timing:" in text
    assert (
        "Ship **does not write memory entries** after finalize-review has run"
        in text
    )
    assert (
        "qualifying lessons discovered at or after Ship are deferred to the next"
        " change's branch" in text
        or "routes qualifying lessons discovered at or after Ship to the next"
        " change's branch" in text
    )


def test_ship_timing_paragraph_after_loom_memory_routing():
    """The timing paragraph sits after the completed loom-memory routing sentence,
    not splitting it (HEAD 48b3161a repositioned it there)."""
    text = _ship_norm()
    idx_timing = text.find("Memory write timing:")
    idx_loom_memory = text.find("`loom-workflow:loom-memory`")
    assert idx_timing > 0, "Memory write timing paragraph missing"
    assert idx_loom_memory > 0, "loom-memory routing sentence missing"
    assert idx_loom_memory < idx_timing, (
        "timing paragraph must follow the loom-memory routing sentence, "
        "not precede/split it"
    )


def test_ship_no_internal_file_line_citations():
    """Sibling-plugin internal `loom-workflow/skills/...SKILL.md:NN-NN` citations
    were removed because they broke isolated-install boundary tests."""
    text = _ship_text()
    assert "loom-workflow/skills/git-memory/SKILL.md:102–111" not in text
    assert "loom-workflow/skills/git-memory/SKILL.md:102-111" not in text
    assert "loom-workflow/skills/loom-memory/SKILL.md:83–92" not in text
    assert "loom-workflow/skills/loom-memory/SKILL.md:83-92" not in text
    assert "references/operations.md:36–40" not in text
    assert "references/operations.md:36-40" not in text


def test_ship_public_skill_name_citations():
    """The timing paragraph cites only public skill names now."""
    text = _ship_text()
    assert "loom-workflow:git-memory" in text
    assert "loom-workflow:loom-memory" in text


def test_ship_memory_timing_consistent_with_closing_review_convergence():
    """No contradiction: closing-review Convergence also defers post-digest lessons to the next change."""
    ship = _ship_norm()
    review = CLOSE_REVIEW.read_text(encoding="utf-8")
    assert (
        "deferred to the next change's branch" in ship
        or "routes ... to the next change's branch" in ship
        or "to the next change's branch" in ship
    )
    assert (
        "rides the next change's branch as a batched passenger" in review
    )
