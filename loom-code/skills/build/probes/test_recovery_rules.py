"""Probes for the Build absence-recovery rule (change 2026-09-19-loom-flow-recovery-loop).

A1 positive: RL-01 — the recovery rule is present in build/SKILL.md.
A1 negative: RL-02 — the recovery paragraph carries no second copy of the
             artifact-to-station mapping; it cites the contract manifest. The
             scan covers the whole recovery passage (this paragraph through
             the bound paragraph and the adversary-update paragraph, up to
             "## 4."), not one paragraph found by a substring match, and
             reads inside code spans once known citations are neutralized —
             a second copy placed in the next paragraph, or hidden in
             backticks, is still a second copy.
A2 positive: RL-09 — Build carries the cross-station bound, as a pointer to the
             station that states it rather than a count of its own, and only
             an entry made to resolve an absent item counts toward it, never
             an ordinary review-round fix entry.
A1 positive: RL-11 — a Build entry with no task to implement is directed to §3,
             stated before the point where such a run would exit.
A1 negative: RL-12 — that early pointer is a pointer, not a second copy of the
             §3 absence rule, and §3 still states the rule exactly once.
A1 positive: RL-13 — a recovered run names the station sequence entered so
             far in Build's hand-off to closing-review.
A3 positive: RL-14 — the manifest lookup is bounded to the three items this
             change's Acceptance #1 names, not left open over the whole
             manifest.

RL-01 and RL-09 also pin the paragraph's exact closing sentence and, where
the pinned sentence is itself affirmative, its polarity: a probe that only
asserts phrase containment is satisfied by a paragraph with a trailing
sentence appended that reverses the rule, because containment has no
polarity and does not see past the paragraph it was told to open (see
docs/loom/memory/a-prose-pin-must-require-an-affirmative-un-negated-sentence.md
and docs/loom/memory/an-assertion-scoped-wider-than-its-clause-is-about-something-else.md).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

from prose_pin import has_negation, split_sentences  # noqa: E402

SKILL = "loom-code/skills/build/SKILL.md"

# Each rule lives in one paragraph, identified by its opening words.
PARAGRAPH_OPENER = "Build enters these end-of-Build checks on absence"
BOUND_OPENER = "A recovery run is bounded across stations"

# Headings that bound the early sections a no-task run reads before it exits,
# and the heading that closes the recovery passage RL-02 scans.
SCOPE_HEADING = "## 1. Establish scope"
VERIFY_HEADING = "## 3. Verify integration"
HANDOFF_HEADING = "## 4. Hand off to closing-review"

# The exact closing sentence of each rule's paragraph, as committed. An
# appended trailing sentence — ADV-02's attack — changes what the paragraph
# ends with even though it removes nothing, so the ending is pinned exactly
# rather than merely required to be present somewhere in the paragraph.
RL_01_ENDING = "committed programs are re-run, never re-dispatched, exactly as after a fix."
RL_09_ENDING = "this file keeps no count of its own."

# The exact sentence REQ-1's bounded lookup adds (finding ADV-04): the
# manifest lookup this rule runs is not open over every manifest key, only
# over the three items Acceptance #1 names.
BOUNDED_LOOKUP_SENTENCE = (
    "This lookup covers only an item this rule names: the adversarial "
    "programs, the acceptance test report or the attestation."
)

# The exact phrase Build's §4 hand-off must carry (finding ADV-05): the
# station sequence a recovery entered, named at the point this rule already
# requires a report.
HANDOFF_SEQUENCE_PHRASE = (
    "the station sequence entered so far when this run recovered from an "
    "absent item"
)

# Artifact nouns a restatement of the mapping would have to name. A second copy
# phrased purely in artifact nouns — "the acceptance test report is produced
# downstream" — names no station and so slips past a station-name check.
ARTIFACT_NOUNS = re.compile(
    r"(?<![\w-])(?:intents?|specs?|plans?|diffs?|attestations?"
    r"|acceptance[- ]test reports?|adversarial programs?)(?![\w-])",
    re.IGNORECASE,
)

# Words that turn an artifact noun into a claim about who produces or owns it.
PRODUCER_PHRASES = re.compile(
    r"(?<![\w-])(?:produce[ds]?|produces|producing|producer"
    r"|owns|owned|owner|owes|upstream|downstream"
    r"|comes from|belongs to|responsible for)(?![\w-])",
    re.IGNORECASE,
)

# A station reference, not any occurrence of a station name as a substring
# ("relationship", "maintains" and "ships" are ordinary English words in this
# prose, not references to closing-review, Maintain or Ship). Excludes
# "build" — this file's own station naming itself is not a restatement of
# the artifact-to-station mapping. Kept identical in wording and structure to
# closing-review's STATION_REFERENCE
# (loom-code/skills/closing-review/probes/test_recovery_rules.py) so the two
# do not drift apart (docs/loom/memory/absence-pin-fix-recurred-in-files-authored-after-the-fix.md):
# if this pattern ever needs to change, change both copies together.
STATION_REFERENCE = re.compile(
    r"(?<![\w-])(?:capture-intent|write-spec|write-plan|closing-review)(?![\w-])"
    r"|(?<![\w-])(?:Ship|Maintain)(?![\w-])"
)

# Code-span content that cites the manifest rather than restating who
# produces what. Only these exact citations are neutralized before a
# restatement scan; anything else inside backticks is still read as prose,
# because a mapping hidden in backticks is still a second copy of it.
LEGITIMATE_CITATIONS = [
    "loom-code/contract/manifest.yaml",
    "stations[].produces",
    "actions[].owner",
    "charter.signoff",
]


def _read():
    with open(SKILL, "r", encoding="utf-8") as f:
        return f.read()


def _normalize(text):
    """Collapse whitespace so these probes test wording, not line wrapping."""
    return " ".join(text.split())


def _paragraph(opener):
    """Return the normalized paragraph carrying these words, or None."""
    for para in _read().split("\n\n"):
        normalized = _normalize(para)
        if opener in normalized:
            return normalized
    return None


def _require(probe, opener, phrases):
    para = _paragraph(opener)
    if para is None:
        print(f"{probe} FAIL: no paragraph containing {opener!r} in {SKILL}")
        sys.exit(1)
    missing = [phrase for phrase in phrases if phrase not in para]
    if missing:
        print(f"{probe} FAIL: paragraph {opener!r} is missing {missing}")
        sys.exit(1)
    return para


def _last_fragment(text):
    """The final sentence of `text`, the seam where ADV-02 appended text."""
    fragments = split_sentences(text)
    return fragments[-1].strip() if fragments else ""


def _early_sections():
    """Return §1 and §2 — everything a no-task run reads before it would exit."""
    content = _read()
    start = content.index(SCOPE_HEADING)
    end = content.index(VERIFY_HEADING)
    return _normalize(content[start:end])


def _recovery_passage():
    """The full run of paragraphs stating the absence-recovery rule and the
    paragraphs that continue it — from its opening paragraph through the
    next heading. A second copy of the mapping one paragraph over (ADV-01)
    is still inside this passage even though it is outside the one paragraph
    a substring match on the opener would find."""
    content = _read()
    start = content.index(PARAGRAPH_OPENER)
    end = content.index(HANDOFF_HEADING, start)
    return _normalize(content[start:end])


def _despan_for_scan(text):
    """Neutralize the known manifest citations, then unwrap any remaining
    code span into plain prose. A citation like `stations[].produces` is not
    a restatement; a mapping hidden in backticks (ADV-09) is, and blanket
    code-span stripping would hide it from the scan below."""
    for citation in LEGITIMATE_CITATIONS:
        text = text.replace(f"`{citation}`", " ")
    return re.sub(r"`([^`]*)`", r" \1 ", text)


def _mapping_restatements(text):
    """Sentences that pair an artifact noun with a claim about its producer —
    either a producer phrase ("produced by") or another station's name."""
    prose = _despan_for_scan(text)
    offenders = []
    for sentence in split_sentences(prose):
        has_artifact = ARTIFACT_NOUNS.search(sentence)
        has_claim = PRODUCER_PHRASES.search(sentence) or STATION_REFERENCE.search(sentence)
        if has_artifact and has_claim:
            offenders.append(sentence.strip())
    return offenders


def test_RL_01_absence_re_enters_end_of_build_checks():
    """Absence is an antecedent for re-running the end-of-Build checks."""
    para = _require(
        "RL-01",
        PARAGRAPH_OPENER,
        [
            # absence, not a fix or a widening, is the antecedent
            "every planned task already committed",
            "is absent",
            # absence is kept distinct from failure
            "distinct antecedent from a failing check",
            # the adversary is not re-dispatched merely because Build re-enters
            "re-run, never re-dispatched",
        ],
    )

    # Polarity: the sentence stating the item is absent must itself be
    # affirmative, not wrapped in a negation that reverses it.
    absent_sentence = next(s for s in split_sentences(para) if "is absent" in s)
    if has_negation(absent_sentence):
        print(f"RL-01 FAIL: the sentence stating the item is absent is negated: {absent_sentence!r}")
        sys.exit(1)

    # Scope: the paragraph must end exactly where the committed rule ends.
    # ADV-02 left every required phrase in place and appended a trailing
    # sentence that permitted skipping recovery under time pressure; that
    # sentence changes what the paragraph ends with even though every
    # `_require` phrase above still matches.
    ending = _last_fragment(para)
    if ending != RL_01_ENDING:
        print(f"RL-01 FAIL: the paragraph's closing sentence changed; ends with {ending!r}")
        sys.exit(1)
    print("RL-01 PASS: absence re-enters the end-of-Build checks")


def test_RL_02_no_second_copy_of_the_artifact_station_mapping():
    """No paragraph in the recovery passage restates the mapping, whether by
    naming a station, by artifact nouns alone, or hidden in a code span."""
    para = _paragraph(PARAGRAPH_OPENER)
    if para is None:
        print(f"RL-02 FAIL: no paragraph containing {PARAGRAPH_OPENER!r} in {SKILL}")
        sys.exit(1)

    for citation in ("loom-code/contract/manifest.yaml", "stations[].produces", "actions[].owner"):
        if citation not in para:
            print(f"RL-02 FAIL: recovery paragraph does not cite {citation}")
            sys.exit(1)

    # Scan the whole recovery passage, not the one paragraph the opener
    # matches: ADV-01 placed a second copy in the very next paragraph, and
    # ADV-09 placed one inside backticks in this paragraph.
    offenders = _mapping_restatements(_recovery_passage())
    if offenders:
        print(f"RL-02 FAIL: the recovery passage states who produces an artifact: {offenders}")
        sys.exit(1)
    print("RL-02 PASS: the producing station is read from the manifest, not restated, anywhere in the recovery passage")


def test_RL_09_build_carries_the_cross_station_bound():
    """Build, the station the 2026-09-19 cycle kept re-entering, reads that a
    recovery run is bounded — by pointer, never by a count of its own."""
    para = _require(
        "RL-09",
        BOUND_OPENER,
        [
            # an entry here is part of the bounded sequence
            "counts toward",
            # only an absence-triggered entry counts (reviewer-skill Round 2
            # finding: an ordinary review-round fix entry must not conflate
            # with the recovery bound)
            "made to resolve an absent item counts toward that bound",
            "an entry made for an ordinary review-round fix never does",
            # where the single statement of the bound lives
            "closing-review",
            # and the record the bound is counted from
            "record of entered stations",
        ],
    )
    # A pointer, not a second copy: the count itself is stated in one place.
    if "more than twice" in para:
        print("RL-09 FAIL: the bound paragraph restates the count instead of pointing at it")
        sys.exit(1)

    # Polarity: "counts toward" is a literal substring of "does not count
    # toward", so containment alone is satisfied by the negated rewrite.
    # The enclosing sentence legitimately contains "not only" (from "not
    # only within Build") before the colon, so a naive whole-sentence
    # has_negation call would false-positive on the committed, correct
    # text; splitting on the colon too isolates the clause after it — the
    # one that actually states "counts toward" — as its own unit.
    counts_clause = next(
        (c for c in split_sentences(para, ends=".:;") if "counts toward" in c),
        None,
    )
    if counts_clause is None:
        print("RL-09 FAIL: no clause found containing 'counts toward'")
        sys.exit(1)
    if has_negation(counts_clause):
        print(f"RL-09 FAIL: the 'counts toward' clause is negated: {counts_clause!r}")
        sys.exit(1)

    ending = _last_fragment(para)
    if ending != RL_09_ENDING:
        print(f"RL-09 FAIL: the paragraph's closing sentence changed; ends with {ending!r}")
        sys.exit(1)
    print("RL-09 PASS: Build points at the cross-station bound without copying it")


def test_RL_11_no_task_to_implement_is_directed_to_section_3():
    """A run that finds nothing to implement is told, before it would exit, that
    Build does not end there and that §3 still runs."""
    early = _early_sections()

    required = [
        # the condition the 2026-09-19 run was in
        "no task left to implement",
        # the wrong conclusion, refused
        "not a reason to end Build",
        # where the run is sent instead
        "§3",
    ]
    missing = [phrase for phrase in required if phrase not in early]
    if missing:
        print(f"RL-11 FAIL: §1–§2 of {SKILL} do not state {missing}")
        sys.exit(1)
    print("RL-11 PASS: a no-task entry is directed to §3 before it would exit")


def test_RL_12_the_pointer_is_not_a_second_copy_of_the_rule():
    """The early pointer points; it does not restate §3's absence rule, and §3
    states that rule exactly once, nor does it name another station."""
    content = _read()
    early = _early_sections()

    if content.count(PARAGRAPH_OPENER) != 1:
        print(f"RL-12 FAIL: the absence rule opener appears "
              f"{content.count(PARAGRAPH_OPENER)} times in {SKILL}, expected 1")
        sys.exit(1)

    # Operative content of §3's rule: if any of it is repeated early, the two
    # statements can drift apart when §3 is edited.
    operative = [
        "distinct antecedent",
        "re-run, never re-dispatched",
        "runs this section from step 1",
        "loom-code/contract/manifest.yaml",
        "stations[].produces",
        "actions[].owner",
    ]
    duplicated = [phrase for phrase in operative if phrase in early]
    if duplicated:
        print(f"RL-12 FAIL: §1–§2 restate §3's absence rule: {duplicated}")
        sys.exit(1)

    # A pointer that names another station would also be a second copy of the
    # artifact-to-station mapping, which RL-02 and closing-review's RL-04
    # forbid. Word-boundary matched, not substring: "ships" and "maintains"
    # are ordinary English words here, not station references.
    restated = sorted(set(STATION_REFERENCE.findall(_despan_for_scan(early))))
    if restated:
        print(f"RL-12 FAIL: §1–§2 name other stations: {restated}")
        sys.exit(1)
    print("RL-12 PASS: the early pointer points at §3 without restating it")


def test_RL_13_recovered_run_names_the_sequence_in_the_handoff():
    """Acceptance #2's sequence is named at the point this rule already
    requires a report: Build's hand-off to closing-review, the station that
    receives the recovered content on the successful-continuation path."""
    content = _read()
    handoff = _normalize(content.split(HANDOFF_HEADING, 1)[-1])
    if HANDOFF_SEQUENCE_PHRASE not in handoff:
        print(f"RL-13 FAIL: the §4 hand-off does not name the station sequence: missing {HANDOFF_SEQUENCE_PHRASE!r}")
        sys.exit(1)
    print("RL-13 PASS: Build's hand-off names the station sequence entered so far")


def test_RL_14_lookup_is_bounded_to_the_three_recovery_items():
    """The manifest lookup this rule runs is bounded to the three items
    Acceptance #1 names, not left open over every manifest key (ADV-04 found
    two of eight candidate keys resolve to two stations with no tie-break)."""
    para = _require("RL-14", PARAGRAPH_OPENER, [BOUNDED_LOOKUP_SENTENCE])
    del para
    print("RL-14 PASS: the lookup is bounded to the three recovery items REQ-1 names")


def test_self_check_negation_discriminates():
    """Self-test for the shared negation guard (prose_pin.has_negation) used
    by RL-01: it accepts the real affirmative sentence and rejects a rewrite
    of it that keeps the same key words but reverses the meaning — the shape
    of ADV-02's attack, applied here in place rather than as a trailing
    append, to prove the guard discriminates rather than just asserting it
    does."""
    affirmative = (
        "when Build is entered with every planned task already committed and "
        "an item Build owes is absent, it runs this section from step 1 to "
        "produce that item"
    )
    negated = (
        "when Build is entered with every planned task already committed and "
        "an item Build owes is absent, it does not run this section from "
        "step 1 to produce that item"
    )
    if has_negation(affirmative):
        print(f"SELF-TEST FAIL: the real RL-01 sentence was flagged as negated: {affirmative!r}")
        sys.exit(1)
    if not has_negation(negated):
        print(f"SELF-TEST FAIL: a negated rewrite of it was not caught: {negated!r}")
        sys.exit(1)
    print("SELF-TEST PASS: the negation guard accepts the affirmative sentence and rejects its negation")


if __name__ == "__main__":
    test_self_check_negation_discriminates()
    test_RL_01_absence_re_enters_end_of_build_checks()
    test_RL_02_no_second_copy_of_the_artifact_station_mapping()
    test_RL_09_build_carries_the_cross_station_bound()
    test_RL_11_no_task_to_implement_is_directed_to_section_3()
    test_RL_12_the_pointer_is_not_a_second_copy_of_the_rule()
    test_RL_13_recovered_run_names_the_sequence_in_the_handoff()
    test_RL_14_lookup_is_bounded_to_the_three_recovery_items()
    print("All probes passed.")
