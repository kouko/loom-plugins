# Build checks

## Scope

Change: 2026-11-16-codex-sandbox-network-recovery. Base: f82b358fabe781dfa929fa6a9a43f2ece0346e97. Production guidance repair is b813d790; release metadata is 03684a0f; adversarial reuse registration is 285eaf4b.

## Focused checks

- Implementer observed RED before the guidance fix: 1 failed, 10 passed (missing recovery section). Its focused GREEN run: 11 passed. These are the implementer's execution reports, not an independently reconstructed historical run.
- Release focused checks: 43 passed; manifest generation consistency check passed.
- Adversary ran `python3 -m pytest loom-code/tests/test_ship_station_text.py`: 11 passed. Six hostile guidance variants were rejected by the actual test module in temporary fixtures. This checks regression guards, not real host execution.
- `sync-trunk` before the adversary: up to date at 03684a0fe2cf55d2ef8276cc03a462921f09a558, containing origin/main f82b358fabe781dfa929fa6a9a43f2ece0346e97.

## Complete inventory attempt 1

Command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` through the permitted host execution mechanism.

Tested HEAD: 285eaf4b53af0ce305386e2a716ae2168743a5f9. Exit 1; code group: 1 failed, 2859 passed in 108.89 seconds. Later groups did not run.

Failure: `loom-code/tests/test_adversarial_batch2_loop_phrase_pin.py::test_batch2_files_after_prune_carry_no_loop_phrase_pin` found a forbidden loop-form phrase pin in `loom-code/tests/test_ship_station_text.py` at line 43. The newly added exact-sentence loop violated the existing regression guard. This is a test-program integration defect, not evidence of a production guidance failure.

The main agent searched both changed test modules in full for the defect class; the new loop was the sole flagged instance. The reused program's adversary was asked to preserve its protections while replacing the phrase pin with semantic assertions, then demonstrate original and overbroad mutations rejected by the updated program. Full inventory must pass after that repair before Closing Review.

## Repair and complete inventory attempt 2

Adversary-owned program repair: a3435949. Stock guard RED reproduced (1 failed, 1 passed); focused GREEN (13 passed). Against the committed program, nine hostile variants were rejected, including the original six, DNS overclaim, authentication escalation, and a broad-word substitution. Three equivalent rewrites passed. Restoring the original loop in a temporary committed-tree copy reproduced RED; reverting it restored GREEN. The trial programs remained temporary, not permanent harnesses.

At HEAD 6f6397a7e472061f0e97a955f5448566417bd608 the same complete inventory command exited 0. Code group: 2860 passed in 119.56 seconds. The remaining pytest groups and shell tests passed; one workflow group reported 250 passed and 5 skipped. The template validator parsed 13/13 Mermaid blocks. No skipped result is promoted to executed coverage. The temporary npm setup reported 3 audit vulnerabilities (2 low, 1 critical); this investigation did not assess or repair that existing dependency surface.

After the inventory, `python3 -m pytest loom-code/tests/test_ship_station_text.py` explicitly re-ran the adversarial program: 11 passed in 0.24 seconds. Closing Review's sync-trunk reported up to date at the same HEAD. Accepted reviewer-count JSON returned reviewer_floor 2 for this change.

No unresolved adversarial findings remain. No outside-vendor review was selected. Remaining checks belong to independent acceptance testing, fresh-context review and finalization; this Build evidence alone is not publication or merge evidence.
