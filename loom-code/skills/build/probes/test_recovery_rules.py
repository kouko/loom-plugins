"""Probes for the Build absence-recovery rule (change 2026-09-19-loom-flow-recovery-loop).

A1 positive: RL-01 — the recovery rule is present in build/SKILL.md.
A1 negative: RL-02 — the recovery paragraph carries no second copy of the
             artifact-to-station mapping; it cites the contract manifest.
A2 positive: RL-09 — Build carries the cross-station bound, as a pointer to the
             station that states it rather than a count of its own.
A1 positive: RL-11 — a Build entry with no task to implement is directed to §3,
             stated before the point where such a run would exit.
A1 negative: RL-12 — that early pointer is a pointer, not a second copy of the
             §3 absence rule, and §3 still states the rule exactly once.
"""

import re
import sys

SKILL = "loom-code/skills/build/SKILL.md"

# Each rule lives in one paragraph, identified by its opening words.
PARAGRAPH_OPENER = "Build enters these end-of-Build checks on absence"
BOUND_OPENER = "A recovery run is bounded across stations"

# Headings that bound the early sections a no-task run reads before it exits.
SCOPE_HEADING = "## 1. Establish scope"
VERIFY_HEADING = "## 3. Verify integration"

# Artifact nouns a restatement of the mapping would have to name. A second copy
# phrased purely in artifact nouns — "the blind-run report is produced
# downstream" — names no station and so slips past a station-name check.
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


def _early_sections():
    """Return §1 and §2 — everything a no-task run reads before it would exit."""
    content = _read()
    start = content.index(SCOPE_HEADING)
    end = content.index(VERIFY_HEADING)
    return _normalize(content[start:end])


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


def test_RL_01_absence_re_enters_end_of_build_checks():
    """Absence is an antecedent for re-running the end-of-Build checks."""
    _require(
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
    print("RL-01 PASS: absence re-enters the end-of-Build checks")


def test_RL_02_no_second_copy_of_the_artifact_station_mapping():
    """The rule cites the manifest and restates no artifact-to-station pair."""
    para = _paragraph(PARAGRAPH_OPENER)
    if para is None:
        print(f"RL-02 FAIL: no paragraph containing {PARAGRAPH_OPENER!r} in {SKILL}")
        sys.exit(1)

    for citation in ("loom-code/contract/manifest.yaml", "stations[].produces", "actions[].owner"):
        if citation not in para:
            print(f"RL-02 FAIL: recovery paragraph does not cite {citation}")
            sys.exit(1)

    # A second copy of the mapping may name the producing station...
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

    # ...or name none and say it in artifact nouns alone.
    offenders = _mapping_restatements(para)
    if offenders:
        print(f"RL-02 FAIL: recovery paragraph states who produces an artifact: {offenders}")
        sys.exit(1)
    print("RL-02 PASS: the producing station is read from the manifest, not restated")


def test_RL_09_build_carries_the_cross_station_bound():
    """Build, the station the 2026-09-19 cycle kept re-entering, reads that a
    recovery run is bounded — by pointer, never by a count of its own."""
    para = _require(
        "RL-09",
        BOUND_OPENER,
        [
            # an entry here is part of the bounded sequence
            "counts toward",
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
    states that rule exactly once."""
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
    test_RL_09_build_carries_the_cross_station_bound()
    test_RL_11_no_task_to_implement_is_directed_to_section_3()
    test_RL_12_the_pointer_is_not_a_second_copy_of_the_rule()
    print("All probes passed.")
