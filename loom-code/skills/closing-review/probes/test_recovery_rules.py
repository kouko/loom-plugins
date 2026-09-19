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
"""

import sys

SKILL = "loom-code/skills/closing-review/SKILL.md"

# Each rule lives in one paragraph, identified by its opening words.
LOOKUP_OPENER = "Absence is a distinct antecedent from a failing check."
DECISION_OPENER = "Stop and ask when producing an absent item needs"
FAILURE_OPENER = "Stop when the attempt to produce an absent item fails."


def _read():
    with open(SKILL, "r", encoding="utf-8") as f:
        return f.read()


def _paragraph(opener):
    """Return the paragraph carrying these words, or None when absent.

    Whitespace is normalized so that these probes test the wording, not where
    the file happens to wrap a line.
    """
    for para in _read().split("\n\n"):
        normalized = " ".join(para.split())
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

    # A second copy of the mapping would have to name the producing stations.
    other_stations = [
        "capture-intent",
        "write-spec",
        "write-plan",
        "Build",
        "build",
        "ship",
        "Ship",
        "maintain",
    ]
    restated = [name for name in other_stations if name in para]
    if restated:
        print(f"RL-04 FAIL: the lookup paragraph restates the mapping for {restated}")
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


if __name__ == "__main__":
    test_RL_03_absence_is_distinct_and_the_producer_is_looked_up()
    test_RL_04_no_second_copy_of_the_artifact_station_mapping()
    test_RL_05_unanswered_decision_stops_and_asks()
    test_RL_06_answered_decision_proceeds_and_the_skip_rule_is_untouched()
    test_RL_07_failed_recovery_stops_and_reports()
    test_RL_08_failed_recovery_neither_retries_nor_hands_on()
    print("All probes passed.")
