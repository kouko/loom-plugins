# Close the follow-ups left by the plain-language reminder change
originator: kouko
kind: engineering
needs-design: no — test guards, runtime prose wording, repository docs, memory entries and a plugin version bump; no surface a user reads or types into changes
evidence: ["docs/loom/2026-09-16-plain-language-replies/blind-run-report.md", "docs/loom/2026-09-16-plain-language-replies/attestation.json"]
status: confirmed 2026-09-16
publication: automatic — authorized 2026-09-16 by kouko

## Problem
The plain-language reminder change (merged 2026-09-16, PR #22) shipped with
four recorded follow-ups, and checking the installed plugins afterwards
surfaced a fifth:

- Two card assertions in `loom-workflow/scripts/test_visualization_card_hook.py`
  were loosened from exact wording to meaning and lost their negation guard, so
  a card sentence flipped to its opposite ("Never verify prescribed box
  diagrams with `scripts/align.py`") still passes every check. The adversary
  proved the same class of hole on the guide tests before it was closed there.
- Moving the decision rule inline into the card removed the only route from a
  decision reply to `references/plain-language.md`. The blind run recorded the
  guide opened in 0 of 6 trials, so its missed-alternatives check — do nothing
  or later, a smaller version, combining two — never reaches replies, while
  spec REQ-7 of that change still requires it.
- The card headers dropped the word "trigger" while
  `loom-workflow/README.md`, `README.ja.md`, `README.zh-TW.md`,
  `CHANGELOG.md`, `.codex-plugin/plugin.json` and the hook docstring still
  call it a trigger card, so the same object has two names in shipped text.
- Two durable lessons from that branch reached no store: a phrase-presence
  test accepts a rule flipped to its opposite, and routing prose to a guide
  fired in 1 of 3 trials where an inline rule fired in 5 of 5. The closing
  review's digest budget was spent, so `docs/loom/memory/` never received
  them, and they now live only in a merged PR body.
- `loom-code` ships from this repository by path, and the installer decides
  whether to refetch by comparing the declared version. Main's `loom-code`
  content moved on across 28 paths without a version bump, so
  `claude plugin update loom-code@loom` answers "already at the latest version
  (3.7.0)" and refreshes nothing. Every Loom run on kouko's machine therefore
  uses station and agent contracts from commit 8a27d668, and this session had
  to pass a field the trunk already removed to get the second-vendor policy to
  run at all.

## Proposed outcome
The follow-ups the previous change deliberately left open are closed: a card
rule flipped to its opposite fails its test, the shipped text calls the card
one name, the two lessons live in the repository's memory store where later
changes can find them, and a released `loom-code` fix reaches an installed
copy instead of stopping at an unchanged version number.

## Acceptance
1. A card sentence whose meaning is negated fails the card tests, and an executable adversarial case covering the coexist card records that failure.
2. No shipped text of the plugin calls the per-turn card a "trigger card" while its own header does not; the three README languages, the changelog, the Codex description and the hook docstring agree on one name.
3. The repository's memory store holds the two lessons from the previous change — that a phrase-presence test accepts a rule flipped to its opposite, and that an inline rule fired where routing prose did not — each with the evidence it came from.
4. `loom-code` declares one new version above 3.7.0 across every place it states its version, and the repository's own consistency checks accept it.
5. The repository's package tests and mechanism checks pass, and the number of registered mechanisms does not grow.
6. When the agent asks or answers how to do something, the reminder it receives every turn states that doing nothing or later, a smaller version, and combining two options are each offered or ruled out, and both reminder variants still fit the word limit they already have.
7. The reminder names the everyday conversation situations that carry a table — a progress report, a before and after, what each choice means, a readiness checklist, what is confirmed and what is not, findings, risks, and which environments are supported — so an agent reaches them without opening a separate file.
8. Shaped content in a reply is a markdown table by default, and the drawn form is reserved for a destination that cannot render markdown, such as a code comment; no rule still tells the agent to prefer the drawn form because of the client it is running in.

## Constraints
- user-decided (kouko, 2026-09-16): the reminder ships only from `loom-workflow`; `loom-code` and `loom-design` carry no copy of it.
- user-decided (kouko, 2026-09-16): the missed-alternatives check is stated in the reminder itself rather than recorded as guide-only, because the guide was opened in none of the six recorded trials while the inline rule reached every one of them.
- The 150-word cap on each card stays as it is; wording that needs room is trimmed from non-rule text rather than raising the cap.
- Committed artifacts stay in English.
- Repository skill conventions hold: flat skill folders, the SKILL.md size cap, and no runtime citation of this repository's development records.
- Whether an installed copy actually refreshes can only be observed after this change merges, by updating the plugin on kouko's machine; the blind run can prove the declared version and the checks, not the post-merge install.

## Out of scope
- Verifying the previous change's Codex and Antigravity acceptance lines in live sessions of those hosts.
- The rewrite fact-drift behaviour kouko accepted at the previous change's acceptance.
- Updating the Obsidian vault's wiki layer.
- Any further change to how the reminder is delivered, beyond the wording the open question below settles.

## Open questions
- none
