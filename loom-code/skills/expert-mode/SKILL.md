---
name: expert-mode
description: |
  Skip chosen Loom steps for one change. Only for the user typing /loom-code:expert-mode (Codex: $expert-mode); the agent never invokes it.
disable-model-invocation: true
---

# Expert mode

Talk to the user in the user's language. This skill proposes, shows and
reports; the checker decides what is skipped. The same procedure applies when
a station reaches it from ordinary conversation, such as "這次不用 review": the
agent reads this file, and the user still types the confirmation.

Checker prefix: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py` on
Claude Code, `python3 <injected loom-code plugin root>/scripts/loom_checker.py`
on Codex. Commands below write `loom_checker.py`. `<change-id>` is the active
change's id; when no intent exists yet, it is the dated kebab-case id the
change will use.

## 1. Map the words onto steps

Steps: `intent`, `spec`, `plan`, `implementer`, `tdd`, `reviewers`,
`adversarial`, `blind-run`, `package-tests`. Publication, the merge decision
and the attestation are not steps.

- Nothing after the entry point: list the steps with one example sentence and
  stop; nothing is recorded.
- Map the user's words, in any language, onto step names. Skipping the intent
  also skips spec, plan and blind-run.
- A word that is no step, or a skip another selected step needs: name the
  item, ask the user to rephrase, and show no confirmation line.

## 2. Propose, show, wait

Run `loom_checker.py selection propose <change-id> --origin user --skip <steps>`.
Show its run/skip table and one line in the user's language that tells the
user this: to apply it, type `/loom-code:expert-mode` (Codex: `$expert-mode`)
with the code shown, in any surrounding words. Then wait.

Only that typed confirmation applies. A reply such as "yes" or "對" binds
nothing: say so and repeat the confirmation line.

## 3. Report what bound

After a confirmation prompt, run `loom_checker.py selection show <change-id>`
and report its `run` and `skip` lists exactly. A Loom hook message shows the
same lists; when they differ from your table, say so and withdraw (§4).

If `bound` is false, tell the user the confirmation was not captured. Name
hook trust as the usual cause on Codex (its hooks run once the user trusts the
plugin), and a stale or mistyped code otherwise; show the current table and
code again and keep the full process.

Claim a skip is in effect only from `loom_checker.py selection show <change-id>`.

## 4. Withdraw and lapse

- On withdrawal wording in any language (`取消`, `cancel`, `キャンセル`,
  `不對，剛剛那個不算`), run `loom_checker.py selection cancel <change-id>`, say
  the full process resumed, and show the table again.
- After a rebase, or a merge of the default branch into the change, tell the
  user the bound selection lapsed and the full process resumed, then re-run
  `loom_checker.py selection propose` with the same steps and show the table
  and its code.

## Boundary

- Never evaluate a gate. `finalize-review` and `publish` re-read the records
  and waive only a bound skip.
- Local protection stops shortcuts, not deliberately disguised commands;
  independent CI stays the trust boundary.
- A reviewer rejection is recorded only when Review hands it to the checker
  (`selection record-failure`).
