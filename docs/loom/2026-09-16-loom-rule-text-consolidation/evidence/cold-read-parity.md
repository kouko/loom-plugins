# Cold-read parity: main vs the consolidated branch

Evidence for intent Acceptance 5 (same steps, same decision-point questions,
same checker commands) and Acceptance 6 (mechanism, citation and cross-reference
checks). Task W3-02.

## Method

- **Trees.** Two static extracts with identical layout, so that readers could
  not reach an installed plugin or the live checkout:
  - main: `git archive dec4e927 | tar -x -C <scratchpad>/parity-main`
  - branch: `git archive HEAD | tar -x -C <scratchpad>/parity-branch`, HEAD =
    `c20255e7f220204b97c16579feff1ba639c894b7` on
    `docs/2026-09-16-loom-rule-text-consolidation`
- **Readers.** For each of 7 scenarios, two fresh-context agents (Agent tool,
  `general-purpose`, model `sonnet`, no `name:`), one per tree, launched
  concurrently with the same prompt apart from the tree root.
- **Prompt template (verbatim).**

  > You are an agent about to execute the Loom station `<station>` for the
  > scenario below. Read `<tree>/<station SKILL.md path>` and any file it tells
  > you to read, resolving relative links and `<loom-code>` /
  > `${CLAUDE_PLUGIN_ROOT}` inside `<tree>/loom-code` (loom-design skills at
  > `<tree>/loom-design`). Read only inside `<tree>`; never read ~/.claude or
  > any installed plugin; do not run commands or write files. Return: (1)
  > ordered numbered steps you would take; (2) every question you would put to
  > the user, with its decision point; (3) every checker/script command you
  > would run; (4) artifacts you would write or commit; (5) agents you would
  > dispatch, with lens/role; (6) any instruction you found ambiguous or
  > contradictory.
  >
  > Scenario (repo under work = a plugin repo with both loom-code and
  > loom-design installed; KICKOFF-DEFAULTS has second-vendor: suggest,
  > package-tests set): `<scenario>`

  Scenario 4 replaced the installed-plugins clause with "loom-code installed
  but loom-design NOT installed".
- **Classes.** (a) same behaviour, different wording; (b) behaviour difference
  explained by an intended consolidation fix in the intent or plan; (c)
  unexplained behaviour difference; (d) reader noise, confirmed by re-running
  the diverging side once and checking the governing text is unchanged between
  the trees.
- **Comparison unit.** One row per field. A field whose two answers list the
  same actions is (a) even when the order of two independent read-only checks
  or the level of detail differs. Field (6) is compared for whether either side
  reports a contradiction the other tree resolves.

## Scenario 1 — capture-intent

"When ship publishes a PR, I want it to print the PR URL at the end so I can
open it." No intent exists. Branch side re-run once.

| Field | main | branch | Class |
|---|---|---|---|
| (1) steps | Step 0 contract check; interview (engineering bank, grounded on ship already reporting the URL); draft intent `kind: engineering`, `needs-design: no`; standing check; decision point ① one message; altitude pass; on yes confirm, commit, `intent` check; hand off to write-plan | Run 1: same steps, locate via `references/locate-loom-code.md`, no altitude-pass step and no publication sentence named. Re-run: same as main including the publication consequence; still does not name the altitude pass | d — the altitude-pass text is unchanged (main `capture-intent/SKILL.md:295,312` = branch `:287,304`; the diff touches only :38-40 and Step 0) |
| (2) questions | Interview `what` questions (what fails today, workaround, outcome, must-not-change, out of scope); ① restatement with automatic-publication consequence; one-way-door scan finds none; no second-vendor question (`suggest`) | Run 1: same interview questions, restatement without publication wording. Re-run: restatement plus publication consequence with opt-out; no second-vendor question | d — publication wording unchanged (main :219, branch :211); re-run matches main |
| (3) checker commands | `contract --require 2.1`, `standing <intent>`, `intent <intent>` | same three | a |
| (4) artifacts | `docs/loom/intent/<id>.md`; commit `docs(loom): intent <id> confirmed` with `needs-design:` in body; `publication: automatic — authorized …` after an informed yes | Run 1: same file and commit, publication field not mentioned. Re-run: same as main | d |
| (5) agents | none | none | a |
| (6) ambiguities | kind product vs engineering for dev-tool output; Claude Code locate row vs co-located tree; which "end" | kind product vs engineering; zero one-way-door wording; change-id naming | a — neither side reports a contradiction the other tree resolves |

## Scenario 2 — write-spec

Confirmed product intent `2026-09-20-checker-status-command`, needs-design:
yes, public CLI contract risk.

| Field | main | branch | Class |
|---|---|---|---|
| (1) steps | contract check; `intake write-spec`; read PRINCIPLES/DESIGN; spec from `spec-minimal.md` with `pre-build-review: required`; completeness pass; decision point ②; `confirmed-behavior` from `git hash-object`; commit spec; **hand to `loom-code:closing-review` with scope `spec`**; `intake write-plan`; hand off to write-plan | same, except the required review step: **dispatch `loom-code:reviewer` directly** with `reviewed_sha` = commit before the spec, intent and spec as ground truth; no blind run, adversary or `finalize-review` | b — C6 (W1-03): a pre-build spec review dispatches the reviewer directly because closing-review has no spec mode |
| (2) questions | ② behaviour read-back plus Requirements in plain words; conditional one-way-door (output format) folded into the same message | ② behaviour read-back plus Requirements; conditional one-way door in the same message, likely empty | a |
| (3) checker commands | `contract --require 2.1`, `intake write-spec <id>`, `git hash-object <spec>`, `intake write-plan <id>` | same four | a |
| (4) artifacts | `docs/loom/<id>/spec.md`, commit `docs(loom): spec <id>` | same; plus fix commits on NEEDS_REVISION | a |
| (5) agents | one fresh-context `loom-code:reviewer`, lens `spec+adversarial`, reached through closing-review scope `spec` | one fresh-context `loom-code:reviewer`, lens `spec+adversarial`, dispatched by the spec author | b — C6 (W1-03); same reviewer and lens, different dispatcher |
| (6) ambiguities | intent file absent from the tree; kind not in scenario; locate host row | locate host row; DESIGN.md for a CLI; `reviewed_sha` "the commit before the spec" could mean parent of the spec commit or pre-Step-2 tip; template comment | b — the `reviewed_sha` question reads the new C6 sentence (`write-spec/SKILL.md` diff hunk @@ -320 +305); main has no `reviewed_sha` because it routed through closing-review |

## Scenario 3 — write-plan (A)

Confirmed engineering intent, needs-design: no, publication authorized, HEAD on
main.

| Field | main | branch | Class |
|---|---|---|---|
| (1) steps | contract check; `selection show`; find intent; `standing`; skip ① (confirmed); needs-design no → Current State Evidence; `intake write-plan`; write plan; `plan` + `intake write-plan` again; second-vendor `suggest` notice; branch off main; commit plan; hand off to build | same actions; `selection show` listed before the contract check; ① skipped without loading `references/confirm-intent.md` | a — same actions; order of two read-only entry checks differs, text unchanged |
| (2) questions | none | none | a |
| (3) checker commands | `contract --require 2.1`, `selection show`, `standing`, `intake write-plan` ×2, `plan`, `second_vendor_policy.py` | same, plus `git branch --show-current`, `git switch -c` listed | a — main names the same git steps in (1) |
| (4) artifacts | new branch `<type>/<id>`; `docs/loom/<id>/plan.md` commit `docs(loom): plan <id>` | same; notes the conditional second-vendor Risks edit | a |
| (5) agents | none (conditional spec review not triggered) | none | a |
| (6) ambiguities | where "Questions asked" comes from when ① ran upstream; host inference; `docs-lint` absence | where "Questions asked" comes from when ① ran upstream; standing check "before ①" scoping; branch type | a — the same gap on both sides |

## Scenario 4 — write-plan (B), loom-design not installed

Small engineering change described by the user; no intent file.

| Field | main | branch | Class |
|---|---|---|---|
| (1) steps | contract check; `selection show`; interview and write intent; `standing`; ① one message (restatement, one-way doors, carried details); on yes confirm + commit + `intent`; needs-design; `intake write-plan`; plan; `plan` + intake; second-vendor notice; branch; commit; hand off. If a spec with `pre-build-review: required` were written: **hand it to closing-review** | same, with ① read from `references/confirm-intent.md` and `one-way-door.md`. If a required spec review arose: **dispatch `loom-code:reviewer` directly** | b — C6 (W1-03) on the conditional path; W2-06 moves ① into `confirm-intent.md` with the same content |
| (2) questions | pre-① interview; ① restatement + publication; one-way-door consequence if any; carried-details table; conditional ② only for a product spec | pre-① interview; ① restatement + one-way doors + carried details in one message; no second-vendor question; conditional ② | a |
| (3) checker commands | `contract`, `selection show`, `standing`, `intent`, `intake write-plan` ×2, `plan`, `charter` (optional), `second_vendor_policy.py`, git branch commands | same list, plus the `command -v codex/gemini` probes written out | a |
| (4) artifacts | intent file + `intent … confirmed` commit; `plan.md` + commit; branch; conditional spec | same | a |
| (5) agents | none; conditional: closing-review runs one `spec+adversarial` reviewer | none; conditional: one `loom-code:reviewer` `spec+adversarial` with `reviewed_sha` | b — C6 (W1-03) |
| (6) ambiguities | `selection show` before a change id exists; template-path wording; second-vendor vs branch ordering; KICKOFF file existence | `package-tests` unused by write-plan; template-path wording; evidence for new code; host detection | a |

## Scenario 5 — build

Plan with 2 tasks in one wave; `selection show` skips nothing; one task adds a
reviewer lens row.

| Field | main | branch | Class |
|---|---|---|---|
| (1) steps | scope; `selection show`; per task: resolve dispatch profile, RED test, implementer, focused tests; integration checks; `sync-trunk`; adversary; package suite + adversarial programs; fix findings; hand off; call closing-review once | same order and actions; dispatch-profile resolution read from `dispatch-profile.md`; adversary works from `adversarial.md` | a |
| (2) questions | none (only stop-and-report on missing implementer dispatch or `sync-trunk` failure) | none (same two stop-and-report cases) | a |
| (3) checker commands | `selection show`, `dispatch_profile.py` per dispatch, `sync-trunk`, KICKOFF `package-tests` command, each adversarial program, focused tests | same | a |
| (4) artifacts | task commits (tests + code, "task trailer" per main `implementer.md:3`); lens-row + pin test; adversarial programs; no `attestation.json` | same, also says "task trailer" although branch `implementer.md:3` now reads "one commit for the task" | a — same actions; the branch reader's "trailer" is its own wording, and C10 (W1-02) only removed a dead reference |
| (5) agents | `loom-code:implementer` ×2; `loom-code:adversary` fresh-context; closing-review called once | same | a |
| (6) ambiguities | "genuinely independent file sets"; `second-vendor` irrelevance; redispatch trigger wording; doc-row TDD; call mechanism | independent file sets; dispatch-profile classification of a lens row; `second-vendor` irrelevance; hand-off report persistence | a |

## Scenario 6 — closing-review

Build handed off; one Acceptance line needs a person to read output; the change
touches review mechanism prose.

| Field | main | branch | Class |
|---|---|---|---|
| (1) steps | establish content; `selection show`; dispatch profile per spawn; `sync-trunk` before Round 1; confirm Build's suite and programs passed; blind run and commit its report; resolve second vendor from recorded selection; `reviewer-count`; dispatch reviewers; `record-failure` per non-pass; bounded rounds; durable lesson check; `finalize-review`; commit attestation; hand off to ship | same actions in the same order | a |
| (2) questions | none in the normal path; ③ belongs to ship | none in the normal path; requirement-changing fix routes to a new intent; ③ at ship | a |
| (3) checker commands | `selection show`, `sync-trunk`, `dispatch_profile.py`, `reviewer-count`, `selection record-failure`, `finalize-review --input`; `claude_reviewer.py` only from Codex | same | a |
| (4) artifacts | `blind-run-report.md` (committed first); temp JSON outside repo; `attestation.json`; optional memory entry | same | a |
| (5) agents | `loom-code:blind-runner`; `loom-code:reviewer` × floor (≥2), `skill` lens for the prose plus lens per remaining paths; no adversary | same | a |
| (6) ambiguities | "a selected second vendor remains required" vs `suggest`; missed opt-in window; lens split across mixed artifact types | "second vendor remains required" vs `suggest`; lens for `references/*.md`; reverse-direction vendor dispatch; citation check scope | a — the shared second-vendor question is present on both sides |

## Scenario 7 — ship

Attestation generated; intent carries `publication: automatic — authorized …`;
the user later answers "接受". Main side re-run once.

| Field | main | branch | Class |
|---|---|---|---|
| (1) steps | read intent + blind-run report; `selection show`; rebuild PR body with nine headings; optional Mermaid; git-memory + secrets scan; self-check; `publish --intent --title --body-file`; poll CI; repair path; present result at ③; git-memory merge checkpoint; `git rev-parse --show-toplevel`; `land --accepted-by`; `--cleanup` on BLOCK; follow `next:`; report | same actions and order | a |
| (2) questions | Run 1: ③ acceptance, plus a question asking the user which name to pass to `--accepted-by`. Re-run: ③ acceptance; name asked only if the accepter does not match originator or authorizer | ③ acceptance; name read from the intent, asked only on mismatch | d — `--accepted-by` text unchanged (main `ship/SKILL.md:191`, branch `:185`); re-run matches branch |
| (3) checker commands | `selection show`, `publish`, `git rev-parse --show-toplevel`, `land --accepted-by`, `land --cleanup` | same | a |
| (4) artifacts | PR body file, the PR, conditional repair commits, git-memory material; no loom files | same | a |
| (5) agents | none; `loom-workflow:git-memory` skill twice | none; git-memory twice | a |
| (6) ambiguities | who runs the CI repair; `--accepted-by` name source; KICKOFF relevance; (run 1 only) whether ship may still make the one skip suggestion | CI repair owner; `--accepted-by` name source; KICKOFF relevance; PR language | a — the run-1 skip-suggestion question read the paragraph that D3 (W2-03) moved to expert-mode; the main re-run did not raise it and neither side proposes a skip

## Summary

| Scenario | a | b | c | d |
|---|---|---|---|---|
| 1 capture-intent | 3 | 0 | 0 | 3 |
| 2 write-spec | 3 | 3 | 0 | 0 |
| 3 write-plan (A) | 6 | 0 | 0 | 0 |
| 4 write-plan (B) | 4 | 2 | 0 | 0 |
| 5 build | 6 | 0 | 0 | 0 |
| 6 closing-review | 6 | 0 | 0 | 0 |
| 7 ship | 5 | 0 | 0 | 1 |
| **Total (42 rows)** | **33** | **5** | **0** | **4** |

- Every (b) row traces to C6 (W1-03): a required pre-build spec review now
  dispatches `loom-code:reviewer` with lens `spec+adversarial` directly instead
  of handing the spec to closing-review. Reviewer count, lens and "no blind run,
  no adversary" are the same on both sides.
- No (c) difference was found. Checker commands and planned artifacts match in
  all seven scenarios.
- One (d) row did not fully clear on its re-run: in scenario 1 neither branch
  run named capture-intent's altitude pass as a step, while the main run did.
  The altitude-pass text is byte-identical between the trees (the only
  capture-intent hunks are the C15 stop sentence and Step 0's move to
  `references/locate-loom-code.md`), so the omission cannot come from the
  branch diff; it is recorded as reader noise with this caveat.
- Scenario 2's branch reader raised a new question the C6 wording creates:
  "the commit before the spec" as `reviewed_sha` does not say whether that is
  the spec commit's parent or the branch tip before drafting. The two coincide
  when the spec commit is made directly on the prior tip, which is what the
  station describes.

## A6 checks

Run on the branch working tree at HEAD `c20255e7`:

```
$ python3 loom-code/scripts/check_mechanisms.py
hook                   10          9
contract               63         63
prose-gate             17         17
net mechanism count (excl. host-hygiene): 136
exempt from net count: PostToolUse:Skill:language-anchor.py
all clear
exit=0

$ python3 loom-code/scripts/check_contract_citations.py
OK: 4 known-violating files unchanged, no new contract citations of this repo's records.
exit=0

$ python3 loom-code/scripts/check-skill-crossrefs.py
OK: all relative skill cross-references resolve.
exit=0
```

The registered prose-gate count stays at 17. The package suite is not run here;
it runs once at the end of Build.

## Limits

- Readers describe what they would do; no station was executed and no artifact
  was produced. "Artifacts pass the same checker commands" is evidenced by
  identical planned checker commands and identical planned artifacts, not by
  running those commands on real output.
- One reader per side per scenario (plus at most one rerun). Sonnet readers vary
  in detail between runs, so a single agreeing pair shows the text leads to the
  same steps, not that every run will.
- Scenario inputs were described, not present: no intent, plan or attestation
  for the scenario change exists in either tree, and some readers noted that.
- Readers were pointed at a co-located `loom-code` beside `loom-design`, which
  is the non-Claude-Code row of the locate table; two readers flagged that
  their host would use the plugin cache instead. Both trees were read the same
  way, so parity is unaffected.
- Only the seven station entry files and what they link were in scope; agent
  contracts were read only where a station sent the reader there.
