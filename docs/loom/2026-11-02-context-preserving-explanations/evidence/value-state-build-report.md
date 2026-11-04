# W3-03 continuation 2 — author report

Same W3-03 task, initial attempt, continuation 1 and all W3-01 history retained. This is a factual-state and source-agreement repair, not a retry reset or cosmetic pass. Read the updated canonical report/evidence and the supplied 119-path `/tmp/loom-value-state-class-scan.json` before editing.

## Actual diagnosis

- Both inspected code fixtures contain `Release date: to be corrected`, with no calendar day. In `code-missing-date-candidate-r1.jsonl`, Write event/line 45 saves “Readers are told the wrong date for when that version became available”; public reply event 51 accurately identifies the missing date. In `code-known-date-candidate-r1.jsonl`, Write event 47 saves “readers are told the wrong day this version became available”; public reply event 54 again identifies the non-date text. Read both saved intent files directly as well as their source RELEASE_NOTES. Supplying a verified correction changes the desired value, not what the current field contains.
- `capture-missing-date-candidate-r2.jsonl`, assistant event 29, proposes TBD and says readers know the date has not been announced and will not be misled. Unknown correct date provides neither announcement history nor measured reader understanding. This was a proposal, not an observed unapproved edit or publication.
- Shared Unknown date Context itself said “release notes show an incorrect date,” conflating a reported shorthand with the inspected missing-value state. Both generic Problem producers and field templates required a consequence without expressly distinguishing observed state from inferred effects. The existing six-check instruction inspected only the proposed reply, allowing an inaccurate delivered intent to coexist with accurate public prose. These source features are consistent with the observed failures; they do not prove a unique internal model cause.

## Minimal repair

- Replaced the paired Unknown date Context with the exact non-date field text and the user's reported shorthand. Good explicitly describes the observed missing date and waits for evidence. Bad now also demonstrates the unsupported wrong-calendar-day, non-announcement and reader-understanding claims, with an explanation of why they fail.
- Revised the Problem instruction in both actual owners and both existing intent field templates: ground present state and effects in evidence, distinguish absent values from incorrect values, keep reported symptoms distinct from inspected observations, and leave unsupported effects unresolved. A local observation does not silently overwrite a separately reported production symptom. Existing no-diagnosis/no-fix and product-identifier boundaries remain.
- Replaced question 2, retaining six private questions, to inspect agreement between the proposed reply and delivered intent, when written, on evidence-backed facts, scope, constraints and guarantees. This does not require a draft for a blocked interview. No extra checklist or workflow step.
- Expanded the existing unreleased continuation note in both changelogs; versions unchanged.

Rejected alternatives: adding a seventh check would duplicate policy without correcting the priming example/field producer; banning all “wrong date” claims would break legitimate inspected wrong-calendar-value cases; adding a TBD decision would change the original requested correction and still fail to establish the required fact. The existing interview already directs unavailable-fact cases to explain the blocker and wait, so no released workflow/style-card change is necessary.

## Whole-class disposition

The supplied scan covers 119 changed paths. Live repair instances are the two Unknown date scenario copies, both Problem producers, both Problem field templates and the six-check source-agreement question. Current ready-format impact guidance already says “supplied impact”; it needs no duplicate rule. The optional Known correction examples describe an actual old date with a supplied outdated impression, so they remain valid and unchanged. Existing interview questions ask for facts rather than declaring unsupported reader effects. Existing unknown-value equality/inequality protections and continuation 1 routing fixes remain intact.

Publication status is separate from knowledge of a date, and missing date evidence supplies no guarantee about readers. The revised counterexample makes that distinction explicit. A known incorrect ISO day with a verified replacement remains eligible to be described as wrong; a non-date field with a verified replacement remains a missing-current-value case. Root's planned controls must verify actual new outputs over both situations.

No source outside the bounded owners, paired references/templates and existing unreleased notes changed. Historical observations, acceptance reports/evidence, attestation, evaluator-owned tests and root's plan edit remain untouched.

## Verification and test decision

No new test was added: this bounded repair changes prose interpretation and source-to-output semantics, without a new executable route, field, schema or rule. A phrase-pin test would merely mirror the new prose. Existing structural tests check portable pairing, phase separation, required obligations and hard caps; actual root-owned host trials must evaluate factual correctness and intent/reply agreement.

- First existing focused run: 156 passed / 1 failed because the revised capture body exceeded 3500 words. Reworded only that edited Problem instruction, preserving the file-list restriction; no cap or test weakened.
- Final command after root's bounded wording review: `python3 -m pytest -q loom-design/tests/spec/test_intent_drafting_fidelity.py loom-design/tests/spec/test_capture_intent_contract.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_write_plan_shape_text.py` → **157 passed in 0.39s**.
- `python3 scripts/sync_codex_manifests.py --check --all` → exit 0.
- `python3 loom-code/scripts/check_contract_citations.py` → exit 0; one pre-existing known violation unchanged, no new citations.
- `git diff --check` → exit 0.
- All three portable reference pairs and both intent templates remain byte-identical. Capture body is exactly **3500 words**.

No paid calls, full suite, agent dispatch, commit, publication or merge performed. Complete-ready consent, publication holds, prior phase fixes and known-value confirmation remain unchanged. Behavioral success is pending root's real cases; green structural checks do not establish the factual/logical floor passed.
