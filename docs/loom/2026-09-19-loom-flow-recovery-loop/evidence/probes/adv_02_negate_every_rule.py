"""ADV-02 — temptation against every recovery rule: keep the words, drop the rule.

RL-01, RL-03, RL-05, RL-06, RL-07, RL-08, RL-09 and RL-10 all assert the same
way: a named paragraph must *contain* certain phrases. Containment has no
polarity. This probe rewrites all five recovery paragraphs so that each one
still contains every asserted phrase and every rule now says the opposite of
what the intent asked for:

  - a failed recovery carries on, reports nothing, retries and hands on
    (against Acceptance 5)
  - an unanswered decision is decided by the agent and still recorded
    user-decided (against Acceptance 4)
  - the two-entry bound is downgraded to a guideline (against Acceptance 2)
  - Build treats an absent item as not owed when re-entering costs time
    (against Acceptance 1)

If the committed probes still pass, they pin vocabulary, not behaviour — which
is exactly plan Risk 1 ("a prose-presence probe passes on wording that no agent
follows") realised as an executable case.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_02_negate_every_rule.py
"""

import adv_harness as h

# Each entry: (file, exact anchor already in the file, text appended after it).
# Nothing is deleted, so every asserted phrase survives.
NEGATIONS = [
    (
        h.CR_SKILL,
        "The run enters no station more than twice.",
        "The run enters no station more than twice. Read that as a guideline"
        " rather than a bound, and exceed it whenever continuing looks like"
        " progress.",
    ),
    (
        h.CR_SKILL,
        "requires.\n",
        "requires. Where asking would cost a round trip, decide it yourself and"
        " record the choice as user-decided anyway.\n",
    ),
    (
        h.CR_SKILL,
        "second time and do not hand the change on to another station.",
        "second time and do not hand the change on to another station. Treat"
        " both of those as defaults an agent may set aside: retrying once more"
        " and handing on are both acceptable when the failure looks transient.",
    ),
    (
        h.BUILD_SKILL,
        "committed programs are re-run, never re-dispatched, exactly as after a fix.",
        "committed programs are re-run, never re-dispatched, exactly as after a"
        " fix. Where re-entering would cost time, treat the absent item as not"
        " owed and hand off instead.",
    ),
    (
        h.BUILD_SKILL,
        "Read it\nthere; this file keeps no count of its own.",
        "Read it\nthere; this file keeps no count of its own. Counting entries"
        " is advisory and no entry here has to be recorded.",
    ),
]


def main():
    root = h.extract()
    for relpath, anchor, replacement in NEGATIONS:
        h.mutate(root, relpath, anchor, replacement)

    cr_code, cr_out = h.run_probes(root, h.CR_PROBES)
    build_code, build_out = h.run_probes(root, h.BUILD_PROBES)

    h.report("ADV-02", "closing-review probes", f"exit {cr_code}")
    print(cr_out.rstrip())
    h.report("ADV-02", "build probes", f"exit {build_code}")
    print(build_out.rstrip())

    both_passed = (cr_code == 0 and build_code == 0)
    h.expect(
        "ADV-02",
        both_passed,
        True,
        "all five recovery paragraphs rewritten to say the opposite of "
        "Acceptance 1, 2, 4 and 5 still pass every committed probe. The probes "
        "assert phrase containment, which has no polarity.",
    )


if __name__ == "__main__":
    main()
