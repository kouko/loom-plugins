# Cumulative boundary reassessment

Load this reference only after the Write Plan screen finds a concrete
dependency, state, test, or relevant-context warning in the likely target set.
This is a change-scoped investigation, not a repository audit.

## Inspect the warning

Start from the named current boundary, requested feature, likely changed
symbols or files, direct callers or consumers, state owner, and focused tests.
Use the screen's metadata set of at most 20 unique commits across all targets.
Classify why each relevant commit touched the area before treating co-change as
evidence. Exclude renames, formatting, generated updates, dependency bumps,
and mass updates. These reveal activity but do not establish responsibility or
coupling.

Metadata is usually sufficient. When the warning depends on patch content,
inspect at most three target-only diffs selected from that same bounded commit
set. Choose diffs that can confirm or falsify the warning; avoid full-commit or
repository-wide patches.

## Decide causally

Name the current responsibility and the different reason to change introduced
or extended by the feature. Then identify an observable locality failure:

- changing one responsibility also changes callers or internals owned by the
  other;
- shared mutable state or dependency direction prevents isolated change;
- focused verification needs unrelated fixtures, setup, or assertions;
- purpose-divergent changes repeatedly touch the same symbol or coupled set
  after noise is excluded; or
- a dependency-complete relevant-context set includes unrelated regions.

Extract only when both a distinct responsibility and an observable locality
failure are supported by named evidence. Preserve the current boundary whenever
either side is absent, uncertain, or explained by cohesive work. Treat file length,
token count, commit count, churn, and a physical file split as
warnings, never extraction verdicts. A prior split that retains shared state, dependency ripple,
or repeated co-change is not isolation; correct ownership rather than adding
another file.

## Carry the decision

Record the boundary, target set, and decisive present/history evidence in
Current State Evidence. Put the preserve or extract reason in the affected
task's Risk line. For extraction, order characterization, the smallest
behavior-preserving extraction, and focused verification before the feature
task. For preservation, keep the feature inside the existing boundary and
name its focused test. Keep this agent-decided: add no user question, separate
skill, checker rule, or permanent artifact.
