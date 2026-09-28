"""
Structural tests for goal-shape.md reference.

Tests verify:
- The four field names appear, in order: Outcome, Constraints, Verification, Stop-when
- Outcome is defined as one measurable end state, not a vision
- Verification names the goal evaluator
- Stop-when bounds the run (a turn-clause example)
- The 4,000-character budget is stated
- Both vendor URLs are cited
- Attribution is accurate: Stop-when is not claimed as a shared four-field
  vendor standard

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
    content_lower = content.lower()

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

    # --- Outcome: one measurable end state, not a vision ---
    assert "measurable" in content_lower, (
        "Outcome must be defined as one measurable end state."
    )
    assert "vision" in content_lower, (
        "Outcome must explicitly contrast with a vision (not a vision)."
    )

    # --- Verification: names the goal evaluator ---
    assert "goal evaluator" in content_lower, (
        "Verification's surfacing rule must name Claude Code's goal evaluator."
    )

    # --- Stop-when: bounds the run, e.g. a turn clause ---
    assert "turn" in content_lower, (
        "Stop-when must give a turn-clause example bounding the run."
    )

    # --- 4,000-character budget ---
    assert "4,000" in content or "4000" in content, (
        "The 4,000-character budget must be stated."
    )
    assert "character" in content_lower, (
        "The budget must be stated in characters."
    )

    # 1,500 is a compression prompt, never another validity boundary.
    assert "1,500" in content
    assert "advisory" in content_lower

    # --- the budget's own attribution caveat: only Anthropic documents
    # this cap; OpenAI does not. Structural: bound to the paragraph that
    # follows the "## The 4,000-character budget" heading's first
    # paragraph, so a mutant that drops or inverts the caveat fails here
    # rather than being rescued by unrelated text elsewhere in the file. ---
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
    # Positive-obligation check: OpenAI must be stated as documenting NO
    # length limit — bind "no" to "limit" within the caveat.
    assert re.search(r"\bno\b.*\blimit\b", caveat_para), (
        "Must state OpenAI's guidance documents no length limit — expected "
        "'no ... limit' within the caveat."
    )
    # Bound negation guard: a mutant that drops the "no limit" fact but
    # keeps both vendor names (e.g. claiming OpenAI documents the same
    # cap) must fail — require the caveat to also deny OpenAI documents
    # its own cap.
    assert re.search(r"\bnot\b.*\bopenai\b.*\bdocuments?\b", caveat_para), (
        "Must state the cap is applied for portability, NOT because "
        "OpenAI documents one — expected a negation bound to 'OpenAI "
        "documents' within the caveat."
    )

    # --- vendor URLs cited ---
    missing_urls = [url for url in VENDOR_URLS if url not in content]
    assert not missing_urls, f"Missing vendor citation URL(s): {missing_urls}"

    # --- attribution accuracy: positive checks on the actual facts, so that
    # reintroducing false vendor attribution in *different* wording fails
    # too, not just the one hardcoded phrase (see loom-code Rule 9) ---
    paragraphs_lower = [
        re.sub(r"\s+", " ", p).lower() for p in re.split(r"\n\s*\n", content)
    ]

    def _paragraph_containing(*keywords: str):
        for p in paragraphs_lower:
            if all(kw in p for kw in keywords):
                return p
        return None

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

    # Fact 2: Stop-when is first-class in OpenAI's guidance.
    assert _paragraph_containing("stop-when", "openai", "first-class"), (
        "Must state that Stop-when is first-class in OpenAI's guidance."
    )

    # Fact 3: Stop-when is only optional/suggested in Anthropic's guidance —
    # not a required field there.
    assert _paragraph_containing(
        "stop-when", "anthropic", "optional"
    ) or _paragraph_containing("stop-when", "anthropic", "suggested"), (
        "Must state that Stop-when is only optional/suggested in Anthropic's "
        "guidance, not a required field there."
    )

    # Fact 4: treating Stop-when as a required fourth field is this skill's
    # own choice, not something either vendor requires.
    assert _paragraph_containing("stop-when", "this skill", "own choice"), (
        "Must attribute Stop-when-as-required-fourth-field to this skill's "
        "own choice, not to either vendor's requirement."
    )

    # --- negative guard: must not claim both vendors require Stop-when as
    # shared/mandatory guidance. Matches "require"/"requires"/"mandatory" as
    # whole words only — "required" (as in "not a required field", the real
    # reference's own negation) must not false-trigger it. This block used
    # to also carry an exact-phrase sibling ("both vendors document four
    # fields" not in content_lower): its own comment already said it was
    # "kept as a cheap extra tripwire; the facts above are what actually
    # gates this" — it pinned one specific wording of the same inaccuracy
    # and nothing else, while Facts 2-4 above plus this regex guard gate
    # the real, wording-independent attribution-accuracy invariant in this
    # same test. Deleted per B1 hard rule 3.
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


def _negation_binds(text: str, negation: str, target: str, max_gap_words: int = 6) -> bool:
    """Bound negation-to-target polarity check (word-boundary safe on
    BOTH ends; the sanctioned copy it once mirrored lived in the deleted
    test_input_floor.py, so this is now the only copy).

    True iff a `negation` alternation sits within `max_gap_words` words
    directly BEFORE `target`. See
    docs/loom/memory/a-list-of-forbidden-words-is-defeated-by-the-word-outside-it.md
    — a bare `negation.*target` is satisfied by unrelated co-occurrence
    anywhere in the text; this keeps the match local to the clause the
    negation actually governs. Punctuation glued to the negation (`never,`)
    and markdown glued to the target (`` `Stop-when` ``) are tolerated; a
    trailing word boundary stops `ask` matching inside `asked`.
    """
    pattern = (
        r"\b(?:" + negation + r")\b"
        r"\W*"
        r"(?:\s+\S+){0," + str(max_gap_words) + r"}"
        r"\s+[`*_]*\b" + target + r"\b"
    )
    return re.search(pattern, text) is not None


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


def test_constraints_carries_the_standing_decision_rule() -> None:
    content = _read_reference()
    section_lower = _section_two(content).lower()

    # --- obligation 2: the run searches first, decides, and records
    # decision + candidates + sources in a named file ---
    for word in ("search", "decide", "record"):
        assert word in section_lower, (
            f"Must state the run must {word} as part of the sequence."
        )
    assert "candidate" in section_lower, (
        "Must state the record includes candidates considered."
    )
    assert "source" in section_lower, (
        "Must state the record includes sources."
    )
    assert re.search(r"named\s+file", section_lower), (
        "Must state the decision is recorded in a named file (the goal "
        "names the file)."
    )

    # --- obligation 3: the run never stops to ask — negation bound to the
    # asking itself, not to a stray nearby word (see
    # docs/loom/memory/a-list-of-forbidden-words-is-defeated-by-the-word-outside-it.md)
    # ---
    assert _negation_binds(section_lower, "never", r"(?:stops?\s+to\s+)?ask"), (
        "Must state the run never stops to ask, with the negation bound "
        "to the asking."
    )

    # --- obligation 4: the entry is tagged `derived` per input-floor.md §5 ---
    assert "derived" in section_lower, (
        "Must state the entry carries the `derived` provenance tag."
    )

    # --- obligation 5: what stays outside the run — an irreversible or
    # outward-facing act, where `Outcome` ends ---
    assert "irreversible" in section_lower and "outward-facing" in section_lower, (
        "Must name an irreversible or outward-facing act as staying "
        "outside the run."
    )
    assert re.search(r"merge|deploy|send", section_lower), (
        "Must give an example of an irreversible or outward-facing act "
        "(merge, deploy, send)."
    )
    assert "outcome" in section_lower, (
        "Must state that outward-facing boundary is where `Outcome` ends."
    )


def test_stop_when_is_one_bound_written_as_completion() -> None:
    content = _read_reference()
    section_lower = _section_four(content).lower()

    # --- count: exactly one bound (turn count or wall-clock limit) ---
    assert re.search(r"\bone\b", section_lower) and "bound" in section_lower, (
        "Stop-when must state exactly one bound."
    )

    # --- completion: reaching the bound with a status report posted in the
    # conversation counts as the run completing, as a failure report ---
    assert re.search(r"\breport\b(?:\s+\S+){0,10}\s+\bcomplet\w*", section_lower) or re.search(
        r"\bcomplet\w*(?:\s+\S+){0,10}\s+\breport\b", section_lower
    ), (
        "Stop-when must bind a status report posted to the run completing."
    )
    assert "failure report" in section_lower, (
        "Must state reaching the bound with a report posted counts as a "
        "failure report."
    )

    # --- why: a bare 'stop after N turns' is read by the evaluator as
    # permission to stop ---
    assert "permission" in section_lower, (
        "Must state the evaluator reads a bare stop clause as permission "
        "to stop."
    )

    # --- forks: a human-dependent fork is never a Stop-when branch — pointer
    # to input-floor.md §4 item 3 (same term "branch" as that item uses) ---
    assert _negation_binds(section_lower, "never|not", r"a\s+`?stop-when`?\s+branch"), (
        "Must state a human-dependent fork is never a Stop-when branch, "
        "negation bound to 'a Stop-when branch'."
    )
    assert "human" in section_lower, (
        "Must name the human-dependent fork explicitly."
    )
    assert "input-floor" in section_lower, (
        "Must point at input-floor.md for where a human-dependent fork "
        "goes instead."
    )

    # --- example: one canonical example, still containing 'turn' (existing
    # pin: "turn" in content_lower must keep holding) ---
    assert "turn" in section_lower, (
        "Stop-when's example must contain 'turn' (existing whole-file pin)."
    )
