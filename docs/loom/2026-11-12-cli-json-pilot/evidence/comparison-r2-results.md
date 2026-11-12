# R2 supplemental capture repair — retained observations

R2 preserves candidate `2cef40163b6a562971780da6e6fd107289304962`, the original
six tasks, oracle and operator identities. The amendment was committed before
execution as `3f43de60fa492241a7444ca513e45135dd267c30`. R1 remains separately
retained and partly complete; neither its observations nor spent recovery
attempt are replaced or reset. This is the second technical capture-repair
path for the same obligation. Both operators already knew R1 outcomes and
their second mode also used first-mode knowledge. It is not a blind trial,
new independent sample or population efficiency estimate.

## Four requested metrics

All 24 retained initial answers match the frozen outcome, cause/rule and
advisory propositions; no interpretation error was identified. Final answers
agree with actual final exit 0. Initial answers were retained before repairs;
the raw evidence contains their original records and capture timestamps.
There is no observed reduction in corrections, native tool calls or check
invocations within either operator. JSON check output is larger.

| Operator | Mode | Initial/final answer errors | Corrections | Native task tool calls | Captured task subprocesses | Check calls | Check stdout bytes | Check stderr bytes |
|---|---|---|---|---|---|---|---|---|
| R2A | text | 0 / 0 | 4 | 19 | 16 | 10 | 748 | 789 |
| R2A | JSON | 0 / 0 | 4 | 19 | 16 | 10 | 2,223 | 0 |
| R2B | JSON | 0 / 0 | 4 | 12 | 28 | 10 | 2,223 | 0 |
| R2B | text | 0 / 0 | 4 | 12 | 28 | 10 | 748 | 789 |

Each operator has the following per-task results in both modes. Counts are
actual unique native tool calls with a single task phase; there are no shared
task wrappers to allocate. Every task has zero identified initial/final
interpretation errors. T2/T5/T6 each required one artifact restoration; T3
required one invocation correction. Captured subprocess counts differ because
B used child Python for answer writes while A used host file operations.
These layers must not be substituted for one another.

| Task | Corrections per operator/mode | Checks per operator/mode | A native calls in text / JSON | B native calls in JSON / text | Text check stdout/stderr bytes per operator | JSON check stdout/stderr bytes per operator |
|---|---|---|---|---|---|---|
| T1 | 0 | 1 | 2 / 2 | 2 / 2 | 0 / 0 | 110 / 0 |
| T2 | 1 | 2 | 4 / 4 | 2 / 2 | 0 / 208 | 321 / 0 |
| T3 | 1 | 2 | 3 / 3 | 2 / 2 | 0 / 148 | 265 / 0 |
| T4 | 0 | 1 | 2 / 2 | 2 / 2 | 187 / 0 | 300 / 0 |
| T5 | 1 | 2 | 4 / 4 | 2 / 2 | 187 / 223 | 526 / 0 |
| T6 | 1 | 2 | 4 / 4 | 2 / 2 | 374 / 210 | 701 / 0 |

Across operators, text and JSON each had 31 native task tool calls, 20 check
calls and eight corrections. Text check streams totaled 3,074 bytes; JSON
totaled 4,446, adding 1,372 bytes (about 44.6%). Four bootstrap help calls per
operator, including the first launcher help, produced 8,049 stdout bytes and
zero stderr bytes. Bootstrap is separate rather than assigned to a mode.
Including both modes and all help, each operator's checker/launcher output
was exactly 11,020 stdout plus 789 stderr bytes, or 11,809 total. File reads
and reporting are excluded from this checker-output metric as preregistered,
but retained in the raw appendix. No missing stream was imputed and byte
counts are not token counts.

## Complete native inventory and provenance

| Operator | Bootstrap calls | Task calls | Reporting calls | Coordination calls | All native calls | All captured child subprocesses |
|---|---|---|---|---|---|---|
| R2A | 3 | 38 | 1 | 2 | 44 | 37 |
| R2B | 3 | 24 | 4 | 1 | 32 | 61 |

Native counts were recovered from the same original session files as R1, but
strictly between the second `task_started` receipt and its `task_complete`.
R2A boundaries are lines 157–397; R2B boundaries are lines 143–324. The
verified agent paths remain `/root/json_operator_a` and
`/root/json_operator_b`. R1 calls were not counted again.

[comparison-r2-raw.json](comparison-r2-raw.json) retains all 98 actual
subprocess records with raw base64 streams, UTF-8 text where valid, separate
byte counts, argv/cwd, phase, UTC timestamps, exits and stream hashes. Every
base64 stream length and UTF-8 representation was recomputed. All 76 original
and repaired artifact hash checks matched the unchanged oracle. All four
help invocations and twenty checks per operator are present; the first
launcher help is 625 stdout bytes and zero stderr bytes in each capture.

The appendix also retains exact native call IDs, phase assignment, source
session/file hashes, receipt/completion lines, tool/result line numbers,
timestamps and bounded command/result excerpts with full-source hashes.
Only tool records and identity/boundary metadata were extracted; no analysis,
reasoning, unrelated messages or decrypted coordination bodies were copied.
It includes the original operator reports and first/final answers for
independent scoring review, not merely external temporary file references.

## Deviations and limitations

- The first two bootstrap file-access calls lacked exact phase comments.
  Their actual packet/harness/instructions read commands identify bootstrap;
  they did not run an uncaptured launcher. A also used a hyphen bootstrap
  label before reading the detailed instruction. Original labels remain.
- B's first reporting request was blocked before execution. It is counted
  as an actual native tool invocation; no child subprocess is invented.
  The subsequent explicit report script succeeded and its captured output
  remains separately labeled reporting.
- Operators used different bookkeeping choices. The 44 versus 32 overall
  native calls, and 37 versus 61 child subprocesses, do not measure JSON
  efficiency. Bootstrap/reporting/coordination are explicit, not hidden.
- R1 remains partly complete. R2's informed, prescribed same-task results
  establish neither a spontaneous error rate nor broader operation gains.
  There is no automatic-routing, other-host, time or token measurement.

This worker provides scoring observations and recomputable metrics, not an
acceptance/review verdict. The comparison did not establish efficiency
improvement. Independent acceptance must judge the retained R1 limitations
and this separately identified supplemental evidence without waiving the
original requirements or pooling rounds into an inflated sample.
