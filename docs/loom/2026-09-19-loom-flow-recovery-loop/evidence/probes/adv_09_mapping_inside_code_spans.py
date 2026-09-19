"""ADV-09 — hide the second copy in backticks, inside the very paragraph.

RL-02 and RL-04 strip inline code spans before looking for station names and
producer claims, so that citing `stations[].produces` is not read as prose.
That exemption is unconditional: anything between backticks is invisible to
both checks.

So the second copy of the mapping does not even have to move to the next
paragraph (ADV-01). Written as a backticked list, it sits inside the lookup
paragraph, reads perfectly clearly to an agent, and both gates stay GREEN.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_09_mapping_inside_code_spans.py
"""

import adv_harness as h

CR_ANCHOR = "Take the owner, never"
CR_COPY = (
    "For reference the lookup gives "
    "`attestation -> closing-review`, `blind-run -> closing-review`, "
    "`adversarial -> build`, `plan -> write-plan`, `spec -> write-spec`. "
    "Take the owner, never"
)

BUILD_ANCHOR = "Absence\ndispatches the adversary"
# Build's RL-02 tests station names against the unstripped paragraph, so it
# still catches a backticked station name. It strips before the artifact-noun
# check, so the same mapping stated in artifact nouns walks through.
BUILD_COPY = (
    "For reference: `the adversarial programs are produced by build`, and "
    "`the blind-run report and the attestation are produced downstream`. "
    "Absence\ndispatches the adversary"
)


def main():
    root = h.extract()
    h.mutate(root, h.CR_SKILL, CR_ANCHOR, CR_COPY)
    h.mutate(root, h.BUILD_SKILL, BUILD_ANCHOR, BUILD_COPY)

    cr_code, cr_out = h.run_probes(root, h.CR_PROBES)
    build_code, build_out = h.run_probes(root, h.BUILD_PROBES)

    h.report("ADV-09", "closing-review probes", f"exit {cr_code}")
    print(cr_out.rstrip())
    h.report("ADV-09", "build probes", f"exit {build_code}")
    print(build_out.rstrip())

    h.expect(
        "ADV-09",
        (cr_code == 0, build_code == 0),
        (True, True),
        "a complete artifact-to-station mapping, written in backticks inside "
        "the lookup paragraph itself, passes RL-02 and RL-04. The code-span "
        "exemption that lets the rule cite `stations[].produces` also hides "
        "the copy the rule exists to prevent.",
    )


if __name__ == "__main__":
    main()
