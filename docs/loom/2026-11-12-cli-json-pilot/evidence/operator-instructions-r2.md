# R2 supplemental operator packet — capture repair

This is a separately identified supplemental measurement of the same six
tasks and candidate. It does not replace your first run. You already know
the first run's command behavior and repairs; this round is informed, not
blind. Your original operator identity and mode order stay unchanged.
The coordinator supplies fresh R2 task directories, immutable authentic
originals, the candidate launcher, and a generic capture harness path.
No task answers or complete checker commands are supplied.

## Capture before any command execution

Do not call the launcher, including launcher help, before loading the capture
harness. Read this packet and the harness as bootstrap file access, then use
the harness's `run(argv, cwd)` for every subprocess command in this round.
Set `LOOM_COMPARISON_LOG` to your assigned results JSONL path and set
`LOOM_COMPARISON_PHASE` to the exact phase label before each command.
The harness records actual argv/cwd, UTC start/end, exit, both original byte
streams as base64, decoded UTF-8 where valid, and separate byte counts. It
does not infer classification, choose commands or supply task answers.
Keep the original logs; do not reconstruct missing streams after the fact.

Tag every native tool call in its visible input with exactly one phase:
`R2A:bootstrap`, `R2A:text:T1` through `R2A:text:T6`,
`R2A:json:T1` through `R2A:json:T6`, and `R2A:reporting` for operator A;
use R2B with the corresponding modes/tasks for operator B. Prefix calls
that load this packet or harness with the bootstrap tag too. Use the same
label in `LOOM_COMPARISON_PHASE`. Coordination messages get a coordination
tag and are inventoried separately from task activity.

One native tool call may serve only one task, or one bootstrap/reporting
phase. Do not combine a preceding task's answer with a later task's check.
Complete the current task's initial interpretation, correction, final check
and final answer before starting another task. Do not batch T2/T3 or T5/T6.
Retain first answers before any correction. Report writing belongs to the
separate reporting phase; per-task answers belong to their task phase.
The coordinator will recover actual native tool-call counts from original
session records afterward, so visible phase labels must be unambiguous.
Missing capture remains a failure/limitation; do not invent zeros.

## Tasks and limits

Use task order T1 through T6 in each assigned mode. Discover syntax from
public help. In JSON mode select the optional JSON representation for
checks; help itself remains text. Do not read the oracle, coordinator
protocol, implementation or another operator's results. The first run's
familiarity is disclosed rather than denied. Corrections affect only the
fresh disposable directories. Do not fetch, publish, merge, install or use
paid external execution.

| ID | Goal |
|---|---|
| T1 | Check the historical change's canonical plan. Explain the outcome and what it does and does not establish. |
| T2 | Check the provided plan copy. Explain any failure, correct only the identified defect using the authentic source supplied, and check it again. |
| T3 | Try the plan check without supplying its required target. Explain the result, discover the missing input and check the historical canonical plan. |
| T4 | Check whether the historical change meets the prerequisites for entering write-plan. Explain the outcome and the meaning of any advisory output. |
| T5 | Check whether the historical change meets write-plan prerequisites. Explain any failure, restore only the affected original content from the supplied authentic source, and check again. |
| T6 | Check whether the historical change meets write-plan prerequisites. Explain any failure and advisory output, restore only the affected original content from the supplied authentic source, and check again. |

For each task report initial classification, reason/rule, whether advisory
output means success, correction made, final classification and remaining
limitation. Preserve failures, unchanged results and larger outputs. No
efficiency improvement or universal correctness verdict is requested.
