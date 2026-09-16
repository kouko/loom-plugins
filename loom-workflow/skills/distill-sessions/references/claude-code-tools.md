# Claude Code — tool name reference for `distill-sessions`

> Scoped to this skill's own dispatch points: this file maps
> `distill-sessions`' two dispatch points to the host's call shape.

## Stage 3 parallel fan-out (`agents/prompt-failure-analysis.md` / `agents/prompt-success-analysis.md`)

The orchestrator dispatches these prompts in parallel as subagents. On
Claude Code the per-host call shape is N
`Agent()` calls issued in a single assistant message so the harness
runs them concurrently:

```
Agent({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "<3-5 word task>",
  prompt: "<agents/prompt-failure-analysis.md or
            agents/prompt-success-analysis.md content +
            session_events / target_skill_path /
            target_skill_md_content JSON>"
})
```

`model: "sonnet"` is required here too — `scripts/main.py` locks the
Stage 3 subagent model to `claude-sonnet-4-6` (SKILL.md's own Step 2:
"runs on `claude-sonnet-4-6`"), and per the alias note below, only the
harness alias reaches `Agent()` without failing enum validation; the
`model` field is easy to drop when copying this call shape since the
literal id in `top.json`'s payload is not directly usable.

One such call per `subagent_payload[]` entry, all issued in the same
assistant message so they run concurrently. **Do not add `name:`**: it turns the one-shot blocking call
into a persistent mailbox-semantics teammate whose output is never delivered.

## Stage 5c single dispatch (`agents/prompt-advisory-analyst.md`)

```
Agent({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "distill-sessions advisory report",
  prompt: "<agents/prompt-advisory-analyst.md content +
            dispatch_payload.input JSON (merged_data / lang / date_str /
            skill_dir)>"
})
```

### Model alias

`model: "sonnet"` is Claude Code's harness-level alias for the current
Sonnet generation (Sonnet 4.6 at time of writing). Passing the literal
model id `"claude-sonnet-4-6"` (the id the prompt's own YAML frontmatter
documents) fails `Agent()`'s enum validation — always dispatch with the
alias, not the literal id.
