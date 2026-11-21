# herdr skill in loom-workflow — spec
intent: 2026-11-21-herdr-skill@dce27e65b
pre-build-review: required — reads every local agent transcript and hands snippets to the calling agent's model vendor (privacy), and drives other agents' terminals (cross-system)

## Requirements
REQ-1 — Official instructions, one skill
  WHEN a user inside a herdr pane asks a Claude Code, Codex or OpenCode agent to operate herdr, the skill shall load the official skill text from the installed herdr (`herdr --skill`) and follow it, with no separately installed official skill ("我會想要做一個把官方 skill 功能都包裝進去的 skill 因為我不想裝兩個 skill") → Acceptance #1
REQ-2 — Outside herdr
  WHEN `HERDR_ENV` is not `1`, the skill shall say it is not running inside herdr and run no herdr control command → Acceptance #2
REQ-3 — Explicit trigger only
  The skill description shall select it only when the user mentions herdr; background work, delegation or parallel work alone shall not select it → Acceptance #3
REQ-4 — Live conversation search
  WHEN asked to search conversations, the skill shall return matching snippets from the Claude, Codex and OpenCode agents of currently open panes in every workspace, worktree and tab, each labelled workspace, tab, pane and working directory ("整個 herdr 裏所有 workspspace / worktree /tab 的對話全文搜尋") → Acceptance #4
REQ-5 — Historical search
  WHEN history is requested, the same search shall also cover Claude, Codex and OpenCode conversations not open in herdr, labelled with working directory and marked not open ("也許都需要") → Acceptance #5
REQ-6 — Led multi-turn conversation
  WHEN asked to converse with an agent in another pane, the leading agent shall run a bounded loop (round limit, timeout on every wait, read before any resend), obtain each complete reply through a file hand-off when the screen read is incomplete, and stop at the limit; the other agent only answers ("透過 herdr 讓 agent A 跟 agent B 對話") → Acceptance #6
REQ-7 — Codex sandbox
  WHEN a herdr command fails with `Operation not permitted`, the skill shall tell the user herdr needs network permission in Codex's sandbox and not retry → Acceptance #7
REQ-8 — Version-following
  The skill shall contain no copy of the official skill text, so a herdr upgrade changes the loaded instructions without a loom-workflow release (Option 1 chosen: "可以先試試看 1 是否真的能運作嗎", then "開始吧") → Acceptance #8

## Design decision
- user-decided — one leader, the other agent only answers; OpenCode is in search scope (decision point ①, 2026-11-21).
- agent-decided — skill name `loom-herdr`: matches the `loom-memory`/`loom-visualization` prefix and avoids a name clash with the official `herdr` skill on hosts without plugin namespacing; `using-*` is reserved for routers.
- agent-decided (REQ-1, REQ-8) — SKILL.md step order: env gate → `herdr --skill` → extensions; extensions never restate official commands, only add rules the official text lacks.
- agent-decided (REQ-4, REQ-5) — one Python 3 stdlib script `scripts/herdr_search.py`: `herdr pane list` JSON → `agent_session` id → transcript; Claude/Codex JSONL by glob, OpenCode via `sqlite3` opened read-only (`mode=ro` URI). Plain substring match, case-insensitive; `--history` adds unopened transcripts; `--json` for machines. No index or cache.
- agent-decided (REQ-4) — if a transcript store or an OpenCode id cannot be resolved, the result lists that pane as "unsearchable: <reason>" rather than failing the whole search.
- agent-decided (REQ-6) — the conversation protocol is SKILL.md prose (round cap default 5, `--timeout` on every wait, file hand-off as the official fallback), not a script: smaller surface; critique complexity verdict PROCEED-WITH-CAVEAT.
- agent-decided (REQ-7) — detect only the literal `Operation not permitted` on a herdr command; any other failure follows the official skill's error rules.
- agent-decided — privacy: the search is read-only; SKILL.md states that matched snippets enter the calling agent's context and so reach its model vendor.

## Alternatives considered
- Copy the official SKILL.md into `references/` with a sync test: drifts every 2–3 weeks; rejected by user (Option 2).
- Separate extension skill beside the official one: user rejected installing two skills.
- Scripted conversation driver: more code than prose rules for a single-leader loop; deferred until a prose run fails.
- External indexers (memex, session-digger): third-party install and no herdr pane labels.

## Current state evidence
- Forward: `herdr --skill` prints SKILL.md byte-identical to herdrdev/herdr `skills/herdr/SKILL.md` (docs/loom/research/2026-11-21-herdr-skill-prototype.md).
- Reverse: no loom skill references herdr; only `loom-code/scripts/loom_checker/helpers.py:256` excludes `.herdr`.
- Error: Codex default sandbox returns `Operation not permitted` on the herdr socket (prototype note, Codex row).
- Data: Claude `~/.claude/projects/*/<id>.jsonl`, Codex `~/.codex/sessions/*/*/*/*<id>.jsonl` verified; OpenCode `~/.local/share/opencode/opencode.db` tables `session`, `session_v2`, `part`; herdr id not found in `part.session_id`.
- Boundary: `loom-code/scripts/check_mechanisms.py` skill budget 27; `loom-workflow/tests/scripts/test_skill_count.py` pins fifteen skills.

## UI flows
N/A — agent-facing skill; the user talks to their agent in natural language.
