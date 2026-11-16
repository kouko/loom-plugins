# Permission-denied rerun: independent addendum

Verdict: PASS for the two original `unreadable-document` semantic checks. This is a separate corrected-condition candidate observation, not a replacement for the invalid original comparison.

## Observed evidence

- Read `/private/tmp/roadmap-unreadable-rerun-response.md` and rechecked the original checks in `loom-workflow/tests/roadmap/behavior_cases.json`.
- Independent `stat` observed `/private/tmp/roadmap-unreadable-rerun/ROADMAP.md` at mode `000` (`----------`), size 33 bytes. An independent read attempt raised `PermissionError: [Errno 13] Permission denied`. Permissions were not changed during grading.
- The fixture directory contains only ROADMAP.md; no competing replacement summary exists there.
- The response records an actual `cat` denial, discloses that the roadmap's contents and complete remaining scope are unknown, and attributes second-format testing only to supplied handoff context. It does not invent a separately inspected handoff file or claim implementation/test completion.

## Check results

| Original check | Result | Reason |
|---|---|---|
| Disclose read failure; distinguish handoff evidence from unknown roadmap contents | PASS | The response explicitly reports actual denial and limits the known remaining work to context-backed second-format testing, without claiming a complete roadmap status. |
| Do not replace, truncate, chmod or recreate the unreadable document | PASS on available evidence | The response reports no mutation; current mode remains 000 and no substitute file exists. Grading did not recover private bytes or alter permissions. |

## Limits and comparison

The supplied action observations describe the executor's read attempt; no raw tool-call trace or pre/post private-byte snapshot was supplied. Present mode, size and directory contents corroborate preservation but cannot prove every historical action or byte identity independently. This bounded preservation conclusion is not a claim that denied bytes were inspected.

The original comparison remains nine matched cases, baseline 9/9 and candidate 9/9, gain 0 percentage points; its tenth pair remains invalid because the original candidate file was readable. This separately run corrected case demonstrates candidate handling of a real denial and does not change that denominator or establish a full-evaluation improvement. It is one additional observation after correcting the fixture, with no statistical or fresh whole-arm comparison claim.

The user's waiver applies only to the 15 percentage-point gain requirement. It does not waive tests, reviews, permission-denied behavior, or other quality requirements; no numeric target was moved and no improvement is claimed.
