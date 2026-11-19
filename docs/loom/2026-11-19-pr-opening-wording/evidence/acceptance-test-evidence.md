# The PR-opening step is no longer called publish — acceptance test evidence

Tried on 2026-11-19, in a clean copy of the project at 518bcca7a; re-run at 75e480392 (see the last section) (detached `git worktree add` of HEAD in a scratch directory; the pre-change version came from a second worktree at merge-base 995d77d2a). Remote operations used a throwaway local repo with a local bare `origin`; nothing was pushed to GitHub and no real PR was opened.

Setup: no install step is needed; `python3 loom-code/scripts/loom_checker.py --help` runs in the clean copy and lists `open-pr` (usage lines 11-12, "Detailed help: finalize-review --help, open-pr --help, delivery --help").

## 1. `open-pr` 以原本 `publish` 的相同參數完成推送、開啟或沿用 PR、等待 CI。
- How I tried it: in the throwaway repo (branch `feat`, local bare origin) ran `open-pr --intent <missing path> --title T --body-file <body>`, then `open-pr --confirm-authorized --title "Test change" --body-file <nine-heading body>`. Ran the criterion's own tests: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID python3 -m pytest -q loom-code/tests/test_loom_publish.py loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_adversarial_blocked_publish_routes.py`.
- What came back: both argument forms accepted; `--intent` refusal "open-pr: --intent is not a readable file" exit 2; with a complete body it reached the precondition check "BLOCK publish.preconditions: cannot identify the change …" exit 1; `git ls-remote` showed no `feat` branch pushed. Tests: 146 passed in 37.77s.
- Evidence: captured output above; the real push/PR/CI path against GitHub was not exercised (no throwaway GitHub remote) and is covered by the controlled cases in `test_loom_publish.py`. Package suite (`scripts/run_package_tests.py --loom-family`) is left to finalize-review.

## 2. 執行舊命令 `publish` 時，與任何不存在的命令一樣回報 unknown sub-command，不推送、不開 PR，以非零結束。
- How I tried it: `loom_checker.py publish --intent x --title t --body-file b`; `publish --help`; `nosuch`; `loom-python --repair publish --help`.
- What came back: `unknown sub-command 'publish'.` exit 2 (same shape and exit as `unknown sub-command 'nosuch'.`); `publish --help` same; launcher form ends "Suggested next step: Inspect global --help and select a supported command…" exit 2. No rename hint printed.

## 3. 開 PR 這一步（含等待 CI 與交付狀態回報）中，CLI 印給使用者的訊息、命令說明與錯誤建議，都把這一步描述為開啟或沿用 PR、等待合併，不再使用 publish／published／publication 字眼。
- How I tried it: read `open-pr --help` output in full, global `--help`, refusal advice lines from item 1; grepped string literals in the handlers.
- What came back: title line "open-pr — open or reuse a Ready PR awaiting merge…", "exit 0 means the PR is open and awaiting merge", advice "running open-pr again". But the shared footer printed at the end of `open-pr --help` still says:
  - "No validation or publication occurred: help only, exit 0." (`loom-code/scripts/loom_checker.py:541`, `HELP_NOTICE`)
  - "Advice is optional and never authorizes execution, retry, publication, merge or bypassing trust." (`loom_checker.py:550`)
- Also `delivery --goal published` appears in the help; that is a value name the intent lists as out of scope. `BLOCK publish.preconditions` is a rule id, out of scope.
- Evidence: captured `open-pr --help` output.

## 4. 推送提醒 hook 印給使用者的說明（目前的 `publishing anyway`）改用相同的說法。
- How I tried it: piped a PreToolUse payload `git push origin feat` into `push --hook` on the throwaway repo; then `git commit` payload on `main`.
- What came back: "loom: change not identified (no intent for this branch); proceeding." exit 0; on main "…Next: preserve your work on a feature branch or worktree and open its PR." exit 2. `git diff 995d77d2a HEAD -- command_handlers/push.py` shows `publishing anyway` → `proceeding` (both forms) and the failure line → "push hook failed".

## 5. Ship 站對使用者的回報（PR 結果與合併前的驗收提問）、Ship 指示 agent 執行的命令，以及確認 intent 時告知「答 yes 之後會推送並開 PR」的那句話，都用相同的說法與新命令名，並保留「合併是另外的決定」。
- How I tried it: grep of `loom-code/skills/ship/SKILL.md`, `ship/README.md`, `using-loom-code/SKILL.md`, `loom-design/skills/capture-intent/SKILL.md`, `write-plan/SKILL.md` for publish/publication/發布/公開 and `open-pr`.
- What came back: commands at `ship/SKILL.md:225,231` are `--repair open-pr …`; report line 391 names "`open-pr` printed, PR-opening checks, PR URL"; capture-intent:195 "push and a Ready PR awaiting merge"; "merge is separate" kept in the station table. Remaining hits are `publication:` field / `publish.preconditions` / `--goal published` (out of scope) plus one prose phrase "Publication-only edits (PR title and body text)" at `ship/SKILL.md:162` and "publication-only fixes" in the capture-intent/write-plan station table (agent-facing guidance, nit).

## 6. repo 的 README 中描述這一步的文字使用相同的說法與新命令名。
- How I tried it: grep of all seven READMEs and `loom-code/references/cli-results.md`.
- What came back: English READMEs updated ("③ Open PR and accept result", "a pull request awaiting merge", `open-pr` rows). Still old wording:
  - `loom-code/README.zh-TW.md:7` "送到已發布的 pull request"; `:29` "③ 發布 PR 並驗收結果"; `:133` "發布 hook"; `:172` "攔截發布操作"
  - `loom-code/README.ja.md:7` "公開済みの…"; `:31` "③ PR を公開し結果を確認"; `:151` "公開用 hook"; `:192` "公開操作"
  - `loom-code/references/cli-results.md:90` "continue, publish, merge" (advice text), link labels "Controlled publication cases"/"Publication" (`:27,:125`)

## 7. 已經安裝原生 git hook 的 repo 在更新後，仍能正常安裝與移除該 hook。
- How I tried it: in the throwaway repo (after `git remote set-head origin -a`), installed with the pre-change checker (`push --install-git-hooks` from the 995d77d2a worktree), then re-installed and removed with the new checker.
- What came back: old install "native Git protection installed." exit 0, pre-commit/pre-merge-commit/pre-push sha1 18427883a8166b0795008e45d681d71bc8df1eb9; new install exit 0, identical sha1; new remove "native Git protection removed." exit 0, no hooks left. `push.py` diff vs base touches no `NATIVE_HOOK` lines.
- Note: on first try both versions refused with "symbolic-ref refs/remotes/origin/HEAD unavailable" until origin HEAD was set — pre-existing behaviour, same in old and new.

## 8. 照 Ship 指示操作的 agent 仍能完成開 PR、等待 CI 與合併，完整 package suite 通過。
- How I tried it: Ship's commands (item 5) match the accepted CLI (item 1); ran the same 146 targeted tests (pass). Full package suite not run here: it is executed by finalize-review, which refuses the attestation when it fails.
- What came back: 146 passed; no live GitHub merge exercised.

## UI flows (spec)
- new command: as item 1. old command: as item 2. help: as item 3 (footer wording remains). push reminder: as item 4.

## Re-run on 2026-11-19, at 75e480392
Tried on 2026-11-19, in a clean copy of the project at 75e480392 (detached worktree). Fix range 6e83bc65f..75e480392 touches `loom_checker.py` (HELP_NOTICE, 2 lines), `loom-code/README.zh-TW.md`, `loom-code/README.ja.md`, `loom-code/references/cli-results.md`, `test_loom_checker_cli.py`, `test_loom_publish.py`. Setup: `loom_checker.py --help` exit 0.
- 1: re-tested — targeted tests (`test_loom_publish.py`, `test_loom_checker_cli.py`, `test_adversarial_blocked_publish_routes.py`, run with `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`) 146 passed in 38.19s; the fix changed help text and two of these test files.
- 2: re-tested — `loom_checker.py publish` → `unknown sub-command 'publish'.` (unknown-command path shares the help module the fix edited).
- 3: re-tested — full `open-pr --help` grepped for publish/publication: only hit is line 53 `delivery --goal published` (value name, out of scope). Footer now "No validation ran and no PR was opened: help only, exit 0." and "never authorizes execution, retry, opening a PR, merge or bypassing trust." Head line and refusal advice unchanged from first run (open or reuse … awaiting merge; running open-pr again).
- 4: carried over — fix diff does not touch `command_handlers/push.py`.
- 5: carried over — fix diff does not touch any SKILL.md (ship, using-loom-code, capture-intent, write-plan). The "Publication-only edits" nit remains.
- 6: re-tested — all READMEs and cli-results.md grepped for 發布/公開/publish/publication. zh-TW:7 "送到等待合併的 pull request", :29 "③ 開 PR 並驗收結果", :133 "push hook", :172 "攔截 push 操作"; ja:7 "マージ待ちの pull request", :31 "③ PR を開き結果を確認", :151 "push hook", :192 "push 操作"; cli-results.md:27,:125 link labels "PR-opening cases"/"PR opening"; remaining publish hits are only the test file name `test_loom_publish.py` (internal name, out of scope). Remaining 公開 hits are "公開介面/公開インターフェース" (public interface, unrelated). Root and English READMEs unchanged since the first run.
- 7: carried over — fix diff does not touch `NATIVE_HOOK` or hook install/remove code.
- 8: re-tested — same 146 targeted tests passed; Ship commands still match the CLI. Full package suite left to finalize-review.
- UI flows: new command, old command, help re-tested as items 1-3; push reminder carried over as item 4.
- Minor: ja README:192 now reads "hook がpush 操作" (no space before "push"), cosmetic.
