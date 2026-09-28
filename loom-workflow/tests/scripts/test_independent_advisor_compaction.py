from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/independent-advisor/SKILL.md"
REFERENCES = (
    "references/executor-detection.md",
    "references/dispatch-protocol.md",
    "references/report-contract.md",
)


def test_entrypoint_points_to_references_that_resolve():
    """Each reference the entrypoint routes to exists. The entrypoint's and the
    references' wording is review-only."""
    assert SKILL_PATH.is_file(), f"missing entrypoint: {SKILL_PATH}"
    text = SKILL_PATH.read_text(encoding="utf-8")

    for reference in REFERENCES:
        assert reference in text, reference
        assert (SKILL_PATH.parent / reference).is_file(), reference


def test_skill_body_stays_under_the_repo_word_cap():
    # mirrors WORD_HARD_CAP in scripts/check-skill-structure.py (CHK-SKL-010)
    assert SKILL_PATH.is_file(), f"missing entrypoint: {SKILL_PATH}"
    word_hard_cap = 4500
    word_count = len(SKILL_PATH.read_text(encoding="utf-8").split())
    assert word_count <= word_hard_cap, (
        f"SKILL.md is {word_count} words, over the {word_hard_cap}-word hard cap"
    )
