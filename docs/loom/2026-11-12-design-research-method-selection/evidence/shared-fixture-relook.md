# Shared short-deadline fixture re-look

## Trigger and repair boundary

The second finalization failed the unchanged
`test_review_stage_times_out_when_descendant_holds_stdout`: expected
`execution-timeout: 6s`, observed `execution-timeout: 5s` during preflight
(`/private/tmp/design-research-finalize-r2.log`). This is the same fake-Python
startup defect class as the first blocked-input repair. That first repair
stopped at an individual consumer; this re-look instead follows both shared
short-deadline factories and every consumer in `test_external_review.py`.
It neither resets the review episode nor changes research requirements.

I read the complete target module, all factory consumers and the production
launcher: normal execution consumes stdin through EOF, whereas Codex discovery
writes three JSON-RPC requests and must keep stdin open until response id 2.
The launcher distinguishes direct-parent exit from descendants holding pipes,
then kills the process group and reaps the parent. Production is unchanged.

## Alternatives and applicability

| Shape | Disposition and reason |
| --- | --- |
| Raise deadlines or reduce concurrency | Rejected: masks startup cost and changes existing regression conditions. |
| Bypass preflight or return a mocked launcher result | Rejected: loses the actual stage transition, pipes and cleanup. |
| Patch only the newly failing consumer | Rejected after recurrence: leaves the shared producer and sibling consumers exposed. |
| Native POSIX shell inside the two existing factories | Selected: removes Python startup from short deadlines while retaining actual stdin, child processes and exit codes; no helper module or harness. |
| Convert longer-budget progress factories too | Excluded: their normal preflight budget is 45 seconds. Their deliberate one-second timeout checks startup-inclusive closing diagnostics without claiming a review-stage marker. |

`_FAKE_CODEX` still records its actual process PID, performs three actual line
reads, hangs in hang mode and emits initialize/notification/non-JSON noise
before model/list. Its answer mode duplicates stdin to fd 3 because an
asynchronous shell command otherwise receives `/dev/null`. A background read
signals the parent on EOF; a ready marker ensures the reader has run before
the original 0.3-second EOF grace begins. The reader is stopped after that
grace. `exec sleep` retains the recorded parent PID for reap assertions.

`_FAKE_CLI` retains separate Codex exit-3, exit-0 and exit-with-orphan modes.
Claude preflight consumes the real input through EOF and returns the same
JSON/model usage only when that input contains `single word ok`. The review
branch emits the Agy model line and starts a real sleep child; hang mode waits
and exit-early mode exits while that child holds the output pipes. The PID
file contains the actual child PID in both paths. Path/mode substitutions
are shell-quoted.

## Existing consumer coverage retained

| Factory | Existing entry-level cases and assertions |
| --- | --- |
| `_FAKE_CODEX` | `discover`: model-list success requires open stdin and reaped parent; no-answer timeout remains 6s and reaps the recorded parent. |
| `_FAKE_CLI` | `discover`: Agy descendant timeout remains 6s/<9s; exited parent with lingering child yields models within <8s; no progress output remains asserted. |
| `_FAKE_CLI` | `execute`: Claude must pass 5s preflight and time out in 6s review, total <15s, with child cleanup. |
| `_FAKE_CLI` | `discover` and `execute`: all three Codex exit modes preserve their exact exit-code diagnostics, combined deadline bound and orphan cleanup. |
| `_FAKE_CLAUDE_STEPS`, `_FAKE_CLAUDE_OK` | Unchanged progress, silence, closing-line, output/privacy and startup-inclusive timeout cases. |

All existing assertions, deadlines, inputs and production worker settings are
unchanged. No tests or assertion harness were added.

## Verification

- Preliminary shape before reader-ready handshake: complete three modules
  `test_external_review.py`, `test_external_review_adversarial.py` and
  `test_adversarial_external_review_progress.py`: 146 passed in 53.50s.
- Preliminary three concurrent critical-case runs: each 9 passed in 34.08s.
- Preliminary throwaway-copy mutations were caught by existing assertions:
  early stdin close produced no models/exit 0; wrong Claude phase produced
  5s rather than 6s; wrong Codex exit produced 0 rather than 3. These preliminary
  receipts do not substitute for checking the committed final test bytes.
- Final handshake shape: complete same three modules: 146 passed in 47.98s.
- Final handshake shape, three concurrent critical-case runs (the same nine
  cases per process): 9 passed in 31.49s, 9 passed in 32.20s and 9 passed in
  30.59s. No worker setting or deadline changed.
- Final committed-byte checks used `git show 5eee5722` for the complete test
  module, production runner and `prose_pin.py`. Every copied test module was
  byte-equal to that commit before execution (SHA-256
  `8e0e1bc0adbc6722a7fcf5950ebc19ada260ce1ce2297cb190b3c20b26c0cb04`).
  Only the copied production runner changed; repository production and test
  bytes were untouched. Commands used the existing test selections with
  `python3 -m pytest -q --confcutdir <copy> <copy>/test_external_review.py -k <selection>`
  and `PYTHONPATH=<copy>`; no new test program or harness was introduced.

| Copied-runner mutation | Existing selection | Observed assertion failure |
| --- | --- | --- |
| Always close stdin after writing, including before response id 2 | `keeps_stdin_open` | 1 failed in 2.90s: candidates `[]` rather than `gpt-a`, `gpt-b`; discovery error reports exit 0. |
| Send the review prompt during the preflight tuple instead of `PROBE_PROMPT` | `review_stage_times_out` | 1 failed in 5.11s: observed preflight timeout 5s rather than review timeout 6s. |
| Replace the model/list nonzero-exit diagnostic with exit 0 | `exit_before_answer` | 2 failed, 1 passed in 9.73s: both expected exit-3 modes reject exit-0 diagnostics; the genuine exit-0 case still passes. |

The committed-byte mutation output is retained in temporary local copies
`/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/committed-shared-fixture-mutations-unpi4w57/{early-eof,wrong-phase,wrong-exit}/receipt.txt`;
these paths are receipts, not package
dependencies. The failing mutation assertions are the intended outcomes.
Three additional concurrent processes ran the same committed-byte early-EOF
mutation: each failed the existing candidates assertion, in 3.29s, 2.70s and
3.82s. This checks EOF detection under bounded concurrent load as well as the
unmutated concurrent success runs above.

## Limits

This removes interpreter startup from these factories; it does not promise
arbitrary scheduler-delay tolerance. The EOF window remains the existing
0.3 seconds. Bounded concurrent runs and targeted mutations support these
specific regression cases, not exhaustive process scheduling or mutation
coverage. No new research behavior is inferred from test-fixture checks.
