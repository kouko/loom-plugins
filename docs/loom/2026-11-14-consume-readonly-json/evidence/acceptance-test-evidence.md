# Checked CLI consumers — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at 3056014736016d39d1a8690cbe03d45fee86873e.

Clean copy: `/private/tmp/loom-consume-acceptance-3056014`, created with `git worktree add --detach ... 3056014736016d39d1a8690cbe03d45fee86873e`. The working source and installed plugin were preserved. README setup uses loom-python --repair; the real source launcher succeeded using its existing prepared cache, without installation, network, or plugin refresh. Candidate is 3.77.0; installed 3.76.0 was not changed. Independent witness did not implement the change.

## 1. 全部十六個子命令的一致性盤點與分批方向可核對，清楚區分首批已交付範圍、必要模式差異及尚未遷移的命令。

Registry AST yielded exactly 16 names; every exact command --help was executed (output below). Compared the inventory with registry/help: intents metadata, intent commit message, push hook/install/remove, delivery hook/result family, land cleanup/sweep, sync-trunk advisory, github-rules print-only, pr-floor summary, charter table/manifest and finalize writes remain distinct. Five existing JSON producers, only two checked station consumers; later read-only/CI then operation designs remain deferred.

## 2. 相容性檢查與審查人數判讀的正式流程採用已發布的 JSON 資料，能依明確欄位決定是否繼續及所需獨立審查人數，不依賴成功訊息的散文格式。

Executed both documented formal patterns through the real source launcher and checked script. Captured station lines show checked invocation and data interpretation. Real contract pass/block/usage; real target reviewer floor 2; synthetic repository real producer floor 1 after eligible branch baseline. No external model was dispatched; this tests the executable invocation and source station adoption, not an LLM's future instruction following.

## 3. 首批消費流程能在使用結果前驗證支援版本、命令、必要欄位、型別與退出碼／結果含義的一致性，容忍相容的額外欄位，拒絕不完整、矛盾或不可解析的結果，不把明確拒絕或結果未知當成成功。

Real producer returns passed 0, blocked 1, usage error 2. Separate fault-injection copy uses unchanged consumer with a replaced sibling checker executed through the real launcher. Compatible extra precision retained byte-for-byte; schema/type/command/request/exit/status, duplicate keys, NaN, trailing and truncated JSON rejected with empty stdout. Future positive reviewer floor accepted. Injected readiness 86 retained; actual 31-second sleeping child timed out at 30.07 seconds. The targeted entry tests additionally cover all required-field omissions, reviewer bool/invalid fields, and single execution boundary.

## 4. 既有文字呼叫、已發布 JSON 結果、判定與審查政策、授權、宿主信任及現有操作結果查證行為保持相容；首批驗證不引入寫入副作用。

Direct text/JSON contract pass/block/usage match checked data and exits; reviewer direct text/JSON both match checked floor 1. Source snapshot before/after real calls: 3924 files, no content changes (bytecode excluded). Diff from base over original producer package, launcher and hooks is empty, so authority, trust and operation reconciliation remain their existing mechanisms. No actual authorized write operation was performed. Focused tests: 19 passed in 15.18s. The automated package suite will run at finalize-review and block acceptance on failure; its future result is not claimed here.

## 5. help、流程說明與獨立 dogfood 證據符合首批實作，涵蓋正常、明確拒絕及格式／執行錯誤，揭露未驗證界線，不以盤點完成冒稱全體工具已遷移。

Executed exact help, -h, empty/unknown command, supplied --json, invalid requirement, missing reviewer operand, dirty/non-repository, cold --ready 86, injected stderr and timeout. Help and README/cli-results/station instructions agree. No retry, text fallback, write, host installation, paid CLI or external network was exercised. Structural checks cannot prove computational truth; installed host parity, LLM routing and efficiency are unverified.

## Fixture correction and limits

Initial synthetic fixture on main returned conservative floor 2 as expected. Adding origin/HEAD alone still returned 2 because local main pointed at current HEAD; this was fixture setup, not a product failure. Corrected only the synthetic repository: `git update-ref refs/heads/main HEAD~1` while on work. Then all three real calls returned floor 1:

```text
$ loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-example
exit=0
{"schema_version":1,"command":"reviewer-count","status":"passed","diagnostics":[],"notices":[],"error":null,"data":{"change_id":"2026-11-14-example","reviewer_floor":1}}
$ loom-python --ready reviewer-count 2026-11-14-example
exit=0; stdout=1; stderr empty
$ loom-python --ready reviewer-count 2026-11-14-example --json
exit=0; same JSON data; stderr empty
```

Focused test environment attempts retained: ordinary offline uv failed to create its existing-cache lock due to sandbox; system Python had no pytest. Authorized escalation reused the locked offline cache:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_checked_readonly.py loom-code/tests/test_preparation_json.py loom-code/tests/test_loom_python_runtime.py -q
```

```text
19 passed in 15.18s
```

No full suite was run by this witness. Package-tests is not skipped; finalize-review will run. No important-or-worse dismissed findings were supplied. All worktrees and prior evidence remain. No implementation or test repair was made.

## Execution programs (temporary, embedded for reproducibility)

Commands in output are rendered by joining argument lists; the programs below preserve exact whitespace arguments, cwd and environment. The second program was invoked with `python3 -c "import pathlib; exec(pathlib.Path('/private/tmp/accept-consume-more.py').read_text())"`.

```python
import subprocess, pathlib, os, json, shutil, hashlib
R=pathlib.Path('/private/tmp/loom-consume-acceptance-3056014'); L=R/'loom-code/scripts/loom-python'
log=[]
def run(args,cwd=R,env=None):
 p=subprocess.run(list(map(str,args)),cwd=cwd,env=env,text=True,capture_output=True)
 log.append('$ '+ ' '.join(map(str,args))+'\nexit='+str(p.returncode)+'\nstdout='+p.stdout+'\nstderr='+p.stderr)
 return p
def call(*a,**kw): return run([L,*a],**kw)
before=run(['git','status','--porcelain']).stdout
call('--repair','--script','checked_readonly.py','contract','--require','2.1')
for a in [('contract','--require','2.99'),('contract','--require','bad'),('contract',),('contract','--require','bad','--require',' 2.00 '),('reviewer-count','2026-11-14-consume-readonly-json'),('--help',),('-h',),(),('plan',),('contract','--json')]:
 call('--ready','--script','checked_readonly.py',*a)
for a in [('contract','--require','2.1'),('contract','--require','2.99'),('contract','--require','bad')]:
 for suffix in [(),('--json',)]:call('--ready',*a,*suffix)
env=dict(os.environ,XDG_CACHE_HOME='/private/tmp/loom-accept-cold-empty')
call('--ready','--script','checked_readonly.py','contract','--require','2.1',env=env)
# Synthetic repository data, real checker and launcher (no mocked producer).
S=pathlib.Path('/private/tmp/loom-accept-reviewer-fixture');S.mkdir(exist_ok=True)
run(['git','init','-q','-b','main'],cwd=S);run(['git','config','user.email','t@example.com'],cwd=S);run(['git','config','user.name','T'],cwd=S)
I=S/'docs/loom/intent/2026-11-14-example.md';I.parent.mkdir(parents=True,exist_ok=True)
I.write_text('# Example\noriginator: tester\nkind: engineering\nneeds-design: no — fixture\nstatus: confirmed 2026-11-14\n\n## Problem\nFixture.\n\n## Proposed outcome\nFixture.\n\n## Acceptance\n1. Fixture passes.\n\n## Constraints\n- none\n\n## Out of scope\n- none\n\n## Open questions\n- none\n')
run(['git','add','.'],cwd=S);run(['git','commit','-q','-m','test fixture'],cwd=S)
call('--ready','--script','checked_readonly.py','reviewer-count','2026-11-14-example',cwd=S)
(S/'guide.md').write_text('Usage clarification.\n');run(['git','add','.'],cwd=S);run(['git','commit','-q','-m','clarify usage'],cwd=S)
call('--ready','--script','checked_readonly.py','reviewer-count','2026-11-14-example',cwd=S)
(S/'guide.md').write_text('Dirty.\n');call('--ready','--script','checked_readonly.py','reviewer-count','2026-11-14-example',cwd=S)
call('--ready','--script','checked_readonly.py','reviewer-count','2026-11-14-example',cwd='/private/tmp')
# Fault injection: unchanged consumer copy, replace only its sibling producer.
F=pathlib.Path('/private/tmp/loom-accept-injected-producer');F.mkdir(exist_ok=True)
shutil.copyfile(R/'loom-code/scripts/checked_readonly.py',F/'checked_readonly.py')
base=dict(schema_version=1,command='contract',status='passed',diagnostics=[],notices=[],error=None,data=dict(contract_version='2.3.1',required_version='2.1',compatible=True))
cases=[]
def add(name,v=None,raw=None,code=0,stderr=''): cases.append((name,json.dumps(base if v is None else v) if raw is None else raw,code,stderr))
add('extra precision preserved',raw=json.dumps(base)[:-1]+', "extra": {"precise": 1.234567890123456789, "huge": 1e999}}')
for name,key,val in [('schema','schema_version',True),('command','command','plan'),('status','status','unknown'),('missing data','data',None),('notice type','notices',[1]),('contradiction','diagnostics',[{'rule_id':'x','message':'blocked'}])]:
 v=dict(base);v[key]=val;add(name,v)
v=json.loads(json.dumps(base));v['data']['required_version']='2.0';add('request mismatch',v)
for name,raw in [('duplicate','{"schema_version":1,"schema_version":1}'),('nested duplicate',json.dumps(base)[:-1]+',"extra":{"x":1,"x":2}}'),('NaN',json.dumps(base)[:-1]+',"extra":NaN}'),('trailing',json.dumps(base)+' {}'),('truncated','{')]:add(name,raw=raw)
add('exit mismatch',code=1);add('unexpected stderr',stderr='unexpected');add('runtime 86',raw='',code=86,stderr='runtime unavailable')
v=dict(base,command='reviewer-count',data={'change_id':'odd id','reviewer_floor':3});cases.append(('future floor',json.dumps(v),0,''))
for name,raw,code,err in cases:
 log.append('INJECTED OBSERVATION: '+name)
 (F/'loom_checker.py').write_text('import sys\nsys.stdout.write('+repr(raw)+')\nsys.stderr.write('+repr(err)+')\nsys.exit('+str(code)+')\n')
 a=['reviewer-count','odd id'] if name=='future floor' else ['contract','--require','2.1']
 call('--ready','--script',F/'checked_readonly.py',*a)
log.append('CLEAN SOURCE FINAL STATUS\n'+run(['git','status','--porcelain']).stdout)
pathlib.Path('/private/tmp/accept-consume-output.md').write_text('\n\n'.join(log))

```

```python
exec(pathlib.Path('/private/tmp/accept-consume.py').read_text().split('before=run')[0])
import ast,time
S=pathlib.Path('/private/tmp/loom-accept-reviewer-fixture')
run(['git','restore','guide.md'],cwd=S)
base=run(['git','rev-parse','HEAD~1'],cwd=S).stdout.strip()
run(['git','update-ref','refs/remotes/origin/trunk',base],cwd=S)
run(['git','symbolic-ref','refs/remotes/origin/HEAD','refs/remotes/origin/trunk'],cwd=S)
run(['git','checkout','-q','-b','work'],cwd=S)
for suffix in [(),('--json',)]:call('--ready','reviewer-count','2026-11-14-example',*suffix,cwd=S)
call('--ready','--script','checked_readonly.py','reviewer-count','2026-11-14-example',cwd=S)
call('--ready','--script','checked_readonly.py','reviewer-count',cwd=S)
tree=ast.parse((R/'loom-code/scripts/loom_checker.py').read_text()); names=[]
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='COMMANDS' for t in n.targets):names=[x.value for x in n.value.keys]
log.append('Registry inventory ('+str(len(names))+'): '+', '.join(names))
for name in names:call('--ready',name,'--help')
for p in ['loom-code/skills/write-plan/SKILL.md','loom-code/skills/write-plan/references/codex-first-contact.md','loom-code/skills/closing-review/SKILL.md']:
 lines=(R/p).read_text().splitlines();log.append(p+'\n'+'\n'.join(str(i+1)+': '+v for i,v in enumerate(lines) if any(s in v for s in ['checked_readonly','compatible','reviewer_floor','contract.requires','invalid','recompute'])))
F=pathlib.Path('/private/tmp/loom-accept-injected-producer')
(F/'loom_checker.py').write_text('import time\ntime.sleep(31)\n')
start=time.monotonic();call('--ready','--script',F/'checked_readonly.py','contract','--require','2.1');log.append('Timeout measured seconds: '+str(round(time.monotonic()-start,2)))
def snapshot():
 return {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts}
b=snapshot();call('--ready','--script','checked_readonly.py','contract','--require','2.1');call('--ready','--script','checked_readonly.py','reviewer-count','2026-11-14-consume-readonly-json');a=snapshot();log.append('Read-only file snapshot: before='+str(len(b))+' after='+str(len(a))+' changed='+str([k for k in set(a)|set(b) if a.get(k)!=b.get(k)]))
log.append(run(['git','diff','6fe61c99ea1981f238f8a8550abbd1e36e93cfab','3056014','--','loom-code/scripts/loom_checker.py','loom-code/scripts/loom_checker','loom-code/hooks','loom-code/scripts/loom-python']).stdout or 'Producer, launcher, hooks, policy and operation reconciliation diff: empty.')
pathlib.Path('/private/tmp/accept-consume-more-output.md').write_text('\n\n'.join(log))

```

## Captured actual output

```text
$ git status --porcelain
exit=0
stdout=
stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --repair --script checked_readonly.py contract --require 2.1
exit=0
stdout={"schema_version": 1, "command": "contract", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": "2.1", "compatible": true}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py contract --require 2.99
exit=1
stdout={"schema_version": 1, "command": "contract", "status": "blocked", "diagnostics": [{"rule_id": "contract.requires", "message": "this repo ships loom contract 2.3.1, but >=2.99 is required \u2014 \u8acb\u66f4\u65b0 loom-code\u3002"}], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": "2.99", "compatible": false}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py contract --require bad
exit=2
stdout={"schema_version": 1, "command": "contract", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "`--require bad` is not <major>.<minor>."}, "data": {"contract_version": null, "required_version": null, "compatible": null}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py contract
exit=2
stdout={"schema_version": 1, "command": "contract", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "contract needs `--require <major>.<minor>`."}, "data": {"contract_version": null, "required_version": null, "compatible": null}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py contract --require bad --require  2.00 
exit=0
stdout={"schema_version": 1, "command": "contract", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": " 2.00 ", "compatible": true}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-consume-readonly-json
exit=0
stdout={"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"change_id": "2026-11-14-consume-readonly-json", "reviewer_floor": 2}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py --help
exit=0
stdout=checked-readonly — validate read-only checker JSON
Usage: loom-python --repair --script checked_readonly.py contract --require <version>
       loom-python --ready --script checked_readonly.py reviewer-count <change-id>
Do not supply --json; this consumer adds it. Exact --help or -h runs no checker.
Validates schema version, command, required fields/types, request identity and
exit/status agreement; preserves compatible extra fields. Passed/blocked/error
JSON retains exits 0/1/2. Invalid results exit 2 with no stdout; startup exit 86
is preserved. The checker subprocess has a configured 30-second timeout.
The outer launcher owns readiness and repair. No writes, retries, text fallback
or change to checker policy, authorization or host trust is introduced.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py -h
exit=0
stdout=checked-readonly — validate read-only checker JSON
Usage: loom-python --repair --script checked_readonly.py contract --require <version>
       loom-python --ready --script checked_readonly.py reviewer-count <change-id>
Do not supply --json; this consumer adds it. Exact --help or -h runs no checker.
Validates schema version, command, required fields/types, request identity and
exit/status agreement; preserves compatible extra fields. Passed/blocked/error
JSON retains exits 0/1/2. Invalid results exit 2 with no stdout; startup exit 86
is preserved. The checker subprocess has a configured 30-second timeout.
The outer launcher owns readiness and repair. No writes, retries, text fallback
or change to checker policy, authorization or host trust is introduced.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py
exit=2
stdout=
stderr=checked-readonly: choose contract or reviewer-count; use --help


$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py plan
exit=2
stdout=
stderr=checked-readonly: choose contract or reviewer-count; use --help


$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py contract --json
exit=2
stdout=
stderr=checked-readonly: omit --json; the consumer adds it


$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready contract --require 2.1
exit=0
stdout=contract 2.3.1 satisfies requires-contract >=2.1

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready contract --require 2.1 --json
exit=0
stdout={"schema_version": 1, "command": "contract", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": "2.1", "compatible": true}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready contract --require 2.99
exit=1
stdout=
stderr=BLOCK contract.requires: this repo ships loom contract 2.3.1, but >=2.99 is required — 請更新 loom-code。


$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready contract --require 2.99 --json
exit=1
stdout={"schema_version": 1, "command": "contract", "status": "blocked", "diagnostics": [{"rule_id": "contract.requires", "message": "this repo ships loom contract 2.3.1, but >=2.99 is required \u2014 \u8acb\u66f4\u65b0 loom-code\u3002"}], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": "2.99", "compatible": false}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready contract --require bad
exit=2
stdout=
stderr=`--require bad` is not <major>.<minor>.


$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready contract --require bad --json
exit=2
stdout={"schema_version": 1, "command": "contract", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "`--require bad` is not <major>.<minor>."}, "data": {"contract_version": null, "required_version": null, "compatible": null}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py contract --require 2.1
exit=86
stdout=
stderr=loom-python: checker runtime is missing or invalid; run loom-python --repair with the same arguments in an agent station.


$ git init -q -b main
exit=0
stdout=
stderr=

$ git config user.email t@example.com
exit=0
stdout=
stderr=

$ git config user.name T
exit=0
stdout=
stderr=

$ git add .
exit=0
stdout=
stderr=

$ git commit -q -m test fixture
exit=0
stdout=
stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-example
exit=0
stdout={"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"change_id": "2026-11-14-example", "reviewer_floor": 2}}

stderr=

$ git add .
exit=0
stdout=
stderr=

$ git commit -q -m clarify usage
exit=0
stdout=
stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-example
exit=0
stdout={"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"change_id": "2026-11-14-example", "reviewer_floor": 2}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-example
exit=2
stdout={"schema_version": 1, "command": "reviewer-count", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "reviewer-count needs a clean tree with completed functional content."}, "data": {"change_id": null, "reviewer_floor": null}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-example
exit=2
stdout={"schema_version": 1, "command": "reviewer-count", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "/private/tmp is not inside a git work tree."}, "data": {"change_id": null, "reviewer_floor": null}}

stderr=

INJECTED OBSERVATION: extra precision preserved

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=0
stdout={"schema_version": 1, "command": "contract", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": "2.1", "compatible": true}, "extra": {"precise": 1.234567890123456789, "huge": 1e999}}

stderr=

INJECTED OBSERVATION: schema

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: unsupported schema_version


INJECTED OBSERVATION: command

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: command mismatch


INJECTED OBSERVATION: status

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: invalid status


INJECTED OBSERVATION: missing data

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: invalid data


INJECTED OBSERVATION: notice type

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: invalid notices


INJECTED OBSERVATION: contradiction

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: contradictory diagnostics/error state


INJECTED OBSERVATION: request mismatch

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: required_version mismatch


INJECTED OBSERVATION: duplicate

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: duplicate JSON key


INJECTED OBSERVATION: nested duplicate

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: duplicate JSON key


INJECTED OBSERVATION: NaN

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: non-JSON numeric constant


INJECTED OBSERVATION: trailing

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: Extra data: line 1 column 201 (char 200)


INJECTED OBSERVATION: truncated

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)


INJECTED OBSERVATION: exit mismatch

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: exit/status mismatch


INJECTED OBSERVATION: unexpected stderr

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: unexpected checker stderr


INJECTED OBSERVATION: runtime 86

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=86
stdout=
stderr=checked-readonly: runtime unavailable


INJECTED OBSERVATION: future floor

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py reviewer-count odd id
exit=0
stdout={"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"change_id": "odd id", "reviewer_floor": 3}}

stderr=

$ git status --porcelain
exit=0
stdout=
stderr=

CLEAN SOURCE FINAL STATUS

```

## Supplemental actual output

```text
$ git restore guide.md
exit=0
stdout=
stderr=

$ git rev-parse HEAD~1
exit=0
stdout=60f23f1a1fd9d2caae93d4bd62ee9c2145795b1f

stderr=

$ git update-ref refs/remotes/origin/trunk 60f23f1a1fd9d2caae93d4bd62ee9c2145795b1f
exit=0
stdout=
stderr=

$ git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/trunk
exit=0
stdout=
stderr=

$ git checkout -q -b work
exit=0
stdout=
stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready reviewer-count 2026-11-14-example
exit=0
stdout=2

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready reviewer-count 2026-11-14-example --json
exit=0
stdout={"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"change_id": "2026-11-14-example", "reviewer_floor": 2}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-example
exit=0
stdout={"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"change_id": "2026-11-14-example", "reviewer_floor": 2}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count
exit=2
stdout={"schema_version": 1, "command": "reviewer-count", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "reviewer-count needs one change-id."}, "data": {"change_id": null, "reviewer_floor": null}}

stderr=

Registry inventory (16): intent, intents, intake, push, publish, delivery, land, sync-trunk, github-rules, pr-floor, standing, contract, charter, plan, reviewer-count, finalize-review

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready intent --help
exit=0
stdout=intent — check one intent's implemented rules
Usage: intent <path> [--commit-msg <file>]
Supply readable relative-to-working-directory or absolute paths. Repository
context is resolved from the intent; the bundled manifest defines its schema.
--commit-msg supplies design-reasoning evidence; it does not create a commit.
Checks cover schema, map existence, product identifiers, design reasoning and
applicable touched-interface/kind rules. Advisory stdout may precede a blocker;
success may have empty stdout.
Conditional interface recomputation needs a resolvable branch base; run on a
change branch rather than trunk and resolve missing trunk metadata as directed.
Exit 0 means these checks passed, Exit 1 reports
BLOCK diagnostics on stderr, Exit 2 means arguments, files or internal failure.
Reads only; it neither creates nor confirms intent or authorizes delivery.
Correct the reported source artifact or path through its owning workflow and retry.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready intents --help
exit=0
stdout=intents — inspect locally derived intent delivery states
Usage: intents [<change-id>] [--remote <name>] [--metadata]
Run in the repository. The remote defaults to origin and must be a safe literal.
Identifiers contain letters, digits, dots, underscores and hyphens; a selected
ID needs its canonical intent file. --metadata requires one ID.
Without an ID, lists active/indeterminate confirmed intents and may print nothing.
With an ID, reports its state. Tab-separated rows start with ID and state;
named active rows add detail, and indeterminate rows add detail plus refresh
advice. Delivered --metadata rows append available commit/pr/committed_at
key=value fields (pr may be absent; dates are committer, not merge dates).
Other rows may contain only two fields; there is no fixed three-column shape.
Exit 0 is a local-ref observation, not live freshness proof. Indeterminate gives
exit 1 and refresh advice; Exit 2 means invocation or internal error on stderr.
Reads local Git only, never fetches. Refresh the selected remote-default ref
explicitly when needed, then retry; this does not perform delivery.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready intake --help
exit=0
stdout=intake — check the selected station's current prerequisites
Usage: intake <write-spec|write-plan> <change-id> [--json]
Run inside the selected repository. Supply a change-id, not a file path;
accepted identifiers contain only letters, digits, dots, underscores and
hyphens. Canonical artifacts are resolved through the bundled contract.

Text results: exit 0 means the applicable prerequisites passed for this snapshot;
it does not perform the station, authorize publication or verify the change.
Conditional interface-surfaces (...) information may appear on stdout for
engineering intents or applicable needs-design=yes write-plan intake.
That information is advisory and may precede a later BLOCK; it is not a
success result. Other intake paths have no stdout payload.

Exit 1 reports BLOCK <rule>: <reason> on stderr. Supply or correct authentic
required artifacts through their owning workflow, then rerun. Exit 2 means
invalid station/change-id/arguments or an internal failure; correct the
invocation or repository/environment from the diagnostic. These checks are
read-only and synchronous; no previous pass waives the next check.
Station and prerequisite guidance: <loom-code>/skills/write-plan/SKILL.md.
The intent needs a real confirmed date and active delivery state. A closed or
delivered intent requires a new intent; indeterminate delivery needs refreshed
remote-default evidence. Conditional interface recomputation needs a resolvable
branch base on a change branch rather than trunk.
Optional JSON: append --json as the final argument only. Exact --help/-h
remains text; help combined with --json is checked as an ordinary invocation.
Duplicate selectors are usage errors. Earlier --json tokens without a final
selector retain their existing operand meaning; ./--json names a literal file.

JSON stdout is one object plus newline; checker stderr is empty. Fields:
schema_version: 1; command: plan|intake; status: passed|blocked|error;
diagnostics: ordered [{rule_id, message}]; notices: ordered strings;
error: null or {kind: usage|internal, message}. Empty arrays are [], not null.
Exit 0 means passed, 1 blocked, 2 error. Blocked includes rule diagnostics;
error has empty diagnostics. Notices may precede a blocker or internal error
and never imply success. Status covers only this invocation's checks, not
workflow completion or authority. Do not depend on key order or message prose.
Launcher/startup failures, termination and broken pipes are outside this
in-process result guarantee. Read the actual process result; do not retry
automatically. Without --json, existing text streams and exits are unchanged.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready push --help
exit=0
stdout=push — provide host-hook feedback or install native branch protection
Usage: push --hook
       push --install-git-hooks
       push --remove-git-hooks
Only --hook reads PreToolUse JSON from stdin; invalid ordinary calls do not.
The host matcher handles command text beginning with literal git commit, git
merge or git push while the payload cwd is on main/master, with refusal exit 2
unless repository-local loom.protectMain=false explicitly allows those commands.
This opt-out affects the host hook, not the separate native hooks below.
Malformed/missing payload also exits 2. Publication reminders may emit a host
JSON systemMessage on stdout and a diagnostic on stderr; reminder failures and
unexpected top-level hook exceptions allow exit 0. It performs no publication.

Native modes are explicit repository configuration operations. They read and
refuse a core.hooksPath override or unreadable setting without changing it.
Install validates local and live origin default metadata; it may create the
Git hooks directory and writes three owned hooks: pre-commit, pre-merge-commit,
pre-push. The shared Git common directory's hooks affect all worktrees.
Remove deletes only those owned files. Foreign/edited hooks and
symlinked locations are refused; preserve them and arrange hook-owner integration.
Native success prints installed/removed on stdout, exit 0. Caught failures
print loom: diagnostics on stderr, exit 2, without BLOCK. Inspect origin and
repair default metadata as directed before retry. Native hooks protect main,
master and the origin default branch, but are ordinary Git safeguards, not a
security boundary or proof of remote branch protection. Help grants no consent.
Global options before the Git verb, wrappers and later compound commands can
evade the host matcher. Native hooks do not intercept fast-forward merges or
reset/rebase; Git options that skip hooks can bypass applicable native checks.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready publish --help
exit=0
stdout=publish — publish an authorized branch and observe required CI
Usage: publish --intent <absolute-intent-path> --title <text> --body-file <absolute-body-path>
Legacy: publish --confirm-authorized --title <text> --body-file <absolute-body-path>

Publication may perform a remote write (push and create/update a Ready PR).
--intent must name this change's canonical, committed, confirmed intent with
an existing valid automatic-publication authorization that remains unrevoked.
The legacy --confirm-authorized argument records an actual explicit user
publication decision; it is not a way to supply missing consent. If neither
authorization exists, stop and obtain that decision. Help grants no authority.
Observation grants neither publication nor merge authorization.

--title is checked here only for nonblank text; title policy remains workflow guidance.
--body-file must be an absolute path to a readable UTF-8 Markdown file.
Prepare the body from the confirmed intent, current diff, review and actual
verification evidence. Include each of these nine headings exactly once,
in this order, with no other level-two headings. Each needs substantive visible
content: at least eight alphanumeric characters, beyond a single ASCII token
or template placeholder (Follow-ups may say None):
## Context
## Intended outcome
## Scope
## Decisions
## Implementation
## Behaviour change
## Verification
## Risks and rollback
## Follow-ups

Under Verification include Verification status: <computed status>.
The checker reports valid, absent or stale (<reason>); if refused, copy the
reported corrected Verification status: line into the body without inventing
a stronger status. Disclose actual instructed skips and missing evidence.
When recorded, include Adversarial outcome: no program — <recorded reason>.
Detailed body, skipped-step and risk requirements: <loom-code>/skills/ship/SKILL.md.
The checker requires a safe symbolic branch, one literal supported GitHub origin
without redirect overrides, known nondiverged remote ancestry and unchanged
HEAD/origin identity between operations. The PR base is the server default
branch. Correct named conditions, preserving work. Use trusted git/gh and
committed selected content; an existing attestation must be committed.
A temporary body snapshot is removed on return. The nonforce push can set
upstream tracking; remote operations are not rolled back on later failure.

Results: exit 0 completes publication and its required-check observation;
exit 1 means blocked or unconfirmed; exit 2 means invocation or authorization
errors, or internal failures. Read the diagnostic to determine the next action;
the exit code alone is not a reason to retry.
Verification output or a PR URL alone is not completion. Stderr progress is
advisory and can also contain errors; while CI is pending keep observing the
same process. Inspect the final exit and evidence. Exit 0 with
"No required checks registered" means no checks registered, not tests passed.
An observation failure may follow a successful remote write. Before considering
another publish, run delivery --goal published --json to observe existing
state and follow its diagnostic; do not blindly repeat a write or switch routes.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready delivery --help
exit=0
stdout=delivery — observe the selected delivery goal without writes
Usage: delivery [--goal local|published|merged] [--intent <path>] [--json]
Run inside the selected repository on its identified feature branch.
--goal defaults to published. local checks that attributable paths are committed;
it does not check finalization, attestation or verification. published checks the
matching Ready PR and required CI; merged checks merged delivery evidence.
--intent optionally identifies the change's canonical committed intent (a
relative or absolute path); it does not create or grant authorization.
Local observation does not claim publication. Observation never authorizes
publication or merge, and does not perform either action.

--json emits the existing object on stdout:
state: observed delivery condition; reason: why it was classified that way;
next: suggested next action, subject to existing authorization;
evidence: observations supporting the result; complete: whether the goal is met.
A JSON object by itself, especially complete: false, is not proof of delivery.
Use state, reason, next and evidence together with the process exit status.
Exit 0 means the selected goal was achieved; exit 1 means incomplete or
unconfirmed; exit 2 means invocation/internal error. State values are local,
uncommitted, unpublished, missing_pr, mismatched_pr, pending, failed, cancelled,
action_required, published, merged and unconfirmed. Pending means wait and
observe again; other incomplete states require the stated next action.
Unconfirmed means evidence is unavailable, not success. Correct errors using the
diagnostic. Re-observation grants no permission to retry a remote write.
Stderr progress is advisory and can also contain errors; inspect final results.
More workflow guidance: <loom-code>/skills/ship/SKILL.md.
Hook forms: delivery --hook; delivery --hook --host claude|codex.
Hook mode consumes host stdin and emits host-specific feedback with its own
exit semantics; it is separate from ordinary --json. Do not mix hook forms
with observation options. Duplicate options are invalid. Malformed ordinary
invocations may report text on stderr even when --json was supplied.
Published/merged observation needs trusted git/gh from supported host install
locations, a literal GitHub origin, authenticated gh and network read access;
missing prerequisites can yield unconfirmed/exit 1. Published completion with
"No required checks registered" does not mean tests passed.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready land --help
exit=0
stdout=land — merge an accepted PR or clean up merged changes
Usage: land --accepted-by <name>
       land --cleanup <branch>
       land --sweep [--confirm <token>]
Choose exactly one form; --confirm applies only to sweep. Run in the repository
with trusted git/gh, eligible change branch/PR and live evidence/checks. A real
maintainer acceptance must already exist; the name or help supplies no consent.
The accepted name must match the committed intent originator or automatic
publication authorizer; matching a name does not establish actual consent.
Exactly one open PR against the default branch must match HEAD, and its live
body must satisfy the nine-heading validator. Land polls all registered checks,
including non-required checks, with at most 360 pending 10-second waits; network
calls and other stages add elapsed time. Failed/cancelled/action-required checks
refuse the merge. Absent/stale local verification is disclosed after merge,
not a gate that prevents it; no registered checks is not proof of testing.
See publish --help for the body heading order and content requirements.
The accepted form may squash merge remotely, verify, sync trunk, then delete
the change worktree and local/remote branch. Cleanup targets a named merged
change. Sweep computes candidates and a confirmation token; even without a
token it fetches/prunes refs. A matching revalidated token enables deletion.
Do not run cleanup when worktree preservation was requested.
Exit 0 can follow successful merge/cleanup even when best-effort trunk sync
was skipped or failed and stdout says "trunk not updated". Read the trunk
result; preserve work before independently resolving local trunk conditions.
Named cleanup never syncs trunk. Sweep listing also returns exit 0. Exit 1 reports
refusal or failed stage with BLOCK stderr, Exit 2 reports usage/internal errors.
Progress/results appear on stdout. Merge can succeed before verification or
cleanup fails: inspect remote merge and preserved work before corrective action;
use cleanup for an already merged change instead of blindly repeating a merge.
Dirty work and divergent local trunk are preserved/refused, not force-discarded.
If cleanup removes the invoking worktree, follow the printed next: cd command
to leave the removed working directory.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready sync-trunk --help
exit=0
stdout=sync-trunk — bring a clean change branch onto fetched trunk
Usage: sync-trunk
Run on a clean attached change branch, not trunk, with trusted Git and resolvable
trunk metadata. Preserve and commit work before resolving a dirty-tree refusal.
Fetches origin, then may rebase safe unpublished commits or merge trunk. Refuses
preflight conflicts/collisions; abort/rollback is attempted after mutation failure,
not guaranteed. Results appear on stdout; WARN/BLOCK diagnostics on stderr.
Exit 0 includes fetch WARN with no sync, already-current and completed sync.
Exit 1 means BLOCK review.sync; Exit 2 means arguments/internal error. Read the
warning before assuming synchronization. Resolve origin/network or conflicts
through normal Build and retry. Changed content needs full tests/probes again;
rebased commit identities require updating pinned references before review.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready github-rules --help
exit=0
stdout=github-rules — inspect GitHub trunk protection as advisory information
Usage: github-rules [--print-setup]
Run in the repository with origin metadata and authenticated gh read access.
Uses network reads to report present, absent or unconfirmed rules on stdout.
It first requires the PR-floor workflow template on trunk; "template not on"
instructions can return before inspecting any rules. Setup text may also appear
without --print-setup when missing rules are found.
Exit 0 includes unavailable/unconfirmed protection; it does not prove protection
or verification. Exit 2 means invalid arguments or unexpected internal failure
on stderr. Restore origin, authentication/network and read access, then rerun.
--print-setup prints a setup command when prerequisites permit, without executing
it. It never changes GitHub rules. Running printed setup is a separate mutation
requiring its own authorization; help grants none.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready pr-floor --help
exit=0
stdout=pr-floor — validate a PR body and disclose verification in CI
Usage: pr-floor --body-file <file> --base <sha> --head <sha> [--branch <name>]
Supply unique paired flags, a readable body file (relative to the working
directory or absolute), required base/head Git evidence and optional branch.
Run in the repository. Emits CI error/notice annotations on stdout. Body
structure failures also report BLOCK ci.pr-floor on stderr, exit 1. Exit 0
means the body passed; recomputed verification may still be stale or absent.
Exit 2 means invocation, unreadable file or internal failure. Correct named
headings or Git context; never fabricate stronger verification status.
Can append a verification line to GITHUB_STEP_SUMMARY when set, so it is not
strictly read-only. It runs no PR-controlled commands, tests or reviews and
does not authorize publication or merge.
See publish --help for the body heading order and content requirements.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready standing --help
exit=0
stdout=standing — check applicable standing-document policy for one intent
Usage: standing <path-to-intent>
Supply one readable relative-to-working-directory or absolute intent path;
repository context is resolved from that file. Checks existence of PRINCIPLES.md,
DESIGN.md and root ARCHITECTURE.md; reads PRINCIPLES.md content for product
intents and KICKOFF-DEFAULTS.md standing/second-vendor policy records. Principles
and design discovery checks root first, then docs/loom; architecture is root-only.
Warnings on stderr can coexist with passing checks and empty stdout. Exit 0
means implemented policy checks passed, not semantic certification of documents.
Exit 1 reports BLOCK diagnostics for second-vendor/product-principles policy;
Exit 2 means missing file, invalid arguments or internal failure. Correct the
authentic policy/document record through its owning workflow, then rerun.
Read-only; does not ratify documents or perform review.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready contract --help
exit=0
stdout=contract — check compatibility with the bundled contract manifest
Usage: contract --require <major.minor> [--json]
Supply a numeric major.minor requirement. Reads the manifest in effect; a
matching major and sufficiently high minor pass. Exit 0 prints current and
required versions on stdout; Exit 1 reports BLOCK contract.requires on stderr;
Exit 2 means malformed/missing arguments or internal failure. Follow the
diagnostic: an older major requirement needs the consuming plugin's
requires-contract updated to a supported major; update loom-code when a newer
major/minor is required. Do not lower a requirement just to pass. Then retry.
Read-only: this does not check plugin release version, provision
runtime, run station prerequisites or authorize a later operation.
JSON data: {contract_version: string|null, required_version: string|null,
compatible: boolean|null}. Passed/blocked provide the stripped manifest version,
the final supplied requirement (last --require wins), and true/false respectively.
Errors set all data values to null. Existing numeric matching is unchanged.
Optional JSON: append --json as the final argument only. Exact --help/-h
remains text; mixed help and final --json is a usage error. Duplicate selectors
are usage errors before domain work. Without a final selector, earlier tokens
retain their existing operand meaning.
JSON stdout is one object plus newline; checker stderr is empty. Fields:
schema_version: 1; command: contract|reviewer-count; status: passed|blocked|error;
diagnostics: ordered [{rule_id, message}]; notices: ordered strings;
error: null or {kind: usage|internal, message}; data: the command object above.
Exit 0 means passed with empty diagnostics and null error; Exit 1 means blocked
with rule diagnostics and null error; Exit 2 means error with empty diagnostics.
Empty arrays are []. Use keys and types, not key order or message prose.
Missing repositories and dirty trees are usage errors. Neither mode writes,
installs runtime, dispatches reviewers, requests authorization or retries.
Correct inputs or repository conditions before deliberately rerunning.
The guarantee begins in the loaded checker: launcher/import failures, unavailable
runtime (--ready exit 86), termination and broken pipes remain outside it.
Inspect process exit and parseability before consuming JSON. Text is unchanged
without --json; these observations do not grant authority or prove completion.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready charter --help
exit=0
stdout=charter — render and validate artifact charter rows
Usage: charter [--manifest <path>]
Defaults to the contract manifest in effect. An override is a readable YAML
path, relative to the working directory or absolute. Repeated --manifest uses
the last path. No repository mutation occurs.
Prints a Markdown table on stdout in manifest artifact order, including an
empty table for missing/empty artifacts. Exit 0 means implemented row checks
passed; Exit 1 reports BLOCK contract.charter-complete on stderr. A table can
coexist with failure and is not an approval. Exit 2 means file, arguments or
internal failure. Correct the reported manifest charter fields and retry.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready plan --help
exit=0
stdout=plan — check the implemented field caps on one named file
Usage: plan <path-to-plan.md> [--json]
Supply a readable file path, relative to the working directory or absolute;
this command does not resolve a change-id or select a canonical plan.

The check applies field caps only when the file has a charter: frontmatter
key. Charter 1.1 or later also requires a valid Simplicity check record.
A file without that key, including an empty file, may pass. Passing does not
approve the plan, prove its requirements are complete or verify the change.

Text results: exit 0 has no success payload on stdout; the implemented checks on
the named file passed. Exit 1 reports BLOCK plan.field-caps on stderr;
correct the reported field and rerun. Exit 2 means a missing/unreadable file,
invalid invocation or internal failure; correct the path, access or invocation
from the diagnostic. No artifact is rewritten and no later station runs.
Planning guidance: <loom-code>/skills/write-plan/SKILL.md.
Optional JSON: append --json as the final argument only. Exact --help/-h
remains text; help combined with --json is checked as an ordinary invocation.
Duplicate selectors are usage errors. Earlier --json tokens without a final
selector retain their existing operand meaning; ./--json names a literal file.

JSON stdout is one object plus newline; checker stderr is empty. Fields:
schema_version: 1; command: plan|intake; status: passed|blocked|error;
diagnostics: ordered [{rule_id, message}]; notices: ordered strings;
error: null or {kind: usage|internal, message}. Empty arrays are [], not null.
Exit 0 means passed, 1 blocked, 2 error. Blocked includes rule diagnostics;
error has empty diagnostics. Notices may precede a blocker or internal error
and never imply success. Status covers only this invocation's checks, not
workflow completion or authority. Do not depend on key order or message prose.
Launcher/startup failures, termination and broken pipes are outside this
in-process result guarantee. Read the actual process result; do not retry
automatically. Without --json, existing text streams and exits are unchanged.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready reviewer-count --help
exit=0
stdout=reviewer-count — compute the required independent reviewer floor
Usage: reviewer-count <change-id> [--json]
Run inside the selected repository with a clean tree and committed functional
content. Supply one nonblank change-id operand. Preserve work and finish and
commit the change before requesting the floor; do not discard files to pass.

Results: exit 0 prints the integer floor and newline on stdout. Obtain that
many independent reviewers; the number is not a verdict or proof of review,
acceptance, finalization or completed verification. The policy conservatively
requires two when it cannot classify the complete committed delta.
Exit 2 means missing/extra operands, a dirty tree or an internal failure;
use the diagnostic to correct the invocation or repository condition, then
rerun. This read-only command neither dispatches reviewers nor writes evidence.
Review guidance: <loom-code>/skills/closing-review/SKILL.md.
JSON data: {change_id: string|null, reviewer_floor: integer|null}. Passed
provides the unchanged operand and floor; errors set both values to null.
There is no blocked result for this command. Two can also follow ordinary
policy or outside-review selection; it does not prove complete classification.
Optional JSON: append --json as the final argument only. Exact --help/-h
remains text; mixed help and final --json is a usage error. Duplicate selectors
are usage errors before domain work. Without a final selector, earlier tokens
retain their existing operand meaning.
JSON stdout is one object plus newline; checker stderr is empty. Fields:
schema_version: 1; command: contract|reviewer-count; status: passed|blocked|error;
diagnostics: ordered [{rule_id, message}]; notices: ordered strings;
error: null or {kind: usage|internal, message}; data: the command object above.
Exit 0 means passed with empty diagnostics and null error; Exit 1 means blocked
with rule diagnostics and null error; Exit 2 means error with empty diagnostics.
Empty arrays are []. Use keys and types, not key order or message prose.
Missing repositories and dirty trees are usage errors. Neither mode writes,
installs runtime, dispatches reviewers, requests authorization or retries.
Correct inputs or repository conditions before deliberately rerunning.
The guarantee begins in the loaded checker: launcher/import failures, unavailable
runtime (--ready exit 86), termination and broken pipes remain outside it.
Inspect process exit and parseability before consuming JSON. Text is unchanged
without --json; these observations do not grant authority or prove completion.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready finalize-review --help
exit=0
stdout=finalize-review — verify committed content and generate an attestation
Usage: finalize-review <change-id> --input <review-input.json>
<change-id> identifies the change; it is not a file path. --input names a
readable JSON file (relative to the working directory or absolute). Keep this
temporary input outside the repository so the checkout stays clean.

Run inside the selected repository after committing functional content, intent,
plan, required acceptance report and adversarial programs. Resolve the trunk
used for the branch diff. Review the current HEAD's content; the diff base is
the comparison starting point, not the reviewed target. Compute the required
reviewer count with reviewer-count <change-id>; use distinct real reviewers
independent of the writer. Preserve each original verdict and its findings;
never invent identities, passing judgments, probe evidence or authorization.

Illustrative JSON shape only — replace placeholders with authentic output;
this is not ready-to-submit review evidence:
{
  "verdicts": [{
    "reviewer": "<actual reviewer id>", "vendor": "<actual vendor>",
    "model": "<actual model>", "lens": "<actual review lens>",
    "verdict": "<original verdict>", "findings": []
  }],
  "findings": [],
  "adversarial": [{"command": "<artifact-bound execution command>",
                   "artifact": "<committed repository-relative program path>"}]
}
Repeat verdict rows for the required reviewers. Empty findings arrays are
appropriate only when the source has none; top-level findings carry every
unresolved adversarial finding from Build. Finalization accepts only PASS or
PASS_WITH_NOTES verdicts; a failing judgment requires the normal fix/review
route, not relabelling. Preserve scores and notes from the actual review too.
For a selected outside reviewer, retain its complete external_review runner
result, dimension_scores, notes and reviewed_sha; review_target_sha is the
concrete HEAD supplied to that review, not the diff base. The raw review output
must match the attributed verdict. Do not manufacture a receipt.

Use the actual committed probe and supported runner command from Build's
handoff. Where required, copy the reviewer's probe confirmation as
"confirmation": {"reviewer": "<id>", "reviewed_sha": "<reviewed commit>",
                 "quote": "<whole output lines naming this probe>"}.
If the adversary actually recorded no program, replace the adversarial list
with [{"no_program": "<observed reason>"}]; never mix it with program rows.
The reason must be nonblank, single-line, trimmed and contain no HTML comment.
This observed outcome is not a bypass. Follow existing explicit skip
instructions: when reviewers, adversarial or package-tests were skipped by
instruction, skip finalization and disclose absent verification. The checker
still recomputes any automatic narrow-change simplification.
Complete outside-review receipt and probe rules: <loom-code>/skills/closing-review/SKILL.md.

Results: exit 0 announces the generated attestation; exit 1 reports a BLOCK
rule and reason; exit 2 reports invocation/internal errors. Correct malformed
JSON or missing inputs using the diagnostic; obtain missing authentic evidence
through the normal review workflow. A passed stage is not overall success.
Stderr progress is advisory and can also contain errors: while running, keep
observing the same process; inspect its final exit and generated evidence.
Finalization executes the package suite and declared adversarial commands and
atomically writes the generated attestation. It grants no publication authority.
Commit that generated attestation before publication.

No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
For a literal file operand named --help or -h, use ./--help or ./-h.

stderr=

loom-code/skills/write-plan/SKILL.md
92: | capture-intent | intent — `docs/loom/intent/<change-id>.md`; `PRINCIPLES.md` and `DESIGN.md` at the repo root are side outputs of the tools it calls | user — decision point ① | `intent.schema`, `intent.product-no-identifiers`, `intent.needs-design-reason`, `intent.needs-design-recompute` | N/A |
98: | maintain | intent — a fresh `docs/loom/intent/<change-id>.md` | agent (dedupe is mechanical) | `intent.schema`, `intent.needs-design-reason`, `intent.needs-design-recompute`, `intent.product-no-identifiers` on a new intent | before hand-off to write-plan |
121: "${CLAUDE_PLUGIN_ROOT}/scripts/loom-python" --repair --script checked_readonly.py contract --require 2.1
125: `data.compatible: true`. The consumer validates the observation before emitting
127: whose `diagnostics` includes `rule_id: contract.requires` establishes the
130: invalid observations and launcher/startup failures stop this prerequisite with
211: You do not get the last word on `no`: the checker recomputes it
212: (`intent.needs-design-recompute`) against this repo's declared

loom-code/skills/write-plan/references/codex-first-contact.md
24:    `"<plugin-root>/scripts/loom-python" --repair --script checked_readonly.py contract --require 2.1`.
26:    `data.compatible: true`. Only an accepted blocked diagnostic with
27:    `rule_id: contract.requires` establishes the outdated-contract response in
28:    Step 0. Valid usage/internal errors, invalid observations and startup failures

loom-code/skills/closing-review/SKILL.md
4:   Run closing review and generate an attestation. Use after Build completes or functional changes invalidate prior review evidence.
136: "<loom-code>/scripts/loom-python" --ready --script checked_readonly.py reviewer-count <change-id>
140: `data.reviewer_floor`, tied to the unchanged `data.change_id`, determines how
143: do not parse success prose. Valid usage/internal errors, invalid observations
151: classify the whole change. `finalize-review` recomputes the same policy, and
170:   `reviewer-count`, finalization and attestation validation can recompute it.
220: available then. Refresh the final-choice record, or invalidate a stale approved
306: valid evidence-only edits keep the functional digest, while missing or invalid

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script /private/tmp/loom-accept-injected-producer/checked_readonly.py contract --require 2.1
exit=2
stdout=
stderr=checked-readonly: checker timed out after 30 seconds; investigate before rerunning


Timeout measured seconds: 30.07

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py contract --require 2.1
exit=0
stdout={"schema_version": 1, "command": "contract", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": "2.1", "compatible": true}}

stderr=

$ /private/tmp/loom-consume-acceptance-3056014/loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count 2026-11-14-consume-readonly-json
exit=0
stdout={"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"change_id": "2026-11-14-consume-readonly-json", "reviewer_floor": 2}}

stderr=

Read-only file snapshot: before=3924 after=3924 changed=[]

$ git diff 6fe61c99ea1981f238f8a8550abbd1e36e93cfab 3056014 -- loom-code/scripts/loom_checker.py loom-code/scripts/loom_checker loom-code/hooks loom-code/scripts/loom-python
exit=0
stdout=
stderr=

Producer, launcher, hooks, policy and operation reconciliation diff: empty.
```

