# Read-only CLI JSON — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at 49653681266bc049fafdd4014983a4412fd0f91c.

## Setup and execution record
Fresh clone: `git clone --no-hardlinks /private/tmp/loom-cli-readonly-json /private/tmp/loom-json-acceptance-4965368-fresh`; verified exact HEAD above. A pre-existing similarly named directory was preserved; a distinct new destination was used. Baseline was another fresh clone checked out detached at 80c8a2744bb8f9a5087bd9ef8e47d73ec6d9ca47. Existing worktrees were preserved.

README development setup: `loom-code/scripts/loom-python --repair contract --require 2.0 --json` returned exit 0, compatible true, version 2.3.1, empty stderr. The existing cached runtime was already usable; no plugin install or fresh dependency download was needed.

Focused verification:
```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_preparation_json.py loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_python_runtime.py -q
```
Result: **56 passed in 21.57s**, exit 0, no skipped tests. Initial sandbox attempt could not acquire the host uv cache lock; rerun with authorized host-cache access passed offline. This is an environment permission boundary, not a checker failure.

Consumer:
```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python /private/tmp/loom-json-acceptance-consumer.py > /private/tmp/loom-json-acceptance-consumer-results.json
```
Result: exit 0. Source and captured results are embedded below so ephemeral files are not required to assess the evidence.

The full suite was deliberately left to the final acceptance-blocking check:
`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
This report does not claim a new full-suite run.

## 1. Typed success, blocking and error results
The actual launcher consumer decoded the entire stdout using json.loads, checked newline termination, empty stderr, status/exit agreement, boolean compatibility and integer floors. Contract 2.0 permitted a simulated next step; 2.99 blocked it; bad rejected it and requested input correction. Reviewer-count produced distinct simulated reviewer lists of length two and one. All error data was null.

Named independent reruns: test_readonly_json_typed_observations_and_text_parity and test_readonly_json_repository_errors_and_late_failure_cleanup passed.

## 2. Existing text, exits, JSON, checks and authorization
The consumer compared baseline and candidate returncode/stdout/stderr exactly for contract pass/block/usage/repeated requirements, reviewer-count missing repository, plan missing input JSON, intake invalid station JSON and delivery local JSON. All eight comparisons passed. The focused tests additionally exercised valid and blocked plan/intake envelopes without data, delivery's distinct five-field shape, unchanged text error/hook behavior, repeated requirements and literal-selector behavior.

Named tests: test_preparation_json_passes_and_preserves_real_notices; test_preparation_json_blockers_usage_and_selector_boundaries; test_preparation_text_errors_hooks_and_other_commands_stay_unchanged; all passed. No live publisher, writer, authorization prompt, paid reviewer or plugin installation was invoked.

## 3. Read-only and honest execution boundaries
The consumer hashed every file including repository metadata before and after successful contract/reviewer observations; snapshots matched. Intentional fixture edits were made only between snapshots. Dirty and absent repositories returned usage error, exit 2. Empty isolated runtime cache with --ready returned exit 86, no stdout and the existing repair hint on stderr; the consumer did not attempt JSON parsing.

test_readonly_json_usage_and_selectors_before_domain_work replaced manifest/repository reads with forbidden sentinels and passed invalid/missing/blank/extra/duplicate/mixed-help selectors before reads. test_readonly_json_repository_errors_and_late_failure_cleanup injected a late handler error after partial output and typed data; the actual dispatcher returned one clean error object, cleared all partial data, and emitted no stderr. Both commands and both usage/internal exception classes passed. Launcher runtime tests passed independently. No completed review, authority, acceptance or delivery was inferred from exit 0.

## 4. Accurate help and safe discovery
Read the README CLI applicability table and loom-code README typed-data, final-selector, conservative-two and launcher-limit sections against actual results. Focused CLI tests passed, including test_exact_help_never_dispatches_handlers: every command and --help/-h was exercised with handlers, stdin, subprocess, socket and filesystem reads/writes forbidden (16 commands, 32 exact help calls). Launcher-backed all-command help tests also passed. Mixed help/JSON usage errors and input/authority wording checks passed.

## 5. Actual consumer decisions and limitations
Fresh clean fixture repository was made by the existing test fixture; the consumer executed the real launcher, not mocked command handlers. The initial unclassifiable delta required two simulated distinct reviewers; a committed guide-only delta required one. Contract compatibility controlled a separate permit/block decision; malformed input and dirty repository controlled correction-before-retry. The launcher boundary was handled separately. These are simulated policy/next-step consumers, not actual review execution.

No live host reload, installed-plugin refresh, external model, remote service, broken pipe/process termination or real writer was tested. No speed, cost or token improvement is claimed. No dismissed important finding was supplied. Package suite is not skipped and final acceptance-blocking verification remains the parent station's responsibility.

## Consumer source
```python
import json, subprocess, tempfile, pathlib, sys, hashlib, os
root=pathlib.Path('/private/tmp/loom-json-acceptance-4965368-fresh')
launcher=root/'loom-code/scripts/loom-python'
sys.path.insert(0,str(root/'loom-code/tests'))
from test_loom_checker_cli import make_intent_state_repo,git
tmp=pathlib.Path(tempfile.mkdtemp(prefix='loom-json-policy-'))
repo,_=make_intent_state_repo(tmp,delivered=False)
records=[]
def run(args,cwd=repo,env=None):
 p=subprocess.run([str(launcher),'--ready',*args],cwd=cwd,env=env,text=True,capture_output=True)
 records.append(dict(args=args,cwd=str(cwd),exit=p.returncode,stdout=p.stdout,stderr=p.stderr))
 return p
def consume(args):
 p=run(args); d=json.loads(p.stdout)
 assert p.stderr=='' and p.stdout.endswith('\n')
 assert p.returncode=={'passed':0,'blocked':1,'error':2}[d['status']]
 if d['status']=='error':
  assert d['error']['kind']=='usage' and all(v is None for v in d['data'].values())
  decision='correct-input-and-rerun'
 elif d['command']=='contract':
  assert type(d['data']['compatible']) is bool
  decision='permit-simulated-next-step' if d['status']=='passed' and d['data']['compatible'] else 'block-simulated-next-step'
 else:
  n=d['data']['reviewer_floor']; assert type(n) is int and n in (1,2)
  decision={'distinct_reviewers':[f'simulated-reviewer-{i}' for i in range(n)],'verification_complete':False}
 records[-1]['consumer_decision']=decision
 return d
def snapshot():
 return {str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in repo.rglob('*') if p.is_file()}
before=snapshot()
for requirement in ('2.0','2.99','bad'):
 consume(['contract','--require',requirement,'--json'])
for args in (['contract','--require','bad','--require','2.0'],['contract','--require','2.99'],['contract','--require','bad']):run(args)
assert consume(['reviewer-count','2026-09-09-example','--json'])['data']['reviewer_floor']==2
assert snapshot()==before
(repo/'guide.md').write_text('Usage clarification.\n');git(repo,'add','guide.md');git(repo,'commit','-qm','clarify usage')
before=snapshot()
assert consume(['reviewer-count','2026-09-09-example','--json'])['data']['reviewer_floor']==1
assert run(['reviewer-count','2026-09-09-example']).stdout=='1\n'
assert snapshot()==before
(repo/'dirty').touch();consume(['reviewer-count','id','--json'])
p=run(['reviewer-count','id','--json'],cwd=tmp);assert json.loads(p.stdout)['error']['kind']=='usage'
env=dict(os.environ,XDG_CACHE_HOME=str(tmp/'empty-cache'))
p=run(['contract','--require','2.0','--json'],env=env);assert p.returncode==86 and p.stdout==''
base=pathlib.Path('/private/tmp/loom-json-baseline-acceptance/loom-code/scripts/loom-python')
for args in (['contract','--require','2.0'],['contract','--require','2.99'],['contract','--require','bad'],['contract','--require','bad','--require','2.0'],['reviewer-count','id'],['plan','--json'],['intake','bad','id','--json'],['delivery','--goal','local','--json']):
 a=run(args,cwd=tmp)
 b=subprocess.run([str(base),'--ready',*args],cwd=tmp,text=True,capture_output=True)
 assert (a.returncode,a.stdout,a.stderr)==(b.returncode,b.stdout,b.stderr),args
 records[-1]['baseline_exact_stream_exit_match']=True
print(json.dumps(records,indent=2))
```

## Captured commands, streams, exits and decisions
Each args list below follows the absolute launcher path and --ready. cwd selects only temporary fixture data. The final eight observations include exact baseline stream/exit comparisons.
```json
[
  {
    "args": [
      "contract",
      "--require",
      "2.0",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 0,
    "stdout": "{\"schema_version\": 1, \"command\": \"contract\", \"status\": \"passed\", \"diagnostics\": [], \"notices\": [], \"error\": null, \"data\": {\"contract_version\": \"2.3.1\", \"required_version\": \"2.0\", \"compatible\": true}}\n",
    "stderr": "",
    "consumer_decision": "permit-simulated-next-step"
  },
  {
    "args": [
      "contract",
      "--require",
      "2.99",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 1,
    "stdout": "{\"schema_version\": 1, \"command\": \"contract\", \"status\": \"blocked\", \"diagnostics\": [{\"rule_id\": \"contract.requires\", \"message\": \"this repo ships loom contract 2.3.1, but >=2.99 is required \\u2014 \\u8acb\\u66f4\\u65b0 loom-code\\u3002\"}], \"notices\": [], \"error\": null, \"data\": {\"contract_version\": \"2.3.1\", \"required_version\": \"2.99\", \"compatible\": false}}\n",
    "stderr": "",
    "consumer_decision": "block-simulated-next-step"
  },
  {
    "args": [
      "contract",
      "--require",
      "bad",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 2,
    "stdout": "{\"schema_version\": 1, \"command\": \"contract\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"`--require bad` is not <major>.<minor>.\"}, \"data\": {\"contract_version\": null, \"required_version\": null, \"compatible\": null}}\n",
    "stderr": "",
    "consumer_decision": "correct-input-and-rerun"
  },
  {
    "args": [
      "contract",
      "--require",
      "bad",
      "--require",
      "2.0"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 0,
    "stdout": "contract 2.3.1 satisfies requires-contract >=2.0\n",
    "stderr": ""
  },
  {
    "args": [
      "contract",
      "--require",
      "2.99"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 1,
    "stdout": "",
    "stderr": "BLOCK contract.requires: this repo ships loom contract 2.3.1, but >=2.99 is required \u2014 \u8acb\u66f4\u65b0 loom-code\u3002\n"
  },
  {
    "args": [
      "contract",
      "--require",
      "bad"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 2,
    "stdout": "",
    "stderr": "`--require bad` is not <major>.<minor>.\n"
  },
  {
    "args": [
      "reviewer-count",
      "2026-09-09-example",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 0,
    "stdout": "{\"schema_version\": 1, \"command\": \"reviewer-count\", \"status\": \"passed\", \"diagnostics\": [], \"notices\": [], \"error\": null, \"data\": {\"change_id\": \"2026-09-09-example\", \"reviewer_floor\": 2}}\n",
    "stderr": "",
    "consumer_decision": {
      "distinct_reviewers": [
        "simulated-reviewer-0",
        "simulated-reviewer-1"
      ],
      "verification_complete": false
    }
  },
  {
    "args": [
      "reviewer-count",
      "2026-09-09-example",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 0,
    "stdout": "{\"schema_version\": 1, \"command\": \"reviewer-count\", \"status\": \"passed\", \"diagnostics\": [], \"notices\": [], \"error\": null, \"data\": {\"change_id\": \"2026-09-09-example\", \"reviewer_floor\": 1}}\n",
    "stderr": "",
    "consumer_decision": {
      "distinct_reviewers": [
        "simulated-reviewer-0"
      ],
      "verification_complete": false
    }
  },
  {
    "args": [
      "reviewer-count",
      "2026-09-09-example"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 0,
    "stdout": "1\n",
    "stderr": ""
  },
  {
    "args": [
      "reviewer-count",
      "id",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 2,
    "stdout": "{\"schema_version\": 1, \"command\": \"reviewer-count\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"reviewer-count needs a clean tree with completed functional content.\"}, \"data\": {\"change_id\": null, \"reviewer_floor\": null}}\n",
    "stderr": "",
    "consumer_decision": "correct-input-and-rerun"
  },
  {
    "args": [
      "reviewer-count",
      "id",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 2,
    "stdout": "{\"schema_version\": 1, \"command\": \"reviewer-count\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b is not inside a git work tree.\"}, \"data\": {\"change_id\": null, \"reviewer_floor\": null}}\n",
    "stderr": ""
  },
  {
    "args": [
      "contract",
      "--require",
      "2.0",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b/intent-state-repo",
    "exit": 86,
    "stdout": "",
    "stderr": "loom-python: checker runtime is missing or invalid; run loom-python --repair with the same arguments in an agent station.\n"
  },
  {
    "args": [
      "contract",
      "--require",
      "2.0"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 0,
    "stdout": "contract 2.3.1 satisfies requires-contract >=2.0\n",
    "stderr": "",
    "baseline_exact_stream_exit_match": true
  },
  {
    "args": [
      "contract",
      "--require",
      "2.99"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 1,
    "stdout": "",
    "stderr": "BLOCK contract.requires: this repo ships loom contract 2.3.1, but >=2.99 is required \u2014 \u8acb\u66f4\u65b0 loom-code\u3002\n",
    "baseline_exact_stream_exit_match": true
  },
  {
    "args": [
      "contract",
      "--require",
      "bad"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 2,
    "stdout": "",
    "stderr": "`--require bad` is not <major>.<minor>.\n",
    "baseline_exact_stream_exit_match": true
  },
  {
    "args": [
      "contract",
      "--require",
      "bad",
      "--require",
      "2.0"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 0,
    "stdout": "contract 2.3.1 satisfies requires-contract >=2.0\n",
    "stderr": "",
    "baseline_exact_stream_exit_match": true
  },
  {
    "args": [
      "reviewer-count",
      "id"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 2,
    "stdout": "",
    "stderr": "/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b is not inside a git work tree.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n",
    "baseline_exact_stream_exit_match": true
  },
  {
    "args": [
      "plan",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 2,
    "stdout": "{\"schema_version\": 1, \"command\": \"plan\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"plan needs a path.\"}}\n",
    "stderr": "",
    "baseline_exact_stream_exit_match": true
  },
  {
    "args": [
      "intake",
      "bad",
      "id",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 2,
    "stdout": "{\"schema_version\": 1, \"command\": \"intake\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"unknown station 'bad'; intake covers write-spec and write-plan.\"}}\n",
    "stderr": "",
    "baseline_exact_stream_exit_match": true
  },
  {
    "args": [
      "delivery",
      "--goal",
      "local",
      "--json"
    ],
    "cwd": "/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b",
    "exit": 1,
    "stdout": "{\"state\": \"unconfirmed\", \"reason\": \"/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-json-policy-atumbp1b is not inside a git work tree.\", \"next\": \"Run delivery inside the selected repository.\", \"evidence\": {}, \"complete\": false}\n",
    "stderr": "Help: \"<loom-code>/scripts/loom-python\" --ready delivery --help (replace <loom-code> with the installed loom-code plugin directory).\n",
    "baseline_exact_stream_exit_match": true
  }
]
```

