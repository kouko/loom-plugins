# Independent semantic grading

The supplied runs do not establish a 15 percentage-point improvement. On the nine comparable cases, baseline passes 9/9 (100%) and candidate passes 9/9 (100%): gain 0 percentage points. The tenth case is invalid for comparison because the permission-denied condition was enforced only in baseline. No genuine semantic failure was found in the nine matched cases in either arm.

## Method and evidence

Graded all checks in `loom-workflow/tests/roadmap/behavior_cases.json` against both summaries, all twenty response files, all twenty diff files, and actual readable fixture files. Baseline snapshot bytes and recorded hashes were checked against final files; unchanged evidence and non-roadmap fixtures were checked against case inputs. All ten cases have response and diff outputs in each arm. Baseline intentionally has no readable byte snapshot for the permission-denied file; this is disclosed rather than counted as a missing successful output. A fresh read during grading also raised PermissionError for that baseline file. Candidate's corresponding file was readable.

Each row requires every supplied semantic check to pass. A response's wording alone is not used as proof of a file update: final file contents and diffs support update/preservation judgments. Raw executor tool-call traces were not included in these output directories; claims about execution history are limited to supplied summaries, responses, and filesystem evidence.

| Case | Baseline | Candidate | Reason |
|---|---|---|---|
| ordinary-document | PASS | PASS | Both create an ordinary root summary with goal, completion conditions, stages, current status, next action and unknown dates/effort. Neither adds an implementation or scheduling artifact. |
| existing-document | PASS | PASS | Both use the selected finance document, recommend the second sample, and preserve its bytes without a competing summary. |
| update-verified-result | PASS | PASS | Both update first-format verification at date/revision scope, link the actual evidence, preserve unknown second-format effort, and avoid overall completion, acceptance or release claims. |
| conflicting-evidence | PASS | PASS | Both explicitly correct the prior success claim to second-format failure, retain failed evidence links, and replace publication with investigation/repair planning. |
| authorized-handoff | PASS | PASS | Both retain the approved build scope, disclose absent implementation inputs, request the existing task/workspace location and preserve the unchanged roadmap. Neither resets authorization or invents completion. |
| plan-as-execution-authority | PASS | PASS | Both review missing verification/acceptance dependencies, identify next Friday as unconfirmed, qualify publication/merge ordering by project procedure, and leave files unchanged. Neither manufactures a firm date. |
| missing-advice-only | PASS | PASS | Both recommend the intent-backed second sample and create no roadmap. |
| ambiguous-document | PASS | PASS | Both identify the two distinct documents and request selection without guessing, rewriting either file or creating a third summary. |
| unreadable-document | INVALID for comparison; standalone response satisfies uncertainty handling | INVALID for comparison | Baseline experienced actual denial and reports only handoff-backed testing uncertainty. Candidate actually read the supposedly unreadable file and accurately discloses this; it cannot demonstrate permission-denied handling. Neither may receive comparative credit for this unmatched condition. |
| preserve-user-change | PASS | PASS | Both preserve today's CSV-only goal and pending sample verification, link limited unit-test evidence, and do not restore the old PDF scope or claim sample acceptance. |

## Counts and limits

- Matched evaluable subset: baseline 9/9, candidate 9/9; gain 0 percentage points.
- Full ten-case comparison: 9 matched PASS pairs and 1 invalid pair; no valid full-evaluation pass rate or improvement claim. Invalid is not a skill failure or an improvement.
- Even the most candidate-favorable resolution of the remaining single case would produce only a 10 percentage-point gain on ten cases, below 15 points; the observed matched results show no gain.
- Baseline's standalone unreadable response passes the visible uncertainty/preservation checks, but denied bytes were not independently snapshotted; do not convert that into a tenth matched PASS.
- Native runs occurred once per case; each arm processed its cases in one shared context. These are descriptive observations, not independent repeated trials or statistical evidence. Shared context can carry information across cases. No installed-host, deployment, adoption, timing or general reliability claim is established.
- Critical evaluation defect: candidate's `readable: false` metadata did not enforce OS denial. Correct fixture parity before claiming coverage of unreadable-document behavior; preserve this failed setup as evidence.
