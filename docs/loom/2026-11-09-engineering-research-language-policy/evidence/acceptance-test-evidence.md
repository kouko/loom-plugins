# Evidence-led search languages — acceptance test evidence

Tried on 2026-11-09, in a clean copy of the project at 771c79adf2eea39b8440e9ff83fa537384ccd37f.

## Clean setup and authorization

- Created a new clone with `git clone --no-hardlinks /private/tmp/loom-engineering-research-language-policy-delivery /private/tmp/loom-language-policy-acceptance-clean`, then `git checkout --detach 771c79adf2eea39b8440e9ff83fa537384ccd37f`. Output: `HEAD is now at 771c79adf test(engineering-research): reuse portable policy loading coverage`. Initial `git status --porcelain` was empty.
- Read root README Install/Development and skill README. The skill README links `SKILL.md` as runtime instructions. Used the explicitly authorized raw-skill loading surface instead of global plugin installation. Read the actual clean-copy `SKILL.md`, `references/research-methods.md`, `references/source-policy.md` and `templates/research.md`. This is explicit loading, not automatic routing or installed-host verification.
- No children were launched, no external model CLI invoked, no public searches made by this acceptance tester, no installation/publication/real Vault access performed. Public archived queries were inspected as evidence, not re-executed.
- Intent and spec were read before testing. Spec UI flows are N/A for this engineering guidance change. Each Acceptance line was walked in order. No implementation repair was made.

## 1. Exploratory defaults and exact identifiers

- How I tried it: extracted the two committed archives into a separate scratch directory after independently validating them. Inspected actual `custom_tool_call` entries in native JSONL traces, not just action summaries. Compared every candidate Markdown file with the clean formal runtime skill; all bytes matched.
- What came back: `first-trial/audit-packet/traces/C01/trajectory.jsonl:7` has separate English `small pull requests tradeoffs large pull requests empirical study code review size` and Japanese `小さい プルリクエスト 分割 デメリット コードレビュー 経験` entries in the same `search_query` array. C04 trace line 7 preserves `rime`, `save_options`, `key_binder` and `toggle` in initial English/Japanese discovery alongside Chinese. Supplemental S01 line 6 preserves `Leaf` and `2017`; S02 line 6 preserves `KakaoPay`, date and `Lettuce` while adapting surrounding language.
- Evidence: [first-trial archive](first-trial.tar.gz), members named above; [supplemental archive](supplemental.tar.gz). Current formal policy: `loom-code/skills/engineering-research/references/source-policy.md`, Search languages. Actual trace inspection supports bounded exemplars; not every identifier type or arbitrary future input was exercised.
- Result: works for demonstrated capability and retained exact-identifier guidance; no reliability or causal improvement claim.

## 2. Sufficient evidence and stopping

- How I tried it: explicitly invoked the clean raw skill for the bounded question: does this copy declare loom-code version 3.61.0 and load its language policy? Read the actual manifest and loaded policy. Local evidence settled that question; made no web call. Saved a complete research record in the clean scratch copy, then `cat` read its substantive contents and parsed all three local Markdown link targets.
- What came back: manifest `name: loom-code`, `version: 3.61.0`; policy text was readable via the existing skill reference. All three linked targets resolved to real files in the clean copy. The record contains question/conditions, method rationale, findings, provenance, decision impact and limitations. No search was added to satisfy a language count.
- Scratch record: `/private/tmp/loom-language-policy-acceptance-clean/docs/loom/2026-11-09-engineering-research-language-policy/research/acceptance-local-version.md`. Essential retained content: local inspection is sufficient; actual explicit source loading and stopping were observed; no installed-host, routing, search benchmark or compatibility conclusion is drawn.
- Prior actual traces: C02 lines 5 and 7 open Git official docs directly and contain no discovery query. C03 has no web call and reads the local manifest; its saved record and link target are read back. These are archived observations, not fresh reruns.
- Result: works.

## 3. Independent original languages and duplicated sources

- How I tried it: inspected original C04–C06 web actions, supplemental S01/S02 web actions and both supplemental independent audits. Read the unchanged formal source policy and the records' provenance/limits.
- What came back: C04 first round includes Chinese separately; C05 opens Korean original guidance directly; C06 opens Russian official documentation directly. S01 and S02 initially batch English/Japanese with Chinese and Korean respectively. S02 later refines a Korean title query. No English/Japanese-only stage followed by adding a previously unused language is present in those trajectories.
- The records attribute first-party material and do not count its translations as separate corroboration. The initial S01 evidence explicitly notes differing-version English/Japanese MySQL manuals are related documentation, not independent confirmation. However, no adversarial translation-duplication case demonstrates actual rejection of misleading duplicate support. The delayed-language branch is also unobserved.
- Evidence: archive traces C04:7, C05:5, C06:5, S01:6–9, S02:6–11; [A01](audits/A01.md), [A02](audits/A02.md). C06's Online Read-Only JDBC completeness disagreement is preserved; original-language reading does not prove answer completeness.
- Result: partly, for the unobserved delayed-expansion and translation-duplication handling paths. This is a coverage boundary, not a reproduced policy defect.

## 4. Honest supplemental observations

- How I tried it: read both archived task prompts and initial-evidence files, actual query/open calls, saved note readbacks, audits A01/A02 and [observations](observations.md). Neutral tasks ask for the historical Leaf buffering rationale and KakaoPay lock-choice rationale/safety boundary. They contain no required search language and no target original-page URL.
- What came back: real supplied concept evidence does not answer either author-attribution question. Both executors include the relevant source language initially and inspect the applicable original. S02 has later Korean refinement and an inaccessible AI Briefing page, not manufactured English/Japanese failure. Both notes were saved and fully read back. Two separate advisory auditors independently inspect the frozen packet and reopen public primary material; their findings remain separate.
- Both audits retain S02's inability to attribute aggregate search returns to individual initial languages. A02 also retains S01's malformed `site.tech.meituan.com` operator. Original notes are unchanged; [observations](observations.md) corrects the supported interpretation without rewriting them.
- Result: works. The acceptance asks for truthful observations and separation of expansion/adequate alternatives/unverified paths; it does not require a manufactured successful delayed expansion.

## 5. Evidence continuity and limits

- How I tried it: used Python standard-library `hashlib`, `json`, `tarfile` to check each archive SHA-256, exact ordered member inventory, regular-file status, size and every member SHA-256 before extracting with `filter="data"`. Separately recomputed all `hashes` in both prospective freezes and `files` in both audit-packet freezes. Compared candidate Markdown with formal skill bytes. Resolved every local link in the original report within extracted archive namespace. Read original report/cold-reader content and audited findings.
- What came back:

```text
first-trial 122 archive and every member independently verified
supplemental 47 archive and every member independently verified
first-trial prospective and audit packet freezes verified
supplemental prospective and audit packet freezes verified
freeze hashes checked 83 candidate Markdown byte parity; original report local links 48 verified
```

- Original report member: `first-trial/workspace/docs/skill-dogfood/2026-11-09-engineering-research-language-policy/report.md`. All C01–C06 cases, both JSON audits, cold reader, frozen candidate and source-return supplement remain available. A01's medium C06 JDBC finding and A02's differing completeness judgment are not collapsed or treated as resolved. Cold-reader standalone-root/review-entry/cleanup concerns remain visible. The document-write guard incident remains a recovered host incident, not a new policy failure.
- Historical `supplemental/verify_evidence_integrity.py` contains its original absolute base path. It was not claimed runnable in an arbitrary checkout and was not executed; the independent checks above do not rely on it. This independent check does not repeat every original provenance/allowlist assertion.
- Result: works for preservation and inspectability. No improvement, reliability, automatic activation or all-host claim is made.

## 6. Portable formal integration and existing workflows

- How I tried it: followed clean skill README to raw instructions and references, performed the bounded local-evidence task in section 2, and ran only the relevant package and release-pin test modules in the clean copy:

```sh
env UV_CACHE_DIR=/private/tmp/loom-uv-relative-cache uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/engineering-research/test_package.py loom-code/tests/test_write_plan_station_text.py -q
```

- Actual captured output (exit 0):

```text
................................................                         [100%]
48 passed in 0.16s
```

- Read `git diff 11b962b7f2c83f397c52d0753fd890ffec06e74b HEAD -- loom-code/skills/engineering-research`: the only runtime change is the Search languages paragraph. Existing source acceptance, authorization, repository inspection, recording, readback and stopping contracts remain. Source loading, metadata synchronization and existing workflow contracts have focused executable coverage; actual general workflows and other hosts were not end-to-end rerun.
- The full suite is not skipped. It belongs to the automated acceptance-blocking check run by `finalize-review`, which will execute `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. Its future result is not prefilled here. Build logs were handed over by the station, but are not relabeled as this tester's clean execution.
- Result: works within explicit loading and focused coverage; no installed-host/automatic-routing claim.

## Findings and decisions

- No new fatal or important implementation defect was reproduced. No dismissed important-or-higher finding was supplied by the station.
- Preserved low-severity supplemental findings: S02 per-query provenance is partial; S01 domain restriction syntax is malformed. Neither is silently repaired or dismissed.
- Retained coverage uncertainty: delayed Chinese/Korean expansion and active rejection of translated duplicates are not demonstrated; row 3 is partly.
- Existing original C06 factual disagreement is an unresolved case-output finding, not evidence that the new language policy caused it.
- Chose explicit raw loading instead of unauthorized global installation, and existing archive inspection instead of a repeated broad benchmark. No skipped-by-instruction entry appears in plan Risks or intent Constraints.

## Reproducibility of independent archive checks

The inventory check iterates `first-trial` and `supplemental`: load `<stem>.inventory.json`; assert SHA-256 of the named archive; open it with `tarfile`; assert the ordered member names equal `members[].path`; for each zipped entry assert regular file, read bytes, compare `size` and SHA-256. Extract only after all checks pass. For each extracted root, load `freeze.json` and recompute each relative `hashes` entry, then load `audit-packet-freeze.json` and recompute each `files` entry relative to `audit-packet/`. The exact source data are the committed inventory/freeze files, not the historical verifier's absolute directory.

## Re-run on 2026-11-09, at 03b1aedf488852f8e3375cf6d6a80f449a180296

### Clean setup and fix-diff audit

- Created another fresh clone: `git clone --no-hardlinks /private/tmp/loom-engineering-research-language-policy-delivery /private/tmp/loom-language-policy-acceptance-clean-round2`; then `git checkout --detach 03b1aedf488852f8e3375cf6d6a80f449a180296`. Output: `HEAD is now at 03b1aedf4 docs(loom-code): record supported finalizer command repair`. Initial porcelain status was empty.
- Inspected the complete fix diff `ceaab3c2fc04b0e7504a704ad73646271cbb626c..03b1aedf488852f8e3375cf6d6a80f449a180296`. Exactly two changed paths: `plan.md` and [finalize-command-repair.md](finalize-command-repair.md), within this change. Runtime skill, maintained tests, release metadata, archived cases and prior acceptance evidence are unchanged.
- Rechecked root README installation/development instructions and skill README runtime link, then actually read the clean `SKILL.md`, research methods, source policy and record template. Explicit raw loading remains the authorized setup; no global installation or installed-host/routing claim.

### Per-row carry-over audit

- 1: carried over — Search-language instructions, exact identifiers and prior actual query traces are untouched by this two-document command-invocation repair. No new external exploratory search is claimed.
- 2: carried over — Sufficiency/stopping rules and prior local/official-source observations are untouched. The current setup check does not relabel previous behavior as freshly observed discovery.
- 3: carried over — Original-language and translation guidance plus all eight trajectories are untouched. The partly result retains both delayed expansion and active duplicate-translation handling as unobserved.
- 4: carried over — Supplemental neutral tasks, initial evidence, actual actions, saved notes and both independent assessments are untouched. No manufactured failed search or forced language selection was added.
- 5: carried over — Both archives, inventories, freezes, original six cases, audits, cold reader and limitations are untouched. The earlier integrity checks and unresolved disagreement remain historical results; they were not rerun or silently revised.
- 6: re-tested — The validation invocation is the only affected surface. Re-tested explicit source loading, bounded research retention/readback, installed command recognition, focused policy package tests and the full release-pin/station module in the new clean copy. No full package suite was run by this acceptance tester.

### Row 6 actual execution and retained record

Read the actual installed `loom_checker/probes.py` path named in the repair record. In the locked isolated environment, called `command_executes_artifact` with the historical env-prefixed string and the direct uv string against `loom-code/tests/engineering-research/test_package.py`:

```text
env-prefixed recognized: False
direct uv recognized: True
```

Both assertions completed with exit 0. This reproduces declaration recognition only; it does not claim finalization succeeded. The historical refusal was before tests, rather than a failed package test, and remains retained in the linked repair record.

Executed from the new clean clone:

```sh
UV_CACHE_DIR=/private/tmp/loom-uv-relative-cache uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/engineering-research/test_package.py loom-code/tests/test_write_plan_station_text.py -q
```

The cache setting is supplied by the shell launcher, while the executable declaration being recognized begins with `uv`. Actual output, exit 0:

```text
................................................                         [100%]
48 passed in 0.15s
```

Saved scratch record: `/private/tmp/loom-language-policy-acceptance-clean-round2/docs/loom/2026-11-09-engineering-research-language-policy/research/acceptance-command-revalidation.md`. Read the whole saved record with `cat`: it states the new tested commit, question, local-inspection rationale, unchanged runtime, actual focused command results, recognition boundary, decision impact and untested paths. Resolved all three relative evidence links to the intended clean-copy skill, policy and repair record; all returned true. No web search was needed to settle this local question, and no unauthorized external action occurred.

Full-suite Build round 2 output was supplied separately by the station (4139 passed, 6 skipped); this tester did not run or independently recalculate it and does not substitute it for the required finalizer execution. The full suite is not skipped, and finalization will run it again and block on failure. No future finalizer result is asserted. No important-or-higher dismissed finding was supplied. No new fatal or important defect was reproduced; all prior limitations remain.
