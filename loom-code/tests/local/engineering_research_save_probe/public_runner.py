"""Native public-only integration control. No model requests at import or prepare time."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

HERE=Path(__file__).resolve().parent
BASE=Path('/private/tmp/engineering-research-save-result-20261108')
PUBLIC=BASE/'public-control'
CLAUDE=Path('/Users/kouko/.local/bin/claude')
ENV_KEYS=('HOME','PATH','USER','LOGNAME','SHELL','TMPDIR','LANG','LC_ALL','SECURITYSESSIONID','__CF_USER_TEXT_ENCODING')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def filemap(root):return {p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file()}


def environment(source=None):
    source=os.environ if source is None else source
    return {**{k:source[k] for k in ENV_KEYS if k in source},'HOME':'/Users/kouko','PYTHONDONTWRITEBYTECODE':'1'}


def command(actor,prompt):
    return [str(CLAUDE),'--restricted','--setting-sources','','--strict-mcp-config','--mcp-config',str(actor/'mcp.json'),
      '--disable-slash-commands','--settings',str(PUBLIC/'isolated-settings.json'),'--no-session-persistence','--no-chrome',
      '--permission-prompts','none','--permission-mode','dontAsk','--tools','Read,Grep,Glob',
      '--allowedTools','Read,Grep,Glob,mcp__save_probe__save_record','--model','claude-sonnet-5-5','--effort','medium',
      '--output-format','stream-json','--verbose','-p',prompt]


def require_fresh(actor):
    if any((actor/n).exists() for n in ['started.json','receipt.json','events.jsonl','answer.txt']):
        raise RuntimeError('Refusing to overwrite public actor '+str(actor))


def communicate(proc,timeout):
    try:
        stdout,stderr=proc.communicate('',timeout=timeout)
        return stdout,stderr,False
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGTERM)
        try:stdout,stderr=proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL);stdout,stderr=proc.communicate()
        return stdout,stderr,True


def sanitize(stdout):
    result=[]
    for line in stdout.splitlines():
        try:e=json.loads(line)
        except ValueError:continue
        if not isinstance(e,dict):continue
        msg=e.get('message')
        if e.get('type')=='assistant' and isinstance(msg,dict) and isinstance(msg.get('content'),list):
            msg['content']=[b for b in msg['content'] if b.get('type') not in ('thinking','redacted_thinking')]
        result.append(e)
    return result


def execute(actor,case,timeout=300):
    require_fresh(actor);prompt=(actor/'prompt.txt').read_text();before=filemap(actor/'project')
    dump(actor/'started.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});tick=time.monotonic()
    proc=subprocess.Popen(command(actor,prompt),cwd=actor/'project',env=environment(),text=True,
      stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    stdout,stderr,timed=communicate(proc,timeout);events=sanitize(stdout)
    (actor/'events.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
    (actor/'stderr.txt').write_text(stderr)
    result=next((e for e in reversed(events) if e.get('type')=='result'),{})
    (actor/'answer.txt').write_text(result.get('result','No final result; inspect trajectory.'))
    after=filemap(actor/'project');dump(actor/'before.json',before);dump(actor/'after.json',after)
    receipt={'actor':actor.name,'case':case,'exit_code':proc.returncode,'timeout':timed,'elapsed_seconds':round(time.monotonic()-tick,3),
      'requested_provider':'first-party Anthropic native account; no provider env inherited','requested_model':'claude-sonnet-5-5','requested_effort':'medium',
      'result':{k:result.get(k) for k in ['is_error','terminal_reason','usage','modelUsage','total_cost_usd','permission_denials','num_turns']},
      'changed_files':[p for p in before if after.get(p)!=before[p]],'added_files':[p for p in after if p not in before],
      'deleted_files':[p for p in before if p not in after],'cost_scope':'CLI list-price equivalent, not subscription bill'}
    dump(actor/'receipt.json',receipt)
    print(json.dumps({k:receipt[k] for k in ['actor','case','exit_code','timeout','elapsed_seconds','changed_files','added_files']},ensure_ascii=False),flush=True)
    return receipt


def run_public():
    freeze=PUBLIC/'execution-freeze.json'
    if freeze.exists():raise RuntimeError('Refusing to refreeze public control')
    for mode in ['confirmation','full']:require_fresh(PUBLIC/mode)
    sources={p.name:sha(p) for p in [HERE/'experiment.py',HERE/'public_runner.py',HERE/'save_tool.py',HERE/'server.py']}
    inputs={mode:{'project':filemap(PUBLIC/mode/'project'),'configuration':{n:sha(PUBLIC/mode/n) for n in ['mcp.json','policy.json','prompt.txt']}} for mode in ['confirmation','full']}
    dump(freeze,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'public_data_only':True,'sources':sources,'inputs':inputs,
      'settings_sha256':sha(PUBLIC/'isolated-settings.json'),'cli_sha256':sha(CLAUDE),'cli_realpath':str(CLAUDE.resolve()),
      'model':'claude-sonnet-5-5','effort':'medium','provider':'first-party Anthropic','timeout_seconds':120,
      'environment_keys':sorted(environment()),'source_mode':'restricted with explicit scoped MCP; safe-mode omitted because it disables MCP',
      'native_customization_isolation':'must be evaluated from public result; not assumed'})
    receipts=[execute(PUBLIC/mode,'PUBLIC_SYNTHETIC',120) for mode in ['confirmation','full']]
    dump(PUBLIC/'receipts.json',receipts)
    dump(PUBLIC/'post-execution-integrity.json',{'sources_unchanged':all(sha(HERE/n)==h for n,h in sources.items()),
      'settings_unchanged':sha(PUBLIC/'isolated-settings.json')==json.loads(freeze.read_text())['settings_sha256'],
      'outside_public_sentinel':(PUBLIC/'outside-public.md').read_text(),'semantic_verdict':'not graded; root must inspect actual tools/canaries/results'})
