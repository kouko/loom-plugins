# Evidence-led search languages — spec
intent: 2026-11-09-engineering-research-language-policy@c0a17318
pre-build-review: required — published runtime guidance needs an independent boundary check before implementation.

## Requirements

REQ-1 — Exploratory defaults
  WHEN external exploratory discovery is necessary, engineering-research shall normally start separate English and Japanese queries in one round, preserving exact technical identifiers → Acceptance #1

REQ-2 — Sufficient evidence
  IF applicable local artifacts, existing evidence or identified official sources answer the question THEN engineering-research shall reuse them without language-count searches and stop when sufficient → Acceptance #2

REQ-3 — Relevant original languages
  WHEN source language, regional conditions or consequential unresolved gaps warrant expansion, engineering-research shall independently consider Chinese or Korean, allow relevant original and other languages early, and distinguish translations from independent support → Acceptance #3

REQ-4 — Honest supplemental observations
  The supplemental evaluation shall retain one genuine Chinese and one Korean evidence-gap case, neutral tasks, actual actions and artifacts, and independent judgments distinguishing expansion, sufficient alternative evidence and unobserved behavior → Acceptance #4

REQ-5 — Evidence continuity
  The evaluation shall preserve the first six cases, both audits, cold reading, disagreement and limitations without claiming general quality gains, stable activation rates or host coverage → Acceptance #5

REQ-6 — Portable integration
  The formal skill shall load the language guidance through its existing source-policy reference while preserving source acceptance, authorization, research recording, stopping and unrelated workflows → Acceptance #6

## Design decision

- user-decided — Keep English/Japanese as exploratory defaults, independently add Chinese/Korean when warranted, and preserve early original-language use and sufficient-evidence exceptions; these details were confirmed at intake.
- agent-decided — Start from the frozen candidate's eight added source-policy lines, since the first six cases support its default and exception paths; adopt only after the two supplements are observed and independently assessed (REQ-1–4).
- agent-decided — Supply genuine initial evidence with an attributable unanswered question, without directing actors toward a language or suppressing later adequate sources; a resolved gap without the anticipated query remains a valid observed result (REQ-4).
- agent-decided — Retain public evidence as an immutable archive with SHA-256/member inventory and a readable report; do not add experimental runners to the runtime or maintained suite (REQ-5).
- agent-decided — Update only source policy, its focused contract tests and required release metadata; no new station, gate, dependency or research-record field is needed (REQ-6).
- agent-decided — Native fresh actors and independent judges use public material; no external-host invocation, private-data export, global installation or real Vault modification is needed.

## Alternatives considered

- Mandatory four-language search: adds work after the decision is already supported.
- English-only followed by forced failure: delays known original evidence and manufactures a benchmark branch.
- A repeated old/new quality benchmark: outside the bounded request and cannot be inferred from these cases.
- Embedding an experimental runner in the plugin: adds a maintenance surface unrelated to runtime guidance.

## Current state evidence

- Forward: `loom-code/skills/engineering-research/SKILL.md`, Select methods and sources, already loads `references/source-policy.md`.
- Reverse: `loom-code/skills/write-plan/SKILL.md`, engineering-research handoff, routes consequential unresolved engineering questions.
- Error: `loom-code/skills/engineering-research/references/source-policy.md`, source selection, currently supplies no search-language defaults.
- Data: `loom-code/skills/engineering-research/references/source-policy.md`, Critical-claim evidence rules, already distinguishes repeated sources and insufficient evidence.
- Boundary: `loom-code/tests/engineering-research/test_package.py`, package checks, and the existing seven runtime Markdown files bound this guidance-only change; loom-design is untouched.

## UI flows

N/A — guidance consumed by an engineering agent adds no command, screen or external API.
