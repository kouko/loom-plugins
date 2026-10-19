"""
Structural tests for goal-shape.md reference.

Tests verify:
- The four field names appear, in order: Outcome, Constraints, Verification, Stop-when
- The 4,000-character budget and the 1,500 compression prompt are stated
- Both vendor URLs are cited, and the budget caveat and the labelled
  attribution paragraph name both vendors
- Stop-when is not claimed as a shared four-field vendor standard (absence)
- §2 carries the `derived` tag and the `Outcome` boundary; §4 points at
  `input-floor.md`

The prose wording of each section is left to review.

WHY: This reference is the SSOT for the four-field goal shape that the rest of
`loom-workflow:goal-create` routes to. Any drift in field names, the budget
number, or the surfacing requirement silently breaks every downstream skill
section that assumes this contract.
"""

import re
from pathlib import Path

REFERENCE_PATH = (
    Path(__file__).resolve().parents[2] / "skills" / "goal-create" / "references" / "goal-shape.md"
)

FIELD_NAMES_IN_ORDER = ["Outcome", "Constraints", "Verification", "Stop-when"]

VENDOR_URLS = [
    "https://code.claude.com/docs/en/goal",
    "https://learn.chatgpt.com/use-cases/follow-goals",
    "https://learn.chatgpt.com/docs/long-running-work",
]


def _read_reference() -> str:
    """Read the reference file; fail with a descriptive message if missing."""
    assert REFERENCE_PATH.exists(), (
        f"Reference file not found: {REFERENCE_PATH}\n"
        "This is expected at RED stage. Create the reference to make this test pass."
    )
    return REFERENCE_PATH.read_text(encoding="utf-8")


def test_defines_four_fields_and_budget() -> None:
    content = _read_reference()

    # --- four field names present, in order ---
    last_index = -1
    for field in FIELD_NAMES_IN_ORDER:
        idx = content.find(field)
        assert idx != -1, f"Field name '{field}' not found in reference."
        assert idx > last_index, (
            f"Field '{field}' must appear after the previous field — "
            "expected order: Outcome, Constraints, Verification, Stop-when."
        )
        last_index = idx

    # --- 4,000-character budget and the 1,500 compression prompt ---
    assert "4,000" in content or "4000" in content, (
        "The 4,000-character budget must be stated."
    )
    assert "1,500" in content

    # --- the budget's attribution caveat: the paragraph after the
    # "## The 4,000-character budget" heading's first paragraph names both
    # vendors. Its wording is left to review. ---
    budget_section_match = re.search(
        r"## The 4,000-character budget\n\n.*?\n\n(.*?)(?=\n---|\Z)",
        content,
        re.DOTALL,
    )
    assert budget_section_match, "Expected the budget section's second paragraph."
    caveat_para = re.sub(r"\s+", " ", budget_section_match.group(1)).strip().lower()
    assert "openai" in caveat_para and "anthropic" in caveat_para, (
        "The budget section must name both vendors when caveating the cap."
    )

    # --- vendor URLs cited ---
    missing_urls = [url for url in VENDOR_URLS if url not in content]
    assert not missing_urls, f"Missing vendor citation URL(s): {missing_urls}"

    # --- attribution accuracy: the labelled paragraph names the field names
    # and both vendors; its wording is left to review ---
    paragraphs_lower = [
        re.sub(r"\s+", " ", p).lower() for p in re.split(r"\n\s*\n", content)
    ]

    # Fact 1: which of the three field names each vendor actually uses.
    # OpenAI's long-running-work names all three; Anthropic's page names only
    # `Constraints`, and calls the other two "One measurable end state" and
    # "A stated check".
    #
    # Selected by the paragraph's own bold lead label, never by keyword
    # soup: the vendor citation bullets are a single paragraph that already
    # contains every vendor name and every field name,
    # so a keyword selector silently binds there instead and every assertion
    # that follows passes against the wrong text. That is not hypothetical --
    # an earlier revision of this block did exactly that and survived two
    # mutations that should have killed it.
    attribution = next(
        (p for p in paragraphs_lower if p.startswith("**attribution accuracy**")),
        None,
    )
    assert attribution, (
        "Must carry a paragraph led by **Attribution accuracy** stating "
        "which of the three field names each vendor actually uses."
    )
    for field in ("outcome", "constraints", "verification"):
        assert field in attribution, (
            f"The attribution paragraph must name {field!r}."
        )
    for vendor in ("anthropic", "openai"):
        assert vendor in attribution, (
            f"The attribution paragraph must name {vendor!r}."
        )
    assert not re.search(r"named by both|both vendors name", attribution), (
        "Must not attribute all three FIELD NAMES to both vendors: Anthropic "
        "names only `Constraints`."
    )

    # --- negative guard: must not claim both vendors require Stop-when as
    # shared/mandatory guidance. Matches "require"/"requires"/"mandatory" as
    # whole words only — "required" (as in "not a required field", the real
    # reference's own negation) must not false-trigger it. ---
    for p in paragraphs_lower:
        if "both" in p and "stop-when" in p and re.search(r"\b(requires?|mandatory)\b", p):
            raise AssertionError(
                "Must not claim both vendors require Stop-when as "
                "shared/mandatory guidance — Stop-when is this skill's own "
                f"addition. Offending paragraph: {p!r}"
            )


def _section_four(content: str) -> str:
    """Extract '## 4 — `Stop-when`' section's own text, heading-scoped.

    Bounded to the text between that heading and the next `---` rule (the
    "## The 4,000-character budget" section starts after it) — so an
    assertion below can only be satisfied by §4's own words, never by
    unrelated text living in §2 or the budget/attribution sections.
    """
    match = re.search(
        r"## 4 — `Stop-when`\n\n(.*?)(?=\n---|\Z)",
        content,
        re.DOTALL,
    )
    assert match, "Expected to find the '## 4 — `Stop-when`' section."
    return match.group(1)


def _section_two(content: str) -> str:
    """Extract '## 2 — `Constraints`' section's own text, heading-scoped.

    Bounded to the text between that heading and the next `## 3` heading (no
    `---` rule separates §2 from §3), so an assertion below can only be
    satisfied by §2's own words, never by unrelated text in §4, the budget
    section, or the attribution paragraph.
    """
    match = re.search(
        r"## 2 — `Constraints`\n\n(.*?)(?=\n## 3|\Z)",
        content,
        re.DOTALL,
    )
    assert match, "Expected to find the '## 2 — `Constraints`' section."
    return match.group(1)


def test_constraints_section_names_derived_tag_and_outcome() -> None:
    """§2 carries the `derived` provenance tag and names the `Outcome` field
    as the outer boundary; the standing decision rule's wording is left to
    review."""
    section_lower = _section_two(_read_reference()).lower()
    assert "`derived`" in section_lower, (
        "Must state the entry carries the `derived` provenance tag."
    )
    assert "`outcome`" in section_lower, (
        "Must name the `Outcome` field as the outward-facing boundary."
    )


def test_stop_when_section_points_at_input_floor() -> None:
    """§4 points at `input-floor.md` for the human-dependent fork; the bound
    and completion wording is left to review."""
    section_lower = _section_four(_read_reference()).lower()
    assert "`input-floor.md`" in section_lower, (
        "Must point at input-floor.md for where a human-dependent fork "
        "goes instead."
    )
