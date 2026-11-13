# Operator task packet — preparation-result comparison

You are an independent operator evaluating two representations of the same
local checks. You did not implement the candidate. Your assigned mode order,
candidate launcher, candidate commit and fresh task directories are supplied
by the coordinator. Use the same task order T1 through T6 within each mode.
Discover command syntax from public help; no prepared commands are supplied.
For JSON mode select the optional JSON representation when checking. Help
itself remains text. Do not read the comparison oracle, coordinator protocol,
implementation, other operators' results or expected-answer files.

The task directories contain authentic historical artifacts; some contain a
deliberately introduced defect for diagnosis and recovery. Immutable original
files are supplied separately when correction is requested. Corrections are
confined to the disposable task directory. Do not publish, merge, fetch or
modify host installation. Preserve an incomplete task instead of inventing
a successful result.

| ID | Goal |
|---|---|
| T1 | Check the historical change's canonical plan. Explain the outcome and what it does and does not establish. |
| T2 | Check the provided plan copy. Explain any failure, correct only the identified defect using the authentic source supplied, and check it again. |
| T3 | Try the plan check without supplying its required target. Explain the result, discover the missing input and check the historical canonical plan. |
| T4 | Check whether the historical change meets the prerequisites for entering write-plan. Explain the outcome and the meaning of any advisory output. |
| T5 | Check whether the historical change meets write-plan prerequisites. Explain any failure, restore only the affected original content from the supplied authentic source, and check again. |
| T6 | Check whether the historical change meets write-plan prerequisites. Explain any failure and advisory output, restore only the affected original content from the supplied authentic source, and check again. |

For each task, retain your first interpretation before editing or issuing a
second check. Report: initial classification; reason/rule; whether advisory
output means success; correction made; final classification; remaining
limitation. Do not replace an initial mistake with the corrected answer.

Record every tool invocation, including reads, help, edits and checks. For
each CLI invocation preserve exact argv, cwd, timestamp, exit, separated raw
stdout/stderr and their UTF-8 byte counts. Also retain all intermediate failed
attempts and your artifact/invocation corrections. Separate coordinator setup
from task activity. Do not infer token or time savings. The coordinator will
score interpretation answers after both operators finish.

Your second mode is informed by your first. Say so; this is not a blind test.
No efficiency improvement or universal correctness verdict is requested.
