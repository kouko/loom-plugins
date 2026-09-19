"""ADV-10 — the attempts that failed to break anything.

Not every attack landed. This probe records the ones that did not, so the set
above reads as an eval rather than a highlight reel. Each case is the blunt
form of an attack that ADV-01, ADV-02 or ADV-09 later got through by being
subtler; the gates catch all of these.

Cases:
  1. Delete the closing-review lookup paragraph outright.
  2. Delete Build's absence paragraph outright.
  3. Delete Build's §1 pointer to §3 — the W0-04 fix.
  4. Swap the manifest citation for a plausible second source
     (`loom-code/contract/stations.yaml`), the evasion REQ-3 is aimed at.
  5. Replace `actions[].owner` with `charter.signoff`, the wrong field the
     spec's Design decision singles out.
  6. State the mapping in plain artifact nouns inside the lookup paragraph
     ("the blind-run report is produced downstream") — the unbackticked form
     of ADV-09.

All six are expected RED. A GREEN here is a regression in the probes.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_10_attempts_that_held.py
"""

import adv_harness as h

CR_LOOKUP_START = "Absence is a distinct antecedent from a failing check."
BUILD_ABSENCE_START = "Build enters these end-of-Build checks on absence as well as after a fix:"
BUILD_POINTER = (
    "Finding no task left to implement is not a reason to end Build. It means §2 has\n"
    "nothing to implement, not that the run is over: continue to §3, which states\n"
    "what such a re-entry runs.\n\n"
)


def drop_paragraph(root, relpath, opener):
    text = h.read(root, relpath)
    paras = text.split("\n\n")
    kept = [p for p in paras if opener not in " ".join(p.split())]
    if len(kept) == len(paras):
        raise AssertionError(f"no paragraph opening {opener!r} in {relpath}")
    h.write(root, relpath, "\n\n".join(kept))


CASES = []


def case(label, probes):
    def register(fn):
        CASES.append((label, probes, fn))
        return fn

    return register


@case("delete the closing-review lookup paragraph", h.CR_PROBES)
def _c1(root):
    drop_paragraph(root, h.CR_SKILL, CR_LOOKUP_START)


@case("delete Build's absence paragraph", h.BUILD_PROBES)
def _c2(root):
    drop_paragraph(root, h.BUILD_SKILL, BUILD_ABSENCE_START)


@case("delete Build's §1 pointer to §3", h.BUILD_PROBES)
def _c3(root):
    h.mutate(root, h.BUILD_SKILL, BUILD_POINTER, "")


@case("cite a plausible second source instead of the manifest", h.CR_PROBES)
def _c4(root):
    h.mutate(
        root,
        h.CR_SKILL,
        "`loom-code/contract/manifest.yaml` (`stations[].produces` and\n`actions[].owner`)",
        "`loom-code/contract/stations.yaml` (the station table)",
    )


@case("look the producer up in charter.signoff", h.CR_PROBES)
def _c5(root):
    h.mutate(root, h.CR_SKILL, "`actions[].owner`) for the station", "`charter.signoff`) for the station")


@case("state the mapping in plain artifact nouns", h.CR_PROBES)
def _c6(root):
    h.mutate(
        root,
        h.CR_SKILL,
        "Take the owner, never",
        "The blind-run report and the attestation are produced downstream. "
        "Take the owner, never",
    )


def main():
    results = []
    for label, probes, apply_case in CASES:
        root = h.extract()
        apply_case(root)
        code, out = h.run_probes(root, probes)
        verdict = "RED" if code != 0 else "GREEN"
        h.report("ADV-10", f"{label} -> {verdict}", f"exit {code}")
        for line in out.splitlines():
            if "FAIL" in line:
                print("    " + line)
        results.append(verdict)

    h.expect(
        "ADV-10",
        results,
        ["RED"] * len(CASES),
        "six blunt attacks, all caught. The gates do hold against deletion, "
        "against a substituted source and against the wrong manifest field; "
        "what they miss is everything that keeps the asserted strings in place "
        "(ADV-01, ADV-02, ADV-09).",
    )


if __name__ == "__main__":
    main()
