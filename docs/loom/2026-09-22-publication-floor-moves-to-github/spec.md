# Publication floor moves to GitHub — spec
intent: 2026-09-22-publication-floor-moves-to-github@71377548
pre-build-review: required — the change removes the only local publication gate, adds a public contract (a CI template other repositories copy) and spans two systems (the local checker and GitHub branch rules)

## Requirements
REQ-1 — PR body floor on GitHub
  WHEN a pull request targeting the protected trunk has a body missing any of Ship's nine contextual headings or carrying an empty section, the loom PR-floor CI check shall fail and name that heading, so GitHub refuses the merge → Acceptance #1
REQ-2 — Trunk accepts pull requests only
  WHERE the trunk carries the rule set that `loom_checker.py` prints for it, the trunk shall accept changes only through a pull request, so a direct push to the trunk is refused by GitHub → Acceptance #2
REQ-3 — Recomputed verification disclosure
  WHEN the loom PR-floor CI check runs, it shall recompute the branch's verification status from repository content as one of `valid`, `absent` or `stale`, publish that status in the check's own output, pass for all three, and ignore any status text written in the PR body → Acceptance #3
REQ-4 — Hook never refuses publication
  WHEN an agent runs any Bash command that pushes or opens a pull request, the publication hook shall exit 0; WHERE the command's first simple command is literally `git push` or `gh pr create`, it shall also emit one reminder line naming the branch's verification status → Acceptance #4
REQ-5 — Ship refuses a malformed body before the PR exists
  WHEN the Ship station's publish command receives a body missing a heading or carrying an empty section, it shall refuse before pushing or creating the pull request and name that heading → Acceptance #5
REQ-6 — Land checks the body and discloses verification
  WHEN `loom_checker.py land` is run, it shall read the pull request's live body and refuse when a heading is missing or empty, naming it; IF the body passes and the verification status is `absent` or `stale` THEN it shall merge and print one reminder line naming that status → Acceptance #6
REQ-7 — Ship reports missing GitHub rules
  WHEN the Ship station runs in a repository whose trunk lacks the pull-request requirement or the loom PR-floor required check, it shall print which of the two is missing and one command that would add it, and shall not change any GitHub setting itself → Acceptance #7
REQ-8 — Ship tolerates unreadable rules
  IF the trunk's rules cannot be read (no permission, no GitHub remote, or the API fails) THEN the Ship station shall print that the rules could not be confirmed and continue publishing → Acceptance #8
REQ-9 — Copyable CI template
  The loom-code plugin shall ship one CI template file that, copied unchanged into a GitHub repository's workflow directory, runs the same PR-floor check as REQ-1 and REQ-3 on every pull request → Acceptance #9
REQ-10 — Skipping needs words, not a code, and is reminded
  WHEN the user tells the agent in plain words to skip a step, the stations shall continue without asking for a generated code and the agent shall tell the user which step it skipped; WHEN such a branch is pushed, has its PR opened or is merged, the reminder line shall list which verification records are absent → Acceptance #10
REQ-11 — Principle 2 amended
  The repository's PRINCIPLES.md non-negotiable 2 shall state that a skipped verification step must be disclosed on the pull request and shall no longer require a typed confirmation, and shall carry the user's ratified-by line → Acceptance #11
REQ-12 — Mentioning a merge is silent
  WHEN a command only mentions the merge words (a search, printed text, a commit message), the publication hook shall exit 0 and emit nothing → Acceptance #12
REQ-13 — Suite green
  The complete package suite shall pass → Acceptance #13

## Design decision
- **The floor is GitHub, loom stops guessing** — the trunk is guarded by a GitHub rule set (pull request required, zero approvals, the loom PR-floor check required) instead of the PreToolUse shell-text parser. user-decided (① answer: move the floor to GitHub; keep nine sections).
- **Where loom still refuses** — only inside its own commands: `publish` (Ship's single push+PR command, which already validates the body at `publish.py:365`) and `land` (new body check against `gh pr view --json body`). The selection-store guard keeps refusing file-tool writes. Carried detail: 「loom 自己的合併指令（`land`）合併前讀 PR 內文再檢查一次」; 「跳站紀錄目錄的防護（`selection.guard`）維持阻擋」. user-decided.
- **Hook becomes warn-only with shallow recognition** — the hook recognises a push, PR create or PR merge only when it is the first simple command after `VAR=` assignments; every other shape is silent. It never exits 2 for publication. Carried detail: 「PreToolUse hook 只提醒，只辨認最常見的寫法；漏看只是少一行提醒」. user-decided. The merge reminder keeps its current meaning (outside `land`); the push/PR reminder names the verification status.
- **Rule ids** — `push.merge` and the hook side of `push.attestation` are retired (removed from `rules.py` and `mechanisms.yaml`); the `publish`/`land` attestation reading becomes disclosure under a new id `publish.verification-status`; the CI check is `ci.pr-floor`; the Ship rules probe is `ship.github-rules`. Net mechanism count must not rise (NN4): three retired or rewritten, two added. agent-decided — reuse of `push.contextual-body` keeps the nine-heading rule's id stable for existing evals.
- **Verification status has two depths** — local (`publish`, `land`, hook) runs the full `validate_attestation`; CI cannot, because selection records live under the git common dir (`selection.py:87-91`) and are absent in a fresh checkout (`attestation.py:104-108`). CI therefore computes status from committed content only: `absent` (no attestation in the branch delta), `stale` (attestation present but its functional-content digest, executions or reviewer verdicts fail), `valid` (all content-level checks pass). agent-decided — the alternative (uploading selection records) would put local-only records into the repository.
- **Status is published by the check, not read from the body** — the CI check writes the status into its job summary and check title; it never parses a status sentence from the PR body, so editing the body cannot change it (REQ-3). Ship still writes the locally computed status into the body for human readers. agent-decided.
- **CI template shape** — a caller workflow `loom-code/templates/loom-pr-floor.yml` that invokes a reusable workflow `.github/workflows/loom-pr-floor.yml` (`on: workflow_call`) in this repository, referenced at `@main` with a comment showing how to pin a commit SHA. The reusable workflow checks out the calling repository and this repository's `loom-code/scripts`, then runs a new read-only subcommand `loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha>` on `pull_request` events `opened, edited, synchronize, reopened`. agent-decided — one source of the nine-heading rule; `@main` chosen over version tags because the repository publishes no release tags today.
- **Ship's rules probe** — reads `gh api repos/{o}/{r}/rules/branches/{trunk}` (rulesets; readable with read access) and, when readable, the classic `branches/{trunk}/protection` endpoint (admin-only; this repository uses it today), taking the union — a repository protected only by classic rules is not reported as missing; `pull_request` rule (or classic `required_pull_request_reviews`) and a `required_status_checks` rule containing the `ci.pr-floor` context are the two things looked for. Missing → print what is missing and one `gh api -X POST repos/{o}/{r}/rulesets --input -` command with the JSON body; never execute it. Unreadable → one line "could not confirm" and continue. Carried detail: 「ship 站用 `gh api` 讀 main 的保護規則；沒設時提示缺什麼，並附一個可以直接設定的指令，由你確認後才執行」. user-decided (no GitHub setting changes without consent — intent Constraint).
- **Skipping** — zero-attestation no longer refuses in `publish` (`publish.py:438`) or `land` (`land.py:954`); `publication_advice` stops offering the typed-code route. Station prose (ship, closing-review, build, using-loom-code) tells the agent: skip only on the user's instruction, and say in one line which step was skipped before continuing. Carried detail: 「agent 可以在跳過的時候給使用者提醒（但是不擋流程繼續執行）」. user-decided (① answer A). The expert-mode skill and its selection store are left as they are: an optional route that still records skips. agent-decided — removing them is a separate change and would raise churn without serving an Acceptance line.
- **Reminder content** — the reminder lists which of these records are absent: confirmed intent, plan, attestation (and, when present but stale, which content-level check failed). TDD order is not listed; no record exists to compute it. agent-decided.
- **PRINCIPLES.md amendment** — non-negotiable 2's last sentence becomes: "A step the user skips by plain instruction falls outside this guarantee, and every such skip must be disclosed on the pull request, where the verification status is recomputed rather than claimed." `ratified-by: kouko 2026-09-22` records the ① answer. user-decided.
- **Parser shrink** — `rule_checks/push.py` keeps only what non-hook callers import (`_shell_segments`, `_strip_prefix`, `_tokenise` for `selection_guard.py:12-14`; `github_repo_from_origin`, `CANONICAL_PUSH_FLAGS` for `publish.py:18-19` and `land.py:27`) plus the shallow recogniser; everything reachable only from the hook's refusal path is deleted with its tests. agent-decided.
- **This repository adopts its own floor** — the caller workflow is added under `.github/workflows/` here. Applying the GitHub rule set to kouko/loom-plugins is an outward action and is proposed to the user, not performed, per the intent's Constraints. agent-decided — no authorisation, conservative option.
- **Not doing** — no pre-push git hook, no `gh api …/merge` recognition, no change to `~/dotfiles`, no deletion of branch `loom-gate-warn` (intent Out of scope).

## Alternatives considered
- Fix branch `loom-gate-warn` and keep the shell parser as the gate — rejected: it cannot see web or user-terminal merges, and each hardening round reopened a bypass (3 confirmed, 23 failing tests).
- Keep a typed confirmation without a generated code (option B) — rejected by the user at ①.
- CI parses a status sentence from the PR body and fails on mismatch — rejected: it reintroduces a hard stop and still trusts text; publishing the status from the check itself is simpler and cannot be edited.
- Inline a copy of the nine-heading validator in the CI template — rejected: two copies drift; the reusable workflow runs the one implementation.
- Pin the template to release tags — rejected for now: the repository has no release tags; a SHA-pin comment covers adopters who need immutability.
- Read the admin-only branch-protection endpoint — rejected: most collaborators lack admin; the branch-rules endpoint answers with read access.
- git pre-push hook for trunk pushes — rejected (intent Out of scope; GitHub rules already refuse them).

## Current state evidence
- Forward: `loom-code/hooks/hooks.json:15-21` runs `loom_checker.py push --hook` on every Bash/Write/Edit; Ship publishes through `loom_checker.py publish` (`loom-code/skills/ship/SKILL.md:118-129`).
- Reverse: `rule_checks/push.py` helpers are imported by `selection_guard.py:12-14`, `publish.py:3,18-19`, `land.py:15-17,27`; the hook is also reached from `hooks/hooks-codex.json:13-28` and `hooks/agy_adapter.py:138-168`.
- Error: zero attestation refuses in `publish.py:438` and `land.py:954` via `_cmd_push`; merges refuse through `push.merge` (`rules.py:124`); the refusal text offers the typed-code route (`command_handlers/push.py:143`, `skills/expert-mode/SKILL.md` §2).
- Data: attestation validation needs local selection records under the git common dir (`attestation.py:104-108`, `selection.py:87-91`); the nine headings are `CONTEXTUAL_PR_HEADINGS` (`rule_checks/publish.py:6`); rule ids registered in `rules.py:108-132` and `docs/loom/evidence/mechanisms.yaml:152-169`.
- Boundary: stops at GitHub branch rules and the PR-floor check; `land`'s other preconditions (`land.py:911-1016`), `land.verify`, `land.cleanup`, expert-mode and the selection guard are unchanged; `.github/workflows/loom-code-ci.yml:87-88` job stays as is.

## UI flows

| case | what the user/agent does | what they see |
|---|---|---|
| push, no record | agent runs `git push …` on a branch with no attestation | command runs; one line `loom: no verification record on this branch (missing: attestation); publishing anyway.`; exit 0 |
| push, stale | same, attestation present but content changed since | command runs; `loom: verification record does not match this branch (<which check>); publishing anyway.`; exit 0 |
| wrapped push | `true; git push …`, `bash -c '…'`, heredoc | command runs; no line |
| merge outside land | agent runs `gh pr merge …` | command runs; `loom: this merges outside loom_checker.py land; merging anyway.`; exit 0 |
| merge words only | `grep "gh pr merge" …`, `echo`, commit message | command runs; no line |
| Ship publish, bad body | Ship station publishes with a missing or empty heading | refused before any push: `BLOCK push.contextual-body: <heading> is missing` (or `is empty`); agent fixes the body and reruns |
| Ship publish, good body | Ship station publishes | branch pushed, PR opened; PR body carries the status line; terminal shows the reminder when status is not `valid` |
| Ship, rules missing | Ship runs where the trunk lacks the rules | `loom: <trunk> does not require a pull request` and/or `does not require the loom PR-floor check`, followed by one `gh api … rulesets` command; publishing continues; nothing on GitHub changes |
| Ship, rules unreadable | no permission / no GitHub remote / API error | `loom: could not confirm GitHub rules for <trunk> (<reason>)`; publishing continues |
| land, bad body | `land --accepted-by <name>` on a PR whose live body lacks a heading | `BLOCK land.merge: PR body <heading> is missing`; nothing merged; fix the PR body on GitHub and rerun |
| land, no record | same, body fine, no attestation | merged; reminder line naming `absent`; exit 0 |
| CI, bad body | PR opened or body edited with a missing heading | check `loom PR floor` fails, summary names the heading; GitHub's merge button stays blocked until the body is edited |
| CI, good body | PR opened/edited/synced | check passes; title reads `verification: valid|absent|stale` |
| skip by words | user: "skip review, open the PR" | agent: "Skipping closing review as you asked; the PR will show verification absent." and continues |

In progress: every check above is a single command run; no waiting surface beyond the command itself. Empty: a repository with no trunk rules and no template behaves as the "rules missing" row.
