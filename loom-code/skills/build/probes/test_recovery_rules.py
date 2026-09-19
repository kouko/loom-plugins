"""Probes for the Build absence-recovery rule (change 2026-09-19-loom-flow-recovery-loop).

A1 positive: RL-01 — the recovery rule is present in build/SKILL.md.
A1 negative: RL-02 — the recovery paragraph carries no second copy of the
             artifact-to-station mapping; it cites the contract manifest.
"""

import sys

SKILL = "loom-code/skills/build/SKILL.md"

# The paragraph the recovery rule lives in, identified by its opening words.
PARAGRAPH_OPENER = "Build enters these end-of-Build checks on absence"


def _read():
    with open(SKILL, "r", encoding="utf-8") as f:
        return f.read()


def _recovery_paragraph(content):
    """Return the recovery paragraph, or None when it is absent."""
    for para in content.split("\n\n"):
        if PARAGRAPH_OPENER in para:
            return para
    return None


def test_RL_01_absence_re_enters_end_of_build_checks():
    """Absence is an antecedent for re-running the end-of-Build checks."""
    para = _recovery_paragraph(_read())
    if para is None:
        print(f"RL-01 FAIL: no paragraph starting {PARAGRAPH_OPENER!r} in {SKILL}")
        sys.exit(1)

    required = [
        # absence, not a fix or a widening, is the antecedent
        "every planned task already committed",
        "is absent",
        # absence is kept distinct from failure
        "distinct antecedent from a failing check",
        # the adversary is not re-dispatched merely because Build re-enters
        "re-run, never re-dispatched",
    ]
    missing = [phrase for phrase in required if phrase not in para]
    if missing:
        print(f"RL-01 FAIL: recovery paragraph is missing {missing}")
        sys.exit(1)
    print("RL-01 PASS: absence re-enters the end-of-Build checks")


def test_RL_02_no_second_copy_of_the_artifact_station_mapping():
    """The rule cites the manifest and names no other station's artifacts."""
    para = _recovery_paragraph(_read())
    if para is None:
        print(f"RL-02 FAIL: no paragraph starting {PARAGRAPH_OPENER!r} in {SKILL}")
        sys.exit(1)

    for citation in ("loom-code/contract/manifest.yaml", "stations[].produces", "actions[].owner"):
        if citation not in para:
            print(f"RL-02 FAIL: recovery paragraph does not cite {citation}")
            sys.exit(1)

    # A second copy of the mapping would have to name the other stations.
    other_stations = [
        "capture-intent",
        "write-spec",
        "write-plan",
        "closing-review",
        "ship",
        "maintain",
    ]
    restated = [name for name in other_stations if name in para]
    if restated:
        print(f"RL-02 FAIL: recovery paragraph restates the mapping for {restated}")
        sys.exit(1)
    print("RL-02 PASS: the producing station is read from the manifest, not restated")


if __name__ == "__main__":
    test_RL_01_absence_re_enters_end_of_build_checks()
    test_RL_02_no_second_copy_of_the_artifact_station_mapping()
    print("All probes passed.")
