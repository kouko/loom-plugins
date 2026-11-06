# Follow-up repair packet — restart resolved

The restarted conversation now injects loom-code 3.57.0. Its launcher exists, contract 2.3.1 passed, and push.contextual-body is present. The blocking-condition section below records the prior obstacle. The follow-up plan task W1-01 now owns the repair.

## User authorization and current state

The user accepted the recommendation to make a narrow repair for the three Claude Code dogfood findings, repair the test environment, rerun the original six scenarios plus two counterexamples, and renew affected tests and independent review. Publication is on hold. Do not push, create a PR or merge under this authorization.

The active intent remains `2026-11-02-context-preserving-explanations`. This is a fix within the active change, not a new capture-intent interview. The original runtime changes and release packet were committed, then host dogfood evidence was committed as `3047f223`. No functional fix for the dogfood findings has started.

## Blocking host condition

This conversation's injected Loom root was `/Users/kouko/.codex/plugins/cache/loom/loom-code/3.56.0`. Its directory and launcher no longer exist. The attempted dispatch oracle failed with `FileNotFoundError` before any worker dispatch. The source contract `loom-code/skills/write-plan/references/codex-first-contact.md`, lines 38–41, requires restart instead of searching another cache version or PATH for a substitute checker. Do not use a repository or temporary copy to bypass that installed-host boundary.

Restart Codex and resume this conversation/worktree so the current installed plugin definition is injected. Confirm the injected root and its contract before dependent workflow work. Existing authorization and the findings below carry forward; do not ask the user to approve plan shape or technical choices again.

## Functional repair scope

- Read `claude-code-dogfood-report.md`, `claude-code-dogfood-evidence.md`, and both audit JSON files in this directory. Classify unsupported additions as one defect class: a stronger deterministic-selection guarantee and an unsupported factual date fallback. Search both first-confirmation owners for the class before dispatching fixes.
- Modify only `loom-design/skills/capture-intent/SKILL.md` Step 4 item 1 and its code-only counterpart `loom-code/skills/write-plan/references/confirm-intent.md`, plus their focused tests, relevant behavioral prompts and existing release notes.
- Preserve user-supplied scope and guarantee strength; unknown factual values remain unknown pending evidence. Keep flexible wording/format. Replace unnecessary publication jargon with concrete consequences; preserve non-forced publication, informed authorization, opt-out and separate merge boundaries. Do not add a fixed script, mandatory section, extra decision point or schema field.
- Keep the capture-intent word cap. Prefer concise replacement within these affected paragraphs, including existing duplicated publication prose, over raising the cap or restructuring unrelated policy.
- Maintain the plan with a bounded fix task and explicit positive/negative evidence. Use a delegated implementer and RED→GREEN. Versions 3.57.0 / 2.20.0 are unpublished candidate bumps for this same change; do not invent another release solely because a local fix round occurs.

## Retest preparation, not an executed result

`/tmp/loom-context-claude-dogfood-retest/cases.json` preserves the original three cases for each entry (six sessions) and adds two counterexamples: random worker selection with own-list isolation, and unknown factual release date. Eight primary sessions are planned, each explicitly selecting `claude-sonnet-5-5` and medium, with a USD 0.50 estimated stop threshold per session. Thresholds are not hard billing caps. Verify current CLI/model availability and inspect actual modelUsage; never inherit chat-agent-group or silently switch models.

The prior shell-command allowlist repeatedly denied legitimate compound read commands. The prepared `settings-proposed.json` changes approach to native strict sandboxing with auto-allowed sandboxed Bash, no unsandboxed fallback, fail-if-unavailable, no shell network domains, and a denied home-directory read region with narrow runtime-package exceptions. It is NOT validated: confirm the consuming CLI accepts and enforces it in a minimal smoke exercise before running paid cases. Do not claim the harness is fixed from JSON syntax alone. Keep restricted file-tool roots, source copies outside each fixture project, user-memory exclusion, disabled hooks/auto-memory/MCP, and independent fresh fixture repositories. Explicitly deny writes to the shared source bundle and real repositories; allow normal temporary-project exploration without accumulating command-specific exceptions.

Only fixture prompts, requester-provided context and necessary plugin resources may be sent. Do not copy personal instructions, memories, credentials or unrelated repositories into the packet. Existing original-provider authentication and the prior model were verified in earlier runs; refresh drift-prone checks before new execution. Current approval covers scoped testing, not publication.

## Evidence and review after repair

Keep prior raw outputs and reports immutable as historical evidence. Two blind auditors should compare the new replies against supplied outcomes, not infer requirements from generated text. Distinguish interview questions from completed confirmation and harness errors from output defects. No global whole-skill dogfood pass: statistical trigger testing, normal installed-hook behavior and every host remain outside this scoped run.

Update affected acceptance rows based on actual new observations. Functional edits invalidate the old attestation. Re-run the required complete locked suite and adversarial evidence, then renew the existing bounded review episode under closing-review before generating a new attestation. Prior reviewer identities are recorded in the existing attestation; do not silently reuse their old verdicts for new content or reset episode limits. Publication remains held.
