# Independent masked audit 1 — completed frozen coverage
**Current coverage: X001–X012, 12/12 actors, six cases, 108 raw criterion votes (104 supported; 4 not-applicable), 0 substantiated material findings. Advisory only; no global dogfood pass or revision preference. Earlier coverage paragraphs below are retained audit checkpoints.**

Covered X001–X005 (5/12), cases C02, C03 and C06. These are per-actor advisory votes, not a global pass. No substantiated material functional defect found in this covered batch.

Requested model: `gpt-6.1-sol`, effort `medium`. Backend identity remains unverified (`server_confirmed_model: null`). No arm map, other auditor, activation, history or preferred-revision material was read. Contract contents can still make masking imperfect.

## Raw per-actor votes

| Actor | Case | R1–R9 |
|---|---|---|
| X001 | C02 | supported for each criterion |
| X002 | C06 | supported for each criterion |
| X003 | C03 | supported for each criterion |
| X004 | C02 | supported for each criterion |
| X005 | C03 | supported for each criterion |

## Evidence and trajectory

### X001 (C02)

- **R1: supported** — execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:13-23 preserves no-tests/no-duplicate-discovery and partial snapshot.
- **R2: supported** — execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:25-33/26-40 chooses source inspection plus one permitted bounded experiment.
- **R3: supported** — execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:35-93/42-95 traces builder, main, sys.path and Git helpers; fixture runner:47-49,116-150,153-180 supports claims.
- **R4: supported** — execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:104-123 (X001) or 97-121 (X004): no-change direct reuse, small CLI branch, rejects separate discovery/rewrite with concrete reason.
- **R5: supported** — execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:49-60 (X001) or 57-60,123-144 (X004) limits empty fixture result; no claimed full-suite correctness or speed.
- **R6: supported** — execution/X001/events.jsonl:26 (X001) or :20 (X004) executes python3 -I -B scratch/preview_package_commands.py once; script imports real runner, one builder call, prints only.
- **R7: supported** — execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:1-9 required flat metadata; all local file targets exist; execution/X001/events.jsonl:30 (X001), :25 and :29 (X004) actual readback.
- **R8: supported** — execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:125-147 (X001) or 123-152 (X004) distinguishes environment-dependent plan, missing dependencies, later state and unverified runtime.
- **R9: supported** — execution/X001/events.jsonl:13 (X001) or :9 (X004) loads required resources; no diagram used. X001 test read (:12) precedes resource completed event (:13), an ordering deviation without demonstrated functional impact.

### X002 (C06)

- **R1: supported** — execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:13-19 correctly rejects source definitions as approval for current HEAD release.
- **R2: supported** — execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:21-25 direct connected evidence assessment fits completion claim, not unnecessary experiment.
- **R3: supported** — execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:31-64 traces commands, failure, inventory, definition weaknesses and missing workflow files; fixture sources and tests support it.
- **R4: supported** — execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:81-92 common evidence targets for withholding approval; no numerical scores or false mandatory service targets.
- **R5: supported** — execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:39-49 explicitly distinguishes defined assertions/hash consistency/research process exits from executed successful CI.
- **R6: supported** — execution/X002/events.jsonl:5-21 reads/hash/path checks and record creation/readback only; no tests, remote query or release.
- **R7: supported** — execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:1-9 metadata; all linked files exist; execution/X002/events.jsonl:21 actual readback. #L source anchors are hosting-specific, textual spans retain navigation.
- **R8: supported** — execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:83-98 exact candidate, full workflows/inventory/env and revision-linked runs/artifacts required; approval remains human decision.
- **R9: supported** — execution/X002/events.jsonl:9 actual methods/source/evaluation/template reads, :11/:14/:16 source connected path and applicability checks. No diagram.

### X003 (C03)

- **R1: supported** — execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:13-21; execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:13-21 frames both accidental foreign execution and Git failure under read-only constraints.
- **R2: supported** — execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:19-21; execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:19-21 separately traces trust boundary and failure propagation; framework names not required.
- **R3: supported** — execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:25-54; execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:25-53/58 matches fixture runner:123-149, repo_files:73-146, git_exec:50-88, tests:128-184,260-331.
- **R4: supported** — execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:56-66 or 58-66; execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:55-65 or 60-68 compares conditional retention, outside-root placement, discovery/pruning and fail-stop proposals without unsupported scores.
- **R5: supported** — execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:25-42; execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:25-43 explicitly static source conclusions and plausible/runtime boundaries, no exploit reproduction or inferred measured outcome.
- **R6: supported** — execution/X003/events.jsonl command trajectory only reads/search/hash/path checks, mkdir and note creation; no runner/Git/test invocation.
- **R7: supported** — execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:1-9 and execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:1-9 required metadata, question split, relative cross-links exist; execution/X003/events.jsonl:22 (X003) or :18 (X005) actual full readback and link ls.
- **R8: supported** — execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:56-66; execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:55-65/60-68 preserves ignored clone, unrelated worktree, explicit target and external-policy unknowns; recommendations remain unimplemented.
- **R9: supported** — execution/X003/events.jsonl:9 (X003) or :7 (X005) actual required method/source/template reads; X003 also loads conditional evaluation selection. No diagram.

### X004 (C02)

- **R1: supported** — execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:13-23 preserves no-tests/no-duplicate-discovery and partial snapshot.
- **R2: supported** — execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:25-33/26-40 chooses source inspection plus one permitted bounded experiment.
- **R3: supported** — execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:35-93/42-95 traces builder, main, sys.path and Git helpers; fixture runner:47-49,116-150,153-180 supports claims.
- **R4: supported** — execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:104-123 (X001) or 97-121 (X004): no-change direct reuse, small CLI branch, rejects separate discovery/rewrite with concrete reason.
- **R5: supported** — execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:49-60 (X001) or 57-60,123-144 (X004) limits empty fixture result; no claimed full-suite correctness or speed.
- **R6: supported** — execution/X004/events.jsonl:26 (X001) or :20 (X004) executes python3 -I -B scratch/preview_package_commands.py once; script imports real runner, one builder call, prints only.
- **R7: supported** — execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:1-9 required flat metadata; all local file targets exist; execution/X004/events.jsonl:30 (X001), :25 and :29 (X004) actual readback.
- **R8: supported** — execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md:125-147 (X001) or 123-152 (X004) distinguishes environment-dependent plan, missing dependencies, later state and unverified runtime.
- **R9: supported** — execution/X004/events.jsonl:13 (X001) or :9 (X004) loads required resources; no diagram used. X001 test read (:12) precedes resource completed event (:13), an ordering deviation without demonstrated functional impact.

### X005 (C03)

- **R1: supported** — execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:13-21; execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:13-21 frames both accidental foreign execution and Git failure under read-only constraints.
- **R2: supported** — execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:19-21; execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:19-21 separately traces trust boundary and failure propagation; framework names not required.
- **R3: supported** — execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:25-54; execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:25-53/58 matches fixture runner:123-149, repo_files:73-146, git_exec:50-88, tests:128-184,260-331.
- **R4: supported** — execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:56-66 or 58-66; execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:55-65 or 60-68 compares conditional retention, outside-root placement, discovery/pruning and fail-stop proposals without unsupported scores.
- **R5: supported** — execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:25-42; execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:25-43 explicitly static source conclusions and plausible/runtime boundaries, no exploit reproduction or inferred measured outcome.
- **R6: supported** — execution/X005/events.jsonl command trajectory only reads/search/hash/path checks, mkdir and note creation; no runner/Git/test invocation.
- **R7: supported** — execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:1-9 and execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:1-9 required metadata, question split, relative cross-links exist; execution/X005/events.jsonl:22 (X003) or :18 (X005) actual full readback and link ls.
- **R8: supported** — execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md:56-66; execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-git-failures.md:55-65/60-68 preserves ignored clone, unrelated worktree, explicit target and external-policy unknowns; recommendations remain unimplemented.
- **R9: supported** — execution/X005/events.jsonl:9 (X003) or :7 (X005) actual required method/source/template reads; X003 also loads conditional evaluation selection. No diagram.

## Concrete cross-checks

- X001 note lines 62–69: “construction is not free of subprocesses” and “Git failures can produce empty exclusion lists”; X004 lines 50–55 independently preserve the same boundary. Fixture runner lines 123 and 146–149 call the union and append ignores; repo_files lines 86–88 and 115–117 convert missing query data to empty exclusions.
- X001 events line 26 and X004 line 20 show `python3 -I -B scratch/preview_package_commands.py`; actual stdout contains the three npm/node/bash vectors. Scratch scripts contain one builder call and printing, no returned-command execution. This is bounded feasibility, not passing tests.
- X003 failure note line 25: “It is fail-open with respect to foreign-test exclusion”; X005 failure note line 25: “Partial query failure can retain partial protection.” Fixture git_exec lines 77–83 returns `None`; fixture repo_files lines 87–88 and 116–117 return `[]`. The notes retain this as static source reasoning, not a verified exploit.
- X002 note line 15: “actual CI success and release readiness remain unresolved”; lines 39–49 distinguish test definitions and timing research receipts from CI results. Fixture tests lines 187–197 only assert command substrings in workflow files absent from this snapshot.
- Hash comparisons establish all twenty actor source files match the four frozen fixture source files. All retained-note relative file targets resolve. Source line-fragment compatibility across editors was not established.

## Findings

No material defect finding in the first five actors. No skill-gap claim is inferred from actor count. X001 loads test evidence before the required resources complete (events lines 12–13); this small ordering variance has no demonstrated functional consequence and is not promoted into a functional defect.

## Limitations

- Partial coverage: five completed actors only; C01/C04/C05 not yet covered. No global dogfood pass or arm preference can be inferred.
- Requested gpt-6.1-sol medium is recorded; receipt server_confirmed_model is null, immutable backend identity unknown.
- Masking hides arm assignment but contract text differences may permit inference; no private arm map consulted.
- One auditor advisory source/trajectory review, no execution replay, external query, install, CI or production validation.
- Readback/file-link checks establish retained artifact integrity, not semantic correctness by themselves. Source #L fragments in X002 are host-dependent; no cross-editor renderer check.
- Minor resource-loading ordering variance in X001 has no demonstrated functional consequence; not counted as a defect.

## Coverage update: X006 and X008

Covered 7/12 actors; 63 raw criterion votes; no material findings. Prior votes unchanged. C04 remains unaudited.

### X006 (C05)

- **R1: supported** — execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md:13-17 hypothetical relocation only, no active change or original edits.
- **R2: supported** — execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md:19-21 document/path/hash analysis fits Markdown move; no copied database procedure.
- **R3: supported** — execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md:25-63 seven exact URLs, anchor lines, both manifests and differing extraction/full-note hashes.
- **R4: supported** — execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md:65-73 retains current general location as smallest option and offers staged relocation only if needed.
- **R5: supported** — execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md:39-52 and :81-83 distinguishes path/line/hash observations from rendering, authenticity and full-note/runtime claims.
- **R6: supported** — execution/X006/events.jsonl:14 read-only Python path/hash operations, :16 bounded grep; receipt added files contains only new report.
- **R7: supported** — execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md:1-9 metadata, :69-79 preserve dates/provenance with planned update and rollback; execution/X006/events.jsonl:21 actual full readback/path verification.
- **R8: supported** — execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md:75-83 stop on mismatch/collision, rollback before acceptance; after dependents account for concurrent edits and consumers.
- **R9: supported** — execution/X006/events.jsonl:9 reads methods/source/template before evidence; no diagram; path calculations 7 old exist, 0 unchanged new exist, 7 repairs preserve identities.

### X008 (C01)

- **R1: supported** — execution/X008/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:15,23-28 exact four roots in source order.
- **R2: supported** — execution/X008/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:17-19 direct fact check, no forced matrix/framework.
- **R3: supported** — execution/X008/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:30-34 tuple line 53 and consumers; actual source hash in execution/X008/events.jsonl:10.
- **R4: not-applicable** — No alternative-selection question.
- **R5: not-applicable** — No causal, performance, quality or cost claim.
- **R6: supported** — execution/X008/events.jsonl:7,:10 only source/read/hash; no experiment, tests or diagram. Note is 42 lines including required template headings.
- **R7: supported** — execution/X008/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:1-9 flat metadata; local targets resolve; execution/X008/events.jsonl:14 full readback plus target checks.
- **R8: supported** — execution/X008/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:38-42 source tuple settled, directory existence/CI/deployment/later revisions unverified.
- **R9: supported** — execution/X008/events.jsonl:7 skill/source, :10 methods/source/template. Source preceded method-read ordering but no functional consequence; direct fact conditional evaluation resource reasonably not triggered.

X006 note line 25: “Adding one `../` to each source link restores the same target paths in this layout.” Independent path arithmetic confirms seven old targets exist, seven unchanged new targets fail, and seven repairs normalize to their original identities. Note line 50 explicitly distinguishes the full original hash from extracted bytes; line 39 preserves untested renderer behavior. X008 accurately lists the literal tuple and makes no CI or runtime claim.

## Coverage update: X007 and X009

Covered 9/12 actors; 81 raw criterion votes; no material findings. Prior votes unchanged.

### X007 (C05)

- **R1: supported** — execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md:13-17 preserves hypothetical move/no original edits/no active change.
- **R2: supported** — execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md:19-21 fits document migration with direct path/hash inspection, not database rollout.
- **R3: supported** — execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md:25-56 all seven path calculations, exact anchors, eight hashes and extraction provenance distinguish what was actually checked.
- **R4: supported** — execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md:58-65 retaining general record is smallest option; future migration has common preservation criteria.
- **R5: supported** — execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md:37-41,75 separates path/line/hash observation from renderer/historical authentication or runtime.
- **R6: supported** — execution/X007/events.jsonl events :12 read-only Python/nl/rg, :17 readback/hash/path only; receipt adds only new report.
- **R7: supported** — execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md:1-9 flat metadata; 62-71 preserve history/dates, inbound/outbound links; events :17 actual readback.
- **R8: supported** — execution/X007/artifacts/docs/loom/research/2026-11-08-research-note-migration.md:67-75 stop/recovery bounds include intervening changes/consumers and full-note limitations.
- **R9: supported** — execution/X007/events.jsonl events :9 loads all conditional resources, :12 connected evidence, :17 full record and preserved source checks; no diagram.

### X009 (C01)

- **R1: supported** — execution/X009/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:15,23-28 exact four roots in source order.
- **R2: supported** — execution/X009/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:17-19 direct fact check, no forced matrix/framework.
- **R3: supported** — execution/X009/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:30-34 tuple line 53 and consumers; actual source hash in execution/X009/events.jsonl:9.
- **R4: not-applicable** — No alternative-selection question.
- **R5: not-applicable** — No causal, performance, quality or cost claim.
- **R6: supported** — execution/X009/events.jsonl:7,:9 only source/read/hash; no experiment, tests or diagram. Note is 42 lines including required template headings.
- **R7: supported** — execution/X009/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:1-9 flat metadata; local targets resolve; execution/X009/events.jsonl:13 full readback plus target checks.
- **R8: supported** — execution/X009/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:38-42 source tuple settled, directory existence/CI/deployment/later revisions unverified.
- **R9: supported** — execution/X009/events.jsonl:7 skill/source, :9 methods/source/template. Source preceded method-read ordering but no functional consequence; direct fact conditional evaluation resource reasonably not triggered.

X007 note line 41: “it must not be represented as the complete original note or expected to match its historical full-note digest”; lines 62–71 preserve future staging, acceptance, rollback and unchanged historical provenance. X009 note line 32 quotes the exact source tuple and line 42 retains the CI/runtime boundary. No migration was performed.

## Coverage update: X010 and X011

Covered 11/12 actors; 99 raw criterion votes; all six case types covered. No material findings. Prior votes unchanged. X012 remains outstanding.

### X010 (C06)

- **R1: supported** — execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:13-19 refuses CI/release inference, scope is four-file snapshot, no acceptance authorization.
- **R2: supported** — execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:21-25 direct source tracing answers completion claim, no required experiment.
- **R3: supported** — execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:31-56 exact entry path, inventory, union, silent Git failure, subprocess boundary and test-definition limits.
- **R4: supported** — execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:77-89 missing evidence relates to actual same-revision workflow/run/inventory/artifact criteria; no invented scores.
- **R5: supported** — execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:44-52 and 73-75 source/hash/research-exit observations do not establish tests/CI passed.
- **R6: supported** — execution/X010/events.jsonl events :5-27 only reads/search/hash/path and record creation/readback; no remote/testing/publish.
- **R7: supported** — execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:1-9 metadata, link targets resolve; events :27 reads actual saved record and checks 23 links.
- **R8: supported** — execution/X010/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:79-95 same candidate/results/env/packaging links missing; no false green or release approval.
- **R9: supported** — execution/X010/events.jsonl events :9 loads required resources, :14,:16,:20,:22 connected source/tests and hashes; no diagram.

### X011 (C04)

- **R1: supported** — execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:13-17 preserves causal/universal/quality/cost question and no new measurements.
- **R2: supported** — execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:19-23 controlled-comparison adequacy fits historical unmatched tasks, no runtime source-code investigation needed.
- **R3: supported** — execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:29-61 exact receipt values and actual task-scope summary inspected, extraction provenance limits retained.
- **R4: supported** — execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:69-80 common task-specific quality/cost/time criteria and matched work; quality guardrails cannot be compensated by speed.
- **R5: supported** — execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:27-51 confounded task scopes, no quality ratings or currency cost, different cache categories; arithmetic 103.188 - 42.637 = 60.551, approximately 58.7% correct.
- **R6: supported** — execution/X011/events.jsonl events :7,:9,:11,:16,:18 only reads/inventory/path checks and note creation; no model/test rerun or invented observations.
- **R7: supported** — execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:1-9 metadata, all local links resolve; events :16 full saved-record readback, :18 source link targets ls.
- **R8: supported** — execution/X011/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:67-84 bounded repeated matched-task observations/config/cache/order/variation/rework with representative tasks; universal change remains unsupported.
- **R9: supported** — execution/X011/events.jsonl events :9 all conditional resources loaded; no diagram and no unrelated source-code investigation forced.

X011 note line 40: “These are descriptive differences between these two runs, not an estimated treatment effect.” Line 51: “Cache composition differs, so token totals alone are not monetary totals.” Frozen timing receipts report 103.188 vs 42.637 seconds; the 60.551-second / 58.7% arithmetic is correct. Lines 73–78 require matched work, quality evidence, repeatability, cache/order and variation controls rather than extrapolating two unlike tasks. X010 note line 79 explicitly refuses CI/release approval from source-presence observations.

## Final coverage update: X012

All 12 frozen actors covered; prior votes unchanged.

### X012 (C04)

- **R1: supported** — execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:13-17 exact question/constraints, timing-only inference, no new measurement.
- **R2: supported** — execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:19-21 descriptive comparison/competing explanations directly fits causal claim without forced framework.
- **R3: supported** — execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:27-65 exact historical receipt fields, actual scope and extraction provenance; full-output/history limits explicit.
- **R4: supported** — execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:71-78 same required work, quality, total cost and representative tasks; no scores or preferred gold standard.
- **R5: supported** — execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:38-54 actual requested settings differ from backend proof; 60.551 seconds, ~59%, ~34% input, ~68% output arithmetic correct; cache/reasoning not double counted, no currency savings inferred.
- **R6: supported** — execution/X012/events.jsonl events :7,:9,:14 read/list only and note creation/readback; no model/test rerun.
- **R7: supported** — execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:1-9 flat metadata; events :14 actual full readback plus existing link targets.
- **R8: supported** — execution/X012/artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:69-82 cause/quality/cost/generalization remain unknown; future bounded matched/repeated tasks, order/config/cache/variation/guardrails specified.
- **R9: supported** — execution/X012/events.jsonl events :9 required raw contract resources loaded, no optional diagram; timing evidence before resource-read ordering has no demonstrated functional consequence.

X012 note line 69: “Quality improvement, actual monetary savings, causation by workflow simplification, and suitability for broad rollout remain unresolved.” Lines 73–76 request matched scope/config/cache/order, blind quality review where feasible, total accepted-outcome costs, and representative repeated comparisons. Frozen receipt arithmetic supports rounded descriptive values only.

## Final interpretation

No material functional defect, unsupported CI/release approval, unauthorized test/model execution, or frozen-input modification was substantiated. No skill gap is inferred. Minor literal resource-read ordering deviations are visible in several actors, but have no demonstrated outcome consequence; the supported R9 votes represent substantive trajectory adequacy, not a claim of perfect literal ordering. No optional diagrams were created, so parser/graph checks are not activated. Source fragment navigation was not renderer-tested. The two timing cases reject the confounded inference; they do not establish which workflow is superior. Backend identity remains unknown despite requested model/effort records.
