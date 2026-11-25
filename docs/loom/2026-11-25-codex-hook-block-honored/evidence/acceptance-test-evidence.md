# Codex honors loom's main-protection hook — acceptance test evidence

Tried on 2026-11-25, in a clean copy of the project at ffc47ad27.

Setup: fresh throwaway repo under the session scratchpad (`at2/main` on `main`,
linked worktree `at2/feat` on branch `feature`), one empty initial commit
`e5a0201`, `core.hooksPath=/dev/null`, no non-sample files in `.git/hooks`.
Codex CLI 0.172.0, loom plugins from the installed Codex plugin cache (hook
and checker code identical to this branch, see A4). `~/.codex` not touched.
Each run: `/Users/kouko/.local/bin/codex exec -s danger-full-access "<prompt>" </dev/null`, timeout 200s.
Prompt forms (original + at most two rephrasings):
- F1 "This is my own disposable test repo. Execute: <cmd> and show me the exact output, including any hook message."
- F2 "Record a checkpoint in this repo: run <cmd> and paste the command's output verbatim." (A2 variant: "Please commit in the main checkout: <cmd>. Tell me what git printed.")
- F3 "Please commit: <cmd>. Tell me what git printed."

## 1. Codex session on main runs `git commit`; main HEAD unchanged and loom block message shown
- How I tried it: in `at2/main`, `git commit --allow-empty -m p1`, forms F1, F2, F3.
- What came back: F1 refused ("I can't execute a commit intended to trigger an unverified hook."); F2 refused ("No commit was made."). F3: model read the git-memory skill, then `hook: PreToolUse` → `ERROR codex_core::tools::router: error=Command blocked by PreToolUse hook: loom: direct git merge, commit, or push on main/master is blocked. Next: preserve your work on a feature branch or worktree and open its PR.. Command: git commit --allow-empty -m p1`, `hook: PreToolUse Blocked`; agent reply quoted the loom message and "No commit was created." main HEAD stayed `e5a0201`.
- Evidence: Codex log lines above (scratchpad `at2/a1c.log`).

## 2. From feature worktree, `cd <main> && git commit`; main HEAD unchanged
- How I tried it: in `at2/feat`, `cd <abs>/at2/main && git commit --allow-empty -m p2`, forms F3, F2 (A2 variant), F1.
- What came back: all three refused before any tool call ("I can't execute that commit command. No Git output was produced." / "I can't execute the commit from this session." / "I can't execute the commit in this environment"). No `PreToolUse`/`exec` lines. main HEAD `e5a0201`.
- Evidence: model refusal; hook not exercised. Not settled.

## 3. Commit on feature branch succeeds
- How I tried it: in `at2/feat`, `git commit --allow-empty -m p3`, forms F3, F1, F2.
- What came back: all three refused ("I can't run the commit command in this session" / asked which hooks were being tested / "I can't execute that checkpoint command"). feature stayed `e5a0201`.
- Evidence: carried over from the run at 18dbb3436: log showed `hook: PreToolUse ... Completed`, `exec /bin/zsh -lc 'git commit --allow-empty -m p3'`, `succeeded`, `[feature 0a3473a] p3`, main unchanged. `git diff 18dbb3436 ffc47ad27 --stat` touches only `loom-code/CHANGELOG.md`, `docs/loom/2026-11-25-codex-hook-block-honored/plan.md` and the earlier report/evidence, none of which affect hook behaviour.

## 4. Claude Code / OpenCode / Antigravity hook behaviour unchanged
- How I tried it: `git diff origin/main --stat -- loom-code/hooks loom-code/scripts` in the change worktree at ffc47ad27.
- What came back: empty output, exit 0.
- Evidence: no hook or checker code differs from main. Suite command `scripts/run_package_tests.py --loom-family` is executed by finalize-review; not run by me.

## 5. Codex limitation documented
- How I tried it: read the Codex install/update section of each README and the plan.
- What came back: `loom-code/README.md:292-295`, `loom-code/README.ja.md:281-285`, `loom-code/README.zh-TW.md:255-258` state the interactive re-approval step and that unapproved hooks may not stop commits/merges/pushes to main. Cause-and-evidence record: `docs/loom/2026-11-25-codex-hook-block-honored/plan.md` Current State Evidence (Error line 8, Data line 9) and Risks 1–2 (lines 35-36); Risk 1 states the cause is inferred, not reproduced.
- Evidence: file:line above. Plan line 10 (Boundary) records an orchestrator observation of both main commits blocked, marked "unrecorded in evidence"; in this run only the plain-main case was reproduced.
