"""Probes for the Build absence-recovery rule (change 2026-09-19-loom-flow-recovery-loop).

A1 positive: RL-01 — the recovery rule is present in build/SKILL.md.
A1 negative: RL-02 — the recovery paragraph carries no second copy of the
             artifact-to-station mapping; it cites the contract manifest.
A1 positive: RL-11 — a Build entry with no task to implement is directed to §3,
             stated before the point where such a run would exit.
A1 negative: RL-12 — that early pointer is a pointer, not a second copy of the
             §3 absence rule, and §3 still states the rule exactly once.
"""

import sys

SKILL = "loom-code/skills/build/SKILL.md"

# The paragraph the recovery rule lives in, identified by its opening words.
PARAGRAPH_OPENER = "Build enters these end-of-Build checks on absence"

# Headings that bound the early sections a no-task run reads before it exits.
SCOPE_HEADING = "## 1. Establish scope"
VERIFY_HEADING = "## 3. Verify integration"


def _read():
    with open(SKILL, "r", encoding="utf-8") as f:
        return f.read()


def _early_sections(content):
    """Return §1 and §2 — everything a no-task run reads before it would exit."""
    start = content.index(SCOPE_HEADING)
    end = content.index(VERIFY_HEADING)
    return content[start:end]


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


def test_RL_11_no_task_to_implement_is_directed_to_section_3():
    """A run that finds nothing to implement is told, before it would exit, that
    Build does not end there and that §3 still runs."""
    early = _early_sections(_read())

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
    states that rule exactly once."""
    content = _read()
    early = _early_sections(content)

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
    # artifact-to-station mapping, which RL-02 and closing-review's RL-04 forbid.
    other_stations = [
        "capture-intent",
        "write-spec",
        "write-plan",
        "ship",
        "maintain",
    ]
    restated = [name for name in other_stations if name in early]
    if restated:
        print(f"RL-12 FAIL: §1–§2 name other stations: {restated}")
        sys.exit(1)
    print("RL-12 PASS: the early pointer points at §3 without restating it")


if __name__ == "__main__":
    test_RL_01_absence_re_enters_end_of_build_checks()
    test_RL_02_no_second_copy_of_the_artifact_station_mapping()
    test_RL_11_no_task_to_implement_is_directed_to_section_3()
    test_RL_12_the_pointer_is_not_a_second_copy_of_the_rule()
    print("All probes passed.")
