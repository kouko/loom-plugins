# A/B protocol — renamed loom-visualization description on Loom station reporting prompts

A copy of the 2026-09-14 change's `ab/protocol.md` (the A/B that shipped the
current description), re-run for intent Acceptance 2 of
2026-09-23-rename-blind-run-to-acceptance-testing: the only change to the
description is the phrase `blind-run results` → `acceptance test results`.
Prompts, measures, run count and session shape are the original's; what
changed is listed under each heading. The decision rule and the validity rule
were written before the runs.

## Variants

- **A** — the description as shipped at HEAD `77e71dec`, unchanged:
  `Show comparisons, flows, decisions, states or reasoning chains as tables, ASCII or Mermaid in coding chat, including when a Loom station reports to the user (intent restatement, choices, blind-run results); not Obsidian notes.`
  Rendered SHA-256 `e98a3ed165415900bf405fe07209dde634cd465ff035fbea4ac2c73f57f6fd45`.
- **B** — the renamed candidate, exact text:
  `Show comparisons, flows, decisions, states or reasoning chains as tables, ASCII or Mermaid in coding chat, including when a Loom station reports to the user (intent restatement, choices, acceptance test results); not Obsidian notes.`
  Rendered SHA-256 `b901f3528a8b1adbaaa412c1eb75034c973a0dac9e88def516f9ea147650c556`.

Budget check before running, using `_description` from
`scripts/test_loom_skill_description_catalog.py`: with B swapped in, the total
rendered Loom description length is 3,136 characters, within the 4,047 budget
(and within 60% of the 6,746 baseline). A renders 226 characters and B 232.

## Plugin copies

1. `git archive 77e71dec loom-code loom-design loom-workflow` is extracted into
   `$AB_SCRATCH/A/` and `$AB_SCRATCH/B/`.
2. In B only, the description block of
   `loom-workflow/skills/loom-visualization/SKILL.md` is replaced with B.
3. `run_ab.py build` compares the two trees file by file and fails unless the
   only difference is that one SKILL.md, whose rendered descriptions are A and B
   respectively and whose B hash equals the value above.

## Session shape

Each session runs from a fresh, empty, non-git working directory under the
scratchpad, with `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` in its environment:

```
claude -p "<prompt>" --output-format stream-json --verbose \
  --plugin-dir <variant>/loom-code \
  --plugin-dir <variant>/loom-design \
  --plugin-dir <variant>/loom-workflow \
  --settings '{"enabledPlugins": {<every key of ~/.claude/settings.json enabledPlugins>: false}}' \
  --setting-sources project --strict-mcp-config
```

- Only the `enabledPlugins` keys are read from `~/.claude/settings.json`; no
  other value is copied. The installed `loom-*@loom` keys are also set to
  false, so the only Loom plugins in a session are the variant's inline copies.
- Changed from the original: `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`,
  `--setting-sources project` and `--strict-mcp-config` isolate each trial from
  the user's CLAUDE.md files, user settings and MCP servers. Slash commands are
  left enabled (`--disable-slash-commands` also disables skills). Both variants
  get the same isolation.
- `--bare` is not used, so SessionStart hooks run in both variants.
- The model and all other configuration are the same for both variants.

## Prompts

Identical for both variants. Each prompt runs twice per variant: 9 prompts ×
2 runs × 2 variants = 36 sessions. If quota or time prevents this, both
variants drop symmetrically to one run per prompt (9 + 9) and the results say so.

### (a) Decision point ① — capture-intent restatement

- **a1-csv-export**：你正在跑 loom 的 capture-intent 站，請寫給使用者的決策點①訊息。要做的小改動：記帳 app 的「匯出」按鈕目前只能匯出 PDF，使用者想加 CSV 匯出。請覆述問題與以下 4 條驗收，並列出兩個單向門選項。驗收：1. 匯出選單多一個 CSV 選項；2. CSV 欄位為日期、分類、金額、備註，UTF-8 含 BOM，Excel 直接開不亂碼；3. 匯出範圍沿用目前畫面篩選的月份；4. 既有 PDF 匯出行為不變。單向門選項：(i) 金額欄輸出成字串「NT$1,200」還是純數字「1200」——之後有人寫了匯入腳本就很難改；(ii) 檔名格式定為「ledger-2026-09.csv」還是「記帳_2026年9月.csv」——使用者的自動化會依賴檔名。
- **a2-login-lockout**：你正在跑 loom 的 capture-intent 站，請寫給使用者的決策點①訊息。要做的小改動：內部後台登入連續輸錯密碼沒有任何限制，要加上鎖定。請覆述問題與以下 4 條驗收，並列出兩個單向門選項。驗收：1. 同一帳號 15 分鐘內連錯 5 次即鎖定；2. 鎖定期間登入頁顯示剩餘解鎖時間；3. 管理員可在帳號頁手動解鎖；4. 每次鎖定寫一筆稽核紀錄。單向門選項：(i) 鎖定依帳號計算還是依 IP 計算——依帳號會讓攻擊者能故意鎖住別人，依 IP 在公司 NAT 後會誤鎖整間辦公室；(ii) 失敗次數存在應用程式記憶體還是資料庫——之後擴成多台機器時，選記憶體要整套重做。
- **a3-image-upload**：你正在跑 loom 的 capture-intent 站，請寫給使用者的決策點①訊息。要做的小改動：社群站的頭像上傳目前原檔直接存，有人傳 20MB 的圖。請覆述問題與以下 4 條驗收，並列出兩個單向門選項。驗收：1. 上傳超過 5MB 直接拒絕並提示；2. 接受的圖一律縮成 512×512 以內；3. 只接受 JPEG、PNG、WebP；4. 舊頭像網址在 30 天內仍可讀。單向門選項：(i) 縮圖後丟掉原檔還是保留原檔——丟掉之後就無法再產生更大尺寸；(ii) 頭像網址改成內容雜湊（換圖就換網址）還是維持使用者 ID 固定網址——外部網站已經嵌入的舊網址會受影響。

### (b) One-way-door choices

- **b1-sqlite-postgres**：你正在跑 loom 的 capture-intent 站，這一步要讓使用者做一個單向門決定，請寫給使用者的訊息。情境：一個 3 人團隊的預約 app，目前約 200 位使用者、預估一年內 5,000 位，單台 VPS 部署。持久化要選 SQLite 或 PostgreSQL。已知後果：SQLite 零維運、備份就是複製檔案，但同時寫入只能一個、之後要換機器或多台部署就得遷移；PostgreSQL 要多一個服務、月費多約 15 美元、要學備份還原，但之後擴充與全文搜尋都現成。之後換資料庫預估要 2–3 週重寫與資料搬移。請列出選項與各自後果，並給你的建議。
- **b2-auth-provider**：你正在跑 loom 的 capture-intent 站，這一步要讓使用者做一個單向門決定，請寫給使用者的訊息。情境：一個 B2B SaaS 要加登入。三個選項：(1) 自己寫帳密登入——免費、完全掌控，但密碼重設、2FA、洩漏風險都自己扛；(2) 用 Auth0 這類託管服務——每月約 240 美元起、半天接好、支援 SSO，但使用者資料在第三方、之後搬走要讓所有人重設密碼；(3) 只做 Google／Microsoft 企業登入——免費、客戶 IT 喜歡，但沒有公司帳號的小客戶無法使用。選定後使用者身分 ID 會寫進所有資料表，事後換方案成本很高。請列出選項與各自後果，並給你的建議。
- **b3-monorepo-split**：你正在跑 loom 的 write-plan 站，這一步要讓使用者做一個單向門決定，請寫給使用者的訊息。情境：前端（React）與後端（FastAPI）目前在同一個 repo。選項：(1) 維持 monorepo——一個 PR 就能同時改 API 與畫面、CI 一條，但 CI 時間已 18 分鐘、權限無法分開；(2) 拆成兩個 repo——CI 各自約 7 分鐘、外包前端可只給前端權限，但跨端改動要兩個 PR 協調版本、git 歷史拆開後無法合回；(3) 拆成兩個 repo 並用共用 OpenAPI 套件——型別同步自動化，但多一個要發版的套件。請列出選項與各自後果，並給你的建議。

### (c) Blind-run result report

- **c1-csv-export**：你正在跑 loom 的 review 站，盲跑已經跑完，請寫給使用者看的盲跑結果報告（使用者要據此決定是否驗收）。結果：驗收 1「匯出選單多一個 CSV 選項」——可用，截圖顯示選單有 PDF 與 CSV；驗收 2「CSV 以 UTF-8 BOM 輸出，Excel 開啟不亂碼」——可用，`xxd` 開頭為 `efbbbf`，Excel 開啟中文正常；驗收 3「匯出範圍沿用目前篩選月份」——可用，篩 2026-08 匯出 42 列，與畫面筆數相同；驗收 4「備註含逗號與換行時欄位不錯位」——部分可用，逗號正確加引號，但備註含換行時 Numbers 開啟會斷成兩列；驗收 5「10 萬筆資料匯出在 5 秒內完成」——尚未可用，實測 11.8 秒，瀏覽器顯示無回應提示。
- **c2-login-lockout**：你正在跑 loom 的 review 站，盲跑已經跑完，請寫給使用者看的盲跑結果報告（使用者要據此決定是否驗收）。結果：驗收 1「15 分鐘內連錯 5 次鎖定」——可用，第 5 次後回應 423，第 6 次正確密碼也被拒；驗收 2「鎖定頁顯示剩餘時間」——可用，顯示「14 分 52 秒後可再試」並每秒遞減；驗收 3「管理員可手動解鎖」——可用，按下解鎖後立即可登入；驗收 4「每次鎖定寫稽核紀錄」——部分可用，紀錄有寫入，但來源 IP 欄位在反向代理後一律是 127.0.0.1；驗收 5「鎖定計數在服務重啟後保留」——尚未可用，重啟後計數歸零，可立即再試 5 次。
- **c3-image-upload**：你正在跑 loom 的 review 站，盲跑已經跑完，請寫給使用者看的盲跑結果報告（使用者要據此決定是否驗收）。結果：驗收 1「超過 5MB 拒絕並提示」——可用，上傳 6.2MB 檔顯示「檔案超過 5MB」；驗收 2「縮成 512×512 以內」——可用，上傳 4000×3000 圖得到 512×384；驗收 3「只接受 JPEG、PNG、WebP」——可用，上傳 GIF 被拒並提示格式；驗收 4「舊頭像網址 30 天內可讀」——部分可用，舊網址可讀，但回應標頭 `Cache-Control: no-store` 導致每次重新下載；驗收 5「iPhone HEIC 照片自動轉檔」——尚未可用，上傳 HEIC 回傳 500 錯誤。

## Measures per session

- **loaded** — the stream's `system`/`init` event lists
  `loom-workflow:loom-visualization` among its `skills` and a plugin whose
  `source` is `loom-workflow@inline` (the variant's copy). New in this copy: a
  session without it is **invalid** — the skill under test was never offered —
  and is excluded from the rates and counted separately, not scored as a
  non-trigger.
- **invoked** — the stream contains an assistant `tool_use` named `Skill`
  whose `skill` input is `loom-visualization` or `loom-workflow:loom-visualization`.
- **table** — the final `result` text contains a markdown table (a pipe row
  followed by a `|---|` separator row).
- **diagram** — the final `result` text contains box-drawing characters
  (U+2500–U+257F) or a ```` ```mermaid ```` fence.

A session whose stream has no final `result` event, or whose result is an
error, is an errored session and is re-run.

## Decision rule

KEEP B if and only if no session errored, each variant has at least one valid
run, and B's trigger rate over valid runs is at least A's (`invoked / valid`,
compared exactly, no tolerance); otherwise STOP and report the numbers — B is
not shipped and A is not silently restored. INCOMPLETE if any session errored.

Why this threshold: the rename is meant to be neutral, so the bar is
non-inferiority rather than the original's strict improvement. The original
results measured A 12/18 against B 18/18, with the whole gap in the six
result-report (c) sessions (0/6 against 6/6) — the prompts this phrase is
aimed at. With 18 runs per variant a tolerance could not be told apart from
a real loss, so none is granted: any shortfall, even one session, stops the
change and goes back to the orchestrator. The per-group breakdown is reported
so a loss confined to the (c) group is visible.

## Evidence

Raw streams go to `../evidence/ab-A/` and `../evidence/ab-B/` as
`<prompt-id>-run<N>.jsonl`, with stderr alongside. A stream larger than 2 MB is
not committed and is named in `results.md`.

## Runner source

The runner is recorded here as text, not committed as a program, so the
change's store holds no program. To reproduce: paste the block below into
`ab/run_ab.py` in this store, then run `AB_SCRATCH=<dir> python3 run_ab.py build`,
`run` and `report` from `ab/`. Its focused tests (`test_run_ab.py`, 15 passing
at commit `7a7dff4f`) are in that commit's history.

````python
#!/usr/bin/env python3
"""A/B the renamed loom-visualization description on Loom station reporting prompts.

Copied from the 2026-09-14 change's ab/run_ab.py; changed: paths, the two
variants, trial isolation, the loaded-skill validity check, the decision rule.

Usage (stdlib only):
  run_ab.py build            # extract A/B plugin copies from HEAD, verify diff
  run_ab.py run [--runs N]   # run every prompt N times per variant (default 2)
  run_ab.py report           # parse streams, write results.md

The prompts are read from protocol.md so the runner cannot drift from it.
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHANGE_DIR = HERE.parent
REPO = CHANGE_DIR.parents[2]
EVIDENCE = CHANGE_DIR / "evidence"
PROTOCOL = HERE / "protocol.md"
RESULTS = HERE / "results.md"


def scratch_dir(env) -> Path:
    return Path(env.get("AB_SCRATCH") or Path(tempfile.gettempdir()) / "loom-ab-rename")


SCRATCH = scratch_dir(os.environ)
BASE_REF = "77e71dec"
PLUGINS = ("loom-code", "loom-design", "loom-workflow")
SKILL_REL = "loom-workflow/skills/loom-visualization/SKILL.md"
SKILL_NAMES = {"loom-visualization", "loom-workflow:loom-visualization"}
MAX_STREAM_BYTES = 2 * 1024 * 1024

DESCRIPTION_A = (
    "Show comparisons, flows, decisions, states or reasoning chains as tables, "
    "ASCII or Mermaid in coding chat, including when a Loom station reports to "
    "the user (intent restatement, choices, blind-run results); not Obsidian notes."
)
DESCRIPTION_B = (
    "Show comparisons, flows, decisions, states or reasoning chains as tables, "
    "ASCII or Mermaid in coding chat, including when a Loom station reports to "
    "the user (intent restatement, choices, acceptance test results); not Obsidian notes."
)
DESCRIPTION_B_SHA256 = "b901f3528a8b1adbaaa412c1eb75034c973a0dac9e88def516f9ea147650c556"
LOADED_SKILL = "loom-workflow:loom-visualization"
INLINE_SOURCE = "loom-workflow@inline"

sys.path.insert(0, str(REPO / "scripts"))
from test_loom_skill_description_catalog import _render_description  # noqa: E402

TABLE = re.compile(r"^\s*\|.*\|\s*\n\s*\|\s*:?-{3,}", re.MULTILINE)
DIAGRAM = re.compile(r"[─-╿]|```mermaid")
PROMPT_LINE = re.compile(r"^- \*\*(?P<id>[abc]\d-[a-z0-9-]+)\*\*：(?P<text>.+)$", re.MULTILINE)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_hash(text: str) -> None:
    if sha256_text(text) != DESCRIPTION_B_SHA256:
        raise ValueError(f"B description hash mismatch: {sha256_text(text)}")


def decide(a_inv: int, a_valid: int, b_inv: int, b_valid: int, errors: int = 0) -> str:
    """KEEP B when B's trigger rate over valid runs is at least A's (no tolerance)."""
    if errors or not a_valid or not b_valid:
        return "INCOMPLETE"  # an unmeasured session leaves the comparison undecided
    return "KEEP B" if b_inv * a_valid >= a_inv * b_valid else "STOP"


def prompts() -> list[tuple[str, str]]:
    found = [(m["id"], m["text"]) for m in PROMPT_LINE.finditer(PROTOCOL.read_text(encoding="utf-8"))]
    assert len(found) == 9 and len({i for i, _ in found}) == 9, found
    return found


def disabled_plugins_settings(user_settings: dict) -> str:
    keys = user_settings.get("enabledPlugins", {})
    return json.dumps({"enabledPlugins": {key: False for key in keys}})


def build_argv(prompt: str, variant_dir: Path, settings_json: str) -> list[str]:
    argv = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose"]
    for plugin in PLUGINS:
        argv += ["--plugin-dir", str(variant_dir / plugin)]
    # Isolation per the trial lesson; slash commands stay on (disabling them disables skills).
    return argv + ["--settings", settings_json, "--setting-sources", "project", "--strict-mcp-config"]


def trial_env(environ) -> dict:
    env = {k: v for k, v in environ.items() if k != "CLAUDECODE"}
    env["CLAUDE_CODE_DISABLE_CLAUDE_MDS"] = "1"
    return env


def parse_stream(path: Path) -> dict:
    invoked, loaded, result, failed, corrupt = False, False, None, False, False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            event = None
        if not isinstance(event, dict):
            corrupt = True  # a corrupted line may have held the invocation
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            # Valid run: the variant's inline loom-workflow copy offered the skill.
            loaded = LOADED_SKILL in (event.get("skills") or []) and any(
                isinstance(p, dict) and p.get("source") == INLINE_SOURCE
                for p in event.get("plugins") or [])
        elif event.get("type") == "assistant":
            for item in event.get("message", {}).get("content", []) or []:
                if (isinstance(item, dict) and item.get("type") == "tool_use"
                        and item.get("name") == "Skill"
                        and (item.get("input") or {}).get("skill") in SKILL_NAMES):
                    invoked = True
        elif event.get("type") == "result":
            result = event.get("result") or ""
            # A rate-limited or failed session (e.g. 429) is not a measured session.
            failed = bool(event.get("is_error")) or event.get("api_error_status") is not None
    text = result or ""
    return {"invoked": invoked, "loaded": loaded, "table": bool(TABLE.search(text)),
            "diagram": bool(DIAGRAM.search(text)), "error": result is None or failed or corrupt}


def _files(root: Path) -> set[str]:
    # Hooks write __pycache__ into a copy once a session runs; that is not a copy difference.
    return {str(p.relative_to(root)) for p in root.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def verify_copies(a: Path, b: Path) -> None:
    fa, fb = _files(a), _files(b)
    if fa != fb:
        raise ValueError(f"file sets differ: {sorted(fa ^ fb)[:10]}")
    differing = sorted(r for r in fa if not filecmp.cmp(a / r, b / r, shallow=False))
    if differing != [SKILL_REL]:
        raise ValueError(f"copies differ beyond the description file: {differing}")
    da = _render_description((a / SKILL_REL).read_text(encoding="utf-8"))
    db = _render_description((b / SKILL_REL).read_text(encoding="utf-8"))
    if da != DESCRIPTION_A or db != DESCRIPTION_B:
        raise ValueError("rendered descriptions are not A and B")
    check_hash(db)
    rest_a = (a / SKILL_REL).read_text(encoding="utf-8").replace(DESCRIPTION_A, "")
    rest_b = (b / SKILL_REL).read_text(encoding="utf-8").replace(DESCRIPTION_B, "")
    if rest_a != rest_b:
        raise ValueError("SKILL.md differs outside the description text")


def build() -> None:
    for variant in ("A", "B"):
        dest = SCRATCH / variant
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        archive = subprocess.run(["git", "-C", str(REPO), "archive", BASE_REF, *PLUGINS],
                                 check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)
    skill = SCRATCH / "B" / SKILL_REL
    text = skill.read_text(encoding="utf-8")
    assert text.count("  " + DESCRIPTION_A + "\n") == 1
    skill.write_text(text.replace("  " + DESCRIPTION_A + "\n", "  " + DESCRIPTION_B + "\n"), encoding="utf-8")
    verify_copies(SCRATCH / "A", SCRATCH / "B")
    diff = subprocess.run(["diff", "-r", str(SCRATCH / "A"), str(SCRATCH / "B")],
                          capture_output=True, text=True).stdout
    print(diff)


def _run_one(variant: str, prompt_id: str, prompt: str, run: int, settings_json: str) -> str:
    out_dir = EVIDENCE / f"ab-{variant}"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{prompt_id}-run{run}"
    stream = out_dir / f"{stem}.jsonl"
    if stream.exists() and not parse_stream(stream)["error"]:
        return f"{variant} {stem} skipped (complete)"
    cwd = SCRATCH / "cwd" / f"{variant}-{stem}"
    shutil.rmtree(cwd, ignore_errors=True)
    cwd.mkdir(parents=True)
    env = trial_env(os.environ)
    with stream.open("wb") as out, (out_dir / f"{stem}.stderr.txt").open("wb") as err:
        try:
            code = subprocess.run(build_argv(prompt, SCRATCH / variant, settings_json),
                                  cwd=cwd, stdout=out, stderr=err, env=env,
                                  stdin=subprocess.DEVNULL, timeout=900).returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    return f"{variant} {stem} exit={code}"


def pending_jobs(jobs: list[tuple], evidence: Path, limit: int | None) -> list[tuple]:
    """Jobs whose stream is missing or has no result event, capped at `limit`."""

    def done(job: tuple) -> bool:
        stream = evidence / f"ab-{job[0]}" / f"{job[1]}-run{job[3]}.jsonl"
        return stream.exists() and not parse_stream(stream)["error"]

    todo = [job for job in jobs if not done(job)]
    return todo if limit is None else todo[:limit]


def run(runs: int, workers: int, limit: int | None = None) -> None:
    verify_copies(SCRATCH / "A", SCRATCH / "B")
    user = json.loads((Path.home() / ".claude/settings.json").read_text(encoding="utf-8"))
    settings_json = disabled_plugins_settings(user)
    jobs = [(v, pid, text, r) for r in range(1, runs + 1)
            for pid, text in prompts() for v in ("A", "B")]
    jobs = pending_jobs(jobs, EVIDENCE, limit)
    print(f"running {len(jobs)} pending sessions", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for line in pool.map(lambda j: _run_one(*j, settings_json), jobs):
            print(line, flush=True)


def _tally(rows: list[tuple], variant: str, group: str = "") -> dict:
    mine = [g for v, p, _, g in rows if v == variant and p.startswith(group)]
    valid = [g for g in mine if g["loaded"] and not g["error"]]
    return {"valid": len(valid), "invoked": sum(g["invoked"] for g in valid),
            "invalid": sum(not g["loaded"] and not g["error"] for g in mine),
            "error": sum(g["error"] for g in mine)}


def _rate(t: dict) -> str:
    return f"{round(100 * t['invoked'] / t['valid'])}%" if t["valid"] else "n/a"


def report(runs: int) -> None:
    rows, dropped = [], []
    for variant in ("A", "B"):
        for pid, _ in prompts():
            for r in range(1, runs + 1):
                stream = EVIDENCE / f"ab-{variant}" / f"{pid}-run{r}.jsonl"
                rows.append((variant, pid, r, parse_stream(stream)))
                if stream.stat().st_size > MAX_STREAM_BYTES:
                    dropped.append(f"{stream.relative_to(CHANGE_DIR)} ({stream.stat().st_size} bytes)")
                    stream.unlink()
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    total = len(rows) // 2
    t = {v: _tally(rows, v) for v in ("A", "B")}
    errors = t["A"]["error"] + t["B"]["error"]
    verdict = decide(t["A"]["invoked"], t["A"]["valid"], t["B"]["invoked"], t["B"]["valid"], errors)
    lines = [
        "# A/B results — renamed loom-visualization description on Loom station reporting prompts",
        "",
        f"Protocol: [protocol.md](protocol.md). Runs per prompt per variant: {runs} "
        f"({total} sessions per variant, {len(rows)} total).",
        "",
        "| variant | prompt | run | loaded | invoked | table | diagram | error |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {v} | {p} | {r} | {yn(g['loaded'])} | {yn(g['invoked'])} | {yn(g['table'])} "
          f"| {yn(g['diagram'])} | {yn(g['error'])} |" for v, p, r, g in rows],
        "",
        "## Totals (valid runs only; invalid = the skill did not load)",
        "",
        "| variant | valid | invoked | rate | invalid | errored |",
        "|---|---|---|---|---|---|",
        *[f"| {v} | {t[v]['valid']} | {t[v]['invoked']} | {_rate(t[v])} | {t[v]['invalid']} "
          f"| {t[v]['error']} |" for v in ("A", "B")],
        "",
        "By prompt group (a = intent restatement, b = one-way-door choices, c = result report):",
        "",
        "| variant | group | valid | invoked | rate |",
        "|---|---|---|---|---|",
        *[f"| {v} | {grp} | {x['valid']} | {x['invoked']} | {_rate(x)} |"
          for v in ("A", "B") for grp in "abc" for x in [_tally(rows, v, grp)]],
        "",
        "## Decision",
        "",
        f"**{verdict}** — rule: KEEP B only if no session errored, both variants have a valid "
        f"run, and B's trigger rate over valid runs ({t['B']['invoked']}/{t['B']['valid']}) is at "
        f"least A's ({t['A']['invoked']}/{t['A']['valid']}); otherwise STOP.",
        "",
        f"B rendered description SHA-256: `{sha256_text(DESCRIPTION_B)}`",
        "",
        "## Dropped streams (> 2 MB)",
        "",
        *([f"- {d}" for d in dropped] or ["- none"]),
        "",
    ]
    RESULTS.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "run", "report"))
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None,
                        help="run at most N pending sessions (keeps one call under a tool timeout)")
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.command == "run":
        run(args.runs, args.workers, args.limit)
    else:
        report(args.runs)


if __name__ == "__main__":
    main()
````
