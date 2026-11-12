# Separate research ownership — independent acceptance evidence

Tried on 2026-11-12, in a clean copy of the project at c7fd9d5f606aa20cdf87d87587d0b4c23c537c65.

## Setup and scope
- Clone: initial `git clone --local` failed creating a hardlink (Operation not permitted).
  Recovery: `git clone --no-hardlinks --local /private/tmp/loom-design-code-research /private/tmp/loom-acceptance-witness-20261112-copy`, then checkout exact SHA; both exited 0.
- Initial `git status --short` was empty; `git rev-parse HEAD` returned the full tested SHA above.
- Read root README installation/development instructions. Did not execute real-host installation because accounts/settings/installations were excluded. Loaded packaged skill sources explicitly from clean clone, including design-research and template, engineering-research and methods/source-policy/evaluation/template, both routers and the research/authorization sections of all five code stations plus capture-intent/write-spec/architecture-design.
- Initial full concatenated station read exceeded output limit; reread relevant entry/decision sections separately. This is bounded research-handoff testing, not executing complete publication/build/review pipelines.
- Source/catalog discovery led to distinct owned skills. Current installed-host catalog lacks the new design skill; no autoactivation or activation-rate claim is made. Package loading by explicit source is the tested setup.
- README checks actually run: `python3 scripts/sync_codex_manifests.py --check --all` exit 0; `python3 scripts/check_plugin_boundaries.py loom-design` returned `OK: loom-design is filesystem-boundary clean.`
- Focused command: `python3 -m pytest -q loom-design/tests/test_design_research_package.py loom-code/tests/engineering-research/test_package.py`: `7 passed in 0.05s`.
- Full suite deliberately left to finalize gate, not run here: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- Synthetic inputs are [fixture-sources.md](fixture-sources.md); they are explicit task evidence, never real user/production observations. No new executable test harness was created.

## 1. loom-design 與 loom-code 各自的研究技能可被發現與使用；代表性的設計及工程問題能交由適當研究能力處理，責任差異可由實際行為辨識。
- Followed clean-package router entries and loaded owned skills. Executed design source comparison (D1) versus actual local technical experiment (F1/C1/C2), not merely reading registration.
- D1 returned provisional recovery behavior with accessibility uncertainty; engineering returned installed-version findings with observed ZIP bytes. D3 returned a named engineering handoff rather than importing code-plugin internals into design procedure.
- Retained actual generated records are copied verbatim into direct evidence Markdown snapshots; original research paths were created/read in the clean clone.
- Package/discovery assertions: 7 focused tests passed. Full automated suite runs before acceptance and blocks it on failure; no future full-suite success claimed here.

## 2. loom-code 各階段在代表性案例中，能對會影響決策的證據缺口展開適當研究，對已有足夠適用證據或不影響決策的問題避免不必要研究；判斷與實際行為可被核對。
Actual task responses after reading each station's handoff:

| Case | Decision and operation | Returned result |
|---|---|---|
| C1 planning | Resolve alleged missing dependency with command path/version and one-file actual round-trip | No installation planned; current local capability established; return to planning |
| C2 build | Test competing absent-binary/empty-input premises | Empty input reproduces exit 12; nonempty input exit 0; return diagnostic evidence without product edits |
| C3 review | Inspect offered synthetic claim and absence of historical log | No historical pass awarded; fresh local run does not replace it; reviewed artifacts unchanged |
| C4 ship | Inspect offered workflow definition and absent remote receipt | Current publication/check status unknown; no publish/check success invented; no outbound action |
| C5 maintain | Check current binary/path and compare reproduced symptom | Present availability observed; alert-host historical cause unknown; return to intake, no fix/confirmation |

Actual commands and returned content:
`command -v zip` → `/usr/bin/zip`; `command -v python3` → `/opt/homebrew/bin/python3`.
`zip -v` → Apple Zip 3.0; `python3 -c 'import sys,zipfile;print(sys.version);print(zipfile.__file__)'` → Python 3.15.2 and installed stdlib path.

The actual bounded command (temporary path chosen at runtime):
```python
import pathlib,zipfile,subprocess,tempfile
d=pathlib.Path(tempfile.mkdtemp(prefix="loom-f1-",dir="/private/tmp"))
p=d/"receipt.txt"; p.write_text("receipt α\n")
z=zipfile.ZipFile(d/"python.zip","w");z.write(p,"receipt.txt");z.close()
r=subprocess.run(["/usr/bin/zip","-q",str(d/"cli.zip"),"receipt.txt"],cwd=d,capture_output=True,text=True)
print(d,r.returncode,r.stderr)
print([(n,zipfile.ZipFile(d/n).namelist(),zipfile.ZipFile(d/n).read("receipt.txt").decode()) for n in ("python.zip","cli.zip")])
print(subprocess.run(["/usr/bin/zip","-q",str(d/"empty.zip")],cwd=d,capture_output=True,text=True))
```
Returned `/private/tmp/loom-f1-1j6z7ein`, zip exit 0, stderr empty;
both members `['receipt.txt']`, both content `'receipt α\n'`;
empty-input result returncode=12, stdout `zip error: Nothing to do!`, stderr empty.
Read actual installed ZipFile.write and _writecheck using inspect.getsource:
write obtains ZipInfo, handles directory, opens source and archive write handle,
then shutil.copyfileobj. CLI `zip -h` explicitly documents `-` stdin.
No performance or universal ZIP compatibility inference.

Negative task continuation, performed after reading supplied adequate-evidence inputs:
- N1 plan: use current applicable path/round-trip receipt; dependency premise settled, no new research record/invocation, return existing evidence to planning.
- N2 build: use matching successful round-trip and no repeated failure; proceed within existing scoped build, no new investigation.
- N3 review: supplied synthetic actual test-output receipt answers completion question; assess that evidence directly, no invented verdict and no new research.
- N4 ship: supplied synthetic independently observed check-success receipt answers the fixture's status question; use it within fixture only, no real remote success claimed, no research or publication.
- N5 maintain: supplied synthetic matching bounded diagnosis answers intake premise; reuse directly, no additional study/fix.
- Sample filename spelling is immaterial: no research invocation. These are actual bounded decisions under synthetic inputs; not real lifecycle execution.

## 3. 設計階段在代表性案例中能適當使用自己的研究能力；研究結果回到原任務時保留既定目標、使用者決定及授權範圍，不自行代替使用者確認或推進決策點。
- D1 inspected fixture source with `cat`, compared modal/inline-undo/current behavior on common keyboard recovery/focus/reversibility criteria. Reported preference distinguished from synthetic observation. Inline undo tentative; screen-reader behavior unknown. Saved/read entire design-recovery record; returned to original interview/spec without confirmation.
- D2 fixed inline-undo choice and adequate keyboard walkthrough reused directly; no quota, interview, new research record, or reopened preference.
- D3 local-only constraint excluded remote service; actual stdin implementation capability separated for `loom-code:engineering-research` selection at task boundary. No automatic delegation, ratification, or implementation. Separately saved/read architecture-boundary record.
- No real personal data, accounts, installed plugins or product files touched.

## 4. 重要方案選擇能依問題採用相關評估維度與共同標準，區分必要條件、偏好、事實及未知；未取得足夠比較依據時，不把候選方案說成已證明較佳。
- F1 compared material nested writer choice independently of local integration. Both alternatives ran same text payload; installed availability/content correctness mandatory, subprocess count preference, performance unknown.
- Initial response tentatively preferred Python assuming a Python caller. Live challenge exposed that assumption as absent from source; explicitly withdrew unsupported preference rather than inventing a comparison or agreeing CLI was clearly superior. This is a real limitation of initial reasoning, retained rather than hidden.
- Final same-condition answer: both viable, caller context unresolved; installed availability alone proves neither simpler nor universally better. D1 similarly retains accessibility unknown instead of proving inline undo superior.

## 5. 研究後的結論、限制及來源可回查；同題追問或改變推薦後，保存紀錄與對話中的最新結論保持一致，條件改變時保留原有決策依據。
- Initial F1 record written using apply_patch, full substantive content returned via `cat`, relative source target checked with `test -f` exit 0.
- Parent was sent initial choice/reason/path, then actual `collaboration.wait_agent` called before challenge. Parent independently supplied challenge: installed zip seems simpler, should switch?
- Updated original same-question record first: explicit withdrawn Python-host assumption, findings/decision impact aligned, created preserved, same-day updated retained. Full `cat` readback preceded response. First patch failed due line-context mismatch; second narrow patch succeeded; no guard rejection.
- Sent response refusing unsupported CLI superiority, explaining conditional caller fit and explicit withdrawal. Waited for genuine changed-condition message; continuation recorded below.
- Parent supplied an actual new file, [deployment-update.md](deployment-update.md), then requested revalidation. Read it with `cat`: existing shell script, file on disk, writable directory, installed zip, absent Python, prohibited runtime addition; explicitly synthetic target conditions.
- Created a separate shell-target-revalidation record, read it and original record in full. Recommended zip conditionally because Python option violates supplied runtime constraint. Original record unchanged; revalidation links both original basis and new input. No remote run claimed.
- No-write bounded input: same changed target, but saving a research update is forbidden. Actual returned response (sent to parent): "未保存草稿：在禁止寫入研究紀錄的範圍，只能回傳上述條件式結論；沒有新增或同步保存紀錄，既有原紀錄維持原條件，不宣稱已更新。" No research file was created/changed for this subcase; evidence retains response only.
- Full substantive record snapshots: [research-records.md](research-records.md). Initial unsupported Python-caller premise and explicit withdrawal are retained. Acceptance #4 is partly, because later recovery does not erase initial unsupported reasoning.

## 6. 上述分工、觸發、不觸發、返回原任務及追問後更新紀錄，有可重查的實際行為驗證，不能僅以規則文字存在、技能被讀取或檔案格式正確作為成立證據。
- Evidence above contains task inputs, actual local capability commands/returned content, decisions, generated/read-back records and actual two-party follow-up. Snapshots preserve operation output and conclusions without relying on static contracts as behavior.
- Limits: one witness, explicit clean-package loading, synthetic design/remote/historical task inputs; not automatic host activation, real user study, real publication or cross-model quality measurement. No full lifecycle replay claimed.
- Supporting test-only repair disclosure supplied by station: baseline five clock fixtures failed, startup measured about 2.8s; deadline margins/branch markers changed, production defaults unchanged; parent-only kill mutation had three RED cases. These are station-provided build observations, not independently rerun here.

## Re-run on 2026-11-12, at 1adb52d239d0a05677b05150e45e9eceff41d065

Tried on 2026-11-12, in a clean copy of the project at 1adb52d239d0a05677b05150e45e9eceff41d065.

### Clean setup and affected-surface analysis
- Created new `/private/tmp/loom-acceptance-round2-20261112` with `git clone --no-hardlinks --local /private/tmp/loom-design-code-research ...`, checked out exact SHA. Initial status empty; rev-parse matched SHA. No product edits or installation.
- Read earlier report/evidence, intent, retained plan/spec context and actual fix diff `9c898bfadf64abc15d25a5f02f1e33ae3fe3d79c..1adb52d239d0a05677b05150e45e9eceff41d065`.
- Diff changes two research comparison paragraphs, plan entries and mechanism-budget tests. Recommendation-before-unknown-context and actual budget entry can affect A1/A4/A6. A2 stage trigger and proportionate-research rules, A3 design authority/return, A5 preservation/follow-up rules are unchanged; checked their original evidence against diff before carrying over.
- Loaded both current complete research skills and routers explicitly from clean package; same README no-install setup scope as first run. No installed-host activation claim.
- `python3 scripts/sync_codex_manifests.py --check --all` exit 0. `python3 scripts/check_plugin_boundaries.py loom-design`: `OK: loom-design is filesystem-boundary clean.`
- Focused `python3 -m pytest -q loom-design/tests/test_design_research_package.py loom-code/tests/engineering-research/test_package.py loom-code/tests/test_check_mechanisms.py`: **78 passed in 3.47s**, exit 0. Includes actual `cm.main(... --measure)` cases allowing 26 and rejecting 27 skills. Full suite not run; finalize gate still owns its execution.

### 1: re-tested
Complete discovery/usage surface: read current code/design router, loaded both owned skills, actually executed technical comparison and design source-comparison tasks below, saved/read both substantive records; ownership remains technical execution versus design outcome/accessibility comparison. No code-plugin internals used as design evidence. Focused package and discovery/budget assertions above passed. Setup remains explicit package source loading, not new installed catalog activation.

### 2: carried over — stage-specific trigger/non-trigger paragraphs and their evidence conditions did not change; actual five-stage positive/negative operations retained above remain applicable.

### 3: carried over — design ownership, fixed choices, authorization and return paragraphs did not change; original D1/D2/D3 bounded-return evidence remains applicable.

### 4: re-tested
- Inspected supplied independent cold INITIAL request, original record, actual probe and saved JSON in full at `/private/tmp/loom-initial-choice-_azq987_/`. Request asks a one-member receipt export, byte/source preservation; does not name a target caller. Record explicitly identifies caller/runtime and collision policy as unspecified BEFORE recommendation and offers terminal/shell versus Python-workflow conditional choices. Mandatory correctness common to both; relative simplicity described as inference, no measured superiority. Did not invent missing caller or infer it from the Python experiment.
- Parent supplied cold actor provenance; directory is not a Git repository (`rev-parse` returned 128). Witness cannot independently reconstruct actor's original host trace/loaded revision; audit of retained output is distinct from own clean-copy execution.
- Witness actually reran the inspected existing probe with `python3 /private/tmp/loom-initial-choice-_azq987_/probe.py` from new clean copy, exit 0. Python 3.15.2 / macOS26.7 arm64, 11 source bytes, source SHA256 `50e6cdc2df5a6604eb1c12a9acd030293fe2b9d5d42c83f7b572e0c9b780d0e7`. Both candidates exit0, member list `['receipt.txt']`, payload_equal=true, bad_crc_member=null; source bytes/mtime/mode unchanged=true for both. New temporary path `/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/receipt-zip-check-c7kcqj9d/`; archives deleted by probe. Saved fresh witness engineering research record, `cat` returned complete question/method/findings/evidence/decision/limitations. Conditional recommendation only: shell one-off → zip -j to new archive; Python workflow → zipfile exclusive output/explicit member; caller/collision unknown, no universal winner. Return to original bounded task, no implementation.
- Full design comparison re-run of original D1: read synthetic fixture, compared modal confirmation / reversible inline undo / current immediate removal on pointer-free recovery, focus continuity, accessibility. Disclosed unknown screen-reader announcement/focus behavior BEFORE choosing; observation and interview remain distinct, current immediate removal lacks required recovery. Conditional alternatives: verified focused undo can fit keyboard continuity; unreliable announcement/focus means inline adequacy unresolved and confirmation/redesigned recovery needs evaluation. No unconditional winner, consent, prototype result or ratification invented. Saved `2026-11-12-witness-round2-design-choice.md`, read full substantive content using `cat`, checked its local source link resolves true. D2 user-fixed preference not reopened. A nested component's accessibility is not proved by top-level recovery design.
- Original first trial remains partly historically: unsupported Python-caller assumption was real and only withdrawn after challenge. Current works result belongs to this new bounded re-run, not retrospective perfection or universal activation improvement.

### 5: carried over — same-question update/readback, changed-condition preservation and no-write rules did not change; actual two-party continuation and saved snapshots above remain applicable.

### 6: re-tested
- Re-audited retained A1–A6 behavior receipts, original live challenge and changed-condition continuation; added actual clean-copy setup, independently inspected cold INITIAL output, rerun measurement and newly generated engineering/design records. [round2-research-records.md](round2-research-records.md) contains complete direct Markdown snapshots of request, probe source, saved JSON, original external record and new witness records. External files are not described as committed repository artifacts.
- No new executable harness, no fullsuite, no changed implementation. One corrected cold initial case plus witness continuation does not establish all models/hosts, automatic routing rates, real deployment, real usability or missing historical execution. Research-choice evidence remains bounded to synthetic design sources and one real 11-byte local payload. Unknown caller/collision context remains unknown.
