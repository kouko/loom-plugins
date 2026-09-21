"""ADV-04 — run the lookup the recovery rule tells an agent to run.

REQ-3 and both SKILL.md paragraphs say: read `stations[].produces` and
`actions[].owner` in `loom-code/contract/manifest.yaml` "for the station that
produces the absent item" — singular. This probe does exactly that, for every
artifact a recovery could find absent, and reports how many stations each one
resolves to.

The rule is only executable where the answer is exactly one. Zero means the run
has no route and falls back to whatever the agent guesses. Two means the run
picks, and nothing in the instructions says which — a coin flip inside a rule
written to remove coin flips.

This probe needs no mutation: the manifest is read as committed.

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_04_lookup_does_not_resolve.py
"""

import os

import yaml

import adv_harness as h

MANIFEST = "loom-code/contract/manifest.yaml"

# Everything a recovery can find absent: the per-change artifacts the manifest
# declares, plus the two verification items named in Acceptance 1.
LOOKUP_KEYS = [
    "intent",
    "spec",
    "plan",
    "diff",
    "attestation",
    "blind-run",
    "adversarial",
    "package-tests",
]


def resolve(manifest, key):
    """The lookup exactly as the recovery paragraphs describe it."""
    owners = [s["name"] for s in manifest.get("stations", []) if s.get("produces") == key]
    owners += [
        a["owner"]
        for a in manifest.get("actions", [])
        if a.get("name") == key and a.get("owner")
    ]
    return sorted(set(owners))


def main():
    with open(os.path.join(h.REPO, MANIFEST), "r", encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh)

    unresolved = []
    ambiguous = []
    for key in LOOKUP_KEYS:
        owners = resolve(manifest, key)
        h.report("ADV-04", key, f"{len(owners)} producing station(s): {owners or '—'}")
        if not owners:
            unresolved.append(key)
        elif len(owners) > 1:
            ambiguous.append((key, owners))

    h.expect(
        "ADV-04",
        (unresolved, sorted(ambiguous)),
        (
            [],
            [
                ("diff", ["build", "ship"]),
                ("intent", ["capture-intent", "maintain"]),
            ],
        ),
        "two of the eight lookup keys resolve to two stations each, and the "
        "instructions say 'the station that produces the absent item' with no "
        "tie-break. An absent diff or an absent intent leaves the recovery "
        "rule undefined.",
    )


if __name__ == "__main__":
    main()
