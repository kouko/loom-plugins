# Decision Map Python boundaries — plan
intent: 2026-10-30-python-implementation-refactor@9ee31084df1337cc7419475c98e2b08c48c63f9a
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/decision-map/scripts/start_delivery.py:127` starts a delivery binding and writes MAP.md plus an intent.
- Reverse: `loom-workflow/skills/decision-map/scripts/map_store.py:35` re-exports validation symbols; sibling mutations call them through that facade.
- Error: `loom-workflow/skills/decision-map/scripts/map_close_transaction.py:125` converts structural validation failures to transaction errors.
- Data: `loom-workflow/skills/decision-map/scripts/map_store.py:225` edits Notes text; its writer preserves atomic compare-and-swap behavior.
- Boundary: `loom-workflow/tests/decision-map/test_map_module_boundaries.py:77` pins facade identity; later tests pin the legacy fault-injection seam.

## Task DAG

### Wave 1 — Give validation calls their owner

**W1-01 Direct validation ownership in ticket and close operations**  after: none  acceptance: 1, 2, 3
- Files: `loom-workflow/skills/decision-map/scripts/map_close_transaction.py` (entry `_close_and_rechart_locked`), `loom-workflow/skills/decision-map/scripts/map_ticket_mutations.py` (entries `_claim_ticket_locked`, `_update_blockers_locked`), `loom-workflow/tests/decision-map/test_map_module_boundaries.py`, `loom-workflow/tests/decision-map/test_map_transaction.py`
- Test: A1 positive: validation-owner-import; boundary: legacy-facade-still-works. A2 positive: existing-close-and-claim; negative: invalid-ticket-refusal. A3 positive: boundary-and-suite-pass; negative: no-new-forwarder.
- Risk: agent-decided — import existing validation owners directly; preserve `test_map_module_boundaries.py` identity and `test_map_transaction.py` fault-injection coverage rather than deleting compatibility exports.

### Wave 2 — Use the existing writer boundary for delivery binding

**W2-01 Remove private store calls from delivery binding**  after: W1-01  acceptance: 1, 2, 3
- Files: `loom-workflow/skills/decision-map/scripts/start_delivery.py` (entry `start_delivery`), `loom-workflow/skills/decision-map/scripts/map_store.py` (existing store operations), `loom-workflow/tests/decision-map/test_start_delivery.py`, `loom-workflow/tests/decision-map/test_map_module_boundaries.py`
- Test: A1 positive: delivery-owner-boundary; boundary: no-extra-public-entry. A2 positive: same-binding-bytes; negative: conflicting-intent-refusal. A3 positive: focused-and-suite-pass; negative: no-forwarder-added.
- Risk: agent-decided — retain `map_store.py` compatibility and the existing atomic writer seam; `test_start_delivery.py` covers created, reused, and refused bindings.

### Wave 3 — Release the verified change

**W3-01 Synchronize loom-workflow release metadata**  after: W2-01  acceptance: 3
- Files: `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`, `loom-workflow/{plugin,package}.json`, `loom-workflow/CHANGELOG.md`, `loom-workflow/README*.md`, `README.md`, `loom-workflow/tests/scripts/test_release_metadata.py`
- Test: A3 positive: synchronized-release-and-suite; boundary: prior-version-pin-updated.
- Risk: agent-decided — patch version; derive the other manifests with the repository sync script before final review so installed copies receive the refactor.

## Simplicity check
- none found

## Questions asked
1 — what — 這一批完成時，你希望整理涵蓋所有 Loom 插件中的 Python 工具，還是先完成最影響維護的核心工具？
1 — what — 這是你要的第一批嗎？

## Risks
1. Existing tests intentionally preserve private facade symbols and fault-injection seams. Removing exports would change compatibility and force unrelated callers to migrate.
2. Direct imports must preserve the current exception ordering, output, and atomic write behavior; compare valid and invalid fixtures before and after.
