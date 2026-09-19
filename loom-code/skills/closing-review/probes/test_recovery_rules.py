"""Probes for the closing-review absence-recovery rules (change 2026-09-19-loom-flow-recovery-loop).

A3 positive: RL-03 — absence is a distinct antecedent and the producing
             station is looked up in the contract manifest.
A3 negative: RL-04 — the lookup paragraph carries no second copy of the
             artifact-to-station mapping.
A4 positive: RL-05 — an unanswered decision point stops the run and asks.
A4 boundary: RL-06 — an answered decision, including a general delegation,
             proceeds as user-decided, and the skip confirmation is untouched.
A5 positive: RL-07 — a failed recovery stops and says what happened.
A5 negative: RL-08 — a failed recovery neither retries nor hands on.
A2 boundary: RL-10 — the station sequence is recorded, a second entry is the
             last one allowed, and a third is a failed recovery.
"""

import re
import sys

SKILL = "loom-code/skills/closing-review/SKILL.md"

# Each rule lives in one paragraph, identified by its opening words.
LOOKUP_OPENER = "Absence is a distinct antecedent from a failing check."
DECISION_OPENER = "Stop and ask when producing an absent item needs"
FAILURE_OPENER = "Stop when the attempt to produce an absent item fails."

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


def _strip_code_spans(text):
    """Drop inline code, so citing `stations[].produces` is not read as prose."""
    return re.sub(r"`[^`]*`", " ", text)


def _mapping_restatements(para):
    """Sentences that pair an artifact noun with a claim about its producer."""
    prose = _strip_code_spans(para)
    offenders = []
    for sentence in re.split(r"(?<=[.;])\s+", prose):
        if ARTIFACT_NOUNS.search(sentence) and PRODUCER_PHRASES.search(sentence):
            offenders.append(sentence.strip())
    return offenders


def test_RL_03_absence_is_distinct_and_the_producer_is_looked_up():
    """Absence routes by a manifest lookup, not as a failing check."""
    _require(
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
    print("RL-03 PASS: absence is distinct and the producer comes from the manifest")


def test_RL_04_no_second_copy_of_the_artifact_station_mapping():
    """The lookup names no artifact-to-station pair of its own."""
    para = _paragraph(LOOKUP_OPENER)
    if para is None:
        print(f"RL-04 FAIL: no paragraph containing {LOOKUP_OPENER!r} in {SKILL}")
        sys.exit(1)

    # A second copy of the mapping may name the producing station...
    restated = sorted(set(STATION_REFERENCE.findall(_strip_code_spans(para))))
    if restated:
        print(f"RL-04 FAIL: the lookup paragraph restates the mapping for {restated}")
        sys.exit(1)

    # ...or name none and say it in artifact nouns alone.
    offenders = _mapping_restatements(para)
    if offenders:
        print(f"RL-04 FAIL: the lookup paragraph states who produces an artifact: {offenders}")
        sys.exit(1)
    print("RL-04 PASS: the lookup carries no second copy of the mapping")


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
    if "proceed" not in para:
        print("RL-06 FAIL: the answered branch does not proceed")
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
    _require(
        "RL-08",
        FAILURE_OPENER,
        ["second time", "another station"],
    )
    print("RL-08 PASS: a failed recovery neither retries nor hands on")


def test_RL_10_the_sequence_is_recorded_and_the_second_entry_is_the_last():
    """Acceptance 2 has two halves, and the boundary sits between them: the run
    keeps a record of the stations it entered, a second entry to a station is
    still allowed, and a third is not."""
    _require(
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
    print("RL-10 PASS: the sequence is recorded and the second entry is the last allowed")


if __name__ == "__main__":
    test_RL_03_absence_is_distinct_and_the_producer_is_looked_up()
    test_RL_04_no_second_copy_of_the_artifact_station_mapping()
    test_RL_05_unanswered_decision_stops_and_asks()
    test_RL_06_answered_decision_proceeds_and_the_skip_rule_is_untouched()
    test_RL_07_failed_recovery_stops_and_reports()
    test_RL_08_failed_recovery_neither_retries_nor_hands_on()
    test_RL_10_the_sequence_is_recorded_and_the_second_entry_is_the_last()
    print("All probes passed.")
