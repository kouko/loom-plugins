"""ADV-06 — RL-02 and RL-12 reject ordinary English.

closing-review's RL-04 matches station names with a word-boundary regex and a
deliberate note that "build" and "ship" are ordinary English words. Build's
RL-02 and RL-12 check the same thing with a bare `name in para` substring test
over the list ["capture-intent", "write-spec", "write-plan", "closing-review",
"ship", "maintain"].

So in build/SKILL.md the words *relationship*, *ships*, *maintain*,
*maintains* and *maintained* are now forbidden inside the recovery paragraph
and anywhere in §1–§2 — not because they name a station, but because they
contain one. This probe writes three sentences a reviewer would wave through
and shows the gate going RED on each.

A gate that is blind to a full negation (ADV-02) and RED on the word
"relationship" costs every future editor of this file and protects nothing.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_06_station_names_as_substrings.py
"""

import adv_harness as h

ANCHOR_PARA = "committed programs are re-run, never re-dispatched, exactly as after a fix."
ANCHOR_EARLY = "nothing to implement, not that the run is over: continue to §3, which states"

INNOCENT_EDITS = [
    (
        ANCHOR_PARA,
        ANCHOR_PARA + " Keep the relationship between the two antecedents clear.",
        "the word 'relationship' in the recovery paragraph",
    ),
    (
        ANCHOR_PARA,
        ANCHOR_PARA + " The run maintains no state of its own here.",
        "the word 'maintains' in the recovery paragraph",
    ),
    (
        ANCHOR_EARLY,
        ANCHOR_EARLY.replace(
            "which states", "which states, for a change that ships incrementally,"
        ),
        "the word 'ships' in §1",
    ),
]


def main():
    results = []
    for old, new, label in INNOCENT_EDITS:
        root = h.extract()
        h.mutate(root, h.BUILD_SKILL, old, new)
        code, out = h.run_probes(root, h.BUILD_PROBES)
        verdict = "RED" if code != 0 else "GREEN"
        h.report("ADV-06", f"{label} -> {verdict}", f"exit {code}")
        for line in out.splitlines():
            if "FAIL" in line:
                print("    " + line)
        results.append(verdict)

    h.expect(
        "ADV-06",
        results,
        ["RED", "RED", "GREEN"],
        "RL-02 and RL-12 now match station names by the same word-boundary "
        "pattern as RL-04, so the 'ships' edit in §1 — away from the pinned "
        "closing sentence — no longer trips a false positive. The "
        "'relationship' and 'maintains' edits still turn Build RED, but now "
        "because they touch RL-01's pinned exact closing sentence (the guard "
        "against ADV-02's trailing-append attack), not because of a "
        "station-name substring match.",
    )


if __name__ == "__main__":
    main()
