# Project and installed-skill retrospectives — spec
intent: 2026-10-14-project-and-skill-retro@92972244d56b34724597e5b0ed217c6f9ba8f66e
pre-build-review: required — renames two public skill entry points, removes an existing approved-write route, and extends proposals across skill and plugin integration surfaces while retaining session privacy boundaries

## Requirements

REQ-1 — One-session project retrospective
  WHEN a user invokes `project-retro` for the current or one specified coding session, the skill shall return source-linked, ranked recommendations limited to that project's implementation workflow, documentation, checks or CI, and repository-level agent instructions, with reusable tool issues separated as unconfirmed candidates → Acceptance #1

REQ-2 — Cross-session installed-skill retrospective
  WHEN a user invokes `skill-retro` over completed supported-host sessions, the skill shall return reviewable, source-linked proposals about an installed target skill's behavior, distinguish instruction defects from directly related plugin registration, loading, hook, bundled-script or dependent-connector defects, and keep one-session observations pending rather than labeling them recurring → Acceptance #2

REQ-3 — Proposal-only boundary
  WHEN either retrospective identifies a possible change, it shall describe a concrete target, evidence, proposed outcome, uncertainty and independent implementation handoff without editing the reviewed project, target skill, plugin or connector → Acceptance #3

REQ-4 — Public names and migration
  WHEN a user invokes or discovers Loom workflow retrospectives, the plugin shall expose `project-retro` and `skill-retro`, route ordinary requests by the intended improvement target, remove `retro` and `distill-sessions` as callable names, and document the old-to-new migration → Acceptance #4

## Design decision

- agent-decided — Keep the two skills in `loom-workflow`. The confirmed intent fixes their ownership and excludes a new plugin or Loom station.
- agent-decided — Preserve `retro`'s single-session, read-only source inspection and split between project recommendations and reusable-tool candidates. Limit project proposals to the adopting repository; a plugin-level issue is only a candidate for `skill-retro`, even when observed during project work. This makes the target of each recommendation explicit.
- agent-decided — Preserve `distill-sessions`' supported Claude Code and Codex ingestion, privacy filters, local preview, explicit approval before external analysis, per-trajectory analysis, cross-session threshold, and pending/anchor-mismatch/deferred visibility. The change does not add a host importer because the intent explicitly excludes it.
- agent-decided — Treat the installed skill as the target. A plugin or connector proposal is eligible only when the observed skill behavior and available source point to that integration surface; absent source yields a bounded investigation candidate, not a guessed file edit. This prevents the retrospective from becoming a general plugin audit.
- agent-decided — Extend per-trajectory analysis prompts and the `merged.json` item contract with an explicit issue surface: `skill-instructions` or a directly related `plugin-integration` subtype. Instruction items retain a real SKILL.md section anchor; integration items carry an observed integration surface and source pointer without a fabricated SKILL.md anchor. Reject unclassified or ungrounded items rather than silently converting them.
- agent-decided — Preserve the two-distinct-session promotion threshold and one-session pending bucket for both item kinds. Cluster integration items by target skill, integration subtype and normalized failure mechanism, then render a separate reviewable integration-proposal form with target surface, observed behavior, supporting sessions, source checks, proposed outcome, uncertainty and verification idea. Keep mechanically rendered SKILL.md proposals for anchored instruction items; anchor-mismatch rules apply only to that kind.
- agent-decided — Remove the retrospective's `apply.py` execution path and approval instructions from its workflow, and retire the script if no external contract requires it. Proposal approval alone does not authorize a retrospective to write; implementation goes through the appropriate independent development workflow. Existing artifacts remain read-only evidence.
- user-decided — Do not retain old names as callable aliases. The user accepted direct rename with explicit migration notes at intent confirmation.
- agent-decided — Update discoverability, host manifests, tests, documentation, examples, and release metadata together; preserve repository history in changelogs and archived development records rather than rewriting historical mentions.
- agent-decided — Keep current privacy controls: observable session material only, no reasoning records or encrypted content, no additional outbound dispatch without existing consent, and no writes to session records. The repo's `PRINCIPLES.md` non-negotiables 2 and 5 require independent verification and explicit consent before data leaves the machine.

## Alternatives considered

- Keep `retro` and `distill-sessions` as aliases: rejected because the confirmed intent explicitly chooses a direct migration and duplicate entry points would weaken routing.
- Extend `project-retro` to change reusable skills and plugins: rejected because one session can only identify a candidate and the target is the current project.
- Turn `skill-retro` into a generic plugin/connector scanner: rejected because evidence must start from a target installed skill's behavior.
- Emit exact plugin patches from transcript evidence alone: rejected because plugin source may be unavailable or the failing layer may be unproven.
- Retain approval-gated `apply.py` inside the retrospective: rejected because it violates the confirmed proposal-only boundary and gives one skill both diagnosis and implementation authority.

## Current state evidence

- Forward: `loom-workflow/skills/retro/SKILL.md` (`## Select and read the session`) starts the one-session review; `loom-workflow/skills/distill-sessions/SKILL.md` (`## Workflow`) starts the multi-session pipeline.
- Reverse: `loom-workflow/skills/using-loom-workflow/SKILL.md` (request-routing table under `# Using loom-workflow`) sends requests to `retro` or `distill-sessions`; `loom-workflow/.codex-plugin/plugin.json` (`skills`) and `.claude-plugin/plugin.json` expose their current names.
- Error: `loom-workflow/skills/distill-sessions/SKILL.md` (`### 5. Human review and approval-gated application`) currently directs `apply.py` to write SKILL.md; `scripts/propose.py` (`render_proposals_markdown`) anchors every proposal to SKILL.md, so related plugin integration issues cannot be represented as first-class proposals.
- Data: `loom-workflow/skills/distill-sessions/SKILL.md` (`### 1. Ingest, detect, and rank`, `### 3. Collect merged.json`) defines `top.json`, trajectory payloads and `merged.json`; `scripts/propose.py` (`extract_memory_items`, `render_proposals_markdown`) groups memory items by title and section anchor and distinguishes promoted from one-session pending items.
- Boundary: `loom-workflow/skills/retro/SKILL.md` (`### Skill candidates`) already keeps skill candidates separate; `loom-workflow/skills/distill-sessions/SKILL.md` (`## Privacy and evidence boundaries`, `## Stop conditions`) defines host ingestion and consent limits; `docs/loom/intent/2026-10-14-project-and-skill-retro.md` (`## Constraints`, `## Out of scope`) excludes a generic scanner and new host importer.

## UI flows

N/A — This engineering change updates skill guidance and generated proposal artifacts, not a distinct UI or command interface; observable invocation and report behavior are specified in REQ-1 through REQ-4.
