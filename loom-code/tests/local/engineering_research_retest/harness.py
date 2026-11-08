"""Optional local six-pair CLI experiment; no model requests during preparation/tests."""
import ast
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[4]
BASE = Path('/private/tmp/engineering-research-small-fix-20261108')
RUN = BASE / 'paired-run'
SRC = Path('/private/tmp/code-owned-engineering-research-execution-20261108')
CLAUDE = Path('/Users/kouko/.local/bin/claude')
OUT = REPO / 'docs/loom/2026-11-08-engineering-research-skill/evidence/small-repair-comparison'
ENV_KEYS = ['HOME','PATH','USER','LOGNAME','SHELL','TMPDIR','LANG','LC_ALL','SECURITYSESSIONID','__CF_USER_TEXT_ENCODING']
ADAPTER = ('本輪僅提供受限的原生檔案工具，沒有命令、網路或代理工具。'
           'fixture-observations.json 是準備階段對此臨時 fixture 進行的實際本地 git 查詢與來源雜湊觀察，'
           '兩個待比較版本收到相同內容；可讀取並引用為 harness 觀察，不可稱為你執行過命令或測試。'
           '無法自行執行的檢查請如實標示限制，不要假裝執行。')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def filemap(path):
    return {str(p.relative_to(path)): sha(p) for p in sorted(path.rglob('*')) if p.is_file()}


def environment(source=None):
    source = os.environ if source is None else source
    return {**{k: source[k] for k in ENV_KEYS if k in source}, 'HOME': '/Users/kouko'}


def command(case, prompt):
    tools = 'Read,Grep,Glob' if case == 'F03' else 'Read,Write,Edit,Grep,Glob'
    return [str(CLAUDE),'--safe-mode','--restricted','--setting-sources','',
            '--strict-mcp-config','--no-session-persistence','--no-chrome',
            '--permission-prompts','none','--permission-mode','dontAsk',
            '--tools',tools,'--allowedTools',tools,'--model','claude-sonnet-5-5',
            '--effort','medium','--output-format','stream-json','--verbose','-p',prompt]


def actor_prompt(common, case):
    return common + '\n' + case + '\n' + ADAPTER + '\n'


def require_fresh(path):
    if path.exists():
        raise RuntimeError('Refusing to overwrite/refreeze existing experiment directory: ' + str(path))


def require_unrun(out):
    if any((out / n).exists() for n in ['started.json','receipt.json','answer.txt','events.jsonl']):
        raise RuntimeError('Refusing actor rerun: ' + out.name)


def inventory_checks(case, before, after):
    changed = [p for p in before if after.get(p) != before[p]]
    added = [p for p in after if p not in before]
    protected = [p for p in before if p.startswith(('src/','skill/','snapshots/','.git/')) or p in ['provenance.json','sample-receipt.json','fixture-cleanup.json','fixture-observations.json']]
    vault_changed = [p for p in changed + added if p.startswith('fixtureVault/')]
    boundary = True
    if case == 'F03': boundary = not changed and not added
    elif case == 'F05': boundary = not vault_changed
    elif case == 'F06': boundary = not changed and added == ['fixtureVault/research/2026-11-08-package-test-roots.md']
    return {'changed_files':changed,'added_files':added,'deleted_files':[p for p in before if p not in after],
            'protected_unchanged':all(before[p] == after.get(p) for p in protected),
            'case_boundary_satisfied':boundary,'fixtureVault_files':{p:h for p,h in after.items() if p.startswith('fixtureVault/')}}


def communicate(proc, prompt):
    try:
        out, err = proc.communicate(prompt, timeout=300)
        return out, err, False
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGTERM)
        try: out, err = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            out, err = proc.communicate()
        return out, err, True


def sanitize(stdout):
    events = []
    for line in stdout.splitlines():
        try: item = json.loads(line)
        except ValueError: continue
        if not isinstance(item, dict): continue
        message = item.get('message')
        if item.get('type') == 'assistant' and isinstance(message, dict) and isinstance(message.get('content'), list):
            message['content'] = [b for b in message['content'] if b.get('type') not in ('thinking','redacted_thinking')]
        events.append(item)
    return events


def observations():
    fixture = SRC / 'fixture'
    cmds = [['git','rev-parse','main','research-fixture'],
            ['git','merge-base','--is-ancestor','research-fixture','main'],
            ['git','log','--all','--oneline','--decorate','-8'],
            ['git','status','--porcelain'],['git','tag','--list'],['git','remote','-v']]
    results = []
    for cmd in cmds:
        p = subprocess.run(cmd, cwd=fixture, capture_output=True, text=True, check=False)
        results.append({'argv':cmd,'cwd':'original isolated fixture before actor skill insertion',
                        'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    sources = {str(p.relative_to(fixture)):sha(p) for p in sorted((fixture/'src').rglob('*')) if p.is_file()}
    sources['docs/loom/research/2026-11-08-package-test-roots.md'] = sha(fixture/'docs/loom/research/2026-11-08-package-test-roots.md')
    return {'kind':'actual local harness observations before actor execution',
            'scope':'Temporary local fixture only; not deployment, suite/CI, actor execution, release or installation. No post-write actor-copy hash is supplied.',
            'git':results,'sha256':sources,'source_provenance_sha256':sha(fixture/'provenance.json')}


def prepare():
    require_fresh(RUN)
    RUN.mkdir(parents=True)
    for name in ['cases.json','rubric.md','fixture-provenance.json']: shutil.copy2(SRC/name,RUN/name)
    shutil.copy2(BASE/'protocol.md',RUN/'protocol.md')
    cases = json.loads((SRC/'cases.json').read_text())
    # Reuse exact prior actor prompts, not grading criteria.
    common_source = ast.parse((SRC/'run.py').read_text())
    common = next(ast.literal_eval(n.value) for n in common_source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='COMMON' for t in n.targets))
    common = common.replace('正式 skill executor','Claude Code explicit skill executor') + '\n本次透過明示讀取原始 skill 執行；safe-mode 不提供該 skill 的原生 Skill 工具註冊，請直接讀 skill/engineering-research/SKILL.md 及它需要的 bundled Markdown。CLI 的安全模式與內建技能存在不代表此工程研究 plugin 已安裝。\n'
    obs = observations()
    mapping = []
    for i, case in enumerate(cases):
        arms = ['old','new'] if i % 2 == 0 else ['new','old']
        for j, arm in enumerate(arms):
            actor = chr(65 + 2*i + j)
            out = RUN / actor; out.mkdir(); work = out/'project'
            shutil.copytree(SRC/'fixture',work)
            source = BASE/'old-skill' if arm == 'old' else REPO/'loom-code/skills/engineering-research'
            dest = work/'skill/engineering-research'
            for p in source.rglob('*.md'):
                if p.name == 'README.md': continue
                q = dest/p.relative_to(source);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
            dump(work/'fixture-observations.json',obs)
            (out/'prompt.txt').write_text(actor_prompt(common,case['prompt']))
            dump(out/'before.json',filemap(work))
            mapping.append({'actor':actor,'case':case['id'],'arm':arm})
    dump(RUN/'arm-map.json',mapping)
    freeze = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'harness_sha256':sha(Path(__file__)),'protocol_sha256':sha(BASE/'protocol.md'),'cli_realpath':str(CLAUDE.resolve()),'cli_sha256':sha(CLAUDE),
              'requested_model':'claude-sonnet-5-5','requested_provider':'firstParty Anthropic via native account; no provider/API env inherited','effort':'medium',
              'timeout_seconds':300,'max_concurrency':2,'order':'case order, old/new lead counterbalanced; pair per case',
              'one_pair_per_case':'directional only; not a statistical rate estimate',
              'tool_adapter':ADAPTER,'environment_keys':ENV_KEYS,'arm_map_sha256':sha(RUN/'arm-map.json'),
              'criteria':{n:sha(RUN/n) for n in ['cases.json','rubric.md','fixture-provenance.json']},
              'actors':{m['actor']:{'before_sha256':sha(RUN/m['actor']/'before.json'),
                                  'prompt_sha256':sha(RUN/m['actor']/'prompt.txt'),
                                  'command':command(m['case'],'<frozen actor prompt>')} for m in mapping}}
    dump(RUN/'freeze.json',freeze)
    print(json.dumps({'prepared':str(RUN),'actors':len(mapping),'freeze_sha256':sha(RUN/'freeze.json'),'no_model_calls':True}))


def one(m):
    out = RUN/m['actor'];work=out/'project';require_unrun(out)
    dump(out/'started.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    before=json.loads((out/'before.json').read_text());prompt=(out/'prompt.txt').read_text();tick=time.monotonic()
    proc=subprocess.Popen(command(m['case'],prompt),cwd=work,env=environment(),text=True,
                          stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    stdout,stderr,timed=communicate(proc,'')
    events=sanitize(stdout)
    (out/'events.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
    (out/'stderr.txt').write_text(stderr)
    result=next((e for e in reversed(events) if e.get('type')=='result'),{})
    (out/'answer.txt').write_text(result.get('result','No final result; inspect trajectory.'))
    after=filemap(work);dump(out/'after.json',after)
    receipt={'actor':m['actor'],'case':m['case'],'requested_model':'claude-sonnet-5-5','requested_provider':'firstParty Anthropic','requested_effort':'medium',
             'exit_code':proc.returncode,'timeout':timed,'elapsed_seconds':round(time.monotonic()-tick,3),
             'result':{k:result.get(k) for k in ['is_error','terminal_reason','usage','modelUsage','total_cost_usd','permission_denials','duration_api_ms','num_turns']},
             **inventory_checks(m['case'],before,after)}
    dump(out/'receipt.json',receipt)
    print(json.dumps({k:receipt[k] for k in ['actor','case','exit_code','timeout','elapsed_seconds','protected_unchanged','case_boundary_satisfied']},ensure_ascii=False),flush=True)
    return receipt


def run():
    frozen=json.loads((RUN/'freeze.json').read_text())
    if frozen['harness_sha256'] != sha(Path(__file__)) or frozen['cli_sha256'] != sha(CLAUDE): raise RuntimeError('harness/CLI drift')
    if frozen['arm_map_sha256'] != sha(RUN/'arm-map.json'): raise RuntimeError('map drift')
    if frozen['protocol_sha256'] != sha(RUN/'protocol.md'): raise RuntimeError('protocol drift')
    if any(sha(RUN/n)!=digest for n,digest in frozen['criteria'].items()): raise RuntimeError('criteria drift')
    mapping=json.loads((RUN/'arm-map.json').read_text())
    for m in mapping:
        out=RUN/m['actor']; require_unrun(out); actor=frozen['actors'][m['actor']]
        if sha(out/'prompt.txt') != actor['prompt_sha256'] or sha(out/'before.json') != actor['before_sha256'] or filemap(out/'project') != json.loads((out/'before.json').read_text()): raise RuntimeError('actor input drift')
    receipts=[]
    # Pair members launch together; later cases cannot consume early-case outputs.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for start in range(0,len(mapping),2): receipts.extend(pool.map(one,mapping[start:start+2]))
    dump(RUN/'receipts.json',receipts)
    OUT.mkdir(parents=True,exist_ok=False)
    for name in ['freeze.json','arm-map.json','cases.json','rubric.md','fixture-provenance.json','protocol.md','receipts.json']:shutil.copy2(RUN/name,OUT/name)
    for m in mapping:
        out=RUN/m['actor'];dest=OUT/m['actor'];dest.mkdir()
        for name in ['prompt.txt','before.json','after.json','events.jsonl','answer.txt','receipt.json','stderr.txt']:shutil.copy2(out/name,dest/name)
        receipt=json.loads((out/'receipt.json').read_text())
        for rel in receipt['changed_files']+receipt['added_files']:
            p=out/'project'/rel
            if p.is_file() and p.suffix.lower() in ['.md','.json','.txt']:
                q=dest/'artifacts'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    dump(OUT/'evidence-integrity.json',{'hashes':filemap(OUT),'raw_root':str(RUN),'reasoning_content':'excluded','semantics':'ungraded; exit0 is not semantic pass','cost':'CLI list-price equivalent, not subscription bill'})
    print('Twelve fresh explicit executions complete; independent semantics not yet judged.')


if __name__ == '__main__':
    {'prepare':prepare,'run':run}[sys.argv[1]]()
