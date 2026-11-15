# Sandbox network recovery — acceptance test evidence

Tried on 2026-11-16, in a clean copy of the project at a17daced.

## Environment and clean setup
- Tested full HEAD: a17daced386e52cf4b0856ad2c751c03a4310189.
- Created fresh clone: `git clone --no-hardlinks --no-checkout . /private/tmp/loom-acceptance-sandbox-20261116`; then `git checkout --detach a17daced386e52cf4b0856ad2c751c03a4310189`.
- Read root README and loom-code README, including Install / Codex and runtime setup guidance. README marketplace installation points to main and changes shared installed caches, so it was not executed. This run verifies clean-source tool loading, not installation or host-native trigger behavior.
- Executed `loom-code/scripts/loom-python --repair --help` from clean clone. Exit 0; printed checker command inventory including publish, delivery, land and github-rules. Output explicitly says no validation runs for help alone. Thus this proves launcher loading only.
- Initial focused command `python3 -m pytest -q loom-code/tests/test_ship_station_text.py loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized` exited 1: `/opt/homebrew/opt/python@3.15/bin/python3.15: No module named pytest`.
- Cached launcher's interpreter also reported `No module named pytest`.
- Attempted isolated setup: `uv run --cache-dir /private/tmp/loom-acceptance-uv-cache --with pytest --python 3.11 python -m pytest -q loom-code/tests/test_ship_station_text.py loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`. Exit 2:
```text
error: Request failed after 3 retries in 11.8s
  cause: Failed to fetch: https://pypi.org/simple/pytest/
  cause: error sending request for url (https://pypi.org/simple/pytest/)
  cause: client error (Connect)
  cause: dns error
  cause: failed to lookup address information: nodename nor servname provided, or not known
```
- The explicit resolver error above describes this PyPI request only; it does not establish the cause of the historical GitHub failure.
- Parent supplied an already available absolute test interpreter. No packages were installed in that environment.
- Executed in clean clone: `/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q loom-code/tests/test_ship_station_text.py loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`.
```text
............                                                             [100%]
12 passed in 0.54s
```
- Exit 0. Subsequent `git status --porcelain` was empty; `git rev-parse HEAD` returned the full tested HEAD above.
- Full package suite intentionally left to finalize-review, as instructed by the tester contract. Its canonical command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. This report does not claim a new full-suite result.
- Report/evidence writer is independent of implementation and of the synthetic decision executor. Parent states no important/fatal findings were dismissed.

## 1. 連線不可用與登入／權限問題得到不同且與證據相符的處理，不將一般連線失敗直接斷定為 DNS 問題。
- How tried: judged raw independently produced A, B, F decisions below; executed the Ship station test module.
- Observed: B classifies explicit HTTP 401 as authentication and refuses host retry; F retains unknown cause and rejects unsupported DNS/elevation inference; A uses matched environment evidence.
- Result: works for tested guidance behavior. No live historical reconstruction or cross-host trigger claim.

## 2. 執行環境限制可在政策允許且既有授權足夠時，透過適當權限重試同一個 Loom 命令；原有發布檢查仍然有效。
- How tried: compared exact A retry command with original; judged G read-only authorization independently; executed focused recovery text test and all retained Ship tests.
- Observed: A repeats the exact canonical publication command once through permitted host approval; G retries only the authorized read-only command and infers no publication/merge authorization.
- Result: partly. Decisions preserve operation consent, command identity and checks, but no actual permission request, remote publication or installed-host trigger ran.

## 3. 平台拒絕、權限不可取得或重試仍失敗時，流程保留失敗證據並準確報告未完成，不改用繞過檢查的發布方式。
- How tried: judged C, D and E raw decisions; focused recovery test also asserts unavailable permission mechanism, one-retry stop, output preservation and no raw publication substitutions.
- Observed: C stops on explicit denial, D preserves unknown remote state and uses canonical read-only delivery observation, E retains merged-versus-cleanup distinction without replaying acceptance.
- Result: partly. Synthetic denial and retry-failure decisions are correct. Unavailable permission mechanism is text-test coverage only; no native platform-denial or unavailable-permission execution was performed.

## 4. 修正具備測試與獨立驗證證據；驗收報告逐條呈現實際結果及限制。
- How tried: clean-source launch, focused 12-test command, raw independent synthetic decisions, exact prompts/responses retained below.
- Observed: 12 passed, including synchronized release metadata. Setup failures retained above; runtime limitations disclosed row by row.
- Result: works within this verification scope. The automated complete package suite runs before acceptance and blocks it on failure; no result of that future execution is asserted here.
- Decisions resolved without asking: narrow guidance-only repair, existing minor release process, bounded one retry via permitted host mechanisms, and clean-source rather than shared-cache marketplace install. No user-instructed skips are present in intent/plan.

## Raw synthetic prompts and responses
### Additional root-provided live read-only evidence
- Parent reported running exact installed launcher argv in this change worktree: `/Users/kouko/.codex/plugins/cache/loom/loom-code/3.81.1/scripts/loom-python --repair github-rules`.
- Default sandbox exit 0, output: `could not confirm ... repos/kouko/loom-plugins: error connecting to api.github.com`; generic authentication/read-access remedy was printed.
- Parent reported repeating the identical argv once with permitted `require_escalated`. Exit 0, output: `loom: main requires a pull request (administrators included) and the check "loom-pr-floor / PR floor"`.
- Attribution: observed and supplied by parent, not directly executed or independently witnessed by this tester. No setup, publication or mutation occurred. This strengthens actual read-only retry evidence but does not establish publication-check execution or real platform-denial behavior; partial verdicts remain.

Parent supplied the following exact scenario input and raw executor response from /private/tmp/loom-sandbox-behavior-cases.md and /private/tmp/loom-sandbox-behavior-decisions.md. The executor was supplied current Ship skill and cases, without intent/plan/expected answers. These are synthetic text decisions, not live host invocations or actual publication results.

```markdown
# Bounded Ship decision cases
Use the supplied Ship skill as an executor. These are synthetic tool-result cases, not live operations. For each independent case, return the immediate next action, any exact canonical command to repeat or observe, whether host execution permission is requested, and the state to report. Do not execute network requests or mutate a repository. Do not assume missing evidence.

Canonical launcher: /plugin/scripts/loom-python --repair.
Original publication command: /plugin/scripts/loom-python --repair publish --intent /project/docs/loom/intent/change.md --title "fix: example" --body-file /tmp/body.md.

## A
The user has authorized publication. The current command ran in a documented network-restricted sandbox. In this same environment an identical read-only gh query failed inside the sandbox and succeeded with permitted host execution. Publication exits before any remote mutation with "error connecting to api.github.com". The shell exposes a permitted approval mechanism for host execution; no platform denial has occurred.

## B
Publication is authorized. Host networking works. The command reports HTTP 401 "Bad credentials". There is no transport error.

## C
Publication is authorized. Sandbox connectivity restrictions are established. The host permission request has been explicitly rejected by the platform. The ordinary sandbox command cannot connect. No remote mutation has occurred.

## D
Publication is authorized. Known sandbox restrictions justified one permitted host execution retry of the original canonical command. That retry also failed with a connection error; remote state is unconfirmed.

## E
The user accepted the report and authorized merge. Canonical land --accepted-by kouko printed "Merged PR" followed by a cleanup BLOCK, preserving branch fix/change in a surviving repository at /project. The merge is confirmed. Cleanup is not.

## F
The canonical command reports "error connecting to api.github.com". Network policy and environment restrictions are unknown; no comparative execution exists. The operator says "It must be DNS, just elevate it". Publication was authorized but no new host evidence was supplied.

## G
The only authorized operation is read-only github-rules observation. No publication or merge is authorized. Known sandbox networking restrictions have been established by matched read-only queries. The current read-only /plugin/scripts/loom-python --repair github-rules command cannot connect. Host policy permits this read-only operation through its available permission mechanism.
# Synthetic Ship execution decisions

These are independent execution decisions from the supplied Ship skill and synthetic outputs. No network request or repository mutation was executed.

## A
- Immediate action: request permitted host execution for one retry of the same authorized publication command, preserving all Loom checks.
- Exact retry: `/plugin/scripts/loom-python --repair publish --intent /project/docs/loom/intent/change.md --title "fix: example" --body-file /tmp/body.md`.
- Host execution permission: yes, scoped to this command. Publication authorization already exists; this request concerns execution context only.
- Reportable state now: initial publication failed before remote mutation; established sandbox connectivity restrictions justify this bounded recovery. Publication and CI success remain unconfirmed until the retry reports them. Preserve the original output and retry output. Retry success supports only its actual reported results; delivery observation is still needed before published handoff.

## B
- Immediate action: report the authentication failure and stop this publication attempt; obtain an authorized authentication remedy rather than retrying with execution permission or altering credentials automatically.
- Exact canonical retry or observation now: none justified by supplied evidence.
- Host execution permission: no.
- Reportable state: HTTP 401 Bad credentials blocks publication; no publication success is established. Host networking is working, so transport recovery does not address this result.

## C
- Immediate action: stop recovery and report the explicit platform denial and unfinished publication. Preserve the failed command and denial outputs. Do not bypass denial or substitute raw publication commands.
- Exact canonical retry now: none; no further automatic retry is allowed.
- Host execution permission: no renewed request after the explicit rejection.
- Reportable state: publication is blocked by denied host execution with sandbox connectivity unavailable; no remote mutation occurred, and publication remains unfinished.

## D
- Immediate action: end automatic recovery, preserve original and retry outputs, and report the blocker and unconfirmed remote state. Before any further mutation, inspect partial publication through the read-only canonical delivery route while the branch remains identifiable.
- Exact observation: `/plugin/scripts/loom-python --repair delivery --goal published --intent /project/docs/loom/intent/change.md --json`.
- Host execution permission: no further publication execution retry request. The failed retry ends this recovery episode. Do not assume another permitted network route or successful observation; if delivery cannot be observed, keep the state unconfirmed and stop rather than restarting the retry cycle.
- Reportable state: the single recovery retry failed; remote publication and CI state remain unconfirmed. Any later delivery result supports only what it actually observes.

## E
- Immediate action: inspect and resolve the specific state named by the cleanup BLOCK, then recover cleanup from the surviving repository without replaying acceptance. The BLOCK's particular remedy cannot be invented from the provided case.
- Exact recovery after its named condition is resolved: `cd '/project' && /plugin/scripts/loom-python --repair land --cleanup fix/change`.
- Host execution permission: no request is justified by the supplied cleanup failure alone.
- Reportable state: merge is confirmed, cleanup is blocked/incomplete, and overall completion cannot yet be claimed. Preserve the full land output and exit status. Do not repeat `--accepted-by kouko`. After successful cleanup use that execution's full result and follow its printed next destination.

## F
- Immediate action: keep the connection failure unattributed and report the blocker; do not automatically retry or elevate. The operator's DNS assertion supplies no diagnostic evidence. Read-only investigation may establish a cause later, but the present evidence does not justify a recovery execution.
- Exact canonical retry now: none justified.
- Host execution permission: no.
- Reportable state: unexplained connection failure; DNS, sandbox restrictions, and credential causes are not established. Publication success remains unconfirmed.

## G
- Immediate action: request permitted host execution for one retry of the same authorized read-only observation. Publication and merge consent are not required for this observation and must not be inferred.
- Exact retry: `/plugin/scripts/loom-python --repair github-rules`.
- Host execution permission: yes, scoped only to that read-only command.
- Reportable state now: rules could not yet be confirmed due to established sandbox connectivity restrictions. Report only what the retry observes. Missing rules would still require explicit setup consent; this recovery authorizes neither setup, publication, nor merge.

```

