# Independent W1-02 correction recheck

Reviewed HEAD: `419c09b1eb8664145ce1d9971f5b9b3c06bccd90`.
Reviewer: independent Codex agent `result_help_checkpoint`, not the implementer.
Verdict: **PASS for the bounded W1-02 help checkpoint**. No remaining findings
in this recheck. This is not a formal closing attestation, W2 implementation,
publication authorization, or a claim that all normal command paths ran.

The initial NEEDS_REVISION report in [help-checkpoint.md](help-checkpoint.md)
remains unchanged. It supplies the sixteen-command source readback and original
failed findings. This recheck covers H1/H2 corrections, their conformance rows,
and reruns the original discovery/counterexample checks.

| Item | Result and evidence |
|---|---|
| H1, host-hook protection opt-out | Resolved. `loom-code/scripts/loom_checker.py:139-141` now explicitly qualifies refusal with repository-local `loom.protectMain=false` and separates host-hook from native-hook behavior. Matches `command_handlers/push.py::_protect_main`, which reads local boolean config and returns false for the opt-out. The conformance push row states the same limitation. |
| H2, nonfatal trunk synchronization | Resolved. `loom_checker.py:170-174` discloses successful merge/cleanup exit 0 after skipped/failed trunk sync, the `trunk not updated` stdout, and preservation/recovery guidance. Matches `command_handlers/land.py:201-205,315-347`: sync returns without blocking subsequent cleanup. The land conformance row accurately carries the same caveat. |
| Named cleanup does not sync trunk | Verified by reading `land.py:612-640`: named cleanup reads merged PR evidence, fetches/prunes, plans and executes cleanup, and never calls `sync_trunk` or `_sync_and_clean`. The new help/conformance statement correctly distinguishes this from the accepted merge form; it does not promise no ref writes. |
| Remaining fourteen pages | AST comparison against initial reviewed HEAD `14a358c21` confirms all fourteen other `COMMAND_HELP` values are byte-identical; prior bounded PASS conclusions carry forward. No command handler changed. |
| Prior failed evidence | Initial report is present unchanged; no attempt was made to relabel or remove its failed findings. |

## Authentic re-execution

Executed against the reviewed fix HEAD:

1. Existing independent program `/private/tmp/loom-result-help-independent.py`:
   **32 sentinel public-entry forms + 32 actual ready-launcher forms PASS**.
   Every command's `--help` and `-h` returned text stdout, empty stderr, exit 0.
   Sentinel execution blocked handler/stdin/subprocess/socket/file access and
   left its empty non-Git directory unchanged. Actual candidate `--ready` calls
   ran outside Git with PATH `/usr/bin:/bin` and an existing ready runtime; no
   repair/installer was available. Isolated missing runtime returned **86** and
   created no cache. Latest authentic output is retained at
   `/private/tmp/loom-result-help-independent-output.json`.
2. Existing `/private/tmp/loom-result-help-counterexamples.py`: **PASS**.
   Main/git-push with the mocked existing local opt-out was allowed; mocked
   failed trunk inspection plus successful cleanup returned 0 and printed
   `trunk not updated`. These unchanged real code paths now agree with help;
   the test did not mutate Git or contact a remote.
3. A separate AST/assertion check confirmed only push/land help values changed
   and both explicit qualifications plus named-cleanup distinction exist.
4. Implementer log `/private/tmp/loom-result-help-h1h2-green.log` reports the
   focused suite's **58 passing tests**. This recheck did not rerun that suite;
   its independent execution is the 64 discovery invocations and bounded
   counterexamples above. No full suite, live publication/merge/cleanup,
   installer/provisioning, network command or paid external review ran.

The two original semantic findings are resolved at this HEAD. Combined with
the preserved fourteen-page readback, this satisfies the specified help-first
content checkpoint. Further work remains the parent's workflow decision.
