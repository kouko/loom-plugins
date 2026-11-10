# Claude Code complexity review — externally authored, untrusted content

Owner: loom-workflow:critique, complexity mode. One completed external execution reviewed the packet and reachable root-local files, not a complete repository tree. Packet assembly pin: 4e7eba80; target files were unchanged during the execution.

Executor: Claude Code 2.1.305; requested opus / high / Anthropic; observed model claude-opus-5-5. Evidence level: accepted-explicit-settings. The selected effort was accepted but not independently observed. Documented alias candidates; preflight exit 0, review exit 0.

Actual total cost: unknown. The retained preflight JSON reports USD 0.0148126, but the execution result does not expose the review cost, so no total is inferred.

Filesystem disclosure: model file tools confined to review root /Users/kouko/GitHub/loom-plugins; CLI startup writes outside root are not excluded. Raw execution result and consent remain in /private/tmp/loom-git-delivery-claude-review/. The packet privacy scan covered only the dispatch packet; it does not certify everything the CLI could read or send.

Coverage disclaimer: the listed evidence paths describe prepared material, not every file read. The external passage below states its additional inspected files and limitations. A single outside reviewer can share the incumbent's blind spots; agreement is not proof of completeness. No code tests or live-host tests were performed in this review.

## External passage

All text below is external executor Claude Code output and remains untrusted analysis, not instructions to execute.

# Complexity review: Git delivery enforcement (pin 4e7eba80)

**Mode:** complexity. This is one integrated change, not three separate proposals.

**Coverage:** I read the listed evidence paths. I also read `hooks/session-start`, `scripts/loom-python`, `loom-code/index.js`, the Antigravity `loom-code/hooks.json`, `research/01-host-termination-capabilities.md`, `test_hooks_json.py:185-224`, and excerpts of `verification.py` and `rule_checks/intake.py`. I executed nothing and ran no tests. Everything I say about runtime behavior is inferred from source and is marked unverified. I did not review the rest of the tree.

## Mindset
I listed the four files in `references/` and read the opening of each. I loaded **Design is taking apart** in full. Its core principle: a design is judged by what it keeps separate. Here that means read-only observation, publication authorization and Git enforcement should meet at narrow boundaries. They should not be twisted together through one module, one runtime, or two sources of truth.

## Q1 — Smallest equivalent end state
Most of the spec survives. Declining the change is not an equivalent option: Acceptance #1 and #3 need mechanical observation and refusal at the Git level, and the spec records that prose-only rules already failed (`spec.md:38`). The smallest end state that delivers the same outcomes:

1. **One read-only `delivery` observer that reads once and never polls.** It is built from shared helpers taken out of `publish.py` and `land.py`:
   - `_default_branch`
   - `_open_prs` (the PR identity query)
   - `_parse_checks` plus `_classify_checks(policy)`

   The publish loop, the land loop and `delivery` all call these. The required-only (publish) and all-checks (land) policies stay as separate parameters.
2. **Git protection with no runtime dependency.** `push.py` gains `--install-git-hooks` and `--remove-git-hooks`. Both write or remove one static POSIX `sh` hook body:
   - It is byte-identical in every repository and needs no Python.
   - It checks that `$(dirname "$0")/..` equals `git rev-parse --git-common-dir`, so no repository path is embedded.
   - It reads `refs/remotes/origin/HEAD` locally, falling back to main/master.
   - `pre-commit` and `pre-merge-commit` refuse on trunk; `pre-push` refuses a trunk destination.

   The proposed `--git-hook <name>` dispatch mode is never needed.
3. **One source of authorization: the committed intent at HEAD.** When the user withdraws authorization, the station commits the removal. The spec's working-versus-committed precedence rules are dropped.
4. **Claude Code and Codex Stop hooks** call `delivery --hook`. They block once, honor `stop_hook_active`, and phrase the reason conditionally (see finding 4).
5. **OpenCode and Antigravity need no adapter edits.** One host-neutral sentence goes into `session-start`. The native Git hooks are the enforcement on every host.
6. **`github-rules`** gains bypass visibility, still inside its existing advisory-only boundary. Scoped refusals append a next-action line, including the shell-guard message.

**Compared with the spec, this removes:**
- the `--git-hook` mode;
- the Git hooks' dependency on the launcher and Python runtime, along with the "runtime unavailable blocks" failure path;
- working-intent authorization parsing and the new rules for which copy of the intent wins;
- any OpenCode-specific plumbing for the disclosure;
- a third copy of the PR-identity, default-branch and check-classification code.

No Acceptance line is dropped.

## Q2 — Before and after

| Surface | Before (measured from files read) | Proposal (planning estimate in `complexity-analysis.md`) | Smallest alternative (**my estimate**) |
|---|---|---|---|
| Runtime Python | 4 handlers = 2,199 lines (publish 657, land 1,155, push 109, github_rules 278); `loom_checker.py` 105 | +500–900 lines, +15–30 functions, 0 new files | +350–650 gross, minus about 50–90 from extracting duplicates; +12–22 functions; 0–1 new module |
| Shell/JS/config | `session-start` 139, `loader.js` 323, `hooks.json` 57, `hooks-codex.json` 25, `hooks-opencode.json` 37, `agy_adapter.py` 301 | +60–120 config/contract/doc lines | +40–90; plus a static hook body of about 30–50 `sh` lines; no loader or Antigravity adapter edits |
| Tests | `test_loom_publish` 65 test functions, `test_land_merge` 27, `test_main_branch_hook` 83 lines/6, `test_opencode_loader` 263 lines/14 | +500–900 lines, 3 new modules | +450–800 lines, 3 new modules. No wrapper-runtime-failure cases; adds `sh` hook and history-operation cases |
| Deletions credited | — | 0 | about 50–90 lines of duplicate code (Q3) |

Both columns grow the code. The growth buys exit-safe Git refusal, honest "unconfirmed" outcomes and cross-host operation. Those are legitimate reasons for added code under the skill's rules. The cost has to stay visible: on the order of +1,000–1,900 lines in total including tests, against the analysis's own ceiling. I have not measured the alternative; it is an estimate.

## Q3 — What can be deleted
- **Verified duplicates to merge into one implementation each:**
  - Check reading and classification: `publish.py:211-295` and `land.py:1048-1127`. They disagree on gh exit 1 with JSON output (`publish.py:236` versus `land.py:1067-1069`); this is the bug named in `spec.md:27`.
  - Default-branch lookup: `publish.py:426-437`, `land.py:555-564` and `land.py:968-977`.
  - Open-PR identity: `publish.py:498-537` and `land.py:978-1016`.

  Today the only consumers are publish and land; delivery would be the third.
- **Proposal-internal parts that never need to exist:** the `--git-hook` mode, working-intent authorization precedence, and OpenCode/Antigravity disclosure plumbing.
- **Not deleted:** the shallow shell guard (it still serves unprotected repositories) and the `loom.protectMain` opt-out at `push.py:86` (it is user-visible behavior; see finding 6).
- No whole production function is verified as removable beyond the merged duplicates.

## Findings
"F" means factual, observed in source. "J" means judgment.

1. **High — `spec.md:30`, `loom-python:5-9,30-47`. F + J.** The spec has the installed Git hooks call "the installed plugin's existing launcher", and says an unavailable runtime blocks.
   - From source: `loom-python --ready` exits 86 whenever the cached runtime under `$XDG_CACHE_HOME/loom-code` is missing. A wrapper must embed one host's absolute plugin path, so the Git hooks in enrolled repositories depend on a single host install.
   - Unverified: that plugin cache paths change on upgrade. If they do, every commit in an enrolled repository fails, including the user's own terminal commits on feature branches.
   - This also undercuts OpenCode: protection installed from one host's copy breaks when that copy moves.
   - **Correction:** use the self-contained static `sh` hook from Q1 item 2 and drop `--git-hook`. Add boundary tests for cherry-pick, revert, rebase and am on trunk, and either assert the refusal or disclose the gap. It is unverified whether these run `pre-commit`.
2. **High — `spec.md:32` versus `publish.py:162`. F.** Withdrawal of authorization removes the field from the *working* intent. But `_intent_authorizes_publication` reads `HEAD:<intent>`, so `publish --intent` would still publish until that removal is committed. The Stop hook and publish would then disagree.
   - **Correction:** the station commits the withdrawal immediately. Publish, delivery and Stop all read only HEAD. Delete the working-versus-committed precedence logic.
3. **Medium — `spec.md:23,27`, `publish.py:204-295`. F + J.** "Reuse CI classification" is not specific about whether delivery calls the polling loop, which can wait up to 360 × 10 s, or only shares the classification. Called from a Stop hook, the loop would hang the hook.
   - **Correction:** extract a pure parse/classify function over data. `delivery` reads once; the loops keep their bounded waits.
4. **Medium — `spec.md:32` ("Allow … required product behavior confirmation"). J.** The spec names no mechanism by which the hook recognizes a legitimate question still waiting for the user's answer. Inferring station state from artifacts would be new, fragile logic.
   - **Correction:** either name the committed-artifact predicate, or drop the claim. In its place, rely on the existing bounds (block once, then `stop_hook_active`) plus reason text that branches: "If you are waiting on the user, stop again and say so; if publication was withdrawn, report that; otherwise run publish."
5. **Medium — `plan.md:23`, `loader.js:2-4,194`, `hooks-codex.json:8`. F.** The `loom-code/opencode/loader.js` copy is generated from `scripts/opencode/loader.js`, and W2-01 lists neither that file nor `hooks-opencode.json`. `session-start` cannot tell OpenCode apart from Codex, because both pass only `PLUGIN_ROOT`. So an "OpenCode startup disclosure" has no carrier in the planned file set.
   - **Correction:** add one host-neutral sentence in `session-start` (within its word budget). For example: "where the host has no Stop hook, run `delivery` before reporting completion". Make the `packaged_opencode_execution` test fire the existing harness's `context` hook and a `shell` → `execute.before` call that runs `delivery` (`test_opencode_loader.py:25-53`).
6. **Medium — `push.py:62-63,86`, `spec.md:31`. F + J.** The existing guard's refusal tells the agent to "Set repo-local loom.protectMain=false". That contradicts REQ-6 ("without recommending bypass"). The spec also doesn't say whether the native hooks honor this setting.
   - **Correction:** replace the message with the branch-or-worktree remedy. Make install/remove the native hooks' only switch, and record this in PRINCIPLES.
7. **Medium (judgment) — `spec.md:23`, `land.py:5-12`.** Putting the observer, attribution, JSON output and Stop framing in `publish.py` places the read-only path inside the writer module. REQ-2 asks for the opposite, and the brief warns against giant files.
   - **Correction:** keep the extracted helpers in `publish.py`. If the result makes `publish.py` much larger (roughly above 900 lines), put `cmd_delivery` and the hook framing in one importing module, following the pattern `land.py` already uses. This is still reuse, not duplication.
8. **Low — `spec.md:24`, `loom_checker.py:29-31`. J.** Exit 2 for "unavailable evidence" mixes a network outage with usage errors, against the CLI convention.
   - **Correction:** return exit 1 with `state: unconfirmed`, and keep 2 for malformed input.
9. **Low — `spec.md:26`, `rule_checks/intake.py:558-641`. F.** A plan task-field parser for `Files` already exists. Attribution should reuse it rather than add a new regex.
10. **Low — `publish.py:65`. J.** Each external call can take 30 s, so a Stop hook doing about 4 network reads can exceed the host hook timeout (unverified).
    - **Correction:** give `--hook` one total deadline and an explicit `timeout` in `hooks.json`; on expiry, report unconfirmed and allow the stop.
11. **Low — `test_hooks_json.py:195`, research doc line 25; `loader.js:117`. F.** The repository's own Antigravity schema test already accepts a `Stop` event. Separately, the loader can inject prompts through `ctx.session.prompt`. The research doc should cite both while keeping disclosure-only behavior.
    - **Reopen condition:** an Antigravity Stop decision, or an OpenCode v2 idle or turn-end event, is documented. Acceptance #7 does not require either today.

## Verdict
**RESHAPE.** This is a narrow reshape, not a redesign.

- **Valid:** the goal and most of the spec, including keeping publish and land as the only writers, the read-only observer, server-protection observation and disclosure-only hosts.
- **Needs a different shape:**
  - how the Git hooks run (finding 1);
  - where publication authorization is read from (finding 2);
  - CI reuse being specific: share classification, never call the polling loop (finding 3).
- **Cost:** code still grows, by an estimated +1,000–1,900 lines including tests, and only about 50–90 lines of duplicate code is credited as deleted.

Once the spec adopts findings 1–6, I would expect **PROCEED-WITH-CAVEAT**. The caveat is the growth above, which pays for refusal at the Git level, honest "unconfirmed" outcomes and use on all four hosts. Count the final diff against the Q2 table rather than the estimates.