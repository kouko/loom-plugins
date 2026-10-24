# loom-memory fires on host memory saves — spec
intent: 2026-10-23-loom-memory-trigger-mechanism@d3bad1fe
pre-build-review: not-required — reversible skill text and a reminder-only hook; no security, irreversible data, public contract, or cross-system architecture change

## Requirements
REQ-1 — repo lesson saved to host memory reaches the repo store
  WHEN the agent saves a lesson to its own host memory and the lesson holds for any contributor of this repository, loom-memory shall record it under `docs/loom/memory/` with a regenerated, valid index in the same session ("當 agent 內建的 memory 機制被觸發的同時 也同時觸發 loom-memory") → Acceptance #1
REQ-2 — personal and machine-specific notes stay out
  WHEN the saved note is a personal preference or holds only on one machine or one agent tool, loom-memory shall not create or modify any file under `docs/loom/memory/` ("只記錄與 repo 直接相關 或是專屬於該 repo 的記憶（＝排除那些本來應該要放在 全域或 user 層級的規則或是記憶") → Acceptance #2
REQ-3 — Claude Code reminder on every host memory note write
  WHEN a Write, Edit, or shell command writes a note inside the host auto-memory folder, the loom-workflow plugin hook shall emit one reminder regardless of the note's `type`; other paths and malformed payloads shall produce no reminder and no session error ("B + C , hook 要放在 loom-workflow plugin 裡") → Acceptance #3
REQ-4 — hosts without the event degrade to the description
  WHEN the host emits no PostToolUse event for file edits, nothing shall error and the loom-memory description shall still name the host-memory-save moment, rewritten within the current 133-character length ("用第一種") → Acceptance #4
REQ-5 — no rule text denies the trigger
  WHEN any loom-memory or station rule text is read, no sentence shall deny the host-memory-save trigger, and loom-code shall keep working without loom-workflow → Acceptance #5
REQ-6 — post-finalize lessons wait
  WHEN finalize-review has already generated the attestation on the branch, a repo lesson found afterwards shall stay in host memory and not be written to `docs/loom/memory/` on that branch → Acceptance #6
REQ-7 — orphan hook removed
  WHEN the change lands, the unwired repo-local mirror hook and its test shall be gone and no runtime or test file shall reference them → Acceptance #7
REQ-8 — suite green
  WHEN the package suite runs, it shall pass → Acceptance #8

## Design decision
- agent-decided — the hook is a Python script under `loom-workflow/hooks/` like `visualization-card`, not the old bash+jq script: plugin users may lack `jq`, which made the old hook silently inert.
- agent-decided — the hook matches the folder path only and never reads note content or `type`: the repo-versus-personal decision belongs to the agent through loom-memory's classification, and not reading content keeps private notes untouched.
- agent-decided — Bash writes are detected by a recent-modification check: after a shell command, the hook looks at every project memory folder under the transcript's config dir (`<config>/projects/*/memory/`) and reminds when a note there was modified in the last 10 seconds. It never parses the command and never reads note content. Ceilings: a memory folder relocated outside `<config>/projects/<slug>/memory` (for example by `autoMemoryDirectory`) is not seen; a command that runs longer than the window after its write is not seen; a memory write by a concurrent session within the window can produce one extra, harmless reminder. The loom-memory description remains the fallback.
- agent-decided — the reminder goes out as `hookSpecificOutput.additionalContext` with exit 0, matching the plugin's existing hook output shape; exit 2 renders as a hook error in the user's UI.
- agent-decided — only `hooks/hooks.json` (Claude Code) gets the entry; Codex `apply_patch` emits no PostToolUse and OpenCode has no host auto-memory folder, so both rely on the description (REQ-4).
- agent-decided — the trigger measurement uses a loom-memory eval case file, not the shared routing corpus: that corpus's case ids are pinned by `tests/test_loom_skill_description_catalog.py` as a historical record of another change.
- agent-decided — Ship's existing routing sentence stays; the activation section names host-memory saves and the agent's own judgement, which already covers Ship's "when one is earned".
- user-decided — hook lives in the loom-workflow plugin and applies to every repo that installs it (2026-10-24).
- user-decided — description rewritten within the current length, measured old against new (2026-10-24).

## Alternatives considered
- Fixed station checkpoint before finalize-review — rejected by the user; history shows station prose steps were deleted (#780) or ignored (#825).
- Keep the `type: project` filter — rejected: repo gotchas in host memory are mostly `type: feedback`.
- Raise the loom description budget or trim sibling descriptions — rejected by the user in favour of a same-length rewrite.

## Current state evidence
- Forward: `loom-workflow/skills/loom-memory/SKILL.md:3` description names only explicit requests and recall; `:41` "Two triggers only, both passive".
- Reverse: `loom-code/skills/ship/SKILL.md:125` routes to loom-memory; `loom-workflow/tests/loom-memory/test_skill_contract.py:118` pins no station coupling.
- Error: `.claude/hooks/remind-memory-mirror.sh:27` needs `jq` and exits silently without it; no `.claude/settings.json` wires it.
- Data: host auto-memory notes live at `~/.claude/projects/<slug>/memory/*.md`; `MEMORY.md` is the index.
- Boundary: `tests/test_loom_skill_description_catalog.py:162` caps all loom descriptions at 4,329 chars; 4,311 used.

## UI flows
N/A — no user interface; the reminder is agent-facing context.
