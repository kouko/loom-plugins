# Plan simplicity check

**Simplicity check.** Run this step after the draft exists and before
`loom_checker.py plan` and `intake write-plan`, which block an empty
`## Simplicity check` until this step records it. Skip it only when the
plan's `## Simplicity check` holds only `- skipped — narrow change`.
Otherwise resolve the profile as the [shared dispatch profile](../../../references/dispatch-profile.md)
defines, then dispatch one fresh-context `loom-code:reviewer` with lens
`plan`, the draft plan's path as `reviewed_sha` and changed paths, and the
intent and draft plan as ground truth; the plan's author never reviews its own plan. For each
smaller shape it returns as a `deletion-first` finding, adopt it by rewriting
the plan, or decline it with a reason, and record each as one `## Simplicity
check` line; a "no simpler shape" answer records `- none found`. Each adoption
or decline is agent-decided. This step never asks the user a question, and
there is no second round.
