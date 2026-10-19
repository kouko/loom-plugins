# Publish refuses a PR body that misstates its verification, and the OpenCode docs are tidied
originator: kouko
kind: engineering
needs-design: no — the publish command gains one more refusal of a malformed PR body, the kind it already prints with a named remedy; no new command, argument or output format, and the rest is wording in existing docs
status: confirmed 2026-09-30
publication: automatic — authorized 2026-09-30 by kouko

## Problem
In the OpenCode acceptance run of 2026-09-29, a weaker third-party model
generated the attestation but never committed it, so `publish` computed and
printed `stale` — and the pull request body the model wrote still claimed
`valid (skipped: reviewers)`, although reviewers had run and nothing was
skipped. Nothing stopped that body. Anyone reading such a pull request is told
the change was verified when it was not, and loom's own disclosure line
becomes the thing that misleads. The same run also left three wording defects
in the OpenCode docs that the last review round could not fix: the acceptance
test report still says the install steps do not name the settings file, the
spec's first requirement names a TUI install dialog that its own design
decision says does not exist, and the READMEs state "the TUI has no
plugin-install option" as an absolute and call a folder a file. And the lesson
behind the removed TUI install route — a host's interface claim was written
into install docs without checking the host's official documentation — is
not recorded anywhere a later contributor will find it.

## Proposed outcome
A pull request can no longer be published with a `Verification status:` line
that differs from the status loom computes, or with a generated attestation
left uncommitted; the refusal names the remedy. The OpenCode docs carry no
known wording defect, and the lesson is in the repository's memory store.

## Acceptance
1. Publishing a change whose PR body states a verification status different from the one loom computes for that branch is refused before anything is pushed, and the refusal names the status the body must carry.
2. Publishing a change whose generated attestation exists in the working tree but is not committed is refused before anything is pushed, and the refusal says to commit it.
3. Publishing a change whose PR body states the computed status, with no uncommitted attestation, behaves as before, including when the status is `absent` or `stale`.
4. The three OpenCode wording defects named in the Problem are fixed where they appear.
5. The repository's memory store holds the lesson that a host's interface or install claim is checked against the host's official documentation before it is written into install docs.
6. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

## Constraints
- Publishing without an attestation, or with a stale one, stays allowed and disclosed; only a body that misstates the status, or an attestation generated but left uncommitted, is refused.
- No record of which agents were dispatched is added; mechanical enforcement of implementer dispatch is not part of this change (user-decided 2026-09-30).
- Claude Code, Codex, Antigravity CLI and OpenCode keep the same install layout and skill names.

## Out of scope
- Mechanically proving that an implementer subagent was dispatched.
- Any change to how the verification status itself is computed.

## Open questions
- none
