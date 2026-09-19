"""ADV-03 — the recipe's "same input one character different" against the gates.

The other side of ADV-02. Here every rule keeps its meaning exactly and only
the wording moves: "no station more than twice" becomes "no station more than
two times", "which item is absent" becomes "which item is missing", and
Build's "re-run, never re-dispatched" becomes "re-run and never re-dispatched".
A human editor would call all three cosmetic.

What the probes do with them tells you what they are really pinning. A gate
that goes RED on a synonym and GREEN on a negation (ADV-02) is pinning a
string, and every future editor of these two SKILL.md files pays that cost
without getting the protection.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_03_one_character_different.py
"""

import adv_harness as h

REWORDINGS = [
    (
        h.CR_SKILL,
        "The run enters no station more than twice.",
        "The run enters no station more than two times.",
        "twice -> two times",
    ),
    (
        h.CR_SKILL,
        "absent, what was attempted, and where it failed.",
        "missing, what was attempted, and where it failed.",
        "absent -> missing in the failure report",
    ),
    (
        h.BUILD_SKILL,
        "committed programs are re-run, never re-dispatched, exactly as after a fix.",
        "committed programs are re-run and never re-dispatched, exactly as after a fix.",
        "comma -> 'and' in the re-run clause",
    ),
]


def main():
    results = []
    for relpath, old, new, label in REWORDINGS:
        root = h.extract()
        h.mutate(root, relpath, old, new)
        probes = h.CR_PROBES if relpath == h.CR_SKILL else h.BUILD_PROBES
        code, out = h.run_probes(root, probes)
        verdict = "RED" if code != 0 else "GREEN"
        h.report("ADV-03", f"{label} -> {verdict}", f"exit {code}")
        first_fail = [line for line in out.splitlines() if "FAIL" in line]
        if first_fail:
            print("    " + first_fail[0])
        results.append(verdict)

    h.expect(
        "ADV-03",
        results,
        ["RED", "RED", "RED"],
        "every meaning-preserving rewording turns a probe RED. Combined with "
        "ADV-02, the gates are exact-string pins: hostile to editing, blind to "
        "meaning.",
    )


if __name__ == "__main__":
    main()
