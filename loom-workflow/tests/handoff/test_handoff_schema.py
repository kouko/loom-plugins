"""
Structural tests for handoff-schema.md bundle.

Tests verify:
- All 10 H2/H3 block headings present (case-insensitive)
- All 5 principle anchors present
- Good-example and bad-example section headings present
- No Markdown links pointing to loom-workflow/skills/recap/ (skill-independence guarantee)

WHY: These tests encode the structural contract for the HANDOFF v0.1 schema bundle.
Any drift in heading names, missing principles, or cross-skill references would
break the SKILL.md routing and the L2 audience contract.
"""

import re
from pathlib import Path

BUNDLE_PATH = (
    Path(__file__).resolve().parents[2] / "skills" / "handoff" / "references" / "handoff-schema.md"
)

REQUIRED_HEADINGS = [
    "frontmatter",
    "situation",
    "background",
    "all user messages",
    "recent decisions",
    "pending",
    "critical files",
    "do not touch",
    "verification",
    "confidence",
]

REQUIRED_PRINCIPLE_ANCHORS = [
    "structured-schema",
    "quote-not-paraphrase",
    "all-user-messages",
    "synthesis-check",
    "technical-precision",
]

FORBIDDEN_CROSS_LINK = "loom-workflow/skills/recap"

# Regex pattern for H2/H3 headings.
# Use a plain r-string (not f-string) to avoid {2,3} being interpreted
# as an f-string expression. The heading text is appended via string concat.
_H2_H3_PREFIX = r"^#{2,3}\s+.*"


def _read_bundle() -> str:
    """Read the bundle file; fail with a descriptive message if missing."""
    assert BUNDLE_PATH.exists(), (
        f"Bundle file not found: {BUNDLE_PATH}\n"
        "This is expected at RED stage. Create the bundle to make this test pass."
    )
    return BUNDLE_PATH.read_text(encoding="utf-8")


def test_all_ten_blocks_and_five_principles_present() -> None:
    """
    Main structural gate: 10 block headings + 5 principle anchors + good/bad
    example headings + skill-independence (no recap cross-links). What the
    bad example demonstrates is left to review.

    WHY: This test encodes the T1 Acceptance criteria from the plan verbatim.
    Splitting into sub-functions would lose the single-commit gate contract.
    """
    content = _read_bundle()
    content_lower = content.lower()

    # --- 10 block headings (case-insensitive) ---
    # Build pattern by string concat: _H2_H3_PREFIX + escaped heading.
    # Cannot use f-string here because {2,3} in rf"^#{2,3}..." would be
    # evaluated as an f-string expression, producing '^#(2, 3)...' instead
    # of the intended regex quantifier '^#{2,3}...'.
    missing_headings = []
    for heading in REQUIRED_HEADINGS:
        pattern = _H2_H3_PREFIX + re.escape(heading)
        if not re.search(pattern, content_lower, re.MULTILINE):
            missing_headings.append(heading)
    assert not missing_headings, (
        f"Missing block headings (case-insensitive): {missing_headings}\n"
        "All 10 blocks must appear as H2 or H3 headings in the bundle."
    )

    # --- 5 principle anchors ---
    missing_anchors = []
    for anchor in REQUIRED_PRINCIPLE_ANCHORS:
        # each principle has its own H2/H3 heading
        if not re.search(_H2_H3_PREFIX + re.escape(anchor), content_lower, re.MULTILINE):
            missing_anchors.append(anchor)
    assert not missing_anchors, (
        f"Missing principle anchors: {missing_anchors}\n"
        "All 5 共通核心原則 anchors must appear as H2 or H3 headings in the bundle."
    )

    # --- good-example section heading present ---
    assert re.search(r"^#{2,3}\s+.*good example", content_lower, re.MULTILINE), (
        "Good-example block not found.\n"
        "The bundle must contain a section demonstrating correct HANDOFF."
    )

    # --- bad-example section heading present ---
    assert re.search(r"^#{2,3}\s+.*bad example", content_lower, re.MULTILINE), (
        "Bad-example block not found.\n"
        "The bundle must contain a section demonstrating HANDOFF failures."
    )

    # --- skill-independence: no cross-links to recap bundle ---
    cross_link_hits = [
        line.strip()
        for line in content.splitlines()
        if FORBIDDEN_CROSS_LINK in line
    ]
    assert not cross_link_hits, (
        f"Found {len(cross_link_hits)} cross-link(s) to recap skill:\n"
        + "\n".join(f"  {line}" for line in cross_link_hits)
        + "\nHandoff bundle must be self-contained (Anthropic skill-independence rule)."
    )


def test_resume_launcher_section_has_directive_and_example_headings() -> None:
    """
    v0.2.0 gate: the schema documents the Resume Launcher (init prompt) as a
    prepare-mode output, with a USER DIRECTIVE field, plus good/bad example
    headings.

    WHY: The launcher is the cross-session entry point. Drift here (dropping the
    thin / portable / no-stale-embeds constraints, or the USER DIRECTIVE field)
    would let prepare mode emit a context-re-dump blob that goes stale — the
    exact failure the bad example warns against.
    """
    content = _read_bundle()
    content_lower = content.lower()

    # --- Resume Launcher section heading present ---
    assert re.search(_H2_H3_PREFIX + re.escape("resume launcher"),
                     content_lower, re.MULTILINE), (
        "Resume Launcher section heading not found.\n"
        "§6 must document the init prompt prepare mode emits."
    )

    # --- USER DIRECTIVE field label present (the optional first-task slot) ---
    assert "USER DIRECTIVE" in content, (
        "'USER DIRECTIVE' field not found in the Resume Launcher spec.\n"
        "The launcher must end with a blank USER DIRECTIVE line."
    )

    # --- both good and bad launcher example headings present ---
    for kind in ("good", "bad"):
        assert re.search(r"^###\s+" + kind + r" example — resume launcher\s*$",
                         content_lower, re.MULTILINE), (
            f"{kind.title()} Resume Launcher example heading not found."
        )


def test_conversation_language_captured_in_frontmatter() -> None:
    """
    v0.3.0 language-preservation gate: the HANDOFF must capture the session's
    conversation language (Block 1 frontmatter). That the Resume Launcher tells
    the next session to reply in it is left to review.

    WHY: a cold resume has no warm context for which language the user was
    conversing in, so it defaults to English — dropping the user's
    conversation-language preference across the session boundary. Recording it in
    frontmatter (the record) and embedding a reply-in-that-language instruction in
    the launcher (the propagation channel, pasted as the new session's first
    message and working even without the skill installed) closes that gap.
    """
    content = _read_bundle()
    cl = content.lower()

    # --- Block 1 frontmatter captures the conversation language ---
    assert "conversation_language" in cl, (
        "'conversation_language' frontmatter field not found.\n"
        "Block 1 must record the language the agent has been replying in so a "
        "cold resume can continue in it instead of defaulting to English."
    )
