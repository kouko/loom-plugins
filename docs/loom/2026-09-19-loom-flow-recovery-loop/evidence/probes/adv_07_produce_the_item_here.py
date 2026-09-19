"""ADV-07 — the temptation: "produce the item here" invites self-production.

Read the new closing-review paragraph as an agent under time pressure. It says:
"When that owner is this station, produce the item here and route it nowhere."

For the blind-run report the owner *is* this station. The expensive, correct
route is to dispatch a fresh-context agent that never touched the change. The
cheap route the sentence permits is to write the report yourself.

The whole quality model rests on writer != judge, and before this change
closing-review only reached the blind run on a forward pass, where §3 governs.
Absence is a new entry point, and it is the one reached by an agent that has
just been implementing.

This probe reads the file the agent reads and asks what is there to stop it:
does closing-review/SKILL.md anywhere name the blind-runner agent, or state
that the blind run is written by an agent that never touched the change? It
also checks the three items the absence rule can send to "produce here".

Run:
    python3 docs/loom/2026-09-19-loom-flow-recovery-loop/evidence/probes/adv_07_produce_the_item_here.py
"""

import os
import re

import yaml

import adv_harness as h

MANIFEST = "loom-code/contract/manifest.yaml"

# Wording that would stop the temptation if it were in this file.
GUARDRAILS = (
    "loom-code:blind-runner",
    "never touched the change",
    "fresh-context",
    "fresh context",
    "clean environment",
    "an agent that never",
)


def main():
    text = " ".join(
        open(os.path.join(h.REPO, h.CR_SKILL), encoding="utf-8").read().split()
    )

    permits = "produce the item here and route it nowhere" in text
    h.report("ADV-07", "absence rule says 'produce the item here'", str(permits))

    # Only a guardrail attached to the blind run counts. "fresh-context"
    # appears in this file, but about reviewer dispatch, not about who writes
    # the blind-run report.
    blind_sentences = [
        s for s in re.split(r"(?<=[.;])\s+", text) if re.search(r"blind[- ]run", s, re.I)
    ]
    present = sorted(
        {g for s in blind_sentences for g in GUARDRAILS if g.lower() in s.lower()}
    )
    h.report("ADV-07", f"blind-run sentences in the file: {len(blind_sentences)}", "")
    h.report("ADV-07", "guardrails attached to any of them", str(present))

    # Which absent items does "produce here" apply to? Everything the manifest
    # says closing-review owns.
    manifest = yaml.safe_load(open(os.path.join(h.REPO, MANIFEST), encoding="utf-8"))
    owned = sorted(
        {s["name"] for s in manifest["stations"] if s["name"] == "closing-review"}
        | {a["name"] for a in manifest["actions"] if a.get("owner") == "closing-review"}
        | {s["produces"] for s in manifest["stations"] if s["name"] == "closing-review"}
    )
    h.report("ADV-07", "items the rule sends to 'produce here'", str(owned))

    # Where the writer != judge constraint for the blind run actually lives.
    summary = next(a for a in manifest["actions"] if a["name"] == "blind-run")["summary"]
    in_manifest = bool(re.search(r"never touched the change", summary))
    h.report("ADV-07", "constraint lives in manifest actions[].blind-run.summary", str(in_manifest))

    h.expect(
        "ADV-07",
        (permits, present, in_manifest),
        (True, [], True),
        "the new entry point tells the agent to produce the blind-run report "
        "'here' and closing-review/SKILL.md never names the blind-runner agent "
        "nor states the never-touched-the-change constraint. The rule cites "
        "manifest.yaml only to resolve ownership, and the one sentence that "
        "would stop self-production sits in a field the rule does not send the "
        "agent to read.",
    )


if __name__ == "__main__":
    main()
