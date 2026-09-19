"""ADV-01 — near-miss against RL-02 / RL-04: move the second copy next door.

REQ-3 forbids the recovery instructions carrying a second copy of the
artifact-to-station mapping, because a second copy drifts silently. RL-02 and
RL-04 enforce that by scanning exactly one paragraph, the one whose opening
words they match on.

The attempt: leave the cited-lookup paragraph untouched — so it still reads as
compliant — and add the second copy of the mapping as the paragraph right after
it, where an agent reading the section top to bottom finds it just as readily.
If the gates still pass, they police a paragraph rather than the instructions,
and REQ-3's purpose is defeated by a line break.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_01_mapping_copy_next_door.py
"""

import adv_harness as h

# A second copy of the mapping, stated the way a hurried author would state it:
# artifact nouns paired with producing stations, in plain prose.
SECOND_COPY = (
    "\n\nIn practice the mapping resolves as follows. The attestation is "
    "produced by closing-review. The blind-run report is produced by "
    "closing-review. The adversarial programs are produced by Build. The plan "
    "is produced by write-plan, and the spec by write-spec.\n"
)

CR_ANCHOR = (
    "Stop and ask when producing an absent item needs a decision point the user"
)
BUILD_ANCHOR = "A recovery run is bounded across stations"


def main():
    root = h.extract()

    # closing-review: insert the copy between the lookup paragraph and the
    # decision-point paragraph.
    text = h.read(root, h.CR_SKILL)
    h.write(root, h.CR_SKILL, text.replace(CR_ANCHOR, SECOND_COPY.strip() + "\n\n" + CR_ANCHOR, 1))

    # build: insert the same copy between the absence paragraph and the bound
    # paragraph.
    text = h.read(root, h.BUILD_SKILL)
    h.write(root, h.BUILD_SKILL, text.replace(BUILD_ANCHOR, SECOND_COPY.strip() + "\n\n" + BUILD_ANCHOR, 1))

    cr_code, cr_out = h.run_probes(root, h.CR_PROBES)
    build_code, build_out = h.run_probes(root, h.BUILD_PROBES)

    h.report("ADV-01", "closing-review probes", f"exit {cr_code}")
    print(cr_out.rstrip())
    h.report("ADV-01", "build probes", f"exit {build_code}")
    print(build_out.rstrip())

    both_passed = (cr_code == 0 and build_code == 0)
    h.expect(
        "ADV-01",
        both_passed,
        True,
        "a verbatim second copy of the artifact-to-station mapping, placed in "
        "the paragraph next to the cited lookup, passes RL-02 and RL-04 "
        "unchanged. The gates bound their scan to one paragraph, so REQ-3 is "
        "satisfiable by a line break.",
    )


if __name__ == "__main__":
    main()
