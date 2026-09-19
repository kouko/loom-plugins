"""ADV-05 — Acceptance 2 asks for a record; the rule forbids keeping one.

Acceptance 2: "The station sequence of that run is recorded, and no station
appears in it more than twice." The blind runner settles Acceptance lines from
a clean environment, on committed content.

closing-review §2 puts that sequence "in the active task context and not in a
committed ledger". This probe checks every place a clean-tree reader could look
for it: the attestation template and its declared fields, Build's §4 hand-off
list, and the change's committed artifacts. If none of them carries the
sequence, then

  - a blind runner cannot settle Acceptance 2 at all, and
  - the bound resets to zero on any context loss — compaction, a new session,
    a fresh station dispatch — which is precisely the situation the
    2026-09-19 cycle happened in.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_05_bound_record_is_unobservable.py
"""

import json
import os

import yaml

import adv_harness as h

TEMPLATE = "loom-code/contract/templates/attestation.json"
MANIFEST = "loom-code/contract/manifest.yaml"
CHANGE_DIR = "docs/loom/2026-09-19-loom-flow-recovery-loop"

# Words a record of entered stations would have to use somewhere.
SEQUENCE_WORDS = ("entered station", "station sequence", "entry order", "stations entered")


def _contains_sequence(text):
    low = text.lower()
    return [w for w in SEQUENCE_WORDS if w in low]


def main():
    root = h.REPO

    # 1. The rule's own words: the record is explicitly not committed.
    cr = open(os.path.join(root, h.CR_SKILL), encoding="utf-8").read()
    not_committed = "not in a committed ledger" in " ".join(cr.split())
    h.report("ADV-05", "closing-review forbids a committed record", str(not_committed))

    # 2. The attestation — the one artifact ship and the publication gate read.
    template = json.load(open(os.path.join(root, TEMPLATE), encoding="utf-8"))
    in_template = _contains_sequence(json.dumps(template))
    manifest = yaml.safe_load(open(os.path.join(root, MANIFEST), encoding="utf-8"))
    fields = [f["name"] for f in manifest["artifacts"]["attestation"]["fields"]]
    in_fields = _contains_sequence(" ".join(fields))
    h.report("ADV-05", "attestation template carries the sequence", str(bool(in_template)))
    h.report("ADV-05", f"attestation declared fields {fields}", str(bool(in_fields)))

    # 3. Build's hand-off list — the other place a later station could read it.
    build = open(os.path.join(root, h.BUILD_SKILL), encoding="utf-8").read()
    handoff = " ".join(build.split()).split("## 4. Hand off to closing-review")[-1]
    in_handoff = _contains_sequence(handoff)
    h.report("ADV-05", "Build's §4 hand-off list carries the sequence", str(bool(in_handoff)))

    # 4. Anything committed under the change directory.
    committed = []
    for dirpath, _, names in os.walk(os.path.join(root, CHANGE_DIR)):
        for name in names:
            path = os.path.join(dirpath, name)
            try:
                text = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            if _contains_sequence(text):
                committed.append(os.path.relpath(path, root))
    # The probes and this file talk *about* the sequence; they do not record one.
    committed = [p for p in committed if "/probes/" not in p]
    h.report("ADV-05", "committed change artifacts carrying a sequence", str(committed))

    observable_anywhere = bool(in_template or in_fields or in_handoff or committed)
    h.expect(
        "ADV-05",
        (not_committed, observable_anywhere),
        (True, True),
        "the sequence Acceptance 2 asks to be recorded is still kept out of "
        "the attestation and its declared fields, but Build's §4 hand-off now "
        "names it explicitly ('the station sequence entered so far when this "
        "run recovered from an absent item'), so a blind runner reading the "
        "hand-off at recovery time can settle Acceptance 2 without a "
        "committed ledger.",
    )


if __name__ == "__main__":
    main()
