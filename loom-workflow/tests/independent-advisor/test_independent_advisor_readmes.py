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
