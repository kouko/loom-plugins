# skill-retro runtime protocol

Read this reference only when dispatching trajectory or advisory subagents,
converting their outputs, changing threshold configuration, or diagnosing
runtime/folder failures. The entrypoint remains the authority for approval,
privacy, required artifacts, stop conditions, and final verification.

## Step 2 dispatch

Read `top.json`, then fan out one subagent for every
`subagent_payload[]` entry. Select
`agents/prompt-failure-analysis.md` or
`agents/prompt-success-analysis.md` from the payload `kind`; pass the
retained observable session events, `session_snapshot`, `source_inspections`,
target identity and optional `target_skill_path` / supplied source text.
Follow [source inspection](source-inspection.md) before diagnosis. Scripts do
not crawl target sources. Empty legacy values mean unavailable. Capture bounds
exclude later appended events. Sibling dispatches analyze separate snapshots.

Claude Code uses the dispatch alias `model: "sonnet"`; its tool rejects the
literal `claude-sonnet-4-6`. Codex has no equivalent per-call Claude alias, so
use the model option supported by the Codex agent tool. The literal stored in
`scripts/main.py` documents the intended model generation; host call syntax is
not portable.

Each analysis prompt defines strict markdown:

```markdown
# Failure Memory Item 1
## Title
...
## Description
...
## Content
...
```

Success analysis uses `# Success Memory Item <i>`. Preserve returned markdown
until collection; do not request raw JSON from the subagent.

## Mechanical collection schema

Convert each Memory Item block to one JSON entry. The source of truth is
`scripts/propose.py` (`normalize_memory_item`) plus
`scripts/fixture_subagent_results.json`:

```json
[{"session_id":"<source session>","target_skill":"<plugin:skill>","target_skill_path":"<SKILL.md>","memory_items":[{"title":"...","description":"...","content":"...","kind":"failure","issue_surface":"skill-instructions","section_anchor":"When to use"},{"title":"...","description":"...","content":"...","kind":"failure","issue_surface":"plugin-integration","integration_subtype":"hook","failure_mechanism":"normalized observed failure","source_pointer":"plugin/hooks/activate.sh"}]}]
```

Map `## Title`, `## Description`, and `## Content` directly. Parse `## Source inspections` as a JSON list into each item's `source_inspections`; preserve each record's session/tool/version attribution. Copy the dispatch `session_snapshot` into its result entry. Missing legacy fields default to empty; do not invent evidence. Set `kind` from the prompt. Require `issue_surface`. Instruction items need a real SKILL.md `section_anchor`; integration items need a directly related subtype, failure mechanism, and concrete source pointer, with no invented anchor. Missing source becomes a bounded investigation candidate outside `merged.json`. `requires_new_reference_file` is optional and false by default.

The per-target renderer accepts an exact target path, or a name-routed record whose full `plugin:skill` matches `<plugin>/skills/<skill>/SKILL.md`. A path without that structure cannot use name fallback. Clustering retains target identity. Two distinct sessions promote a cluster, including one requesting a new reference file; a lone observation stays pending with its deferred-file flag visible. Only promoted instruction requests enter the SKILL.md reference-file deferred bucket. Promoted integration requests keep their source pointers and sessions in the integration proposal, with a reference-file caveat. Only instruction items undergo SKILL.md anchor validation.

## Advisory report dispatch

1. Read `agents/prompt-advisory-analyst.md` completely.
2. Run `report.py --input <merged.json> --lang <zh-TW|en|ja>` and read stdout
   JSON.
3. Dispatch one subagent with the advisory prompt path and
   `dispatch_payload.input` (`merged_data`, `lang`, `date_str`, `skill_dir`).
   On Claude Code use its current Sonnet alias; on Codex inherit the active
   model or use an explicitly selected model supported by the host.
4. Write the returned markdown verbatim to `output_path`; the response is the
   entire file.

The report is cross-target and independent from `propose.py`.
Its prose language follows `--lang`; identifiers and commands retain their
literal syntax. The advisory analyst follows [source inspection](source-inspection.md), including
permitted target reads and per-session version evidence. Paste-ready edits require
exact target wording and source-language evidence from collected records or
permitted reads; otherwise mark a `--lang` proposal for implementer adaptation.
Source snippets already present in the input stay verbatim. The analyst performs semantic clustering;
there is no heuristic fallback. Historical token-based clustering incorrectly
merged unrelated items through generic shared tokens, which is why LLM
judgment is retained here.

## Configuration meanings

The partial JSON config overrides these defaults:

| Key | Default | Meaning |
| --- | ---: | --- |
| `interrupt_window_sec` | 600 | User interruption within this many seconds of brainstorming/planning contributes an interrupt signal. |
| `needs_revision_threshold` | 2 | Consecutive review rejections needed for a streak. |
| `redispatch_threshold` | 2 | Implementer re-dispatches on one task needed for concentration. |
| `tool_error_proximity_events` | 10 | Event window used to classify a tool-error cluster. |
| `min_session_count` | 3 | Qualifying sessions needed before a skill ranks. |
| `cross_project_count` | 2 | Distinct projects needed for the confidence bump. |

Override only the keys needed. These defaults were derived from the original
v0.1 mining demo; changing them changes signal sensitivity, not privacy or
approval policy.

## History relevant to operations

- Minimal Stage 4 clustering shipped after single-session suggestions proved
  too weak for automatic promotion. Full SDD consolidation remains deferred.
- The per-trajectory model moved from Haiku to Sonnet for analysis quality.
  The observed maximum trajectory was 559K tokens (56% of the 1M window);
  this is evidence, not permission to omit the runtime estimate.
- Claude facet availability depends on local retention and interactive
  `/insights`; Codex events normally have no matching facet.
- Future engines and instruction-file write-back are outside the current
  implementation. Do not simulate those paths.

## Runtime cleanup

Always disable bytecode for tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  loom-workflow/tests/skill-retro/ -v
```

If bytecode directories already exist, remove files first and then empty
directories:

```bash
find loom-workflow/skills/skill-retro -type d -name __pycache__ \
  -print | xargs -I {} find {} -type f -delete
find loom-workflow/skills/skill-retro -type d -name __pycache__ \
  -empty -delete
```

Avoid recursive deletion and inline `shutil.rmtree` shortcuts; repository
safety hooks intentionally block destructive command patterns.
