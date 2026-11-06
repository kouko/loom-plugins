# W3-03 continuation 1 — author report

Same W3-03 task and initial attempt retained; prior W3-01 failures/counts and historical evidence are unchanged. This continuation repairs correctness and phase conflicts, not cosmetic output preferences.

## Diagnosis from actual traces

- `/tmp/loom-six-checks-trial/code-missing-date-candidate-r1.jsonl`: event/line 21 reads `no-intent-interview.md`; line 26 explicitly cats the entire `confirm-intent.md`; line 35 reads ready `confirmation-format.md`; final line 52 uses five headings and offers option B to confirm now and supply the required date later. The source interview explicitly eager-loaded the full confirmation reader, main Step 3 unconditionally ordered confirmation for open intents, and code Open questions omitted missing required content although design included it. These are competing source instructions consistent with the observed path; the trace does not prove a unique model-internal cause.
- `capture-csv-candidate-r1.jsonl`: line 18 batches interview, grounding and ready-format reads; project context is read at line 21; final line 46 admits two required value facts are missing but still uses all five ready headings. The design interview now returns before later readers and resumes Step 2 only when settled; required value fields and their current obligations remain unchanged.
- `capture-missing-date-candidate-r1.jsonl`: line 23 reads grounding; final line 29 states today's date is not the actual release date and would replace one incorrect value with another. The evidence establishes no reliable release date, not inequality. The shared unknown-date explanation now explicitly permits coincidence with today while requiring evidence; confirmation cannot supply that evidence.

Read the updated plan, current canonical acceptance report/evidence, and `/tmp/loom-correct-consistent-class-scan.json` before editing.

## Minimal design and preserved boundaries

- Removed eager full-confirmation loading from code-only no-intent interview. Its existing portable intent template supplies field boundaries instead, and Step 3 loads ready confirmation only after required facts are settled.
- Main code Step 3 now checks sufficiency before loading `confirm-intent.md`, retaining unresolved required content and refusing to treat yes as evidence. The already-confirmed fast path remains unchanged.
- Aligned code Open questions and both intent templates with design's existing missing-required-content blocker. No schema/field was added.
- Consolidated design's duplicate missing-fact sentences into the early return before confirmation preparation or later readers. Body remains exactly **3500 words**.
- Clarified the paired unknown-date explanation and made the existing six-check editing instruction phase-aware, without adding questions or a checklist layer.
- Added one concise note to each existing unreleased version section. Versions remain unchanged.

Rejected alternative: append more warnings beside the unchanged eager reader loads. That would preserve the competing instructions and add policy duplication. Moving complete ready composers into a new file was unnecessary and outside the bounded no-new-file design.

User-visible consequences narrow the invalid offered path: required facts must precede confirmation, and an unknown date must remain unknown rather than definitely different from today. Verified known dates, including a verified release date equal to today, remain eligible for ordinary ready confirmation. No implementation method, new guarantee, data-handling constraint, publication authorization or extra user decision was introduced. Complete-ready consequences, numbered anchors 2..6, publication/merge wording and publication-hold text remain unchanged.

## Red / green and verification

- Retained five regression instances in existing `loom-design/tests/spec/test_intent_drafting_fidelity.py`: incomplete code reader routing and missing-required-content parity across two owners and two templates. A newly added unknown-date prose pin was removed on root review because it mirrored the implementation; actual unknown/known-date host controls own that semantic verification. No style-label/checklist mirror test remains.
- Red before source changes: **5 failed / 48 passed** in that module. Design's existing blocker already passed; the eager route, code omission, both field-template omissions and unknown-date distinction failed.
- Intermediate broader checks found the legacy prose-anchor capitalization and the capture hard cap; repaired the prose/consolidated redundant instructions, without changing any legacy test, cap or exercised coverage.
- Final focused command after removing that new prose-only test: `python3 -m pytest -q loom-design/tests/spec/test_intent_drafting_fidelity.py loom-design/tests/spec/test_capture_intent_contract.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_write_plan_shape_text.py` → **157 passed in 0.40s**.
- `python3 loom-code/scripts/check_contract_citations.py` → passed, one known-violating file unchanged and no new citations.
- `git diff --check` → passed.
- All three portable reference pairs byte-identical; both intent field templates byte-identical. Existing complete-ready layout/examples were not edited. New relative template link resolves within the code plugin.

## Whole-class disposition and limits

The supplied class scan covers all **109** current changed paths plus relevant owner content. Live instances addressed: no-intent eager read, main open-intent route, code Open questions, both intent field templates, design early return, and the paired unknown-date explanation. Existing ready-reader guards and both six-question copies remain consistent. Other skill source instances concern optional diagrams, case examples or already-grounded source-scope rules and need no change for this defect class; historical observations and attestations are evidence rather than repair targets.

The default-invoice broad existing-data claim is another unsupported-certainty risk. Current shared grounding already requires evidence for every constraint and preservation claim and retains source targets/qualifiers; consequence disclosures still require examining actual existing-data actions rather than inferring safety from an internal-fix label. This repair adds no blanket no-data-effects guarantee or method ban. Root's default-invoice control must evaluate the actual new reply; source integrity tests cannot establish that behavior.

No evaluator-owned `test_capture_intent_contract.py`, old evidence, attestation or parent's plan edit was modified. No paid call, full suite, agent dispatch, commit, publication or merge was performed. Root owns the real repeated missing-date cases, known-date positive control, CSV case and invoice consent controls; no behavioral success is claimed here.
