from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,random,shutil,signal,subprocess,sys,time
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[4]
TARGET=OUT.parent.parent/'input/engineering-research'
TEMP=Path('/private/tmp/engineering-research-dogfood-A-20261108')
MODEL='gpt-6.1-sol'
SOURCES=['loom-workflow/skills/critique','loom-workflow/skills/independent-advisor','loom-workflow/skills/project-retro','loom-code/skills/write-plan','loom-design/skills/capture-intent']
POS=[
('Before we commit our Loom intent, determine whether the current package test runner really discovers shell tests. That capability decides whether our proposed guard can ship. Read the provided runner and identify the evidence gap.','intent capability'),
('The active intent assumes new test roots are discovered automatically, while a reviewer says they must be listed. Resolve this contradiction before we choose an approach.','contradiction'),
('We are writing a spec, and whether pytest and shell tests share inventory determines the design. Check the actual runner rather than accepting the assumption.','spec capability'),
('During planning, we need evidence on whether tests/local runs in CI. An incorrect assumption changes our validation plan. Investigate the runner slice.','planning compatibility'),
('Build has failed repeatedly because a shell test seems absent from package execution. Stop retrying and establish what the runner actually discovers.','repeated build failure'),
('我們正在確認 intent；「新增 plugin 不用改測試入口」只是猜測，會影響方案可行性。請先用現有 runner 查證。','intent feasibility zh'),
('spec 的兩份說法互相衝突：一份說自動探索測試，一份說固定 roots。先查清楚它們如何同時成立。','spec contradiction zh'),
('規劃尚未定案：若本機 CLI 測試會在一般 suite 跑，CI 方案就要改。請以實際程式判斷，不要直接排工作。','planning evidence zh'),
('build 已連續兩次找不到新增測試；先找出真正原因與證據，再決定要不要調整 discovery 設計。','build repeated zh'),
('採用這個測試入口之前，請確認它有沒有支援 shell 測試。這會決定我們能不能沿用既有驗證方式。','generic capability zh'),
('実装方針を決める前に、テスト実行器が新しい plugin の tests を自動発見するという前提を確認してください。前提が違えば設計が変わります。','generic feasibility ja'),
('Loom の intent を確認中です。ローカル CLI 専用テストが通常 suite に混ざるかで採用判断が変わります。コードで確かめてください。','intent compatibility ja'),
('spec 作成中です。pytest と shell が別々の一覧を使うという説明と、共通 inventory という説明の矛盾を解消してください。','spec contradiction ja'),
('ビルドで同じ test discovery の失敗を繰り返しました。再試行より先に、何が探索対象かを確認してください。','build repeated ja'),
('We need an engineering decision, not implementation yet: can this runner support a fifth plugin without changing production code? Verify the relevant constraint first.','generic decision'),
('A proposed acceptance strategy depends on shell tests being discovered recursively. Establish whether the current implementation supports that before recommending the strategy.','acceptance assumption'),
('The plan treats tests/local as ordinary package tests. I suspect that assumption is wrong and would invalidate CI. Resolve it from source before planning further.','plan invalid premise'),
('Before approving the spec, check whether the runner requires node or only Python. That environment requirement could make the design infeasible.','environment feasibility'),
('目前沒有要修 code；先調查 runner 對 test roots 的限制，因為它會改變我們要不要新增 plugin 的決定。','decision boundary zh'),
('Compatibility is the open decision: will a test named example_test.py and one named test-example.sh both be collected by the supplied runner? Verify rather than assume.','compatibility concrete'),
]
NEG=[
('Critique this proposal on value and complexity only: add an optional summary flag to our runner. Assume technical feasibility is established; do not investigate capabilities.','critique'),
('Please obtain an independent second opinion from another coding agent on this test-plan decision. Do not execute it yet; explain what review input is missing.','independent-advisor'),
('Do a retrospective of this session: we agreed scope, made one small test update, and forgot to record the command. No unresolved technical question; what process should improve?','project-retro'),
('The intent is confirmed and feasibility is established. Break adding one shell test into implementation tasks, without investigating technical assumptions.','write-plan'),
('I want to add a new optional --summary flag to the runner. Capture my goal and acceptance criteria first; there are no feasibility questions to investigate yet.','capture-intent'),
]
def init():
 OUT.mkdir(exist_ok=True)
 cases=[dict(id=f'P{i:02}',query=q,should_trigger=True,rationale=r) for i,(q,r) in enumerate(POS,1)]+[dict(id=f'N{i:02}',query=q,should_trigger=False,rationale=r) for i,(q,r) in enumerate(NEG,1)]
 (OUT/'corpus.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
 (OUT/'findings.md').write_text('''# Probe A activation findings (advisory)\n\nNative Codex host-adapted raw-skill discovery; not Claude Skill() fidelity, installation parity, or full Loom hooks. Requested model gpt-6.1-sol, first-party OpenAI, medium. Corpus labels/rationales withheld from actors. 20 positive and 5 negative cases, two fresh runs each; repetitions are not independent production reliability samples.\n\nDesigner limitation: the orchestrator accidentally displayed the first 30 body lines while extracting frontmatter before corpus creation. Actors remain blind until actual native tool reads; the corpus designer is partially informed.\n\nAll work projects are isolated in /private/tmp. Each receives the genuine current scripts/run_package_tests.py as its only source fixture. Only selected raw skill packages and that source slice are available. No vault or private sessions. Temporary auth is symlinked locally, never read as prompt content.\n\n''')
 return cases
COMMON='''Handle the user request below using the available skills when relevant. This is a read-only engineering discussion, not authorization to implement or publish anything. Work only inside this isolated project and the skills listed in your initial catalog. Do not read other files, private sessions, or credentials. No subagents, installation, commits, external CLI model calls or configuration changes. The only project source fixture is scripts/run_package_tests.py; report missing evidence instead of inventing it. Keep your answer concise (maximum 200 words), and do not continue beyond the user's requested stage.\n\nUser request:\n'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def one(case,rep):
 rid=f"{case['id']}-r{rep}";out=OUT/'runs'/rid;out.mkdir(parents=True,exist_ok=True)
 receipt_path=out/'receipt.json'
 if receipt_path.exists():return json.loads(receipt_path.read_text())
 work=TEMP/rid/'project';home=TEMP/rid/'home';home.mkdir(parents=True);work.mkdir()
 (work/'scripts').mkdir();shutil.copy2(REPO/'scripts/run_package_tests.py',work/'scripts/run_package_tests.py')
 skills=home/'skills';skills.mkdir()
 for p in SOURCES:
  dest=skills/Path(p).name;dest.mkdir()
  front=(REPO/p/'SKILL.md').read_text().split('---',2)[1]
  (dest/'SKILL.md').write_text('---'+front+'---\n\nDescription-only adjacent skill stub for activation testing. No workflow body is available in this isolated test. Answer the user request concisely within the read-only boundary.\n')
 shutil.copytree(TARGET,skills/'engineering-research')
 (home/'config.toml').write_text('model = "gpt-6.1-sol"\nmodel_provider = "openai"\nmodel_reasoning_effort = "medium"\nweb_search = "disabled"\n[features]\napps = false\nmulti_agent = false\n')
 (home/'auth.json').symlink_to('/Users/kouko/.codex/auth.json')
 env={k:v for k,v in os.environ.items() if k in ['PATH','HOME','USER','LOGNAME','SHELL','TMPDIR','LANG','LC_ALL']};env['CODEX_HOME']=str(home)
 prompt=COMMON+case['query']+'\n';(out/'prompt.txt').write_text(prompt);shutil.copy2(home/'config.toml',out/'config.toml')
 rec=dict(context_variant='resumed-description-only-adjacents',authorization='../../authorization-resume.json',web_search='disabled',apps=False,multi_agent=False,id=rid,case_id=case['id'],repetition=rep,expected=case['should_trigger'],model_requested=MODEL,provider_requested='openai',effort_requested='medium',excluded_reasoning_events=0,started=datetime.datetime.now(datetime.timezone.utc).isoformat())
 start=time.monotonic()
 try:
  debug=subprocess.run(['codex','-C',str(work),'debug','prompt-input','CATALOG_CHECK'],env=env,capture_output=True,text=True,timeout=30)
  (out/'catalog.json').write_text(debug.stdout);(out/'catalog-stderr.txt').write_text(debug.stderr)
  assert debug.returncode==0,debug.stderr
  assert 'engineering-research' in debug.stdout
  assert 'Use evidence proportionate to the engineering question.' not in debug.stdout
  assert all(Path(p).name in debug.stdout for p in SOURCES)
  rec['catalog_verified']=True
  rec['fixture_sha256']=sha(work/'scripts/run_package_tests.py')
  rec['skill_file_sha256']={str(f.relative_to(skills)):sha(f) for f in skills.rglob('*') if f.is_file()}
  cmd=['codex','exec','--ephemeral','--skip-git-repo-check','--json','--sandbox','read-only','-C',str(work),'-o',str(out/'answer.txt'),'-'];rec['command']=cmd
  with (out/'stderr.txt').open('w') as err,(out/'events.jsonl').open('w') as events:
   proc=subprocess.Popen(cmd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True,start_new_session=True);proc.stdin.write(prompt);proc.stdin.close()
   def consume():
    for line in proc.stdout:
     try:e=json.loads(line)
     except json.JSONDecodeError:e=dict(type='unparsed',text=line)
     if e.get('item',{}).get('type') in ['reasoning','reasoning_summary']:rec['excluded_reasoning_events']+=1;continue
     events.write(json.dumps(e,ensure_ascii=False)+'\n');events.flush()
   with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
    f=pool.submit(consume)
    try:rec['exit_code']=proc.wait(timeout=120);rec['timed_out']=False
    except subprocess.TimeoutExpired:
     os.killpg(proc.pid,signal.SIGTERM)
     try:proc.wait(timeout=5)
     except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
     rec.update(exit_code=proc.returncode,timed_out=True)
    f.result(timeout=15)
  es=[json.loads(l) for l in (out/'events.jsonl').read_text().splitlines()]
  items=[e['item'] for e in es if e.get('type')=='item.completed' and 'item' in e]
  commands=[i for i in items if i.get('type')=='command_execution']
  reads=[i for i in commands if 'engineering-research' in i.get('command','') and 'Use evidence proportionate to the engineering question.' in i.get('aggregated_output','')]
  rec['target_body_read']=bool(reads);rec['target_read_commands']=[i['command'] for i in reads]
  rec['skill_read_commands']=[i['command'] for i in commands if 'SKILL.md' in i.get('command','')]
  rec['thread_id']=next((e.get('thread_id') for e in es if e.get('type')=='thread.started'),None)
  rec['usage']=next((e.get('usage') for e in es if e.get('type')=='turn.completed'),{})
  rec['classification']=('true-positive' if reads else 'trigger-miss') if case['should_trigger'] else ('over-trigger' if reads else 'true-negative')
  if rec['classification'] in ['trigger-miss','over-trigger'] and not rec.get('timed_out') and rec['exit_code']==0:
   with (OUT/'findings.md').open('a') as f:f.write(f"## Observed {rid}: {rec['classification']}\n\nSeverity: Medium; category: {rec['classification']}; pass: blind; fidelity: native-Codex-adapted.\n\nPrompt: {case['query']}\n\nExpected target body read: {case['should_trigger']}; observed: {bool(reads)}. Transcript: [events](runs/{rid}/events.jsonl), [answer](runs/{rid}/answer.txt), [catalog](runs/{rid}/catalog.json), [receipt](runs/{rid}/receipt.json).\n\nLocation: input/engineering-research/SKILL.md frontmatter description. Suggested edit class: revisit trigger boundary wording after examining this prompt and adjacent skill reads. Root cause remains uncertain: description coverage, competition, and host policy can all contribute; a routing observation alone cannot isolate them. Static review cannot establish actual activation.\n\n")
 except Exception as exc:rec['harness_error']=repr(exc)
 finally:
  (home/'auth.json').unlink(missing_ok=True)
  rec['auth_symlink_removed']=not (home/'auth.json').exists();rec['elapsed_seconds']=round(time.monotonic()-start,3)
  for p in ['prompt.txt','catalog.json','events.jsonl','answer.txt']:
   if (out/p).exists():rec[p+'_sha256']=sha(out/p)
  (out/'receipt.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 return rec

def main():
 if (OUT/'EXECUTION_STOPPED').exists():raise SystemExit('External execution stopped: see EXECUTION_STOPPED and findings.md. Do not resume as a workaround.')
 cases=json.loads((OUT/'corpus.json').read_text()) if (OUT/'corpus.json').exists() else init();jobs=[(c,r) for r in [1,2] for c in cases];random.Random(1108).shuffle(jobs)
 if '--preflight' in sys.argv:jobs=[(cases[0],1)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  fs=[pool.submit(one,c,r) for c,r in jobs];receipts=[]
  for f in concurrent.futures.as_completed(fs):
   rec=f.result();receipts.append(rec);(OUT/'receipts.json').write_text(json.dumps(sorted(receipts,key=lambda x:x['id']),ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:rec.get(k) for k in ['id','classification','elapsed_seconds','harness_error','timed_out']},ensure_ascii=False),flush=True)
 valid=[r for r in receipts if 'classification' in r and not r.get('timed_out') and r.get('exit_code')==0]
 counts={s:sum(r['classification']==s for r in valid) for s in ['true-positive','true-negative','trigger-miss','over-trigger']}
 summary=dict(counts=counts,planned=50,completed=len(receipts),valid=len(valid),invalid=len(receipts)-len(valid),positive_n=counts['true-positive']+counts['trigger-miss'],negative_n=counts['true-negative']+counts['over-trigger'],positive_rate=counts['true-positive']/max(1,counts['true-positive']+counts['trigger-miss']),negative_rate=counts['true-negative']/max(1,counts['true-negative']+counts['over-trigger']),context_note='P01-r1 preflight has full adjacent bundles and default capabilities; remaining49 use description-only stubs and web/apps/multiagent disabled. Original stop/summary/receipts retained in history.')
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
