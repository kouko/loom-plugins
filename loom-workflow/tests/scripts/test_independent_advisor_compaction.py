from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/independent-advisor/SKILL.md"
REFERENCES = (
    "references/executor-detection.md",
    "references/dispatch-protocol.md",
    "references/report-contract.md",
)
STRUCTURAL_TOKENS = [
    "name: independent-advisor",
    "version: 0.1.0",
    "`explore`",
    "`audit`",
    "`mode_basis`",
    "`mode_override`",
    "`loom-code:external-review`",
    "owning review skill",
    "incumbent",
    "recorded consent",
    "`review_root`",
    "`allowed_families`",
    "`filesystem_access_outside_root`",
    "`filesystem_write_not_guaranteed`",
    "`proposer`",
    "`normalizer`",
    "`blind judge`",
    "`actual_cost`",
    "`corroborated_by`",
    "`coverage_disclaimer`",
    "`degraded_legs`",
    "`early_stopped`",
    "`known_weaknesses`",
    "`leg_count`",
    "`scope_boundary`",
]
REFERENCE_TOKENS = {
    "references/executor-detection.md": [
        "`loom-code:external-review`",
        "owning review skill",
        "complete consent record",
        "`review_root`",
        "`allowed_families`",
        "`filesystem_access_outside_root`",
        "`filesystem_write_not_guaranteed`",
        "explicit model and effort",
        "evidence level",
    ],
    "references/dispatch-protocol.md": ["`normalized_by_is_incumbent_author`"],
    "references/report-contract.md": [
        "divergence_points",
        "known_weaknesses",
        "coverage_disclaimer",
        "degraded_legs",
        "`evidence_level`",
        "`refusal`",
        "`empty-output`",
        "`missing-field`",
        "`no-reasoning-trace`",
        "`restates-input`",
        "`unbacked-claim`",
    ],
}


def test_entrypoint_points_to_references_that_resolve():
    """Each reference the entrypoint routes to exists. The entrypoint's and the
    references' wording is review-only."""
    assert SKILL_PATH.is_file(), f"missing entrypoint: {SKILL_PATH}"
    text = SKILL_PATH.read_text(encoding="utf-8")

    for reference in REFERENCES:
        assert reference in text, reference
        assert (SKILL_PATH.parent / reference).is_file(), reference


def test_entrypoint_and_references_keep_structural_tokens():
    """Keep consultation roles and reports alongside the named outside handoff."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    missing = [token for token in STRUCTURAL_TOKENS if token not in text]
    assert not missing, f"entrypoint no longer names: {missing}"
    for reference, tokens in REFERENCE_TOKENS.items():
        reference_text = (SKILL_PATH.parent / reference).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in reference_text]
        assert not missing, f"{reference} no longer names: {missing}"


def test_advisor_does_not_reintroduce_its_retired_cli_probe():
    """The shared executor owns CLI-specific commands and credential checks."""
    entrypoint = SKILL_PATH.read_text(encoding="utf-8")
    detection = (SKILL_PATH.parent / REFERENCES[0]).read_text(encoding="utf-8")
    for stale_token in (
        "`credential-missing`",
        "`credential-unusable`",
        "codex exec",
        "model_reasoning_effort=",
        "--skip-git-repo-check",
    ):
        assert stale_token not in entrypoint
        assert stale_token not in detection


def test_skill_body_stays_under_the_repo_word_cap():
    # mirrors WORD_HARD_CAP in scripts/check-skill-structure.py (CHK-SKL-010)
    assert SKILL_PATH.is_file(), f"missing entrypoint: {SKILL_PATH}"
    word_hard_cap = 4500
    word_count = len(SKILL_PATH.read_text(encoding="utf-8").split())
    assert word_count <= word_hard_cap, (
        f"SKILL.md is {word_count} words, over the {word_hard_cap}-word hard cap"
    )
