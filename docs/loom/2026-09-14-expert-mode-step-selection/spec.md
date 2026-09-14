# Let the user choose which Loom steps a single change runs — spec
intent: 2026-09-14-expert-mode-step-selection@6a8cdbfe
pre-build-review: required — changes who may waive verification at the publication gate (a security boundary) and extends the public attestation and contract format

## Requirements
REQ-1 — Proposal and typed confirmation
  WHEN the user describes in natural language which steps to run or skip, through the expert-mode entry point or in ordinary conversation, the agent shall show a run/skip table carrying a confirmation code, and WHEN the user then types the entry point's confirmation with that code, Loom shall apply that table to the change's remaining steps → Acceptance #1
REQ-2 — Full process until a typed confirmation is bound
  WHILE no user-typed confirmation is bound to the change, the checker shall report the full step set and shall refuse every skip at finalization and publication, including after a plain reply such as "yes" → Acceptance #2
REQ-3 — Fixed floor
  The checker shall require, for every change regardless of selection, publication through the canonical publish command and a generated attestation whose content digest matches the pushed content; IF package tests are not skipped THEN finalization shall execute them and require them to pass → Acceptance #3
REQ-4 — Non-blocking agent suggestion
  IF the agent proposes a skip that the user did not ask for THEN the checker shall accept at most one agent-origin proposal per change, the agent shall continue the full process without waiting, and no step shall be skipped without a later user-typed confirmation → Acceptance #4
REQ-5 — Disclosure of skipped steps and authority
  WHERE a change's attestation carries a selection, the publish command shall refuse a pull-request body whose skipped-steps disclosure does not name every skipped step and its authority, `user-typed` or `agent-recorded`, exactly as the attestation records them → Acceptance #5
REQ-6 — One selection, one change
  The checker shall bind every selection to exactly one change-id and shall apply no selection to any other change-id → Acceptance #6
REQ-7 — Mid-change selection
  WHEN a further selection is confirmed partway through a change, the checker shall apply it only to steps that have not yet produced evidence, and the pull request shall still disclose every earlier selection and every failure recorded before it → Acceptance #7
REQ-8 — Skipped-review ledger
  WHEN the user runs the skipped-review query, the checker shall list each merged change on the default branch whose attestation records reviewers as skipped, or print that none did → Acceptance #8
REQ-9 — Both supported hosts
  The expert-mode entry point, the confirmation capture and the checker behaviour shall produce the same selection outcome on Claude Code (`/loom-code:expert-mode`) and Codex CLI (`$expert-mode`) → Acceptance #9
REQ-10 — Unused lane settings removed
  The contract manifest, the intent and KICKOFF templates, the intent checker and this repository's `KICKOFF-DEFAULTS.md` shall carry no `lane:` field, `default-lane` key or express/gate-only grammar, and the repository's package tests shall pass → Acceptance #10

## Design decision
**Shape.** One skill surface, one capture hook per host, one checker command
group, and a selection field in the attestation. The skill talks; the hook
records what the user typed; the checker decides.

```
user types / speaks ─► agent: selection propose ─► table + code shown
user types confirm  ─► UserPromptSubmit hook ─► confirmation event (user-typed)
stations            ─► selection show ─► effective run/skip steps
review              ─► finalize-review reads bound selection ─► attestation.selection
ship                ─► publish validates attestation + disclosure ─► PR
```

1. **Step vocabulary is checker-owned** — agent-decided. The manifest gains
   `step_selection.steps`: `intent`, `spec`, `plan`, `implementer`, `tdd`,
   `reviewers`, `adversarial`, `blind-run`, `package-tests`, each with
   `requires:` dependencies (`spec`, `plan` and `blind-run` require `intent`).
   Publication, the merge decision and the attestation are not in the
   vocabulary, so no instruction can name them. `propose` refuses unknown
   names and unmet dependencies. Reason: one source for names the skill,
   stations and checker all use.
2. **Records live outside the tracked tree** — agent-decided. Append-only
   JSON lines at `<git common dir>/loom/selections/<change-id>.jsonl`:
   `proposal {id, code, origin, run, skip, session_id, created_at}` and
   `confirmation {proposal_id, code, source, session_id, prompt_id,
   prompt_sha256, at}`. The common dir is shared by worktrees; untracked
   records never enter the functional digest. Threat model: an agent that
   skips on its own under pressure. Deliberate forgery inside `.git` is the
   same class as editing the checker and stays at the independent-CI trust
   boundary the attestation design already chose.
3. **Capture hook** — agent-decided. `UserPromptSubmit` entries in
   `loom-code/hooks/hooks.json` and `hooks-codex.json` run
   `loom_checker.py selection capture --hook`. It acts only on a prompt whose
   first token is `/loom-code:expert-mode` or `$expert-mode` followed by
   `confirm <code>` or `確認 <code>`; it appends a `user-typed` confirmation
   for the pending proposal with that code in the same session, prints one
   context line for the agent, and always exits 0 so it never blocks a
   prompt. Claude Code does not fire `UserPromptSubmit` for a model-invoked
   skill, so model invocation cannot leave a user-typed record.
4. **Confirmation code** — agent-decided. Four characters derived from the
   proposal's content hash, shown in the table. It stops the agent from
   showing one table and recording another; a stale or mistyped code binds
   nothing.
5. **Proposal origin** — agent-decided. `selection propose <change-id>
   --origin user|agent`. A second `--origin agent` proposal for the same
   change is refused (REQ-4). Origin is not a trust input: a mislabelled
   origin changes only whether the agent waits, never whether a skip binds.
6. **Stations query, gates recompute** — agent-decided. `selection show
   <change-id>` prints the effective JSON step set (full set when nothing is
   bound). write-plan, build, review and ship read it at entry and omit only
   listed prose steps (intent, spec, plan, implementer, tdd, blind-run).
   Checker-enforced steps (`reviewers`, `adversarial`, `package-tests`) are
   waived only inside `finalize-review` and `publish`, which re-read the
   records themselves.
7. **Attestation `loom-attestation/v2`** — agent-decided. Adds `selection:
   {proposal_ids, skip, source, confirmed_at, prompt_sha256} | null`.
   Finalization accepts empty `verdicts`, no adversarial entries or no
   package run only for steps in `skip`; `push.attestation` validates the
   field against the local records. v1 attestations stay valid for changes
   with no selection.
8. **Mid-change** — agent-decided. Each confirmation carries its time;
   finalization runs once, so checker-enforced steps have no earlier
   evidence to override. Committed evidence (blind-run report, probes)
   stays functional content; the disclosure lists every confirmed selection
   in order and the Verification section names earlier failure evidence.
9. **Disclosure placement** — agent-decided. Ship's nine headings stay
   exact. Under `## Verification` the first line reads `Skipped steps:
   <steps> — authority: <user-typed|agent-recorded> (<code>, <date>)`;
   `validate_contextual_pr_body` compares it with the attestation. No line
   is required when `selection` is null.
10. **Skipping the intent** — agent-decided. The change-id is given at
    `propose`. Automatic publication authority lives only in a confirmed
    intent, so a change without one publishes through the existing
    `--confirm-authorized` path: one publication decision at ship.
11. **Agent-recorded fallback** — agent-decided. `selection confirm
    <change-id> --code <code> --agent-recorded` is refused whenever the
    installed plugin's hook manifest for the running host declares the
    capture hook; both shipped manifests do, so on supported installs the
    fallback is dormant and exists for a host without prompt capture.
    Its disclosure authority is `agent-recorded`.
12. **Skill** — agent-decided. `loom-code/skills/expert-mode/SKILL.md` with
    `disable-model-invocation: true`, plus `agents/openai.yaml` with
    `policy.allow_implicit_invocation: false` for Codex. It maps the user's
    words onto the vocabulary, runs `propose`, shows the table, waits for a
    user-origin proposal, reports the binding, and never evaluates a gate.
    Suggestion rule for other stations: at most one agent-origin proposal,
    shown without waiting.
13. **Ledger** — agent-decided. `selection skipped-review` reads
    `docs/loom/*/attestation.json` in the remote default branch tree and
    prints `<change-id> <merge commit> skipped: <steps>` per match.
14. **Lane residue** — agent-decided. Remove manifest `intent.lane` and
    kickoff `default-lane`, the template lines, `LANE_GRAMMAR`,
    `check_lane_schema`, `check_lane_reason` and the rule text's "or lane
    line", and this repo's KICKOFF line. `second_vendor_policy.py`'s
    small/full lanes are a live, different concept and stay.
15. **PRINCIPLES.md non-negotiable 2** — user-decided at ①: amended so
    user-skipped steps fall outside its guarantee and must be disclosed;
    kouko re-ratifies.
16. **Versioning and budget** — agent-decided. Contract minor bump when an
    undeclared `lane:` line is tolerated by `intent.schema`, major otherwise
    (write-plan measures it). New mechanisms: one skill, two hooks, the
    selection checker rule(s) and any prose gates, each with an eval and a
    budget-exception line in `loom-code/CHANGELOG.md`.

## Alternatives considered
- Declared `lane:` frontmatter (loom-code 1.6.0) — the agent can write it; loom-code 3.1.0 already removed it.
- Push hook reads `transcript_path` for the user's words — the transcript format is not a documented interface; a format change would lock or open the gate.
- Persistent expert-mode switch or named presets — rejected by the user in favour of per-change instruction.
- Plain "yes" as confirmation — an agent-suggested table would bind on a casual reply.
- Bind the latest proposal without a code — the agent could swap the recorded table after showing another.
- Records committed in the change folder — agent-authored, would enter the functional digest, and are trivially rewritten in a commit.
- Hook parses natural language — brittle across Chinese, Japanese and English phrasing.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker/command_handlers/finalize.py:67` — finalization refuses without an adversarial artifact and below the reviewer floor before writing the attestation.
- Reverse: `loom-code/hooks/hooks.json` PreToolUse → `loom_checker.py push --hook` (`command_handlers/push.py:47`); `loom-code/skills/ship/SKILL.md` §3 `publish`.
- Error: `loom-code/scripts/loom_checker/attestation.py:79` "attestation records no adversarial execution"; `:87` reviewer count.
- Data: `loom-code/contract/manifest.yaml:178` attestation fields, `:111` intent `lane`, `:253` kickoff `default-lane`; `rule_checks/intent.py:333` `LANE_GRAMMAR`.
- Boundary: `loom-code/scripts/loom_checker/rule_checks/publish.py:7` nine PR headings; `loom-code/scripts/second_vendor_policy.py:11` `LANES` (kept).

## UI flows
**Entry point (Claude Code `/loom-code:expert-mode`, Codex `$expert-mode`)**
- Empty: types `/loom-code:expert-mode` with nothing after it → the agent lists the step names with one example sentence; no table, nothing recorded.
- Success: types `/loom-code:expert-mode 這次只跑測試，直接開 PR` → the agent shows a run/skip table and the line `要生效請輸入 /loom-code:expert-mode 確認 K7Q2`, then waits.
- Success: says `這次不用 review` in ordinary conversation → the same table and confirmation line appear, and the agent waits.
- Success: types `/loom-code:expert-mode 確認 K7Q2` → the agent says `已生效：跳過 reviewers、adversarial（依據：你輸入的確認）` and continues with the steps marked to run.
- Error: replies `對` → the agent answers that only the typed confirmation applies, repeats the confirmation line, and keeps waiting; nothing is skipped.
- Error: types a stale or mistyped code → the agent says no table matches that code, shows the current table and code again; nothing is skipped.
- Error: names something that is not a step, or skips a step another selected step needs → the table marks the item it cannot use and the agent asks the user to rephrase; no confirmation line is shown.
- In progress: none — proposing and binding are instant.

**Agent suggestion**
- Success: the agent judges a step unnecessary → it posts one suggestion with the table and confirmation line and keeps working on the full process.
- Success: the agent would suggest again in the same change → nothing is shown.
- Success: the user later types the confirmation → the steps after that point follow the table.

**Mid-change**
- Success: types a new selection partway through → a new table and code appear; after confirmation the remaining steps follow it, and the pull request lists both selections.

**Pull request**
- Success: a change with a bound selection → `## Verification` starts with `Skipped steps: reviewers, adversarial — authority: user-typed (K7Q2, 2026-09-14)`.
- Success: a change with no selection → no skipped-steps line; the full process ran.
- Success: the intent was skipped → ship asks one publication decision before pushing.
- Error: the disclosure line disagrees with the attestation → publication is refused with the mismatch named; the agent rewrites the line.

**Skipped-review ledger**
- Success: runs the query → one line per merged change that skipped review.
- Empty: no merged change skipped review → prints `no merged change skipped review`.

**Fallback host without prompt capture**
- Success: the user confirms → the agent records it and the pull request shows `authority: agent-recorded`.

**Paths.** Abandoning a table (never confirming) leaves the full process in
force. A new change starts with no selection. An error line returns to the
current table; nothing already bound is lost.
