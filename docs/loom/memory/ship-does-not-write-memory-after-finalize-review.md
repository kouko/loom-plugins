---
name: ship-does-not-write-memory-after-finalize-review
description: Ship must not write memory entries after finalize-review has generated the attestation — committing such a file changes the functional content digest and invalidates the attestation (forcing another review round or Verification status: stale)
type: project
sources:
  - resource: change 2026-10-21-ship-memory-write-timing (PR #109) — memory write timing rule
---

**Why:** The `ship` station commits branch-local memory entries, but once `finalize-review` has generated the attestation the memory file becomes part of the functional content digest the attestation pins as the live statement. Committing it afterwards therefore invalidates the attestation — forcing another review round or a manual `Verification status: stale` reset.

**How to apply:** Qualifying lessons discovered at or after Ship ride the next change's branch instead; Ship must not write memory entries after finalize-review has generated the attestation.

**Related:** [[version-bump-on-every-pr]] — the version-bump arc whose discipline this lesson runs alongside.
