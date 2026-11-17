---
title: "Bounded diagnosis of two planning-trial command blocks"
type: loom-research
status: concluded
created: 2026-11-17
updated: 2026-11-17
change: 2026-11-16-roadmap-simplification
tags:
  - loom/research
---

# Bounded diagnosis of two planning-trial command blocks

## Question and scope

Determine the immediate cause of the two candidate trial blocks and whether
that evidence warrants changing roadmap guidance. Inspect those two native
session records and replay at most one case. Do not execute the rejected write
commands, change guard configuration, rerun model trials, merge or install.

## Method and evidence

Recovered literal tool inputs and corresponding guard outputs from the original
local native sessions. Decoded the command strings as data, without evaluating
the tool-input JavaScript. The earlier evaluation's missing-command limitation
can now be narrowed; its frozen outputs remain unchanged.

Evidence directory: `/private/tmp/roadmap-bounded-diagnostic/`.

| Trial | Recovered evidence | Observed block |
|---|---|---|
| useful-software-stages, candidate run 3 | `stages-command.txt`, `stages-diagnostic.txt`, `stages-provenance.json` | `heredoc.posix:inline-launcher-unverified`, heredoc line 46 |
| nonsoftware-research-plan, candidate run 1 | `research-command.txt`, `research-diagnostic.txt`, `research-provenance.json` | Same rule, heredoc line 61 |

SHA-256 of the decoded commands:

- stages: `19e447015163eee40d3ff8df9e21eb9bb3d8a3a084cc570355f3d8baa7a8b20f`
- research: `9293994788e368b7af3b80413cf4fa24e9bcfa4e778cb6e82a6abaf7aae9ae3d`

Both commands wrap file editing and execution logging in an outer Python
heredoc, then launch another Python interpreter with dynamically supplied
`-c` source through `subprocess.run`. The guard reports that it cannot verify
that inline source. The subprocess uses an argument list, not an explicit shell;
this observation does not establish shell injection or malicious content.

One data-only analyzer replay used current DCG 0.16.0:

```sh
dcg test --dialect posix --heredoc-scan --stdin --explain --format json < /private/tmp/roadmap-bounded-diagnostic/research-command.txt > /private/tmp/roadmap-bounded-diagnostic/research-dry-run.json
```

The analyzer completed with exit 0 but returned `decision: deny`, the same rule
and heredoc line 61. Exit 0 means the analysis completed, not that the command
was allowed. No original command was executed. Historical DCG version was not
captured, so this is a current reproduction of the observed classification.

An existing successful baseline research trial used direct `Path.write_text`
in the outer interpreter rather than a nested dynamic Python launcher. Its
recovered tool input/output are `baseline-control-tool-input.txt` and
`baseline-control-tool-output.json`; it was not replayed. Previously recorded
assisted `apply_patch` recoveries also succeeded. All six current fixture files
match their prior recovery snapshots (`diagnostic-summary.json`).

## Conclusion and recommendation

The immediate block concerns the execution/logging command construction, not
rejection of roadmap planning content. The [roadmap skill](../../../../loom-workflow/skills/roadmap/SKILL.md)
does not prescribe Python, nested subprocesses or that logging wrapper. This
evidence does not warrant adding planning rules or changing its description.
For future trials, prefer the host's ordinary file-edit API and retain literal
tool commands before invocation. This is a harness recommendation, not an
implemented change or a guard bypass.

This diagnosis does not prove that candidate instructions had no influence on
command selection, establish a DCG implementation bug, or demonstrate improved
planning quality. Original completion remains baseline 12/12 versus candidate
10/12; the two assisted recoveries remain separate. The
[evaluation review](planning-knowledge-review.md) retains the original
observations and limitations. Full-command availability is the newly recovered
evidence, not a retroactive conversion of blocked trials to passes.

This diagnostic is retained as supplemental execution evidence. The acceptance
report and publication explanation may reference it; skill content, frozen
evaluation artifacts, installation and guard configuration remain unchanged.
No new model trial or original write command was executed.
