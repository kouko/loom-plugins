# The detected package suite runs in a uv project's locked environment
originator: kouko
kind: engineering
needs-design: no — checker suite-command detection only; no CLI, API or template surface changes
evidence: [/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-consistence-review-2/5b11059c-24eb-4eec-9170-a767ecffcf0e/scratchpad/dogfood-report-2026-10-29.md]
status: confirmed 2026-10-29
publication: automatic — authorized 2026-10-29 by kouko

## Problem
In a Python repository managed with uv that declares no package-tests command, Loom runs the complete package suite with whatever `python3` is first on PATH. Any interpreter outside the project's own environment fails it (a fresh clone of the sandbox fails collection with 3 errors under the conda `python3`; the project package itself is not installed there), so on such a machine the suite fails at the end of Build and again in finalize-review even though the project's own tests pass, so the agent has to patch PATH by hand. Both dogfood rounds of 2026-10-28/29 hit this.

## Proposed outcome
When the repository commits a uv lockfile and declares no package-tests command, the suite Loom detects runs inside the project's locked environment, independent of which `python3` is first on PATH.

## Acceptance
1. In a uv-managed Python repository with no declared package-tests command, the end-of-Build suite and finalize-review's suite pass on a machine where the first `python3` on PATH is an interpreter without the project's dependencies, with no PATH change by the agent.
2. A Python repository without a uv lockfile, and any repository that declares a package-tests command, gets the same suite command as before.
3. In such a repository whose committed lockfile no longer matches its declared dependencies, the suite stops with a message naming how to update the lockfile, and the lockfile is left unchanged.
4. In such a repository, an adversarial program graduated into the package suite is recognized at finalize-review as collected by that suite.

## Constraints
- A declared `package-tests:` value in KICKOFF-DEFAULTS keeps precedence over detection.
- Running the suite never modifies a committed file.

## Out of scope
- Other lockfile-based tools (Poetry, PDM, pnpm and the like).
- How the adversary records the command for its own adversarial programs.

## Open questions
- none
