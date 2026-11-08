"""Prepare/freeze an eight-actor tool-result comparison; run requires explicit consent."""
import ast
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import shutil
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=Path('/private/tmp/engineering-research-save-result-20261108')
RUN=BASE/'private-run'
SRC=Path('/private/tmp/code-owned-engineering-research-execution-20261108')
PRIOR=Path('/private/tmp/claude-code-engineering-research-audits-20261108/packet')
OUT=REPO/'docs/loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/execution'
spec=importlib.util.spec_from_file_location('save_probe_public_runner',HERE/'public_runner.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
ADAPTER=('本輪只提供受限原生讀取工具，唯一保存工具是 mcp__save_probe__save_record；沒有命令、網路或代理工具。'
 '工具僅可在本案例授權範圍保存 Markdown。工具中的雜湊、路徑與連結存在性是機械性觀察，不是研究正確性的判斷。'
 'fixture-observations.json 是準備階段對臨時 fixture 的實際本地 git 與來源雜湊觀察；可引用為 harness 觀察，'
 '不可稱為你執行過命令或測試。無法自行執行的檢查請如實標示限制，不要假裝執行。')


def policy_for(case,mode,root):
    result={'root':str(root),'result_mode':mode}
    if case=='F01':
        result.update(create_roots=['docs/loom/research'],update_files=['docs/loom/research/2026-11-08-package-test-roots.md'])
    elif case=='F04':result['create_roots']=['docs/loom/research']
    elif case=='F06':result['create_files']=['fixtureVault/research/2026-11-08-package-test-roots.md']
    elif case!='F03':raise ValueError('case not in bounded experiment')
    return result


def actor_prompt(common,case):return common+'\n'+case+'\n'+ADAPTER+'\n'


def observations():
    prior_path=REPO/'loom-code/tests/local/engineering_research_retest/harness.py'
    spec=importlib.util.spec_from_file_location('prior_fixture_observations',prior_path)
    h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    return h.observations()


def prepare():
    if RUN.exists():raise RuntimeError('Refusing private experiment refreeze/overwrite')
    RUN.mkdir(parents=True)
    for name in ['cases.json','rubric.md','fixture-provenance.json']:shutil.copy2(SRC/name,RUN/name)
    shutil.copy2(PRIOR/'shared-declared-contract.md',RUN/'shared-declared-contract.md')
    shutil.copy2(BASE/'prospective-protocol.md',RUN/'prospective-protocol.md')
    original=json.loads((SRC/'cases.json').read_text());cases={c['id']:c for c in original}
    tree=ast.parse((SRC/'run.py').read_text())
    common=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='COMMON' for t in n.targets))
    common=common.replace('正式 skill executor','Claude Code explicit skill executor')
    common+='\n本次明示讀取原始 skill/engineering-research/SKILL.md 及必要 bundled Markdown；這不是已安裝 plugin 或原生 Skill 啟動測試。\n'
    obs=observations();mapping=[];actors={};equivalence=[]
    for index,case in enumerate(['F04','F01','F06','F03']):
        modes=['confirmation','full'] if index%2==0 else ['full','confirmation']
        pair=[]
        for second,mode in enumerate(modes):
            name=chr(65+2*index+second);actor=RUN/name;actor.mkdir();work=actor/'project'
            shutil.copytree(SRC/'fixture',work)
            skill=REPO/'loom-code/skills/engineering-research'
            for p in sorted(skill.rglob('*.md')):
                if p.name=='README.md':continue
                dest=work/'skill/engineering-research'/p.relative_to(skill);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
            r.dump(work/'fixture-observations.json',obs)
            (actor/'prompt.txt').write_text(actor_prompt(common,cases[case]['prompt']))
            r.dump(actor/'policy.json',policy_for(case,mode,work))
            r.dump(actor/'mcp.json',{'mcpServers':{'save_probe':{'command':sys.executable,'args':[str(HERE/'server.py'),'--policy',str(actor/'policy.json')],
               'env':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}}}})
            r.dump(actor/'before.json',r.filemap(work))
            actors[name]={'case':case,'inputs':r.filemap(work),'prompt_sha256':r.sha(actor/'prompt.txt'),
              'policy_sha256':r.sha(actor/'policy.json'),'mcp_sha256':r.sha(actor/'mcp.json'),
              'command':r.command(actor,'<frozen actor prompt>')}
            mapping.append({'actor':name,'case':case,'mode':mode});pair.append(actor)
        equal_prompt=(pair[0]/'prompt.txt').read_bytes()==(pair[1]/'prompt.txt').read_bytes()
        equal_project=r.filemap(pair[0]/'project')==r.filemap(pair[1]/'project')
        p0=json.loads((pair[0]/'policy.json').read_text());p1=json.loads((pair[1]/'policy.json').read_text())
        for p in [p0,p1]:p.pop('root');p.pop('result_mode')
        assert equal_prompt and equal_project and p0==p1
        equivalence.append({'case':case,'actors':[x.name for x in pair],'prompt_identical':equal_prompt,'all_project_files_identical':equal_project,'authorization_policy_identical':p0==p1})
    r.dump(RUN/'arm-map.json',mapping)
    dependencies=[HERE/n for n in ['experiment.py','public_runner.py','paired_experiment.py','save_tool.py','server.py']]
    dependencies.append(REPO/'loom-code/tests/local/engineering_research_retest/harness.py')
    freeze={'dependencies':{str(p):r.sha(p) for p in dependencies},'cli_sha256':r.sha(r.CLAUDE),'cli_realpath':str(r.CLAUDE.resolve()),
      'settings_sha256':r.sha(r.PUBLIC/'isolated-settings.json'),'arm_map_sha256':r.sha(RUN/'arm-map.json'),
      'criteria':{n:r.sha(RUN/n) for n in ['cases.json','rubric.md','fixture-provenance.json','shared-declared-contract.md','prospective-protocol.md']},
      'actors':actors,'model':'claude-sonnet-5-5','effort':'medium','provider':'first-party Anthropic native account',
      'tool_adapter':ADAPTER,'timeout_seconds':300,'max_concurrency':2,'replication':'one pair per four cases; directional only',
      'manipulation':'save result content only; identical name/schema/description, internal write/readback/link checks and current seven runtime Markdown files',
      'model_calls_during_prepare':0,'authorization':'run requires explicit user-specific approval and parent public-isolation verification'}
    r.dump(RUN/'freeze.json',freeze);r.dump(RUN/'prepare-verification.json',{'pairs':equivalence,'freeze_sha256':r.sha(RUN/'freeze.json'),'model_calls':0})
    print(json.dumps({'prepared':str(RUN),'actors':8,'freeze_sha256':r.sha(RUN/'freeze.json'),'model_calls':0},ensure_ascii=False))


def validate_freeze():
    freeze=json.loads((RUN/'freeze.json').read_text())
    for p,h in freeze['dependencies'].items():
        if r.sha(Path(p))!=h:raise RuntimeError('dependency drift: '+p)
    if r.sha(r.CLAUDE)!=freeze['cli_sha256'] or r.sha(r.PUBLIC/'isolated-settings.json')!=freeze['settings_sha256']:raise RuntimeError('CLI/settings drift')
    if r.sha(RUN/'arm-map.json')!=freeze['arm_map_sha256']:raise RuntimeError('arm map drift')
    for n,h in freeze['criteria'].items():
        if r.sha(RUN/n)!=h:raise RuntimeError('criterion drift: '+n)
    for name,actor in freeze['actors'].items():
        out=RUN/name;r.require_fresh(out)
        if r.filemap(out/'project')!=actor['inputs']:raise RuntimeError('actor input drift: '+name)
        for n,k in [('prompt.txt','prompt_sha256'),('policy.json','policy_sha256'),('mcp.json','mcp_sha256')]:
            if r.sha(out/n)!=actor[k]:raise RuntimeError('actor configuration drift: '+name)
    return freeze


def require_authorization():
    consent=json.loads((RUN/'authorization.json').read_text())
    if consent.get('approved_private_execution') is not True or consent.get('actor_count')!=8 or consent.get('provider')!='first-party Anthropic':
        raise RuntimeError('Specific eight-actor Anthropic authorization required')
    control=json.loads((r.PUBLIC/'verified.json').read_text())
    if control.get('customization_isolation_confirmed') is not True or control.get('mcp_tool_connected') is not True:
        raise RuntimeError('Parent must verify actual public custom-tool isolation before private calls')


def one(item):
    actor=RUN/item['actor'];receipt=r.execute(actor,item['case']);before=json.loads((actor/'before.json').read_text());after=json.loads((actor/'after.json').read_text())
    protected=[p for p in before if p.startswith(('src/','skill/','snapshots/','.git/')) or p in ['provenance.json','sample-receipt.json','fixture-cleanup.json','fixture-observations.json']]
    receipt['protected_unchanged']=all(after.get(p)==before[p] for p in protected)
    receipt['fixtureVault_changes']=[p for p in receipt['changed_files']+receipt['added_files'] if p.startswith('fixtureVault/')]
    r.dump(actor/'receipt.json',receipt);return receipt


def run():
    require_authorization();validate_freeze()
    mapping=json.loads((RUN/'arm-map.json').read_text());receipts=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for i in range(0,len(mapping),2):receipts.extend(pool.map(one,mapping[i:i+2]))
    r.dump(RUN/'receipts.json',receipts)
    OUT.mkdir(parents=True,exist_ok=False)
    for n in ['freeze.json','arm-map.json','cases.json','rubric.md','fixture-provenance.json','shared-declared-contract.md','prospective-protocol.md','receipts.json','authorization.json','prepare-verification.json']:
        shutil.copy2(RUN/n,OUT/n)
    for item in mapping:
        actor=RUN/item['actor'];dest=OUT/item['actor'];dest.mkdir()
        for n in ['prompt.txt','before.json','after.json','events.jsonl','answer.txt','receipt.json','stderr.txt']:shutil.copy2(actor/n,dest/n)
        receipt=json.loads((actor/'receipt.json').read_text())
        for name in receipt['changed_files']+receipt['added_files']:
            p=actor/'project'/name
            if p.is_file() and p.suffix in ['.md','.json','.txt']:
                q=dest/'artifacts'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    r.dump(OUT/'evidence-integrity.json',{'hashes':r.filemap(OUT),'raw_root':str(RUN),'semantics':'ungraded; actual observable tool content is not research correctness','reasoning':'excluded'})
    print('Eight explicit actors completed; independent semantic judgments still required.')
