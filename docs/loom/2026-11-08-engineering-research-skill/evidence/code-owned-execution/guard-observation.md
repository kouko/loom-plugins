# Pre-execution guard observation

Before any actor launch, a harness-only attempt to run Python which would delete the already merged temporary `research-fixture` branch was rejected by the PreToolUse hook. The operation was not dispatched and was not retried or bypassed. The existing topic branch remains.

Exact rejection text (the tool itself truncated the displayed command preview):

```text
Command blocked by PreToolUse hook: BLOCKED by dcg

Reason: Embedded shell command blocked: A dynamic shell expansion in this git branch command can expand into a deletion or forced ref update. Quote the branch name or add `--` to make it a literal creation. (line 5 of heredoc)

Explanation: An unquoted command substitution or variable in a git branch invocation is expanded and field-split by the shell before git parses it, so its output can inject `-D`, `-f`, `-M`, or `-C` and turn a branch creation into a deletion or forced ref update. dcg cannot statically bound the expansion's output.

Rule: core.git:branch-dynamic-token

If this operation is truly needed, ask the user for explicit permission and have them run the command manually.

To permit this single command once, the user can approve it with: dcg allow-once 894162.
```

The rejected Python subprocess argument list was `['git','-C',str(f),'branch','-d','research-fixture']`, where `f` was exactly `/private/tmp/formal-engineering-research-execution/fixture`. This was an already merged fixture branch; there was no attempt against the real repository.

The later, non-destructive fixture observation recorded `git status --porcelain` with exit 0 and empty stdout. No linked worktree or build artifact had been created by this fixture harness. That observation is bounded to the clean main working tree. It is **not** successful topic-branch removal, real worktree cleanup, release, installation or host verification.

Auditors should distinguish a skill behavior failure from insufficient lifecycle-fixture prerequisites. If the preservation contract requires additional cleanup beyond this exact fixture scope, F05/F06 cannot establish that precondition and should be marked inconclusive for that portion. No behavior result has been graded by this executor.
