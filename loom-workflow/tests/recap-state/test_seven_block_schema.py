"""
Tests for loom-workflow/skills/recap-state/references/seven-block-schema.md

Asserts:
  - 7 H2/H3 block headings (Situation, Background, Assessment, User messages,
    Why-this-question, Pending, Synthesis-check) are present (case-insensitive)
  - 5 shared-core-principle anchors present: structured-schema, quote-not-paraphrase,
    all-user-messages, synthesis-check, plain-language
  - 1 good-example heading + 1 bad-example heading

WHY: The seven-block-schema.md is the SSOT for the Recap skill's output contract.
     Every principle must be machine-verifiable at test time so schema drift
     (someone editing the file and dropping a block) is caught immediately —
     before SKILL.md routing breaks silently at runtime.
"""

import pathlib
import re

BUNDLE_PATH = (
    pathlib.Path(__file__).resolve().parents[2] / "skills" / "recap-state" / "references" / "seven-block-schema.md"
)

# ── helpers ─────────────────────────────────────────────────────────────────


def load_bundle() -> str:
    """Load bundle file; fail with a clear message if missing (RED state)."""
    assert BUNDLE_PATH.exists(), (
        f"Bundle file not found: {BUNDLE_PATH}\n"
        "This is the expected RED state — create the file to go GREEN."
    )
    return BUNDLE_PATH.read_text(encoding="utf-8")


def heading_present(text: str, keyword: str) -> bool:
    """
    Return True if any H2/H3 heading contains `keyword`.
    Case-insensitive. Accepts zh-TW / ja alongside English.
    A heading line is one that starts with ## or ###.
    """
    pattern = re.compile(
        r"^#{2,3}\s+.*" + re.escape(keyword) + r".*$",
        re.IGNORECASE | re.MULTILINE,
    )
    return bool(pattern.search(text))


def anchor_present(text: str, anchor: str) -> bool:
    """
    Return True if `anchor` appears as a markdown anchor target or
    as a heading/bold keyword in the file.
    We look for the anchor string with optional surrounding formatting
    (bold, heading markers, or bare text). Case-insensitive.
    """
    pattern = re.compile(re.escape(anchor), re.IGNORECASE)
    return bool(pattern.search(text))


# ── main test ────────────────────────────────────────────────────────────────


def test_all_seven_blocks_and_five_principles_present() -> None:
    """
    Verify the bundle ships:
      1. All 7 V1 block headings (case-insensitive; multilingual-friendly)
      2. All 5 shared-core-principle anchors
      3. A good-example section heading
      4. A bad-example section heading
      What the bad example demonstrates is left to review.

    WHY each check matters:
      Blocks: the fixed schema is the user-visible value; any dropped block
              silently breaks the agent's output structure.
      Principles: the 5 principles are the WHY behind each schema rule;
                  dropping one removes the rationale that makes the rule
                  memorable and enforceable in downstream reviews.
      Examples: without a concrete good/bad pair the schema is abstract;
                the contrast is the primary teaching mechanism.
    """
    text = load_bundle()

    # ── 7 block headings ────────────────────────────────────────────────────
    required_headings = [
        "Situation",
        "Background",
        "Assessment",
        # "User messages" — allow partial match; "User" is the key token
        "User",
        # "Why-this-question" — allow partial match; "Why" is the key token
        "Why",
        "Pending",
        "Synthesis",
    ]
    for keyword in required_headings:
        assert heading_present(text, keyword), (
            f"Expected H2/H3 heading containing '{keyword}' not found.\n"
            f"All 7 V1 blocks (Situation / Background / Assessment / "
            f"User messages / Why-this-question / Pending / Synthesis-check) "
            f"must appear as section headings."
        )

    # ── 5 shared-core-principle anchors ─────────────────────────────────────
    required_anchors = [
        "structured-schema",
        "quote-not-paraphrase",
        "all-user-messages",
        "synthesis-check",
        "plain-language",
    ]
    for anchor in required_anchors:
        assert anchor_present(text, anchor), (
            f"Expected principle anchor '{anchor}' not found.\n"
            f"All 5 shared core principles (structured-schema / quote-not-paraphrase / "
            f"all-user-messages / synthesis-check / plain-language) must be "
            f"present. The 5th (plain-language) is skill-specific per the "
            f"2026-05-26 brief amendment."
        )

    # ── good-example block ───────────────────────────────────────────────────
    assert heading_present(text, "Good Example"), (
        "Expected a 'good example' section not found. "
        "The good/bad contrast is the primary teaching mechanism for the schema."
    )

    # ── bad-example block ────────────────────────────────────────────────────
    assert heading_present(text, "Bad Example"), (
        "Expected a 'bad example' section not found. "
        "The good/bad contrast is the primary teaching mechanism for the schema."
    )


def test_l3_contract_defines_goal_grounded_natural_output() -> None:
    """The L3 template carries its six section headings and no planning tags or block labels."""
    text = load_bundle()

    l3_template_start = text.index("## L3 user-visible template")
    next_h2 = re.search(r"^## (?!#)", text[l3_template_start + 3 :], re.MULTILINE)
    assert next_h2, "L3 template must be followed by another H2 section"
    l3_template_end = l3_template_start + 3 + next_h2.start()
    l3_template = text[l3_template_start:l3_template_end]
    sections = (
        "### Purpose and current position",
        "### Essential background",
        "### Gap and current assessment",
        "### Why confirmation is needed now",
        "### Pending work",
        "### Align purpose and next step",
    )
    missing = [section for section in sections if section not in l3_template]
    assert not missing, f"L3 template missing section headings: {missing}"
    for forbidden in ("<thinking>", "</thinking>", "<recap>", "</recap>", "Block "):
        assert forbidden not in l3_template

    assert "Renumber the rendered output" not in text
    assert "instead of the 7 blocks" not in text
    assert "`loom-workflow:recap-state`" in text
    assert "loom-workflow/skills/recap-state/scripts/" in text


def test_english_reference_keeps_localized_text_to_explicit_quotations() -> None:
    text = load_bundle()

    # The reference is English. Localized source titles, verbatim user feedback,
    # confirmation examples, and quoted repository rules remain valid evidence,
    # but prose headings and English example fields must not drift across languages.
    forbidden_prose_labels = (
        "The Five 共通核心原則",
        "the 5 共通核心原則",
        "**距離目的還缺**",
        "**假設**",
        "**信心**",
        "**卡住**",
    )
    present = [label for label in forbidden_prose_labels if label in text]
    assert not present, f"Localized labels leaked into English reference prose: {present}"
