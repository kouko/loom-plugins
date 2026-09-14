# Let the user choose which Loom steps a single change runs — spec
intent: 2026-09-14-expert-mode-step-selection@17aaaa83
pre-build-review: required — changes who may waive verification at the publication gate (a security boundary) and extends the public attestation and contract format

## Requirements
REQ-1 — Proposal and typed confirmation
  WHEN the user describes in natural language which steps to run or skip, through the expert-mode entry point or in ordinary conversation, and then types the entry point's confirmation with the code shown, Loom shall show the user, through the hook's own message rather than the agent's reply, the exact run/skip lists that bound, and shall apply them to the change's remaining steps; WHEN the user withdraws the selection in their own words, the full process shall resume → Acceptance #1
REQ-2 — Full process until a captured confirmation is bound
  WHILE no confirmation captured from a user-submitted prompt is bound to the change, the checker shall report the full step set and shall refuse every skip at finalization and publication, including after a plain reply such as "yes", after an agent-run capture command, and after an agent-written selection record → Acceptance #2
REQ-3 — Fixed floor
  The checker shall require, for every change regardless of selection, publication through the canonical publish command and a generated attestation whose content digest matches the pushed content → Acceptance #3
REQ-4 — Agent suggestion never binds
  IF the agent suggests skipping steps the user did not ask for THEN no step shall be skipped unless a later confirmation is captured from a user-submitted prompt, and the agent shall show the suggestion at most once per change and continue the full process without waiting → Acceptance #4
REQ-5 — Disclosure of skipped steps and authority
  WHERE a change's attestation carries a selection, the publish command shall refuse a pull-request body whose skipped-steps disclosure does not name every skipped step, its authority, and every recorded prior failure exactly as the attestation records them → Acceptance #5
REQ-6 — One selection, one change
  The checker shall apply a selection only to the change-id, branch and merge base it was confirmed for → Acceptance #6
REQ-7 — Mid-change selection
  WHEN a further selection is confirmed partway through a change, the checker shall apply it only to steps that have not yet produced evidence, and the pull request shall disclose every earlier selection and every recorded failure dated before it → Acceptance #7
REQ-8 — Skipped-review ledger
  WHEN the user runs the skipped-review query, the checker shall list each merged change on the default branch whose attestation records reviewers as skipped, or print that none did → Acceptance #8
REQ-9 — Both supported hosts
  The expert-mode entry point, the confirmation capture and the checker behaviour shall produce the same selection outcome on Claude Code and Codex CLI → Acceptance #9
REQ-10 — Unused lane settings removed
  The contract manifest, the intent and KICKOFF templates, the intent checker, the review lens text, the mechanism registry and this repository's `KICKOFF-DEFAULTS.md` shall carry no `lane:` field, `default-lane` key or express/gate-only grammar, and the repository's package tests shall pass → Acceptance #10
REQ-11 — Package tests when not skipped
  IF package tests are not in the bound skip list THEN finalization shall execute them and require them to pass → Acceptance #3

REQ-3 was split: its floor obligation keeps the number, and the package-test
clause took REQ-11. Both answer Acceptance #3.

## Design decision
**Shape.** One skill surface, one capture hook per host, a PreToolUse guard
over the record store, one checker command group, and a selection field in
the attestation. The skill talks; the hook records what the user submitted
and tells the user what bound; the checker decides.

```
user types / speaks ─► agent: selection propose ─► table + code in reply
user types confirm  ─► UserPromptSubmit hook ─► record + systemMessage to user
agent tool calls    ─► PreToolUse guard ─► deny capture CLI / record writes
stations            ─► selection show ─► effective run/skip steps
review              ─► finalize-review ─► failures recorded; attestation.selection
ship                ─► publish validates attestation + disclosure ─► PR
```

1. **Step vocabulary is checker-owned** — agent-decided. The manifest gains
   `step_selection.steps`: `intent`, `spec`, `plan`, `implementer`, `tdd`,
   `reviewers`, `adversarial`, `blind-run`, `package-tests`, each with
   `requires:` dependencies (`spec`, `plan` and `blind-run` require
   `intent`). Publication, the merge decision and the attestation are not in
   the vocabulary, so no instruction can name them. `propose` refuses
   unknown names and unmet dependencies.
2. **Record store and threat model** — agent-decided. Append-only JSON lines
   at `<git common dir>/loom/selections/<change-id>.jsonl` with events
   `proposal {id, code, origin, run, skip, branch, merge_base, created_at}`,
   `confirmation {proposal_id, code, source, session_id, prompt_ref,
   prompt_text, prompt_sha256, branch, merge_base, at}`, `cancel {...}` and
   `failure {step, rule, head_sha, at}`. Records are untracked and never
   enter the functional digest. Threat model: an agent that takes a shortcut
   under pressure, including running a documented command or writing a file
   to get past a gate. Out of the model: an agent that deliberately disguises
   a command to evade the guard in decision 3; that stays at the same
   independent-CI trust boundary the attestation design chose for a
   malicious repository author, and the skill states it.
3. **Capture path is closed to the agent** — agent-decided.
   - `UserPromptSubmit` entries in `hooks.json` and `hooks-codex.json` run
     `loom_checker.py selection capture --hook`.
   - `capture` refuses input whose `hook_event_name` is not
     `UserPromptSubmit` or that lacks the host's prompt reference
     (`prompt_id` on Claude Code, `turn_id` on Codex), and refuses to run
     without `--hook`.
   - The PreToolUse hook on both hosts denies any Bash command whose text
     names `selection capture` or `loom/selections`, and any file-writing
     tool call (Claude Code Write, Edit, MultiEdit, NotebookEdit; Codex
     apply_patch) whose target resolves under `<git common dir>/loom/`.
     The Claude Code matcher widens from `Bash` to those tools; whether
     Codex fires PreToolUse for apply_patch is measured in the plan, and if
     it does not, that gap is disclosed as a Codex limitation.
   - A confirmation prompt is one whose first token is an entry-point token
     and which contains a pending proposal's code as a standalone token; the
     other words are free, in any language. The record keeps `prompt_text`,
     and finalize-review and publish accept a confirmation only when
     `prompt_sha256` matches that text and the text still satisfies this
     grammar for the bound code.
4. **What bound reaches the user outside the agent** — agent-decided. The
   code is four characters of sha256 over the change-id and the sorted run
   and skip lists. On a successful capture the hook returns JSON
   `systemMessage` naming the change-id and the exact run and skip lists
   read from the record, so a table the agent misrepresented is visible at
   once. Withdrawal only restores checks, so it needs no proof of origin:
   the agent reads the user's intent in any wording or language and runs
   `selection cancel <change-id>`, which records a cancel for the newest
   confirmation on the branch. The guard does not block that command.
5. **Proposal origin and suggestions** — agent-decided. `selection propose
   <change-id> --origin user|agent`. Origin is not a trust input: it decides
   only whether the agent waits. "At most once per change, never waiting" is
   a skill and station prose rule with a regression eval, because no checker
   datum can prove whether a suggestion was shown; no binding depends on it.
6. **Binding rule** — agent-decided. `capture` binds to the newest
   unconfirmed proposal for the change whose code matches and whose branch
   and merge base equal the current ones, regardless of the proposal's
   session; it records the hook payload's `session_id` and `prompt_ref`.
   finalize-review and publish ignore any record whose branch or merge base
   differs from the current branch and base, so a reused change-id inherits
   nothing.
7. **Stations query, gates recompute** — agent-decided. `selection show
   <change-id>` prints the effective JSON step set (full set when nothing is
   bound). write-plan, build, review and ship read it at entry and omit only
   listed prose steps (intent, spec, plan, implementer, tdd, blind-run).
   `reviewers`, `adversarial` and `package-tests` are waived only inside
   finalize-review and publish, which re-read the records themselves.
8. **Failures are recorded where they are observed** — agent-decided.
   finalize-review appends a `failure` event on every non-zero exit. The
   review station passes each non-passing reviewer verdict to `selection
   record-failure <change-id> --step reviewers --input <verdict>` before
   any fix round. `attestation.selection.prior_failures` lists failures
   dated before each confirmation. A reviewer failure the station never
   passes to the checker cannot be detected; that limit is stated in the
   skill and the pull request's Verification section.
9. **Attestation `loom-attestation/v2`** — agent-decided. The key set adds
   `selection: {confirmations, skip, source, prior_failures} | null`.
   Finalization and `validate_attestation` waive exactly the checks of
   steps in `selection.skip` — empty `verdicts` and zero reviewer floor for
   `reviewers`, no adversarial run for `adversarial`, no package run for
   `package-tests` — and nothing else; `executions` may then be empty.
   v1 attestations stay valid for changes with no selection.
10. **Disclosure placement** — agent-decided. Ship's nine headings stay
    exact. Under `## Verification` the first line reads `Skipped steps:
    <steps> — authority: <source> (<code>, <date>)`, followed by one
    `Prior failure: <step> <rule> <date>` line per recorded failure;
    `validate_contextual_pr_body` compares them with the attestation. No
    line is required when `selection` is null.
11. **Skipping the intent** — agent-decided. The change-id is given at
    `propose`. Automatic publication authority lives only in a confirmed
    intent, so a change without one publishes through the existing
    `--confirm-authorized` path: one publication decision at ship.
12. **Agent-recorded authority is reserved** — agent-decided. The
    attestation and disclosure grammar keep `agent-recorded` as a source
    value, satisfying the intent's fallback constraint, but no command
    writes it while both supported hosts provide prompt capture.
13. **Skill** — agent-decided. `loom-code/skills/expert-mode/SKILL.md` with
    `disable-model-invocation: true`, plus `agents/openai.yaml` with
    `policy.allow_implicit_invocation: false`. It maps the user's words onto
    the vocabulary, runs `propose`, shows the table and the confirm line,
    waits for a user-origin proposal, and after a confirm prompt runs
    `selection show`; when no confirmation was recorded it tells the user
    the confirmation was not captured, names Codex hook trust as the usual
    cause there, and keeps the full process. The capture hook matches
    `/loom-code:expert-mode`, bare `/expert-mode`, and the Codex mention
    token for a plugin skill, which the plan measures before building.
14. **Ledger** — agent-decided. `selection skipped-review` reads
    `docs/loom/*/attestation.json` in the remote default branch tree and
    prints `<change-id> <merge commit> skipped: <steps>` per match.
15. **Lane residue** — agent-decided. Remove manifest `intent.lane` and
    kickoff `default-lane`, the template lines, `LANE_GRAMMAR`,
    `check_lane_schema`, `check_lane_reason`, the rule text's "or lane
    line", the `lane:` clause in the `deciding_commit` docstring
    (`rule_checks/intent.py:131`), the `lane:` sentence in
    `review/references/lenses.md`'s user-judgment-leak row, the
    `artifact:intent.lane` row in `docs/loom/evidence/mechanisms.yaml`, and
    this repo's KICKOFF line. `second_vendor_policy.py`'s small/full lanes
    are a live, different concept and stay.
16. **PRINCIPLES.md non-negotiable 2** — user-decided at ①: amended so
    user-skipped steps fall outside its guarantee and must be disclosed;
    kouko re-ratifies.
17. **Versioning and mechanisms** — agent-decided. Contract minor bump when
    an undeclared `lane:` line is tolerated by `intent.schema`, major
    otherwise (the plan measures it). The skill, both hooks, the guard, the
    selection rules and the attestation field each get a
    `docs/loom/evidence/mechanisms.yaml` row with its eval and a
    budget-exception line in `loom-code/CHANGELOG.md`.

## Alternatives considered
- Declared `lane:` frontmatter (loom-code 1.6.0) — the agent can write it; loom-code 3.1.0 already removed it.
- Push hook reads `transcript_path` for the user's words — the transcript format is not a documented interface.
- Persistent expert-mode switch or named presets — rejected by the user.
- Plain "yes" as confirmation — an agent-suggested table would bind on a casual reply.
- Trusting the agent's table text with a code alone — the agent writes that text; only a hook message shows what actually bound.
- Records committed in the change folder — agent-authored, inside the functional digest, trivially rewritten.
- A committed review-round ledger for reviewer failures — Review forbids a round ledger; untracked failure events carry the same fact.
- Hook parses natural language — brittle across Chinese, Japanese and English phrasing.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker/command_handlers/finalize.py:67` — finalization refuses without an adversarial artifact and below the reviewer floor, and writes nothing on failure.
- Reverse: `loom-code/hooks/hooks.json` PreToolUse matcher `Bash` → `loom_checker.py push --hook` (`command_handlers/push.py:47`); `loom-code/skills/ship/SKILL.md` §3 `publish`.
- Error: `loom-code/scripts/loom_checker/attestation.py:79` "attestation records no adversarial execution"; `:42` empty executions refused.
- Data: `loom-code/contract/manifest.yaml:178` attestation fields, `:111` intent `lane`, `:253` kickoff `default-lane`; `docs/loom/evidence/mechanisms.yaml:232` `artifact:intent.lane`.
- Boundary: `loom-code/scripts/loom_checker/rule_checks/publish.py:7` nine PR headings; `loom-code/scripts/second_vendor_policy.py:11` `LANES` (kept).

## UI flows
**Entry point (Claude Code `/loom-code:expert-mode` or `/expert-mode`; Codex skill mention)**
- Empty: types `/loom-code:expert-mode` with nothing after it → the agent lists the step names with one example sentence; nothing is recorded.
- Success: types `/loom-code:expert-mode 這次只跑測試，直接開 PR` → the agent shows a run/skip table and `要生效請輸入 /loom-code:expert-mode 確認 K7Q2`, then waits.
- Success: says `這次不用 review` in ordinary conversation → the same table and confirmation line appear, and the agent waits.
- Success: types the entry point with the code and any words, such as `/loom-code:expert-mode 確認 K7Q2` or `/expert-mode OK K7Q2` → a Loom hook message shows `已綁定 <change-id>：執行 …；跳過 …`, and the agent continues with the steps marked to run.
- Error: the hook message's lists differ from the table the agent showed → says so in any words (for example `不對，剛剛那個不算`) → the agent withdraws the selection, says the full process resumed, and shows the table again.
- Error: replies `對` → the agent answers that only the typed confirmation applies and repeats the confirmation line; nothing is skipped.
- Error: types a stale or mistyped code → no hook message appears; the agent says the confirmation was not recorded and shows the current table and code again.
- Error: the confirmation was typed but not captured (for example, Codex has not trusted the plugin's hooks) → the agent says it was not recorded, names hook trust as the likely cause, and keeps the full process.
- Error: names something that is not a step, or skips a step another selected step needs → the table marks the item and the agent asks the user to rephrase; no confirmation line is shown.
- In progress: none — proposing and binding are instant.

**Agent suggestion**
- Success: the agent judges a step unnecessary → it posts one suggestion with the table and confirmation line and keeps working on the full process.
- Success: the user later types the confirmation → a hook message shows what bound, and the steps after that point follow it.

**Mid-change**
- Success: types a new selection partway through → a new table and code appear; after confirmation the remaining steps follow it, and the pull request lists both selections and any failure recorded before them.

**Pull request**
- Success: a change with a bound selection → `## Verification` starts with `Skipped steps: reviewers, adversarial — authority: user-typed (K7Q2, 2026-09-14)` and any `Prior failure:` lines.
- Success: a change with no selection → no skipped-steps line; the full process ran.
- Success: the intent was skipped → ship asks one publication decision before pushing.
- Error: the disclosure disagrees with the attestation → publication is refused with the mismatch named; the agent rewrites the lines.

**Skipped-review ledger**
- Success: runs the query → one line per merged change that skipped review.
- Empty: no merged change skipped review → prints `no merged change skipped review`.

**Paths.** Abandoning a table leaves the full process in force. A cancel
returns to the full process. A new change, or a new branch reusing a
change-id, starts with no selection. An error line returns to the current
table; nothing already bound is lost.
