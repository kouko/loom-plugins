# Context-preserving explanations — acceptance evidence

Tried on 2026-11-06 in a clean clone at 09a5841939ee0ce52fdaaef5fdfe5739c8b2cb61. Four principal synthetic cases and three controls used isolated git repositories without remotes; actors were directed to the skill in the clean clone. Captured prompts, final replies, executed command summaries, drafts, stderr and token usage: `final-acceptance-09a58419-data.json`. The clone passed `python3 scripts/sync_codex_manifests.py --check --all` and was clean before tests. README's Codex installation targets the actual marketplace and was not run; installed-plugin discovery remains unverified.

Requested model/provider/effort were `gpt-6.1-sol`/`openai`/medium; no independent provider receipt was emitted. Seven sessions started and completed, within eight per round. An intended original-versus-candidate control was rejected by automatic approval review before either process started because sending the private baseline to OpenAI was not established as authorized. The candidate-only control was separately authorized and completed. No rejected action was retried or bypassed.

## 1. Supplied background and outcomes

- Case 4 (report-title change) described manual correction and re-export in the final reply.
- Case 5 (invoice currency) did not say an accountant encounters the error and must re-export. Case 6 (preview command) did not restate affected editors or preview failure. These are observed omissions; no original-versus-final conclusion is attributed to them.
- Case 3's final reply did not repeat manual-copying pain, though its open draft retained it. No unsupported roadmap was observed in these outputs.

## 2. Flexible structure and missing facts

- Case 3 asked why the work should be prioritized and left the draft open; it did not ask for confirmation of complete intent.
- Cases 4, 5 and 6 used Chinese replies without fixed five sections. The instruction files are English and instruct responses in the user's language.

## 3. Proportion and useful diagrams

- Case 4 included a requested before/expected-after graph and preserved the explicit publication hold. Its eight nonblank graph lines were each 35 ASCII cells.
- Cases 5 and 6 omitted material supplied problem context from the final reply, so this row remains partly.
- In the clean clone: `env UV_CACHE_DIR=/private/tmp/loom-uv-relative-cache UV_OFFLINE=1 uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/spec/test_capture_intent_contract.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_write_plan_shape_text.py -q` returned 94 passed. The finalization package command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; the acceptance tester did not run the full suite.

## 4. Confirmation and publication

- Case 4 explicitly retained the user's continuing hold after confirmation.
- The neutral candidate-only invoice control explained that yes authorizes later non-forced push and PR after checks, cancellation before publication, and separate merge.
- Principal cases 5/6 said no publication authorization but their wrapper had instructed stopping before publication. Control 5 additionally said no push/PR while its prompt prohibited sending messages. These wrappers are ambiguous, so those replies alone are not attributed to product behavior. The neutral baseline comparison was not run after the automatic rejection.

## Earlier results

Previous report and evidence were preserved in `acceptance-report-pre-09a58419-historical.md` and `acceptance-evidence-pre-09a58419-historical.md`. Earlier results remain historical and are not represented as tests of this commit.
