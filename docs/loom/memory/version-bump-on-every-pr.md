---
name: version-bump-on-every-pr
description: Proposal to change loom plugin versioning from "patch bump only when no station/field/rule/contract change" to "bump on every merged PR" — ensures every change reaches installed copies via `claude plugin update`
type: project
sources:
  - resource: user request 2026-09-21 — discussed during 2026-09-20-mechanical-calculations merge
---

**Proposed rule**: Every merged PR that touches a plugin must increment that plugin's version (patch by default; minor/major per semantic impact). Current rule: patch bump only when no station guidance, field, rule id, or contract manifest change (per CHANGELOG 3.7.2 entry).

**Why:**
- Current `claude plugin update` compares version string only; without bump, merged fixes never reach installed copies (3.7.2 bump PR #32 fixed this for #30 + #31 after they merged)
- Bump-on-every-PR eliminates "forgot to bump" class of release failures
- Keeps CHANGELOG as continuous record of every released change

**How to apply:**
1. Update `loom-code/scripts/test_write_plan_station_text.py` version assertion to allow bump on every PR
2. Modify version bump PR template to be standard for every change (not special-case)
3. Consider mechanization: pre-push hook or CI check that plugin.json version changed iff CHANGELOG has new entry
4. Per-change decision: patch vs minor vs major still follows semantic impact (station/field/rule/contract = minor; otherwise patch)

**Related:** [[version-bump-packets-must-name-changelog-entry]] — existing gotcha about requiring CHANGELOG entry in bump commits