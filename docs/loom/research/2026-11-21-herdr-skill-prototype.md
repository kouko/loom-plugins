# herdr skill prototype — 2026-11-21

Question: can one skill load herdr's official skill at run time (`herdr --skill`)
instead of copying it, on Claude Code, Codex and OpenCode?

## Official skill facts
- herdr 0.9.5. `herdr --skill` output is byte-identical (`cmp`) to
  `herdrdev/herdr` `skills/herdr/SKILL.md` (214 lines, single file).
- 9 revisions 2026-07-29 → 2026-10-13; six `##` sections unchanged; largest
  diffs 19 lines (v0.9.0) and 24 lines (v0.9.1), mostly behaviour wording.
- `herdr integration install claude` installs only
  `~/.claude/hooks/herdr-agent-state.sh` (reports session identity), no skill.
- Official skill covers single prompt→wait→read; no multi-turn control, no
  conversation search.

## Prototype
Skill `herdr-proto`: (1) `test "$HERDR_ENV" = 1` else stop; (2) run
`herdr --skill` and follow it; (3) extra marker rule `PROTO-SKILL-ACTIVE`.
Three scenarios, one sample each:

| Host | inside herdr | outside (HERDR_ENV unset) | no herdr mention |
|---|---|---|---|
| Claude Code, sonnet | pass | pass (stops) | pass (not used) |
| Codex 0.171.0 | pass only with `sandbox_workspace_write.network_access=true`; default sandbox → `Operation not permitted` on herdr socket | pass | pass |
| OpenCode 2.3.2, `litellm/hyper-coding-group` | pass | pass | pass |

"pass inside" = loaded `herdr --skill`, ran `herdr pane list`, answered an
official-only rule (`recent-unwrapped`, file fallback only as last resort),
and followed the extension marker.

## Transcript mapping (search feasibility)
`herdr pane list` gives `agent_session.value` per pane. Of 17 live panes:
Claude 2/2 and Codex 6/6 resolved to `~/.claude/projects/*/<id>.jsonl` and
`~/.codex/sessions/*/*/*/*<id>.jsonl`; OpenCode 3 ids stored in
`~/.local/share/opencode/opencode.db` (not verified); 5 plain shells.

## Pitfalls from upstream issues (reported by a research subagent, not re-verified)
#2900 `--current` outside a pane falls back to the focused pane; #4764 name
reuse after agent exit; #5462 `agent read --lines` returns only the screen
for short Claude transcripts; #3993 state misdetection.
