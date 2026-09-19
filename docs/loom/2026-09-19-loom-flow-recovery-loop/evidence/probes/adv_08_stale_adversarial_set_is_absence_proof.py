"""ADV-08 — one committed program makes "the adversarial programs" present forever.

Build's new rule: "Absence dispatches the adversary only when no adversarial
program is committed; committed programs are re-run, never re-dispatched,
exactly as after a fix."

The antecedent is *no* program committed, not *no adequate coverage*. The
paragraph after it is the only other route to a re-dispatch, and its antecedent
is a fix that "widens or changes what the change covers", or a trunk sync.

Put those two together on the exact state Acceptance 1 describes — every
planned task already committed, so no fix happens — and a change that has one
stale probe file from its first task can never get adversarial coverage for
its later tasks. The absence route is closed by the one file; the widening
route is closed by the absent fix.

This probe reads the two antecedents out of the committed SKILL.md and
evaluates them against that state, so it re-runs against the real text rather
than against a quote of it.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_08_stale_adversarial_set_is_absence_proof.py
"""

import os
import re

import adv_harness as h

ABSENCE_ANTECEDENT = "Absence dispatches the adversary only when no adversarial program is committed"
WIDENING_ANTECEDENT = "when a fix widens or changes what the change covers"


def main():
    text = " ".join(
        open(os.path.join(h.REPO, h.BUILD_SKILL), encoding="utf-8").read().split()
    )

    has_absence_rule = ABSENCE_ANTECEDENT in text
    has_widening_rule = WIDENING_ANTECEDENT in text
    h.report("ADV-08", "absence route antecedent found verbatim", str(has_absence_rule))
    h.report("ADV-08", "widening route antecedent found verbatim", str(has_widening_rule))

    # Is there any third route that could re-dispatch the adversary?
    dispatch_sentences = [
        s
        for s in re.split(r"(?<=[.;])\s+", text)
        if re.search(r"dispatch(?:es)? the .*adversar", s, re.I)
        or re.search(r"adversary.*(?:dispatch|re-dispatch)", s, re.I)
    ]
    h.report("ADV-08", "sentences that can dispatch the adversary", str(len(dispatch_sentences)))
    for s in dispatch_sentences:
        print("    " + s)

    # The Acceptance-1 state: all tasks committed, so no fix; one stale probe
    # file committed from an earlier task, so "no adversarial program is
    # committed" is false; no trunk sync.
    state = {"a_program_is_committed": True, "a_fix_widened_scope": False, "trunk_changed": False}
    absence_route = not state["a_program_is_committed"]
    widening_route = state["a_fix_widened_scope"] or state["trunk_changed"]
    h.report("ADV-08", "absence route fires on that state", str(absence_route))
    h.report("ADV-08", "widening route fires on that state", str(widening_route))

    h.expect(
        "ADV-08",
        (has_absence_rule, has_widening_rule, absence_route or widening_route),
        (True, True, False),
        "on the exact state Acceptance 1 names, neither route to the adversary "
        "fires once a single adversarial program is committed. 'The "
        "adversarial programs are absent' is decided by file count, not by "
        "coverage, so a change whose probes cover its first task and nothing "
        "else recovers to a valid attestation with that gap intact.",
    )


if __name__ == "__main__":
    main()
