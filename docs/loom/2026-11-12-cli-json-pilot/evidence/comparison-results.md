# Matched preparation-result comparison — retained observations

Two independent, non-implementing operators completed the six preregistered
tasks in both modes against candidate
`2cef40163b6a562971780da6e6fd107289304962`. A used text then JSON; B used JSON
then text. Every final check exited 0 after the bounded corrections. The
retained first answers match the frozen outcome/cause/advisory propositions:
no interpretation error was identified in these 24 answers. This is a
coordinator scoring observation, not an acceptance or review verdict.

There is no observed reduction in check invocations or corrections. JSON
check output was larger. Complete all-tool counts and total output including
uncaptured bootstrap help cannot be established from the retained capture;
the comparison is incomplete for those metrics, not a zero or an improvement.

## Provenance and scoring

The task set and oracle were committed before implementation in
`030eb89604df322e6dafea25294c76c97edd645e`; candidate binding and the
operator-only packet were committed in
`0c683067ec1e1f02d32d4ec5e69e97d74855d7d4`. The checked historical repository
was `c2bab0811a1ba1083e2452d84375d9c02c79bc3a`, with selected comparison base
`21cdc28d0044f642c6b8409b166ed510e24d3a12`. Neither operator received the oracle.
Both used existing ready runtime, without installation, remote writes or paid
external execution. Concrete inherited model/effort were not independently
observed and are not inferred here.

[comparison-raw.json](comparison-raw.json) embeds all 85 captured constituent
operation records, exact argv/cwd, original timestamps, exits, complete
separated raw stdout/stderr, recomputed byte lengths and stream hashes,
retained answers, operator reports and their capture gaps. The 220 KB-scale
appendix preserves actual task and discovery streams rather than relying on
external temporary paths. Original result/ledger SHA-256 values are included.
It also preserves B's answer-logging subprocesses, without pretending those
are checker calls. A's answer chronology is operator-reported and lacks
independent per-answer timestamps; do not use it for a response-time claim.

The coordinator checked first-answer outcome, cause/rule and advisory meaning
against the frozen oracle, at most one initial interpretation error per
answer. Final answers were checked separately against their actual final
check exits. Scoring annotations and answer text remain in every raw task row
for independent acceptance to judge. A missing metric stays null. Repairs
were independently checked after both operators: all 72 original artifact
copies and four T2 plan copies match their frozen authentic hashes (76 checks,
zero mismatches). No extra task, operator or success threshold was substituted.

## Per-operator mode totals

Bytes below cover actual checker checks, including failed attempts and
recovery, excluding help and file reads. Corrections count one bounded
artifact restoration for T2/T5/T6 and one invocation correction for T3.
Recorded constituent operations are observed reads/edits/checks within task
directories, not outer tool calls and not a complete operation-cost metric.

| Operator | Mode order position | Mode | Initial/final answer errors | Corrections | Check invocations | Recorded task constituents | Check stdout bytes | Check stderr bytes | Complete all-tool count |
|---|---|---|---|---|---|---|---|---|---|
| A | First | text | 0 / 0 | 4 | 10 | 19 | 748 | 789 | unknown |
| A | Second | JSON | 0 / 0 | 4 | 10 | 16 | 2,223 | 0 | unknown |
| B | First | JSON | 0 / 0 | 4 | 10 | 18 | 2,223 | 0 | unknown |
| B | Second | text | 0 / 0 | 4 | 10 | 16 | 748 | 789 | unknown |

Across operators, text and JSON each had 20 check invocations, eight
corrections and zero identified initial/final interpretation errors. Check
streams totaled 3,074 bytes for text and 4,446 for JSON: JSON added 1,372 bytes,
about 44.6%. This is output volume, not tokens or time. The smaller recorded
task-constituent counts in each operator's second mode are confounded by
learning, different read choices and incomplete bookkeeping; they do not
establish a JSON benefit.

Each operator captured three checker-help invocations in their first mode,
7,424 stdout bytes and zero stderr bytes. Thus captured check-plus-help
subtotals are A text 8,961, A JSON 2,223, B JSON 9,647 and B text 1,537 bytes.
These are captured subtotals only: both operators also ran uncaptured
bootstrap launcher help. Do not impute its bytes from a later help call.
The all-bootstrap-inclusive total CLI bytes remain unknown in both modes.

## All task rows

Discovery help is reported above rather than charged to T1. Recorded task
constituents exclude answer/report bookkeeping outside task directories;
all captured records remain available in the appendix. Every complete
all-tool task count remains unknown.

| Operator | Mode | Task | Initial/final errors | Corrections | Recorded task constituents | Checks | Check stdout/stderr bytes |
|---|---|---|---|---|---|---|---|
| A | text | T1 | 0 / 0 | 0 | 1 | 1 | 0 / 0 |
| A | text | T2 | 0 / 0 | 1 | 6 | 2 | 0 / 208 |
| A | text | T3 | 0 / 0 | 1 | 2 | 2 | 0 / 148 |
| A | text | T4 | 0 / 0 | 0 | 1 | 1 | 187 / 0 |
| A | text | T5 | 0 / 0 | 1 | 4 | 2 | 187 / 223 |
| A | text | T6 | 0 / 0 | 1 | 5 | 2 | 374 / 210 |
| A | JSON | T1 | 0 / 0 | 0 | 1 | 1 | 110 / 0 |
| A | JSON | T2 | 0 / 0 | 1 | 4 | 2 | 321 / 0 |
| A | JSON | T3 | 0 / 0 | 1 | 2 | 2 | 265 / 0 |
| A | JSON | T4 | 0 / 0 | 0 | 1 | 1 | 300 / 0 |
| A | JSON | T5 | 0 / 0 | 1 | 4 | 2 | 526 / 0 |
| A | JSON | T6 | 0 / 0 | 1 | 4 | 2 | 701 / 0 |
| B | JSON | T1 | 0 / 0 | 0 | 1 | 1 | 110 / 0 |
| B | JSON | T2 | 0 / 0 | 1 | 6 | 2 | 321 / 0 |
| B | JSON | T3 | 0 / 0 | 1 | 2 | 2 | 265 / 0 |
| B | JSON | T4 | 0 / 0 | 0 | 1 | 1 | 300 / 0 |
| B | JSON | T5 | 0 / 0 | 1 | 4 | 2 | 526 / 0 |
| B | JSON | T6 | 0 / 0 | 1 | 4 | 2 | 701 / 0 |
| B | text | T1 | 0 / 0 | 0 | 1 | 1 | 0 / 0 |
| B | text | T2 | 0 / 0 | 1 | 4 | 2 | 0 / 208 |
| B | text | T3 | 0 / 0 | 1 | 2 | 2 | 0 / 148 |
| B | text | T4 | 0 / 0 | 0 | 1 | 1 | 187 / 0 |
| B | text | T5 | 0 / 0 | 1 | 4 | 2 | 187 / 223 |
| B | text | T6 | 0 / 0 | 1 | 4 | 2 | 374 / 210 |

## Deviations and limits retained from the original protocol

- Both operators lacked complete bootstrap timestamps/streams and did not
  instrument all answer/report bookkeeping. A's complete outer tool count is
  unavailable. B self-reported 20 exec calls plus two messages, but that total
  includes bootstrap/report work and is not independently reconstructed or
  allocated per task; do not compare it with A's 38 constituents.
- A captured 38 constituent operations: 35 task operations and three helps.
  B captured 47: 34 task operations, three helps and ten answer-logging
  subprocesses outside task cwd. Different capture choices do not imply that
  B needed more work or that A omitted the equivalent work in reality.
- B ran JSON T3's initial check before T2 repair/final, and JSON T5/T6 initial
  checks before completing their repairs. The 24 task directories remained
  distinct, but sequential task-completion order deviated. Preserve that
  deviation; do not silently describe fully isolated sequential behavior.
- B's derived `check_operation_ids` fields were empty due to its result
  generator's cwd filter. This aggregate derives actual operation IDs from
  the retained cwd/argv records, preserving the original empty fields in
  retained answer records. No new check execution was invented.
- Both second modes were informed by the first; opposite order does not
  remove carryover. T3's missing-operand start was explicitly requested, so
  it measures diagnosis/recovery rather than a spontaneous error rate.
- There is no population estimate, automatic routing measurement, cross-host
  evaluation, token/time measurement or observed efficiency improvement.
  The JSON mode's stable fields are a functional capability; these two
  informed operators do not establish that agents perform better with it.

Requirements and the preregistered task set were not changed to erase these
limitations. Independent acceptance must judge whether the evidence fulfills
the requested comparison despite the incomplete operation capture. No passing
gate verdict is produced by this worker.
