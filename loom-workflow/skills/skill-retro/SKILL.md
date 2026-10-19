---
name: skill-retro
description: |
  Review completed Claude Code or Codex sessions for recurring problems in an installed skill's instructions or directly related plugin integration. Produces source-linked proposals without applying changes.
version: 0.6.0
---

# Skill retrospective

Review several completed sessions for recurring behavior of an installed target skill. Produce proposals for its instructions or directly related plugin registration, loading, hooks, bundled scripts, and dependent connectors. This is a review-only workflow. The previous callable name was `distill-sessions`; use `skill-retro` now.

`<skill-dir>` is this skill's folder: `${CLAUDE_SKILL_DIR}` on Claude Code, otherwise the folder containing this file.

## Privacy and consent

Local ingestion reads supported Claude Code and Codex session logs and available Claude `/insights` facets. Retain observable user and assistant text, tool calls, and tool outputs. Exclude hidden or encrypted reasoning. A policy stop needs both an observable stop or ask and its reason. Do not write to session records.

`main.py`, `propose.py`, and `report.py` run locally. Before dispatching session-derived text to analysis agents or an optional advisory agent, show the local preview and obtain explicit scope approval. An explicitly named target skips only the target-selection pause; it does not waive approval for outbound analysis. Never send a trajectory above the 1M-token estimate (`len(json.dumps(payload.input)) // 4 > 1_000_000`); report the exclusion.

## Workflow

1. Run `python <skill-dir>/scripts/main.py --target-skill-pattern 'loom-code:*' > top.json`, or use the user's named target. Show the stderr preview, including skill and session friction. For a bare invocation, confirm the target subset before analysis dispatch.
2. Read `top.json`. Dispatch one independent analysis agent per trajectory using `agents/prompt-failure-analysis.md` or `agents/prompt-success-analysis.md`. Give only that trajectory's observable events and target skill name. If the host cannot supply the skill text by name, analyze the events and disclose the missing source; do not invent instruction anchors. Read [runtime protocol](references/runtime-protocol.md) for host calls and collection details.
3. Convert returned strict-markdown Memory Items to `merged.json`. Keep each `session_id`, `target_skill`, and `target_skill_path`. Every item has `title`, `description`, `content`, `kind`, and `issue_surface`. `skill-instructions` requires a nonblank real `section_anchor`. `plugin-integration` requires `integration_subtype` (`registration`, `loading`, `hook`, `bundled-script`, or `dependent-connector`), normalized `failure_mechanism`, and a concrete `source_pointer`; it has no SKILL.md anchor. Reject missing classification or source instead of guessing. If the integration source is unavailable, retain a bounded investigation candidate in the review narrative; do not put an unsupported item into `merged.json`.
4. Run `python <skill-dir>/scripts/propose.py --input merged.json --target-skill /path/to/target/SKILL.md --output proposals.md`. The renderer accepts only records with the exact target path or, for name-routed records, the full matching `plugin:skill` identity derived from `<plugin>/skills/<skill>/SKILL.md`; an ambiguous path cannot use name fallback. It groups instruction items by target, title and anchor, and integration items by target, subtype and failure mechanism. Two distinct sessions promote a proposal, including one that needs a new reference file; one session remains pending. Promoted instruction requests for new reference files enter the deferred bucket; promoted integration requests stay in integration proposals with a reference-file caveat. Only instruction items undergo SKILL.md heading checks. The proposal shows integration target, observed behavior, supporting sessions, source, proposed outcome, uncertainty, and verification idea.
5. Review the proposals and hand chosen changes to an independent implementation workflow. Do not modify the target skill, plugin, connector, or reviewed project from this retrospective. Proposal approval is a decision about what to implement later, not permission for this workflow to write.

## Optional advisory report

Run `report.py --input merged.json --lang zh-TW|en|ja`, then dispatch `dispatch_payload.input` only with explicit consent. Its `skill_dir` key gives the analyst the local bundled resource path. The report complements per-target proposals and has no write authority.

## Evidence and completion

Keep `top.json`, `merged.json`, and each per-target proposal for audit. Report target, analyzed trajectories, facet availability, overflow or validation exclusions, and artifact paths. An empty valid result means no qualifying evidence; malformed or missing artifacts are failures. Preserve pending, anchor-mismatch, and deferred-reference buckets even when no item promotes. Signals rank review order, not proof of a defect. A session contributing both success and failure observations still counts as one distinct session for a given cluster.

Stop on missing target, denied analysis consent, hidden reasoning, overlong payload, missing prompt or artifact, unclassified or unsupported item, or a failed relevant test. State what remains unresolved. Run tests with bytecode disabled:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/skill-retro/ -q
```
