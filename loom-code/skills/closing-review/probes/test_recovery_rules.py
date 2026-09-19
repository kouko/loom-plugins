"""Probes for the closing-review absence-recovery rules (change 2026-09-19-loom-flow-recovery-loop).

A3 positive: RL-03 — absence is a distinct antecedent and the producing
             station is looked up in the contract manifest.
A3 negative: RL-04 — the lookup paragraph carries no second copy of the
             artifact-to-station mapping. The scan covers the whole recovery
             passage (the lookup paragraph through the decision and failure
             paragraphs, up to the next unrelated paragraph), not one
             paragraph found by a substring match, and reads inside code
             spans once known citations are neutralized — a second copy
             placed in the next paragraph, or hidden in backticks, is still
             a second copy.
A4 positive: RL-05 — an unanswered decision point stops the run and asks.
A4 boundary: RL-06 — an answered decision, including a general delegation,
             proceeds as user-decided, and the skip confirmation is untouched.
A5 positive: RL-07 — a failed recovery stops and says what happened.
A5 negative: RL-08 — a failed recovery neither retries nor hands on.
A2 boundary: RL-10 — the station sequence is recorded, a second entry is the
             last one allowed, and a third is a failed recovery.
A2 positive: RL-12 — the recorded sequence is named at both stops and at the
             hand-off to another station, not only promised in the abstract.
A1 positive: RL-11 — a blind run is always dispatched fresh-context to an
             agent that never touched the change, including when the absence
             route produces it here.
A3 positive: RL-13 — the manifest lookup is bounded to the three items this
             change's Acceptance #1 names, not left open over the whole
             manifest.
A2 boundary: RL-15 — the station-entry bound counts only entries made to
             resolve an absent item under this rule; it is independent of,
             and never incremented by, §4's ordinary round-and-digest
             progression, so an unrelated healthy Round 2/3 review bounce
             never trips it.

RL-03, RL-05, RL-06, RL-07, RL-08 and RL-10 also pin the paragraph's exact
closing sentence and, where the pinned sentence is itself affirmative, its
polarity: a probe that only asserts phrase containment is satisfied by a
paragraph with a trailing sentence appended that reverses the rule, because
containment has no polarity and does not see past the paragraph it was told
to open (see
docs/loom/memory/a-prose-pin-must-require-an-affirmative-un-negated-sentence.md
and docs/loom/memory/an-assertion-scoped-wider-than-its-clause-is-about-something-else.md).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

from prose_pin import has_negation, split_sentences  # noqa: E402

SKILL = "loom-code/skills/closing-review/SKILL.md"

# Each rule lives in one paragraph, identified by its opening words.
LOOKUP_OPENER = "Absence is a distinct antecedent from a failing check."
DECISION_OPENER = "Stop and ask when producing an absent item needs"
FAILURE_OPENER = "Stop when the attempt to produce an absent item fails."

# The paragraph immediately after the recovery passage: a different topic
# (announcing the blind run to reviewers), the natural stopping point for a
# scan of "the paragraphs that state the same rule" (ADV-01's near miss).
NEXT_UNRELATED = "When a blind run is needed, finish it and commit its report"

# The exact closing sentence of each rule's paragraph, as committed. An
# appended trailing sentence — ADV-02's attack — changes what the paragraph
# ends with even though it removes nothing, so the ending is pinned exactly
# rather than merely required to be present somewhere in the paragraph.
RL_03_10_ENDING = (
    "The run enters no station more than twice, a count that tracks only "
    "entries made to resolve an absent item under this rule and is never "
    "incremented by §4's ordinary round-and-digest progression."
)

# The exact clause distinguishing this count from §4's Round 1/2/3
# progression (reviewer-skill Round 2 finding): read literally without it,
# an ordinary Round 2 fix-and-reverify bounce — re-entering Build, then
# closing-review — could be misread as two of the three station entries this
# rule bounds, with no absent item ever involved.
RL_15_INDEPENDENCE_CLAUSE = (
    "a count that tracks only entries made to resolve an absent item under "
    "this rule and is never incremented by §4's ordinary "
    "round-and-digest progression"
)
RL_06_ENDING = (
    "a user-requested skip is still confirmed exactly as "
    "[expert-mode](../expert-mode/SKILL.md) requires."
)
RL_08_ENDING = "Do not attempt that item a second time and do not hand the change on to another station."

# The exact sentence REQ-1's bounded lookup adds (finding ADV-04): the
# manifest lookup this rule runs is not open over every manifest key, only
# over the three items Acceptance #1 names.
BOUNDED_LOOKUP_SENTENCE = (
    "This lookup covers only an item this rule names: the adversarial "
    "programs, the blind-run report or the attestation."
)

# The exact phrases naming the recorded sequence at the points this rule
# already requires a report or a hand-off (finding ADV-05).
DECISION_SEQUENCE_PHRASE = "naming the station sequence entered so far"
FAILURE_SEQUENCE_PHRASE = "Also report the station sequence entered so far."
RETURN_SEQUENCE_PHRASE = "return the change there, naming the station sequence entered so far"

# The guardrails a blind run must carry in its own home section (finding
# ADV-07): the agent, and that it never touched the change.
BLIND_RUNNER_AGENT = "loom-code:blind-runner"
BLIND_RUNNER_INDEPENDENCE = "never an agent that touched any part of the change"
BLIND_RUNNER_ROUTE_PHRASE = "for a blind-run report specifically, that means following §3"

# A station reference, not any occurrence of a station name as a substring.
# `build` and `ship` are ordinary English words here ("the build", "rebuild",
# "we ship"); this prose names those stations capitalized, so only the
# capitalized word is a reference to them.
STATION_REFERENCE = re.compile(
    r"(?<![\w-])(?:capture-intent|write-spec|write-plan|closing-review)(?![\w-])"
    r"|(?<![\w-])(?:Build|Ship|Maintain)(?![\w-])"
)

# Artifact nouns a restatement of the mapping would have to name. A second copy
# phrased purely in artifact nouns — "the blind-run report is produced
# downstream" — names no station and so slips past the check above.
ARTIFACT_NOUNS = re.compile(
    r"(?<![\w-])(?:intents?|specs?|plans?|diffs?|attestations?"
    r"|blind[- ]run reports?|adversarial programs?)(?![\w-])",
    re.IGNORECASE,
)

# Words that turn an artifact noun into a claim about who produces or owns it.
PRODUCER_PHRASES = re.compile(
    r"(?<![\w-])(?:produce[ds]?|produces|producing|producer"
    r"|owns|owned|owner|owes|upstream|downstream"
    r"|comes from|belongs to|responsible for)(?![\w-])",
    re.IGNORECASE,
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


def _clause_containing(text, phrase):
    """The smallest comma/semicolon/period-delimited clause of `text` that
    contains `phrase`, for a negation guard on one clause of a multi-clause
    sentence. Whole-sentence granularity is too coarse here: the sentence
    carrying "return the change there" also carries "dispatch no reviewer"
    later in the same sentence, so a whole-sentence has_negation call is
    tripped by that unrelated "no" and would flag the committed, correct
    text. Splitting on commas too isolates each clause from its neighbors."""
    for clause in split_sentences(text, ends=".;,"):
        if phrase in clause:
            return clause
    return None


def _recovery_passage():
    """The full run of paragraphs stating the absence-recovery rule — the
    lookup paragraph through the decision and failure paragraphs — stopping
    at the next unrelated paragraph. A second copy of the mapping one
    paragraph over (ADV-01) is still inside this passage even though it is
    outside the one paragraph a substring match on the opener would find."""
    content = _read()
    start = content.index(LOOKUP_OPENER)
    end = content.index(NEXT_UNRELATED, start)
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


def test_RL_03_absence_is_distinct_and_the_producer_is_looked_up():
    """Absence routes by a manifest lookup, not as a failing check."""
    para = _require(
        "RL-03",
        LOOKUP_OPENER,
        [
            # the re-entry state, not a failing check
            "every planned task already committed",
            "is absent",
            # the lookup, cited rather than restated
            "loom-code/contract/manifest.yaml",
            "stations[].produces",
            "actions[].owner",
            # the field that would route a missing blind-run report wrongly
            "charter.signoff",
            # both outcomes of the lookup
            "produce the item here",
            "return the change there",
            # no gate is waived, and the run is bounded (REQ-2)
            "no station more than twice",
        ],
    )

    # Polarity: the sentence stating the item is absent must itself be
    # affirmative, not wrapped in a negation that reverses it.
    absent_sentence = next(s for s in split_sentences(para) if "is absent" in s)
    if has_negation(absent_sentence):
        print(f"RL-03 FAIL: the sentence stating the item is absent is negated: {absent_sentence!r}")
        sys.exit(1)

    # Polarity of each outcome clause: "produce the item here" is a literal
    # substring of "do not produce the item here", and likewise for "return
    # the change there", so containment alone is satisfied by the negated
    # rewrite. Each clause is guarded on its own, at clause granularity, so
    # neither trips on an unrelated negation word in a neighboring clause
    # of the same sentence (e.g. "dispatch no reviewer" further along the
    # "return the change there" sentence).
    for outcome_phrase in ("produce the item here", "return the change there"):
        clause = _clause_containing(para, outcome_phrase)
        if clause is None:
            print(f"RL-03 FAIL: no clause found containing {outcome_phrase!r}")
            sys.exit(1)
        if has_negation(clause):
            print(f"RL-03 FAIL: the clause containing {outcome_phrase!r} is negated: {clause!r}")
            sys.exit(1)

    # Scope: the paragraph must end exactly where the committed rule ends.
    ending = _last_fragment(para)
    if ending != RL_03_10_ENDING:
        print(f"RL-03 FAIL: the paragraph's closing sentence changed; ends with {ending!r}")
        sys.exit(1)
    print("RL-03 PASS: absence is distinct and the producer comes from the manifest")


def test_RL_04_no_second_copy_of_the_artifact_station_mapping():
    """No paragraph in the recovery passage restates the mapping, whether by
    naming a station, by artifact nouns alone, or hidden in a code span."""
    para = _paragraph(LOOKUP_OPENER)
    if para is None:
        print(f"RL-04 FAIL: no paragraph containing {LOOKUP_OPENER!r} in {SKILL}")
        sys.exit(1)

    # Scan the whole recovery passage, not the one paragraph the opener
    # matches: ADV-01 placed a second copy in the very next paragraph, and
    # ADV-09 placed one inside backticks in this paragraph.
    offenders = _mapping_restatements(_recovery_passage())
    if offenders:
        print(f"RL-04 FAIL: the recovery passage states who produces an artifact: {offenders}")
        sys.exit(1)
    print("RL-04 PASS: the recovery passage carries no second copy of the mapping")


def test_RL_05_unanswered_decision_stops_and_asks():
    """An unanswered decision point for this change stops the run."""
    _require(
        "RL-05",
        DECISION_OPENER,
        ["decision point the user has not answered for this change"],
    )
    print("RL-05 PASS: an unanswered decision stops the run and asks")


def test_RL_06_answered_decision_proceeds_and_the_skip_rule_is_untouched():
    """An answered decision, delegation included, proceeds as user-decided."""
    para = _require(
        "RL-06",
        DECISION_OPENER,
        [
            "has answered it",
            "you decide",
            "user-decided",
            # scope: this governs asking again, not how a skip is confirmed
            "whether the run asks again",
            "expert-mode",
        ],
    )
    # "proceed" is a literal substring of "do not proceed", so containment
    # alone is satisfied by the negated rewrite. Isolate the clause carrying
    # it and guard its polarity directly.
    proceed_clause = _clause_containing(para, "proceed")
    if proceed_clause is None:
        print("RL-06 FAIL: the answered branch does not proceed")
        sys.exit(1)
    if has_negation(proceed_clause):
        print(f"RL-06 FAIL: the proceed clause is negated: {proceed_clause!r}")
        sys.exit(1)

    ending = _last_fragment(para)
    if ending != RL_06_ENDING:
        print(f"RL-06 FAIL: the paragraph's closing sentence changed; ends with {ending!r}")
        sys.exit(1)
    print("RL-06 PASS: an answered decision proceeds; the skip confirmation is untouched")


def test_RL_07_failed_recovery_stops_and_reports():
    """A failed recovery reports the item, the attempt and the failure point."""
    _require(
        "RL-07",
        FAILURE_OPENER,
        ["which item is absent", "what was attempted", "where it failed"],
    )
    print("RL-07 PASS: a failed recovery stops and says what happened")


def test_RL_08_failed_recovery_neither_retries_nor_hands_on():
    """A failed recovery is terminal for that item."""
    para = _require(
        "RL-08",
        FAILURE_OPENER,
        ["second time", "another station"],
    )

    ending = _last_fragment(para)
    if ending != RL_08_ENDING:
        print(f"RL-08 FAIL: the paragraph's closing sentence changed; ends with {ending!r}")
        sys.exit(1)
    print("RL-08 PASS: a failed recovery neither retries nor hands on")


def test_RL_10_the_sequence_is_recorded_and_the_second_entry_is_the_last():
    """Acceptance 2 has two halves, and the boundary sits between them: the run
    keeps a record of the stations it entered, a second entry to a station is
    still allowed, and a third is not."""
    para = _require(
        "RL-10",
        LOOKUP_OPENER,
        [
            # the sequence is recorded, in order, and where
            "list in entry order",
            "active task context",
            # the boundary: the last allowed entry...
            "second entry to a station is the last one allowed",
            # ...and the first disallowed one, with its consequence
            "third entry to any station",
            # the bound itself, stated once
            "no station more than twice",
        ],
    )

    ending = _last_fragment(para)
    if ending != RL_03_10_ENDING:
        print(f"RL-10 FAIL: the paragraph's closing sentence changed; ends with {ending!r}")
        sys.exit(1)
    print("RL-10 PASS: the sequence is recorded and the second entry is the last allowed")


def test_RL_12_the_recorded_sequence_surfaces_at_both_stops_and_the_hand_off():
    """RL-10's pointer promises the recorded list is named 'in the handoff and
    in either stop below'; a blind runner can only settle that promise by
    reading it named at the three concrete sites, not by reading the
    promise itself (ADV-05: the sequence Acceptance #2 asks to be recorded
    was nowhere a clean-tree reader could actually find it)."""
    return_para = _paragraph(LOOKUP_OPENER)
    if RETURN_SEQUENCE_PHRASE not in return_para:
        print(f"RL-12 FAIL: the return-to-another-station branch does not name the sequence: missing {RETURN_SEQUENCE_PHRASE!r}")
        sys.exit(1)

    decision_para = _paragraph(DECISION_OPENER)
    if DECISION_SEQUENCE_PHRASE not in decision_para:
        print(f"RL-12 FAIL: the unanswered-decision stop does not name the sequence: missing {DECISION_SEQUENCE_PHRASE!r}")
        sys.exit(1)

    failure_para = _paragraph(FAILURE_OPENER)
    if FAILURE_SEQUENCE_PHRASE not in failure_para:
        print(f"RL-12 FAIL: the failed-recovery report does not name the sequence: missing {FAILURE_SEQUENCE_PHRASE!r}")
        sys.exit(1)

    print("RL-12 PASS: the recorded sequence is named at the return, both stops")


def test_RL_15_recovery_count_is_independent_of_ordinary_review_rounds():
    """The station-entry bound counts only entries made to resolve an absent
    item under this rule. Read literally without this clause, an ordinary,
    healthy Round 2 fix-and-reverify bounce (re-entering Build, then
    closing-review — §4) has nothing to do with an absent item, yet could be
    misread as counting toward 'a third entry to any station is a recovery
    that has failed', incorrectly aborting a healthy review episode."""
    para = _require("RL-15", LOOKUP_OPENER, [RL_15_INDEPENDENCE_CLAUSE])

    ending = _last_fragment(para)
    if ending != RL_03_10_ENDING:
        print(f"RL-15 FAIL: the paragraph's closing sentence changed; ends with {ending!r}")
        sys.exit(1)
    print("RL-15 PASS: the recovery-entry bound is independent of §4's ordinary round progression")


def test_RL_11_blind_run_independence_is_stated_in_its_own_section():
    """The blind run's writer-never-judge constraint lives in this station's
    own §3, not only in the blind-runner agent definition and the manifest's
    action summary (ADV-07: the absence route's 'produce the item here' is
    newly reachable by an agent that has just been implementing, and nothing
    in this file told it to dispatch fresh-context instead of writing the
    report itself)."""
    content = _read()
    section3 = _normalize(content.split("## 3. Run the blind run", 1)[-1].split("## 4.", 1)[0])

    blind_sentences = [
        s for s in re.split(r"(?<=[.;])\s+", section3) if re.search(r"blind[- ]run", s, re.I)
    ]
    guarded = any(
        BLIND_RUNNER_AGENT in s and BLIND_RUNNER_INDEPENDENCE in s for s in blind_sentences
    )
    if not guarded:
        print(f"RL-11 FAIL: §3 does not state, in a sentence about the blind run, both {BLIND_RUNNER_AGENT!r} and {BLIND_RUNNER_INDEPENDENCE!r}")
        sys.exit(1)

    # The absence route's "produce the item here" is routed through §3 by
    # reference for the blind-run-report case, not left as a freestanding,
    # unconstrained instruction (mirrors how the §1 pointer routes a no-task
    # Build entry through §3 rather than restating its rule).
    lookup_para = _paragraph(LOOKUP_OPENER)
    if BLIND_RUNNER_ROUTE_PHRASE not in lookup_para:
        print(f"RL-11 FAIL: the absence route does not send the blind-run-report case to §3: missing {BLIND_RUNNER_ROUTE_PHRASE!r}")
        sys.exit(1)
    print("RL-11 PASS: blind-run independence is stated in §3 and the absence route defers to it")


def test_RL_13_lookup_is_bounded_to_the_three_recovery_items():
    """The manifest lookup this rule runs is bounded to the three items
    Acceptance #1 names, not left open over every manifest key (ADV-04 found
    two of eight candidate keys resolve to two stations with no tie-break)."""
    _require("RL-13", LOOKUP_OPENER, [BOUNDED_LOOKUP_SENTENCE])
    print("RL-13 PASS: the lookup is bounded to the three recovery items REQ-1 names")


def test_self_check_negation_discriminates():
    """Self-test for the shared negation guard (prose_pin.has_negation) used
    by RL-03: it accepts the real affirmative sentence and rejects a rewrite
    of it that keeps the same key words but reverses the meaning — the shape
    of ADV-02's attack, applied here in place rather than as a trailing
    append, to prove the guard discriminates rather than just asserting it
    does."""
    negated_target = (
        "on a re-entry with every planned task already committed, the item "
        "this station needs is absent"
    )
    negated = (
        "on a re-entry with every planned task already committed, the item "
        "this station needs is not absent"
    )
    if has_negation(negated_target):
        print(f"SELF-TEST FAIL: the real RL-03 sentence was flagged as negated: {negated_target!r}")
        sys.exit(1)
    if not has_negation(negated):
        print(f"SELF-TEST FAIL: a negated rewrite of it was not caught: {negated!r}")
        sys.exit(1)
    print("SELF-TEST PASS: the negation guard accepts the affirmative sentence and rejects its negation")


if __name__ == "__main__":
    test_self_check_negation_discriminates()
    test_RL_03_absence_is_distinct_and_the_producer_is_looked_up()
    test_RL_04_no_second_copy_of_the_artifact_station_mapping()
    test_RL_05_unanswered_decision_stops_and_asks()
    test_RL_06_answered_decision_proceeds_and_the_skip_rule_is_untouched()
    test_RL_07_failed_recovery_stops_and_reports()
    test_RL_08_failed_recovery_neither_retries_nor_hands_on()
    test_RL_10_the_sequence_is_recorded_and_the_second_entry_is_the_last()
    test_RL_15_recovery_count_is_independent_of_ordinary_review_rounds()
    test_RL_12_the_recorded_sequence_surfaces_at_both_stops_and_the_hand_off()
    test_RL_11_blind_run_independence_is_stated_in_its_own_section()
    test_RL_13_lookup_is_bounded_to_the_three_recovery_items()
    print("All probes passed.")
