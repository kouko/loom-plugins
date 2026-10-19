# Session start survives control characters in the repo defaults
originator: kouko
kind: engineering
needs-design: no — internal hook output escaping; the session-start text and its format stay the same, no new command, argument or file
evidence: [loom-code/hooks/session-start, loom-code/CHANGELOG.md]
status: confirmed 2026-10-03
publication: automatic — authorized 2026-10-03 by kouko

## Problem
When a repository's `docs/loom/KICKOFF-DEFAULTS.md` contains an invisible control character other than a tab or line break, such as a form feed or a terminal colour code pasted with copied output, the session-start hook emits invalid JSON. The session then starts with none of loom's guidance: no station order, no decision points and no repository defaults, so the agent does not know to route work through loom. Anyone adopting loom can hit this by pasting terminal output into that file, and nothing tells them why loom went silent.

## Proposed outcome
A control character in the repository defaults no longer stops loom's session-start guidance from reaching the session.

## Acceptance
1. With a form feed or a terminal escape character in a defaults line, the session-start output is valid JSON and still carries the station order and the repository's other defaults lines.
2. With an ordinary defaults file, the session-start output is unchanged.
3. The loom-code 3.29.0 CHANGELOG no longer claims that pytest options which run no tests are always refused; it states that such an option passed through a configuration override still gets through.
4. The existing package test suite passes, and loom-code carries a new version consistent across manifests, CHANGELOG and READMEs.

## Constraints
- The session-start text keeps its current wording and length budget.

## Out of scope
- Validating or rewriting the defaults file itself.

## Open questions
- none
