"""Tests for loom-workflow/skills/independent-advisor tri-language READMEs — Task 8.

Assertions:
  1. All 3 README files exist: README.md, README.ja.md, README.zh-TW.md
  2. Each names the skill and the sibling `critique` skill.
  3. Each documents BOTH modes (`explore` / `audit`).
  4. None claims complete / comprehensive / exhaustive coverage (absence).

The prose of the executor-not-lens distinction, the honest-framing caveats
and the native invocation phrases is left to review.
"""

import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "independent-advisor"
README_EN = SKILL_DIR / "README.md"
README_JA = SKILL_DIR / "README.ja.md"
README_ZHTW = SKILL_DIR / "README.zh-TW.md"
SKILL = SKILL_DIR / "SKILL.md"
DETECTION = SKILL_DIR / "references" / "executor-detection.md"
DISPATCH = SKILL_DIR / "references" / "dispatch-protocol.md"
PROMPTS = SKILL_DIR / "test-prompts.json"

READMES = [
    (README_EN, "README.md (EN)"),
    (README_JA, "README.ja.md (JA)"),
    (README_ZHTW, "README.zh-TW.md (zh-TW)"),
]

# Concept matchers — each is a list of candidate substrings; any match satisfies
# the concept. Keys are human-readable concept names used in error messages.
CONCEPT_MATCHERS = {
    "skill-name": ["independent-advisor", "Independent Advisor"],
    "sibling-distinction": [
        "critique",
    ],
    "mode-explore": ["explore"],
    "mode-audit": ["audit"],
}

REQUIRED_CONCEPTS = [
    "skill-name",
    "sibling-distinction",
    "mode-explore",
    "mode-audit",
]

# Overclaim words the honest framing forbids anywhere in the READMEs.
OVERCLAIM_PATTERN = re.compile(
    r"comprehensive|exhaustive|complete coverage|網羅的|完全な網羅|完整涵蓋|全面涵蓋",
    re.IGNORECASE,
)


def _check_concepts(readme_text: str, label: str) -> None:
    missing = [
        concept
        for concept in REQUIRED_CONCEPTS
        if not any(phrase in readme_text for phrase in CONCEPT_MATCHERS[concept])
    ]
    assert not missing, (
        f"{label}: missing concept(s) {missing}. Checked phrases per concept: "
        + "; ".join(f"{c}: {CONCEPT_MATCHERS[c]}" for c in missing)
    )


def test_all_three_language_readmes_exist_and_agree():
    """Three READMEs exist, name the skill, its sibling and both modes, and
    never overclaim coverage."""

    for path, label in READMES:
        assert path.exists(), f"{label} does not exist at {path}"

    texts = {label: path.read_text(encoding="utf-8") for path, label in READMES}

    for label, text in texts.items():
        _check_concepts(text, label)
        overclaim = OVERCLAIM_PATTERN.search(text)
        assert overclaim is None, (
            f"{label}: coverage overclaim {overclaim.group(0)!r} — the skill's "
            "honest framing forbids describing coverage as complete."
        )


def test_named_external_review_handoff_preserves_owning_contract_and_consent():
    skill = SKILL.read_text(encoding="utf-8")
    detection = DETECTION.read_text(encoding="utf-8")
    dispatch = DISPATCH.read_text(encoding="utf-8")
    assert "code, plan, or decision" in skill
    assert "loom-code:external-review" in skill
    assert "owning review skill" in skill
    assert "incumbent" in skill
    assert "consent record" in skill
    assert "single checkpoint" in skill
    assert "loom-code:external-review" in detection
    assert "loom-code/scripts/" not in detection
    assert "codex exec" not in detection
    assert "owning review skill" in dispatch
    assert "loom-code:external-review" in dispatch


def test_bounded_consent_allows_discovery_before_exact_model_selection():
    skill = SKILL.read_text(encoding="utf-8")
    handoff = DETECTION.read_text(encoding="utf-8")
    assert "bounded model selection after consent" in skill
    assert "provider family and effort bound" in skill
    assert "explicit model and effort" in handoff
    assert "within the recorded bounds" in handoff
    assert "any unknown choice resolved before recording consent" not in skill
    assert "A different executor, model," not in handoff


def test_review_root_is_not_a_read_boundary_and_agy_family_is_selected_later():
    skill = SKILL.read_text(encoding="utf-8")
    handoff = DETECTION.read_text(encoding="utf-8")
    for text in (skill, handoff):
        assert "review_root" in text
        assert "filesystem_access_outside_root" in text
        assert "filesystem_write_not_guaranteed" in text
        assert "allowed_families" in text
    assert "not a filesystem read boundary" in skill
    assert "readable scope" not in handoff
    assert "authorized scope" not in skill


def test_readmes_and_prompts_cover_outside_reviews():
    import json

    for path, label in READMES:
        body = path.read_text(encoding="utf-8")
        assert "loom-code:external-review" in body, label
    prompts = json.loads(PROMPTS.read_text(encoding="utf-8"))["prompts"]
    cases = {case["id"]: case for case in prompts}
    for review_type in ("code", "plan", "decision"):
        assert any(review_type in case["prompt"].lower() and
                   "external-review" in case["expected_behavior"]
                   for case in prompts)
    assert len(cases) == len(prompts)
