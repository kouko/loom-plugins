# Concise document-delivery guidance — acceptance test evidence

Tried on 2026-11-06, in a clean copy of the project at 08c92ede3adbdec971fc3397db5e7d196cb3fc7a.

## Current clean setup and limits

- Independent native witness: /root/short_delivery_acceptance; effective profile inherited, overrides=null. No implementation edits, no external CLI/API-backed model calls, credentials, installation, trust changes or model-destination rerouting.
- R = /private/tmp/loom-short-08c92-rcxpl5h7; clean candidate in R/bundle from git archive of the exact full SHA above; R/source.json pins provenance. Fixture has a real Git main checkout and a distinct linked worktree named worktree 工作, plus a sibling external document.
- Read README Install instructions. Host marketplace install/activation was NOT re-tested: external-model sessions were previously rejected and are not bypassed. Locally verifiable setup: python3 scripts/sync_codex_manifests.py --check --all exited 0; bash loom-code/hooks/session-start emitted valid JSON with the current rule, retained at R/hook.json. This proves script emission, not a host receiving it.
- Focused command in the clean export: /Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q loom-code/tests/test_conversation_document_paths.py loom-code/tests/test_check_skill_crossrefs.py loom-design/tests/spec/test_capture_intent_contract.py → 54 passed in 0.38s. Five design entry points, emitted code context and both visualization surfaces are covered. R/surface-counts.json independently records all eight delivery paragraphs as 60 words. Capture is inline and no loom-design Markdown references conversation-paths.md.
- Setup failures retained: system python lacks pytest (R/targeted-tests.txt); offline uv could not create its default cache-lock temporary file under sandbox restrictions (R/targeted-tests-locked.txt). Used the already installed interpreter, without installing packages or repeating that guard. An audit shell-redirection command was blocked by dcg's dynamic-target rule; a read/check with a fixed Python destination completed instead. No product fix resulted.
- No full package rerun by witness. Required station command remains uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q; finalize-review runs it before acceptance and blocks on failure. Parent supplied Build result 4133 passed / 6 skipped plus shell tests, /tmp/loom-short-build-suite.log; this is parent evidence, not witness execution.
- All four rows re-tested; no old verdict carried over. No skipped-by-instruction marker or dismissed important finding supplied.

## 1. Actual absolute deliveries; incidental references preserved

- Executed the focused tests over all eight surfaces. Loaded candidate capture inline body, visualization plain-language body and emitted hook JSON. One native witness then directly exercised this guidance: exact input, path-loaded guidance and actual response are at R/native-smoke.md. No additional model was launched. This is a single explicitly guided in-session smoke, not independent fresh host samples or proof of automatic routing.
- Known-support response delivered docs/操作 指南.md and docs/Review Notes.md with actual worktree absolute targets, plus external 外部 Notes.md with basename label. Copyable open instructions used the full worktree path. Original quote docs/操作 指南.md remained unchanged. Captured actual output, not old host output.
- Result: partly. Mechanical coverage and bounded smoke succeed; real activation/delivery in all three plugin hosts is not newly verified.

## 2. Known support versus unknown fallback

- R/native-smoke.md records exact receiver facts and both actual response branches: known support uses project-relative labels, absolute targets and angle brackets around targets with spaces; unknown support gives full absolute text for all three files. No clickability promise.
- The focused tests execute coverage of known/otherwise clauses on every surface, including negated/missing-clause rejection. Unsupported/unknown host UI was not operated; this is a direct native exercise rather than runtime host equivalence.
- Result: partly. Correct output in the bounded smoke; new external-host and actual click/wrap behavior not verified.

## 3. Active worktree and external identity

- R/native-audit.json independently checks all three delivered Markdown targets: exists=true and root_correct=true for each. git rev-parse --show-toplevel identifies R/worktree 工作, distinct from R/main checkout. External target equals R/外部 Notes.md, not plugin source or main checkout.
- Source tests reject fixed developer prefixes in emitted/shared guidance. No particular realpath command or spelling oracle was required.
- Result: partly. Actual native response targets are correct in a real linked worktree with CJK/spaces; shortened-policy external host behavior remains unverified.

## 4. Portable references and underlying data

- Executed cross-reference and capture-contract tests within the 54 passing focused tests. R/native-audit.json records tracked_changes="" after smoke, the original Markdown destination Review%20Notes.md and package.json main="docs/操作 指南.md". This witnesses actual unchanged fixture bytes, not merely source prose.
- Inspected capture changes against integrated base 968b329bedeee164eefdb7ef8a7f32a714e94ab0 and the previous functional tree 13ecd257. Checked /private/tmp/loom-capture-budget-meaning-map.md against the actual old/new text as input, not as a trusted verdict: question-record shape and four types, verbatim step-5 handoff, canonical plan section and receiver obligation remain; carried-details scope, timing, explicit yes, three nonagreement exclusions, inference/background exclusions, original quotation, no additions and no intent insertion remain. No lost obligation found. The confirmation-template change comes from integrated trunk; its reference resolves in the clean export.
- Result: works for executed portability contracts and unchanged fixture references; automated package suite remains a blocking station check.

## Historical evidence — NOT execution of shortened 60-word text

- Full prior report/evidence remain retrievable at tested commit 08c92ede3adbdec971fc3397db5e7d196cb3fc7a before this evidence-only update. They concern 100-word guidance, not this shortened text; no historical works verdict carries forward.
- Previous fixed run at 165ad485ad97db0932d8d1dc0ba7f4994cb86d33: H=/private/tmp/loom-delivery-165ad-xt_8s6hd (valid /tmp alias). Source provenance H/source.json; setup/install H/setup.json; cache/fixture checks H/audit.json; tests H/targeted-tests.txt. Four bounded host cases code/design/workflow/unknown (one Claude and three Codex) have exact prompt/config/metadata/stdout/stderr/final at H/runs/<case>/{prompt.txt,config.toml,metadata.json,stdout.jsonl,stderr.log,final.txt}. All exited 0, durations 23.75/44.24/24.75/18.41s. Explicit model/provider selections and returned telemetry remain in raw evidence; no new calls occurred here. Cache parity or installation listing alone was never host startup proof.
- Earlier run at 5c98f92f35c339492ffec1df267c94f5305c4d39: P=/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-delivery-5c98-3f08fc2x; P/current-observations.md, P/source.json, P/setup.json, P/runs, P/audit.json and P/hooks-list.jsonl retain evidence. Four initial Codex sessions exited 0 (22.96/63.26/26.65/22.22s), but code delivered relative targets without observed startup payload. hooks/list reported candidate hooks untrusted; no trust write/bypass occurred. Codex code after trust remains NOT VERIFIED. The later Claude code sample does not validate that Codex boundary.
- Initial design used a generic label with unspecified receiver support; fixed old-tree known-support sample re-tested that case. Initial unknown output had no policy-read event, so causal policy routing was not established. P/runs/excluded-code-invalid-override retains the one excluded invalid dotted-override/DNS setup attempt. Across those two old snapshots: eight valid bounded sessions plus one excluded attempt; no broad benchmark.
- Historical harness/oracle pointers: /tmp/loom-delivery-accept-setup.py, /tmp/loom-delivery-run.py, /tmp/loom-delivery-audit.py; earlier versions under P. No required-realpath, file-URI-ban, byte-matching or adoption-rate oracle applies. These are private temporary artifacts, not permanent public reproducibility.
- Current pending twelve external-model sessions were not run after their approval refusal. Current evidence supports no universal host compliance, causal improvement rate, actual terminal click/wrap claim, installed-plugin update or merge.
