# Quarterly Skill Audit Runbook

Operational runbook for quarterly review of loom-workflow's skill
ecosystem. Companion to `skill-governance.md`.

**Cadence**: every 3 months (Jan / Apr / Jul / Oct), or on demand
when significant change events occur (major skill release,
external dependency update, framework migration).

**Time budget**: ~1-2 hours per audit when ecosystem is stable;
more if findings require investigation.

**Output**: a brief audit report committed to
`loom-workflow/docs/audit-reports/YYYY-Qn-audit.md` recording what
was checked, what was found, and what action items resulted.

---

## When to run

### Scheduled

Quarterly:
- Q1: end of January
- Q2: end of April
- Q3: end of July
- Q4: end of October

### On demand

Whenever any of these happen:
- Major skill release (new skill, breaking change, version major bump)
- External dependency update (upstream skill named in a NOTICE modified, Anthropic
  Skills API contract change)
- User-reported regression that suggests systemic drift
- Validation gate from architecture doc §6 has been completed and
  needs reflection in governance docs
- Cross-plugin contract violation discovered

(Note 2026-11-22: the validation-gate trigger above is historical;
loom-workflow keeps no outstanding validation gates, and step 5 is
skipped. The external-dependency trigger used to read "upstream MIT
skill modified"; upstream licenses are those their NOTICE entries state.)

---

## Pre-audit checklist

- [ ] Last audit report read and any open action items reviewed
- [ ] Current git status clean (no in-flight branches that block
      file inspection)
- [ ] `gh` CLI authenticated; can read PRs
- [ ] Python 3 available for running `score_history.py` (step 6)

---

## The audit checklist

### 1. Skill membership and licensing

Goal: confirm the plugin's skill list and licensing match what is on
disk.

```bash
# Skills that ship in loom-workflow today
ls loom-workflow/skills
# Skills that carry their own LICENSE (all others follow the
# repository-level LICENSE)
ls loom-workflow/skills/*/LICENSE*
```

Action items:
- [ ] `ls loom-workflow/skills` matches the Skills table in
      `loom-workflow/README.md`
- [ ] Each skill without its own LICENSE is covered by the
      repository-level `LICENSE`; each skill listed by the second
      command (as of 2026-11-21, only `critique`) still has its LICENSE
      and NOTICE

(Note 2026-11-21: this step used to verify the SSOT Registry in
`skill-governance.md` by running `scripts/check-shared-conventions-drift.py`,
and to compare each skill's LICENSE with the owner named in the
governance doc's ownership table. That script has been removed, the
registry's conventions moved to the `skill-dev-toolkit` plugin, and the
ownership table is a historical snapshot, so those checks no longer
apply here.)

### 2. Skill lifecycle state review

Goal: confirm each skill's state matches its activity level.

For each Active skill, check:
- Last commit date (`git log --oneline -1 -- "loom-workflow/skills/<skill>/"`)
- Recent invocation patterns (informally; if telemetry available, use it)
- Open issues / known regressions

For each Deprecated skill:
- Has 3 months passed? If yes, eligible for Retired transition
- Has a replacement skill matured? If yes, expedite retirement
- Is anyone still using it? If usage signal present, postpone retirement

Action items:
- [ ] No Active skill has been untouched for >12 months without
      recent invocation evidence (suggests it should be Deprecated)
- [ ] All Deprecated >3 months reviewed for Retired transition
- [ ] Any state change (deprecation, merge, retirement) recorded in
      the new release's entry in `loom-workflow/CHANGELOG.md`, and the
      Skills table in `loom-workflow/README.md` updated to match

(Note 2026-11-22: the last item used to read "Lifecycle table in
governance doc updated if states changed". That table in
`skill-governance.md` is now a historical snapshot, kept as written.
Lifecycle decisions are recorded in `loom-workflow/CHANGELOG.md`, and
the README Skills table lists the skills that ship today.)

### 3. Convention drift inspection

Goal: catch drift between the mindsets bundled in
`loom-workflow/skills/critique/references/` and their canonical copies
in `domain-teams:code-team/standards/mindset-*.md` (see
`loom-workflow/skills/critique/NOTICE`).

- Read the canonical version of each mindset
- Verify critique's bundled copy still matches it
- If drift discovered: file an action item to either align the copy
  with the canonical version or record why it differs

Action items:
- [ ] Each bundled mindset in critique compared with its canonical
      copy in domain-teams:code-team

(Note 2026-11-21: this step used to spot-check the three shared
conventions (golden-anchor / test-prompts / constitution) and catch
"drift not caught by CI". Those conventions moved to the
`skill-dev-toolkit` plugin with skill-refactor and skill-tuning, and no
drift CI runs in this repository.)

### 4. External dependency audit

Goal: ensure upstream attribution chains are intact and each upstream
license still matches its NOTICE entry.

For each skill with NOTICE file:
- Verify upstream URL still resolves
- Verify upstream skill / project still exists at stated path
- Check each upstream license still matches the license its NOTICE entry
  states (licenses differ: loom-visualization's `NOTICE.md` lists MIT
  entries and CC BY 4.0 for the C4 model)
- Note any upstream updates that would warrant local sync

Skills with NOTICE files (as of v1.7.0):
- skill-creator-advance (Anthropic → AllanYiin → kouko)
- skill-judge (Leonardo Flores → kouko)
- complexity-critique (joshuadavidthomas → softaworks → kouko)
- skill-refactor (original; design influence from darwin-skill)
- skill-tuning (original; design influence from darwin-skill)

(Note 2026-11-21: the list above is as of v1.7.0. Today, check with
`ls loom-workflow/skills/*/NOTICE*`: critique (`NOTICE`; complexity mode
adapted from joshuadavidthomas → softaworks → kouko) and
loom-visualization (`NOTICE.md`; ascii-graph-toolkit).
skill-creator-advance, skill-judge, skill-refactor and skill-tuning moved
to the `skill-dev-toolkit` plugin; audit their NOTICE files there.)

Action items:
- [ ] All upstream URLs resolve
- [ ] Each upstream license confirmed to match its NOTICE entry
- [ ] Significant upstream updates noted for follow-up sync

(Note 2026-11-22: this step used to require every upstream license to be
"still MIT (or compatible)" and its action item read "All upstream licenses
confirmed still MIT". The criterion is now the license each NOTICE entry
states.)

### 5. Validation gate status

Goal: track outstanding validation gates from architecture doc §6.

```bash
# Search for OUTSTANDING markers in CHANGELOG
grep -A 2 "OUTSTANDING" loom-workflow/CHANGELOG.md
```

For each outstanding gate:
- Determine if validation has been performed since last audit
- If yes: update CHANGELOG / governance doc to reflect completion
- If no: assess whether outstanding for >2 quarters; if so, decide
  to either schedule validation or formally accept the risk

Currently outstanding (as of v1.7.0):
- skill-refactor: dry-run on ≥2 existing skills; ≥90% equivalence-
  check agreement with manual review
- skill-tuning: 1 real-skill walkthrough verifying A/B flow
  produces meaningful preference signal

(Note 2026-11-21: skill-refactor and skill-tuning moved to the
`skill-dev-toolkit` plugin; track their validation gates there, not in
this repository's CHANGELOG.)

(Note 2026-11-22: this step is historical; skip it. The search above
finds only the skill-refactor and skill-tuning gates, which belong to
`skill-dev-toolkit`. loom-workflow keeps no OUTSTANDING validation gates
today. The step's former action items were "All outstanding validation
gates inventoried" and "Each gate >2 quarters outstanding has explicit
accept-risk or schedule-validation decision".)

### 6. Skill-judge score history (if data available)

Goal: detect drift in skills that have been using
`scripts/score_history.py` for evaluation tracking. The tool ships with
the `skill-dev-toolkit` plugin (skill-judge moved there).

For each skill with a `.skill-judge-history.jsonl` file, run
`score_history.py` from the installed skill-dev-toolkit plugin's
`skills/skill-judge/scripts/` folder (not from this repository root;
skill-dev-toolkit is not part of this repository):

```bash
# Set both to real paths first. TOOLKIT is the installed plugin's folder,
# outside this repo (find it with:
#   find ~/.claude/plugins/cache -name score_history.py -path '*skill-dev-toolkit*')
TOOLKIT="/path/to/skill-dev-toolkit"
SKILL_DIR="/path/to/audited-skill"
python3 "$TOOLKIT/skills/skill-judge/scripts/score_history.py" \
    drift "$SKILL_DIR/.skill-judge-history.jsonl"
```

If drift flagged: investigate (refactor introduced subtle
regression? tuning moved skill in unintended direction?). Recommend
running skill-tuning to capture human preference signal before
deciding action.

Action items:
- [ ] Drift detection run on all skills with history
- [ ] Flagged drift findings noted for investigation

### 7. Documentation freshness

Goal: catch stale documentation.

- [ ] Plugin README version line matches plugin.json version
- [ ] Plugin README skills table matches actual skills directory
- [ ] CHANGELOG.md most recent entry is for the current version
- [ ] Governance doc SSOT Registry rows that still apply here (the
      Cross-plugin SSOT table and the Architecture planning doc row)
      name files that exist

(Note 2026-11-22: the SSOT Registry item used to read "Governance doc
SSOT Registry has no orphaned entries". The other loom-workflow internal
rows moved to `skill-dev-toolkit` and stay in the registry as history.
A further item, "Architecture doc §10 acceptance criteria still reflect
reality (skills that have shipped should not still appear as \"to be
implemented\")", was removed: `skill-evolution-architecture.md` is the
preserved original proposal, historical, and its wording is kept as
written, not aligned with shipped behaviour.)

---

## Audit report template

Save to `loom-workflow/docs/audit-reports/YYYY-Qn-audit.md`:

```markdown
# YYYY-Qn Quarterly Audit

**Date**: YYYY-MM-DD
**Auditor**: <name>
**Plugin version at audit**: vX.Y.Z

## Findings summary

- N skills active, M deprecated, K retired
- Convention drift (manual check, §3): PASS / FAIL (details if FAIL)
- Score-history drift findings: N (list)

## Action items

- [ ] Item 1
- [ ] Item 2
...

## Notes

Any observations that don't fit elsewhere.
```

(Note 2026-11-21: this template used to ask for "Drift CI: PASS / FAIL".
That CI check, `scripts/check-shared-conventions-drift.py`, has been
removed from this repository, so the line now records the manual
convention drift inspection of §3 instead.)

(Note 2026-11-22: the template also used to ask for "Outstanding
validation gates: N (list)". Step 5 is historical and skipped, so the
report no longer carries that line.)

Commit the audit report. The next quarterly audit references the
prior one's open action items.

---

## What to do with findings

| Finding type | Action |
|---|---|
| Convention drift (manual check, §3) | File an action item to align the skill or update the convention |
| Skill should be Deprecated | Open PR adding deprecation marker + not-trigger; minor bump |
| Skill should be Retired | Wait for 3-month deprecation; then PR removing skill; major bump |
| External upstream broken | Investigate; if upstream gone, update NOTICE; if a license no longer matches its NOTICE entry, follow the new license terms and update the NOTICE |
| Score-history drift | Investigate; possibly run skill-tuning; possibly accept (taste evolved with intent) |

(Note 2026-11-21: the first row used to read "Convention drift in CI —
Block merging until same-PR drift rule honored". No drift CI runs in this
repository any more, so it is no longer a merge blocker. Note 2026-11-22:
two rows, "Validation gate complete" and "Validation gate >2 quarters
outstanding", were removed because step 5 is historical and skipped; the
external-upstream row used to say "if MIT changed, follow license terms".)

---

## When to extend this runbook

This runbook is itself a living document. Extend it when:

- A new class of governance check becomes routinely needed
- A finding type recurs across audits without a clear response policy
- A new skill class enters the family (e.g., agent-team skills)
  with its own audit needs

The plugin owner maintains this runbook as part of governance
responsibility.
