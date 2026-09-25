# Plan simplicity check

**Simplicity check.** After both checks pass and before the plan commit,
unless the plan's `## Simplicity check` holds only `- skipped — narrow change`,
resolve the profile as the [shared dispatch profile](../../../references/dispatch-profile.md)
defines, then dispatch one fresh-context `loom-code:reviewer` with lens
`plan`, the draft plan's path as `reviewed_sha` and changed paths, and the
intent and draft plan as ground truth; the plan's author never reviews its own plan. For each
smaller shape it returns, adopt it by rewriting the plan and rerunning both
checks, or decline it with a reason, and record each as one `## Simplicity
check` line; a "no simpler shape" answer records `- none found`. Each adoption
or decline is agent-decided. This step never asks the user a question, and
there is no second round.
