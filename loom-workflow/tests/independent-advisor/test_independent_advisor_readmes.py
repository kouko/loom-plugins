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
REPORT = SKILL_DIR / "references" / "report-contract.md"
PROMPTS = SKILL_DIR / "test-prompts.json"
EXTERNAL_REVIEW = SKILL_DIR.parents[2] / "loom-code/skills/external-review/SKILL.md"
CLOSING_REVIEW = SKILL_DIR.parents[2] / "loom-code/skills/closing-review/SKILL.md"

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


def test_explicit_review_selects_a_real_owner_before_external_execution():
    skill = SKILL.read_text(encoding="utf-8")
    dispatch = DISPATCH.read_text(encoding="utf-8")
    for owner in ("loom-code:closing-review", "loom-code:write-plan", "loom-workflow:critique"):
        assert owner in skill
    assert "advisor audit consultation" in skill
    assert "assembles the review packet" in skill
    assert "validates the returned verdict" in skill
    assert "owning review skill" in dispatch


def test_unowned_code_plan_or_decision_uses_advisor_audit_without_formal_verdict():
    skill = SKILL.read_text(encoding="utf-8")
    dispatch = DISPATCH.read_text(encoding="utf-8")
    assert "code, plan, or decision without an applicable Loom review owner" in skill
    assert "uncommitted code" in skill
    assert "advisor audit consultation report" in skill
    assert "separately from the incumbent" in skill
    assert "not a formal owner verdict" in skill
    assert "code, plan, or decision" in dispatch
    assert "advisor's `audit` consultation report contract" in dispatch


def test_coverage_disclaimer_does_not_claim_unobserved_file_access():
    report = REPORT.read_text(encoding="utf-8")
    assert "dispatch packet" in report.lower()
    assert "cannot attest which other files the CLI accessed" in report
    assert "Anything outside that list was not looked at" not in report


def test_named_direct_request_authorizes_one_review_without_repeat_confirmation():
    skill = SKILL.read_text(encoding="utf-8")
    handoff = DETECTION.read_text(encoding="utf-8")
    external = EXTERNAL_REVIEW.read_text(encoding="utf-8")
    closing = CLOSING_REVIEW.read_text(encoding="utf-8")
    for text in (skill, handoff, external, closing):
        assert "authorization_source" in text
        assert "direct user request" in text
        assert "without a second" in text
    assert "consent record" in external
    assert "disclose" in skill
    assert "provider or target is ambiguous" in skill
    assert "material scope expands" in skill


def test_readmes_describe_direct_request_and_nonblocking_disclosure():
    markers = {
        README_EN: "no second confirmation",
        README_JA: "二度目の確認",
        README_ZHTW: "第二次確認",
    }
    for path, label in READMES:
        body = path.read_text(encoding="utf-8")
        assert "loom-code:external-review" in body, label
        assert markers[path] in body.lower(), label


def test_prompt_cases_cover_direct_request_and_ambiguous_boundaries():
    import json

    cases = json.loads(PROMPTS.read_text(encoding="utf-8"))["prompts"]
    by_id = {case["id"]: case for case in cases}
    assert "without a second confirmation" in by_id[10]["expected_behavior"]
    assert "ambiguous target" in by_id[11]["expected_behavior"]
    assert "expanded scope" in by_id[12]["expected_behavior"]
    assert "suggestion alone" in by_id[13]["expected_behavior"]
