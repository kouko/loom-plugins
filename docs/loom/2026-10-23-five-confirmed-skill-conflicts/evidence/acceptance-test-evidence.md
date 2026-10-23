# Five confirmed skill conflicts — acceptance test evidence

Tried on 2026-10-23 in a fresh local clone at `87fe39685baeea052e45275c19a5b82c0e643486`.
Independent tester: `/root/acceptance_five`; no implementation edits, no child agents.
Working copy: `/tmp/five-acceptance-clean-20261023`.
Scope: synthetic fixtures only, no private histories, vendor calls, or installation changes.

## Setup and verification environment

- Created clean copy with `git clone --no-hardlinks . /tmp/five-acceptance-clean-20261023`; verified HEAD.
- Read root README installation instructions. Used its documented local validation route:
  `agy plugin validate ./loom-workflow`: exit 0, 13 skills and one hook processed.
  `agy plugin validate ./loom-design`: exit 0, six skills processed.
- Installation into live hosts was not attempted. Validation and local CLI execution prove the checked-out artifacts load for these checks; they do not establish live host installation or model behavior.
- Default `uv run --isolated --with-requirements requirements-package-tests.lock ...` could not create a cache lock under sandbox restrictions. Retried with a temporary cache; dependency fetching failed due to DNS/network restrictions. System Python lacked pytest. Used an existing read-only cached Python environment containing pytest and YAML instead; this is not a newly resolved locked environment.
- Interpreter: `/Users/kouko/.cache/uv/archive-v0/utdSjmbwmpv5OstcOQxSj/bin/python`.
- Targeted command: `python -m pytest -q loom-design/tests/spec/test_write_spec_contract.py loom-workflow/tests/scripts/test_dbt_model_style_compaction.py loom-workflow/tests/loom-memory/test_loom_memory.py loom-workflow/tests/loom-memory/test_skill_contract.py loom-workflow/tests/skill-retro/test_issue_surface.py`.
- Observed: **95 passed in 1.28s**, exit 0.
- Full suite deliberately not executed by this tester. Station says package-tests is enabled and finalize-review will execute it. Required suite command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. A build pass was supplied by the station; this report does not treat it as an independently rerun result.

## 1. Preserve confirmed Acceptance ordering and principles

Behavioral attempt: following checked-out write-spec Steps 1–2, produced two requirements from a synthetic confirmed intent whose principles were deliberately ordered opposite to Acceptance. Kept the Acceptance mapping, constrained viewing by authentication and export by secret exclusion. A genuinely incompatible secret-export request produced a conflict response rather than silent renumbering or relaxing a principle.

Observed output is retained below, under A1. Result: works in this bounded manual skill execution. The prose-pin tests alone are not the basis for this verdict. This was not a vendor-host skill invocation or a blind repeated model study.

## 2. Truthful product versus engineering handoff

Behavioral attempt: composed handoffs for (a) a product request with an explicit recorded answer, (b) engineering without that question, and (c) product with no answer. Product reports the actual answer, engineering reports exemption, unanswered product waits. Exact synthetic inputs and responses appear below under A2. Result: works within the stated simulation boundary.

### Captured A1/A2 inputs and outputs

# Synthetic skill walkthrough outputs

## A1
Input: Confirmed Acceptance is (1) view saved notes; (2) export notes. Non-negotiables, deliberately reverse ordered: exported notes must omit secrets; viewing notes requires sign-in. Engineering change, no product behavior approval required.

Output after following write-spec Steps 1–2:
REQ-1 — View saved notes
  The notes view shall show saved notes only after sign-in → Acceptance #1
REQ-2 — Export notes
  The export shall omit secrets from exported notes → Acceptance #2
Design decision: agent-decided — require sign-in and redact exports because the two non-negotiables pin those choices; retain confirmed Acceptance order.

Boundary input: Acceptance explicitly requests exporting stored secrets, while the non-negotiable prohibits exporting secrets.
Output: These obligations cannot both be met. Preserve Acceptance #2 and its mapping, report the conflict, and return for intent clarification; do not silently reorder or relax the principle.

## A2
Input product: user explicitly answered “Yes, show the date beside each note”; recorded question: {decision_point: ②, text: "Show the date beside each note?", type: behaviour}.
Output: Product behavior was confirmed by the stated answer. Carry that question verbatim into the plan's Questions asked. Do not repeat decision point ②; plan is agent-decided; next stop is acceptance.
Input engineering: confirmed intent to reorganize internal validation, no product confirmation question or answer.
Output: Engineering exemption applies to decision point ②; no product behavior confirmation occurred. Carry only the existing intent question. Do not run decision point ②; plan is agent-decided; next stop is acceptance.
Boundary input product: no answer yet.
Output: Await the user's behavior confirmation; do not emit a confirmed handoff.

These are outputs composed by the independent acceptance tester following the checked-out skill, not executions of an installed vendor host or repeated model evaluations.


## 3. Working-language dbt descriptions

Behavioral attempt: applied the checked-out dbt header guidance to one minimal staging header in English, Japanese and Traditional Chinese. Preserved `raw_orders` and `order_id` identifiers; translated title, summary, grain and narrative. Ran the bundled validator on each authored file. All three returned `✓ 1 file(s) clean.`, exit 0. The validator verifies shape, while language was checked against the explicit scenario request by this tester.

The SQL fixtures intentionally exercise only the touched header scope, not warehouse execution or comment persistence. Complete inputs and outputs are retained in the reproducer and transcript below. Result: works.

## 4. First record and protection of existing stores

Behavioral attempt: classified a synthetic durable schema lesson as recordable, then followed Record order: initialize an absent/empty store, read index, write a concept, regenerate index, validate. Both shapes validated. Invoked initialization against populated valid stores and compared the complete filename-to-bytes mapping before and after: unchanged. Corrupt and legacy fixtures were rejected, also byte-identical. Legacy returned explicit migration guidance. No real memory was read or changed.

Result: works for initialization and preservation. The local reproducer ran the actual CLI and asserted state, rather than merely reading the prose.

Residual limitation, **not dismissed**: `loom-workflow/skills/loom-memory/evals/record-timing.md`, fifth reference run, records changed reader scarcity MISS (4 candidates) versus baseline PASS (1), one fresh reader/sample per text. The pre-step clauses are byte-identical. The changed reader additionally recorded candidate 3; the baseline omitted ground-truth candidates 1 and 12. Timing and exception passed. These observations neither establish causation nor equivalence. This acceptance test did not repeat or override that independent evaluation, and successful initialization does not resolve the scarcity miss.

## 5. Source-grounded analysis, version attribution, unavailable source and cutoff

Behavioral attempt:
1. Created an explicit readable source under the clean copy's temporary fixture tree, outside any plugin installation.
2. Created one synthetic Claude Code JSONL and one synthetic Codex JSONL, each with observable events tying historical source bytes to a SHA-256. The two historical sources deliberately differ: `Save immediately.` versus `Ask before saving.`.
3. Read both historical fixtures and the current source. Produced a concrete analysis distinguishing event observation, source observation and causal inference: immediate-save wording is consistent with the first observation; confirmation wording conflicts with the second, so wording alone does not explain it.
4. Passed the retained events through real ingestion and dispatch payload code. Appended another log event after capture; the retained snapshot and iterator did not absorb it.
5. Tried reading a nonexistent source and retained an explicit unknown/unavailable limitation; no invented anchor or missing-source instruction item was created.
6. Normalized, clustered and rendered the collected analysis. The promoted proposal retained six source inspection records, two distinct host histories, current-source status and missing-source uncertainty. The advisory dispatch payload preserved the collected input.
7. No execution of reviewed source instructions, modification of reviewed sources after capture, or vendor/model dispatch occurred.

Observed transport result: PASS, exact output below. This demonstrates local transport plus the tester's actual source comparison, not automatic compliance of a live analyst model.

**Important unresolved finding — entry scope contradiction:** scenario request: “Review the currently running session, using this explicit readable target source; the target is not installed here.” At `loom-workflow/skills/skill-retro/SKILL.md:4` and `:10`, the entry description and opening scope say completed sessions / installed skill. At `:23`, the workflow explicitly says no target installation is required. The spec and source-inspection contract admit a captured current-session boundary. Following the entry scope literally excludes the scenario, while following Step 2 admits its target. The tester cannot give a consistent entry decision without choosing which instruction to override. This is an observed prose-contract conflict, **not** evidence that a live host actually rejected the request.

Related instances independently read after the station identified them: `loom-workflow/skills/skill-retro/README.md:5` repeats completed/installed scope; `agents/prompt-failure-analysis.md:90` and `agents/prompt-success-analysis.md:43` still define recommendations in terms of the installed skill. These belong to the same scope-consistency finding.

Result: **partly**. To close: align description, opening scope, related analyst wording and workflow with selected bounded snapshots and readable explicit target paths; rerun the full A5 scenario including entry handling.

## Reproducible synthetic CLI and transport exercise

Run with the cited Python environment from the clean clone:
`python acceptance_probe.py > /tmp/five-acceptance-probe-r2.log 2>&1`.

First attempt failed because this tester wrote `skill-instruction` instead of the documented `skill-instructions` enum. Corrected only the temporary test fixture and reran into a fresh fixture directory. No production repair occurred. Successful attempt exit 0.

The complete local exercise is retained here as non-executable evidence:

```python
from pathlib import Path
import subprocess, sys, json, hashlib
ROOT = Path(__file__).parent
OUT = ROOT / 'acceptance-fixtures-r2'
OUT.mkdir(exist_ok=True)

def run(*args):
    p = subprocess.run([sys.executable, *map(str,args)], text=True, capture_output=True)
    print('COMMAND', ' '.join(map(str,args)), 'EXIT', p.returncode)
    print((p.stdout+p.stderr).strip())
    return p

# A3: translate descriptive values while preserving technical identifiers.
for locale, title, summary, grain, narrative in [
    ('en','Daily orders','Orders for daily order analysis','One row per order','Cancelled orders remain visible.'),
    ('ja','日次注文','日次の注文分析に用いる注文','一行は一件の注文','キャンセル済みの注文も表示します。'),
    ('zh','每日訂單','供每日訂單分析使用的訂單','每列代表一筆訂單','已取消的訂單仍會保留。'),
]:
    p = OUT/f'stg_orders_{locale}.sql'
    p.write_text(f'/* ---\ntitle: {title}\nsummary: {summary}\ngrain: {grain}\nsources: [raw_orders]\n---\n{narrative}\n*/\n/* {narrative} */\nSELECT order_id FROM raw_orders\n')
    assert run(ROOT/'loom-workflow/skills/dbt-model-style/scripts/validate_header.py',p).returncode == 0
    print('A3',locale,p.read_text().strip())

cli = ROOT/'loom-workflow/skills/loom-memory/scripts/loom_memory.py'
for shape in ('absent','empty'):
    store = OUT/shape
    if shape == 'empty': store.mkdir()
    assert run(cli,'init',store).returncode == 0
    assert (store/'index.md').read_text()
    concept = '---\nname: preserve-identifiers\ndescription: Preserve published identifiers when changing display labels.\ntype: practice\nsources:\n  - resource: synthetic schema contract\n---\n\n## Trigger\nRenaming a published label.\n\n## Correct path\nChange the display label only.\n\n## Why\nConsumers depend on stable identifiers.\n'
    (store/'preserve-identifiers.md').write_text(concept)
    assert run(cli,'regenerate-index',store).returncode == 0
    assert run(cli,'validate',store).returncode == 0
    assert 'preserve-identifiers.md' in (store/'index.md').read_text()
    before = {p.name:p.read_bytes() for p in store.iterdir()}
    assert run(cli,'init',store).returncode != 0
    assert before == {p.name:p.read_bytes() for p in store.iterdir()}
    print('A4 first record and valid-store preservation PASS',shape)
for shape in ('corrupt','legacy'):
    store = OUT/shape; store.mkdir()
    (store/'lesson.md').write_text('existing content')
    if shape == 'legacy': (store/'README.md').write_text('# Memory\n## Index\n- lesson\n')
    before = {p.name:p.read_bytes() for p in store.iterdir()}
    assert run(cli,'validate',store).returncode != 0
    assert run(cli,'init',store).returncode != 0
    assert before == {p.name:p.read_bytes() for p in store.iterdir()}
    print('A4 refused and preserved PASS',shape)

# A5: use adapters and payload/renderer with a source outside plugin installation.
sys.path.insert(0,str(ROOT/'loom-workflow/skills/skill-retro/scripts'))
from ingest import ingest_claude_jsonl, ingest_codex_jsonl
from main import _build_subagent_entries
from propose import extract_memory_items, render_proposals_markdown
from report import build_dispatch_payload
from cluster import cluster_memory_items
results=[]
target=OUT/'uninstalled-source'/'SKILL.md'; target.parent.mkdir()
target.write_text('# Demo\n## Usage\nAsk before saving.\n')
for host,adapter,wording in [('claude-code',ingest_claude_jsonl,'Save immediately.'),('codex',ingest_codex_jsonl,'Ask before saving.')]:
    root=OUT/host; root.mkdir()
    historical=root/'SKILL.md'; historical.write_text('# Demo\n## Usage\n'+wording+'\n')
    digest=hashlib.sha256(historical.read_bytes()).hexdigest()
    content=f'Synthetic loaded source {historical}, sha256 {digest}. User requested a preview; assistant saved without a preview.'
    record=({'type':'user','sessionId':host,'timestamp':'2026-10-23T00:00:00Z','message':{'role':'user','content':content}} if host=='claude-code' else {'type':'response_item','timestamp':'2026-10-23T00:00:00Z','payload':{'type':'message','role':'user','content':content}})
    log=root/f'{host}.jsonl'; log.write_text(json.dumps(record)+'\n')
    stream=adapter(root); events=[next(stream)]
    entry=_build_subagent_entries('demo:save',[host],{host:events},{},target_skill_path=str(target))[0]
    snapshot=entry['input']['session_snapshot']
    captured=json.dumps(entry)
    with log.open('a') as f: f.write(json.dumps(record)+'\n')
    assert list(stream)==[] and json.dumps(entry)==captured
    inspections=[]
    for p,status,proof in [(historical,'historical',f'Synthetic retained event records sha256 {digest}'),(target,'current','Read during acceptance; not proof of past loading')]:
        inspections.append({'session_id':host,'tool':host,'path':str(p),'location':'Usage:3','version_status':status,'version_evidence':proof,'observation':p.read_text().splitlines()[2],'uncertainty':'Synthetic evidence only; current source does not establish past causation.'})
    missing=OUT/'unavailable'/'SKILL.md'
    try: missing.read_text()
    except FileNotFoundError:
        inspections.append({'session_id':host,'tool':host,'path':str(missing),'location':'','version_status':'unknown','version_evidence':'','observation':'Source unavailable','uncertainty':'Cannot diagnose this unavailable revision; bounded investigation only.'})
    inference=('Historical wording permits immediate saving and is consistent with the observed outcome.' if host=='claude-code' else 'Historical wording requires confirmation; observed saving conflicts with it, so wording alone does not explain the outcome.')
    results.append({'session_id':host,'target_skill_path':str(target),'session_snapshot':snapshot,'source_inspections':inspections,'memory_items':[{'title':'Preview before save','description':'Provide an explicit preview confirmation rule.','kind':'failure','issue_surface':'skill-instructions','section_anchor':'Usage','content':f'Event observation: saved without preview. Source observation: {wording} Inference: {inference} Current-source proposal: require a preview and explicit confirmation before saving.'}]})
items=extract_memory_items(results,str(target))
promoted,pending=cluster_memory_items([{**i,'session_id':i['_source_session']} for i in items])
assert len(promoted)==1 and len(promoted[0]['source_inspections'])==6
rendered=render_proposals_markdown(items,target_skill_path=str(target),target_skill_md_content=target.read_text())
assert 'historical' in rendered and 'current' in rendered and 'Source unavailable' in rendered
assert build_dispatch_payload(results,'en','2026-10-23','out.md')['dispatch_payload']['input']['merged_data']==results
(OUT/'retro-results.json').write_text(json.dumps(results,indent=2))
(OUT/'retro-proposals.md').write_text(rendered)
print('A5 PASS: two hosts, distinct historical digests, current uninstalled source, missing source, snapshot append cutoff, six preserved inspections, advisory payload')
print('A5 interpretation:',*[r['memory_items'][0]['content'] for r in results],sep='\n')

```

### Captured successful output

```text
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/dbt-model-style/scripts/validate_header.py /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/stg_orders_en.sql EXIT 0
✓ 1 file(s) clean.
A3 en /* ---
title: Daily orders
summary: Orders for daily order analysis
grain: One row per order
sources: [raw_orders]
---
Cancelled orders remain visible.
*/
/* Cancelled orders remain visible. */
SELECT order_id FROM raw_orders
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/dbt-model-style/scripts/validate_header.py /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/stg_orders_ja.sql EXIT 0
✓ 1 file(s) clean.
A3 ja /* ---
title: 日次注文
summary: 日次の注文分析に用いる注文
grain: 一行は一件の注文
sources: [raw_orders]
---
キャンセル済みの注文も表示します。
*/
/* キャンセル済みの注文も表示します。 */
SELECT order_id FROM raw_orders
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/dbt-model-style/scripts/validate_header.py /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/stg_orders_zh.sql EXIT 0
✓ 1 file(s) clean.
A3 zh /* ---
title: 每日訂單
summary: 供每日訂單分析使用的訂單
grain: 每列代表一筆訂單
sources: [raw_orders]
---
已取消的訂單仍會保留。
*/
/* 已取消的訂單仍會保留。 */
SELECT order_id FROM raw_orders
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py init /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent EXIT 0
loom_memory init: created /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent/README.md and /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent/index.md
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py regenerate-index /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent EXIT 0
loom_memory regenerate-index: wrote /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent/index.md
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py validate /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent EXIT 0
loom_memory validate: OK — OKF v0.2-compatible Loom memory profile holds.
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py init /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent EXIT 1
loom_memory init: FAIL — nothing was created.

  [store-not-empty] /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/absent: the store directory already holds content; refusing to touch an existing store
A4 first record and valid-store preservation PASS absent
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py init /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty EXIT 0
loom_memory init: created /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty/README.md and /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty/index.md
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py regenerate-index /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty EXIT 0
loom_memory regenerate-index: wrote /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty/index.md
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py validate /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty EXIT 0
loom_memory validate: OK — OKF v0.2-compatible Loom memory profile holds.
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py init /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty EXIT 1
loom_memory init: FAIL — nothing was created.

  [store-not-empty] /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/empty: the store directory already holds content; refusing to touch an existing store
A4 first record and valid-store preservation PASS empty
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py validate /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/corrupt EXIT 1
loom_memory validate: FAIL — the following invariants are violated.

  [index-missing] index.md: the Loom profile requires a generated index.md
  [frontmatter] lesson.md: no parseable YAML frontmatter block
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py init /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/corrupt EXIT 1
loom_memory init: FAIL — nothing was created.

  [store-not-empty] /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/corrupt: the store directory already holds content; refusing to touch an existing store
A4 refused and preserved PASS corrupt
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py validate /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/legacy EXIT 1
loom_memory validate: FAIL — the following invariants are violated.

  [frontmatter] README.md: no parseable YAML frontmatter block
  [index-missing] index.md: the Loom profile requires a generated index.md
  [frontmatter] lesson.md: no parseable YAML frontmatter block
COMMAND /private/tmp/five-acceptance-clean-20261023/loom-workflow/skills/loom-memory/scripts/loom_memory.py init /private/tmp/five-acceptance-clean-20261023/acceptance-fixtures-r2/legacy EXIT 1
loom_memory init: FAIL — nothing was created.

  [legacy-store] README.md: legacy README-indexed store (a `## Index` heading and no generated index.md); an explicit migration is required — run migrate_legacy_store.py
A4 refused and preserved PASS legacy
A5 PASS: two hosts, distinct historical digests, current uninstalled source, missing source, snapshot append cutoff, six preserved inspections, advisory payload
A5 interpretation:
Event observation: saved without preview. Source observation: Save immediately. Inference: Historical wording permits immediate saving and is consistent with the observed outcome. Current-source proposal: require a preview and explicit confirmation before saving.
Event observation: saved without preview. Source observation: Ask before saving. Inference: Historical wording requires confirmation; observed saving conflicts with it, so wording alone does not explain the outcome. Current-source proposal: require a preview and explicit confirmation before saving.

```

## Decisions and exclusions

- No user-instructed skip markers were present in intent Constraints or plan Risks.
- No dismissed important findings were supplied. The entry contradiction and scarcity limitation remain explicit.
- No product UI flow is applicable: spec declares an engineering change.
- User data was untouched. Only synthetic fixtures, the report and this evidence were created by acceptance work.
- Report/evidence commit is authorized; no publish or merge.

