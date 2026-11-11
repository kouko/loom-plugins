---
title: "Can existing artifacts justify a publication reminder?"
type: loom-research
status: concluded
created: 2026-11-11
updated: 2026-11-11
change: 2026-11-11-stop-feedback-noise
tags:
  - loom/research
---

# Can existing artifacts justify a publication reminder?

## Question and scope

At commit 5d47d2a6f, can existing evidence distinguish implementation/review in progress, stale review, explicit skips, human waiting and publication-ready work without a new station ledger? Preserve explicit publication/observation policy and the confirmed intent.

## Method and rationale

Inspect the connected Stop, verification and station paths; run a bounded local experiment using the existing verification test fixtures in disposable Git repositories. Repository evidence is sufficient for this internal design decision; no external model or network experiment is needed. Compare conservative reminder eligibility against blanket authorized-change reminders and a new persisted station field.

## Findings

- Source observation: Stop checks automatic authorization but does not check review completion before requesting publication. The explicit observer correctly reports remote incompletion, which alone does not establish the next Loom station.
- Measured: implementation incomplete, review incomplete and explicit reviewer skip without attestation all return `absent`; a matching attestation returns `valid`; modifying and committing functional content returns `stale (attestation functional content digest does not match the selected tree)`.
- Boundary: the same repository while waiting for a human also returns `valid`. There is no new repository evidence in that conversational difference. A valid review is not proof that the agent should disregard a pending question.
- Source observation: `verification_status` validates committed content; an additional local delivery observation is needed to exclude attributable uncommitted work. Publication itself intentionally permits absent/stale verification with disclosure. Reminder eligibility must not change that policy.

## Evidence

- [Stop and delivery implementation](../../../../loom-code/scripts/loom_checker/command_handlers/publish.py), `_delivery_stop`, `observe_delivery`, `_cmd_publish_trusted`.
- [Verification implementation](../../../../loom-code/scripts/loom_checker/verification.py), `verification_status` and its existing attestation validator.
- [Verification fixtures](../../../../loom-code/tests/test_verification_status.py), `branch_repo`, `confirmed_intent`, `attestation`, `commit_attestation`.
- [Closing Review](../../../../loom-code/skills/closing-review/SKILL.md), finalize handoff and explicit-skip handoff; [Ship](../../../../loom-code/skills/ship/SKILL.md), Publish once.

Experiment: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python` with fixture imports from `loom-code/scripts` and `loom-code/tests`; create a temporary branch repo, commit intent, plan, reviewer-skip line, fixture attestation and then changed `src.py` in that order; call `verification_status(repo, CHANGE)` after each step. Actual results: `absent`, `absent`, `absent`, `valid`, `valid` (same tree with hypothetical human waiting), `stale (attestation functional content digest does not match the selected tree)`. This is an evidence-classification experiment, not execution of a real review or host UI.

## Decision impact

Agent-decided: restrict automatic publication continuation to matching verified committed content with no attributable pending work. Reuse verification and local delivery observation, then the existing remote observer; keep a stable selected HEAD across these reads. Absent/stale review or pending local work permits a silent pause, without asserting completion. Explicit skipped flows continue through their existing station handoff and publish command; they receive no automatic publication continuation from Stop without matching evidence. This is deliberately a narrower reminder, not a new publication gate.

Keep conditional human-wait/withdrawal guidance for eligible reminders and the strict repeated-Stop exit. Do not infer conversation state from text, introduce a new station field, or reimplement the workflow in the hook. Keep host-specific response formatting. These decisions refine the existing Acceptance conditions, not scope or authorization; prior RED/GREEN and native-host evidence remains relevant to formatting only. Closing review has not started; no review budget resets.

## Limitations and open questions

This cannot prove that no human question is pending. One eligible first continuation can still occur; the agent must respect the conditional stop guidance. Silent absence cannot prove success and does not enforce recovery from an abandoned pre-review task. Explicit delivery remains mandatory before completion claims. Claude native runtime is still quota-blocked; source tests cannot establish installed behavior. Test the new applicability boundary and evidence races independently before publication.
