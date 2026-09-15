"""Adversary probe for plan Risk 2: a fresh-context cold reader, given only
capture-intent's SKILL.md and a sample conversation, must carry every detail
the user stated or agreed to and nothing else.

The sample conversation holds six details:
  carry   T3  the user states: ask before overwriting an existing file
  carry   T4+T5 agent proposes a count line, the user says yes
  carry   T10 the user corrects the filename to a fixed todo-export
  refuse  T2  agent proposes CSV, the user never answers
  refuse  T6+T7 agent proposes empty-list exit 1, the user says "later"
  refuse  T8  the date-based filename the user retracted at T10
  refuse  inference from T9 (runs under cron) that the prompt is skipped

Recorded runs live in ../coldread/run-<i>.txt, each headed with the git blob
sha of the SKILL.md it read. Re-record (needs the `claude` CLI):
    python3 docs/loom/2026-09-15-readable-flow-details/evidence/probes/test_probe_carried_details_coldread.py --record 3
Score the recorded runs:
    python3 -m pytest docs/loom/2026-09-15-readable-flow-details/evidence/probes/test_probe_carried_details_coldread.py -q -p no:cacheprovider
Add LOOM_PROBE_LIVE=1 to also run one fresh cold read.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    """Walk upward until a directory holding docs/loom is found."""
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs" / "loom").is_dir() and (candidate / "loom-code").is_dir():
            return candidate
    raise RuntimeError(f"repo root not found above {start}")


ROOT = _find_repo_root(Path(__file__).parent)
SKILL = ROOT / "loom-design/skills/capture-intent/SKILL.md"
RUN_DIR = Path(__file__).resolve().parent.parent / "coldread"

CONVERSATION = """\
T1 kouko: 我想加一個把本機待辦資料庫匯出成檔案的維護指令，給我自己備份用。
T2 agent: 了解。匯出格式預設用 CSV 如何？
T3 kouko: 對了，如果匯出的目標檔案已經存在，要先問我要不要覆蓋，不要直接蓋掉。
T4 agent: 好。匯出完成後，顯示一行「已匯出 N 筆」可以嗎？
T5 kouko: 好，這樣可以。
T6 agent: 清單是空的時候，印出「nothing to export」並以 exit code 1 結束，好嗎？
T7 kouko: 嗯…再說吧。
T8 kouko: 檔名預設用今天的日期。
T9 kouko: 我通常是在 cron 裡排程跑這個。
T10 kouko: 算了，檔名不要用日期，固定叫 todo-export 就好。
"""

INSTRUCTION = """\
You are the capture-intent station. The full station text is between the
STATION markers below; follow it. The interview conversation after it has
already happened. The intent is drafted: kind: engineering,
needs-design: no, Open questions none. You are now composing decision point ①
and then, after the user's yes, the Step 5 hand-off.

Reply with exactly two blocks and nothing else:
a line `=== STEP4 ITEM 5 ===` followed by item 5 of your decision point ①
message exactly as you would send it to the user; then a line
`=== STEP5 CARRIED ===` followed by the carried-details lines of your
hand-off message, one per line.
"""

REQUIRED = {
    "overwrite question (T3)": re.compile(r"覆蓋|overwrite", re.I),
    "count line (T4+T5)": re.compile(r"筆|count", re.I),
    "fixed filename (T10)": re.compile(r"todo-export"),
}

FORBIDDEN = {
    "CSV default (T2, unanswered)": lambda line: bool(re.search(r"csv", line, re.I)),
    "empty-list exit (T6, deferred)": lambda line: bool(
        re.search(r"nothing to export|exit\s*(code\s*)?1|空清單|清單.{0,3}空", line, re.I)
    ),
    "date filename (T8, retracted)": lambda line: bool(re.search(r"日期|date", line, re.I))
    and "todo-export" not in line,
    "no-prompt inference (T9)": lambda line: bool(
        re.search(r"非互動|non-?interactive|不詢問|不要?問|unattended|無人|--yes|--force|(?<![不會])自動覆蓋", line, re.I)
    ),
}


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def build_prompt(skill_text: str) -> str:
    return f"{INSTRUCTION}\n=== STATION ===\n{skill_text}\n=== /STATION ===\n\nConversation:\n{CONVERSATION}"


def parse_run(text: str) -> tuple[list[str], list[str]]:
    """(step4 lines, step5 lines) of one reply, header comments and blanks dropped."""
    body = text.split("=== STEP4 ITEM 5 ===", 1)
    assert len(body) == 2, "reply lacks the STEP4 block"
    step4, _, step5 = body[1].partition("=== STEP5 CARRIED ===")
    assert _, "reply lacks the STEP5 block"

    def lines(block: str) -> list[str]:
        return [ln.strip() for ln in block.splitlines() if ln.strip() and not ln.strip().startswith("```")]

    return lines(step4), lines(step5)


def score(step4: list[str], step5: list[str]) -> dict[str, list[str]]:
    table_rows = [ln for ln in step4 if ln.count("|") >= 2 or re.search(r"[│┃]", ln)]
    result = {"missing": [], "invented": [], "no_table": [] if len(table_rows) >= 2 else ["step4"]}
    for block_name, block in (("step4", table_rows), ("step5", step5)):
        joined = "\n".join(block)
        for name, pattern in REQUIRED.items():
            if not pattern.search(joined):
                result["missing"].append(f"{block_name}: {name}")
        for line in block:
            for name, hit in FORBIDDEN.items():
                if hit(line):
                    result["invented"].append(f"{block_name}: {name}: {line}")
    return result


def run_once(claude_bin: str, model: str, prompt: str, timeout: int = 600) -> str:
    workdir = tempfile.mkdtemp(prefix="coldread-")
    completed = subprocess.run(
        [claude_bin, "-p", prompt, "--model", model, "--output-format", "text"],
        cwd=workdir, capture_output=True, text=True, timeout=timeout,
    )
    shutil.rmtree(workdir, ignore_errors=True)
    return completed.stdout


def record(runs: int, model: str) -> int:
    claude_bin = shutil.which("claude")
    if claude_bin is None:
        print("claude CLI not found on PATH")
        return 2
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(SKILL.read_text(encoding="utf-8"))
    for i in range(1, runs + 1):
        stdout = run_once(claude_bin, model, prompt)
        header = f"# skill-blob: {blob_sha(SKILL)}\n# model: {model}\n# run: {i}\n\n"
        (RUN_DIR / f"run-{i}.txt").write_text(header + stdout, encoding="utf-8")
        print(f"run {i}: {score(*parse_run(stdout))}")
    return 0


def _recorded() -> list[Path]:
    return sorted(RUN_DIR.glob("run-*.txt"))


def _reply(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("\n\n", 1)[1]


# --- synthetic self-tests for the scorer ---

CLEAN = """=== STEP4 ITEM 5 ===
| 細節 | 內容 |
|---|---|
| 覆蓋 | 目標檔已存在時先問要不要覆蓋 |
| 完成訊息 | 顯示「已匯出 N 筆」 |
| 檔名 | 固定叫 todo-export |
=== STEP5 CARRIED ===
目標檔已存在時先問要不要覆蓋
匯出後顯示「已匯出 N 筆」
檔名固定為 todo-export
"""


def test_coldreadScorer_syntheticCleanReply_scoresClean() -> None:
    """A reply carrying exactly the three agreed details scores clean."""
    assert score(*parse_run(CLEAN)) == {"missing": [], "invented": [], "no_table": []}


def test_coldreadScorer_syntheticInventedReply_flagsInvention() -> None:
    """A reply adding the unanswered CSV and cron inference is flagged."""
    invented = CLEAN + "預設格式 CSV\n在 cron 下非互動執行，不詢問直接覆蓋\n"
    result = score(*parse_run(invented))
    assert any("CSV" in item for item in result["invented"])
    assert any("T9" in item for item in result["invented"])


def test_coldreadScorer_syntheticNegatedOverwriteWording_notFlagged() -> None:
    """The agreed overwrite question phrased as 'will not overwrite automatically' is not an inference."""
    reply = CLEAN.replace("目標檔已存在時先問要不要覆蓋\n匯出後", "檔案已存在時：先詢問是否覆蓋，不會自動覆蓋\n匯出後")
    assert score(*parse_run(reply)) == {"missing": [], "invented": [], "no_table": []}


# --- recorded and live cold reads ---


def test_coldreadRuns_recordedSet_matchesCurrentSkill() -> None:
    """Recorded runs exist and were produced against the current capture-intent text."""
    runs = _recorded()
    assert runs, f"no recorded runs in {RUN_DIR}; re-record with --record 3"
    current = blob_sha(SKILL)
    for path in runs:
        assert f"# skill-blob: {current}" in path.read_text(encoding="utf-8"), (
            f"{path.name} is stale against SKILL.md; re-record with --record 3"
        )


def test_coldreadRuns_sampleConversation_carriesOnlyAgreedDetails() -> None:
    """Every recorded cold read carries the three agreed details, in a table, and invents none."""
    runs = _recorded()
    assert runs
    for path in runs:
        result = score(*parse_run(_reply(path)))
        assert result == {"missing": [], "invented": [], "no_table": []}, f"{path.name}: {result}"


@pytest.mark.skipif(os.environ.get("LOOM_PROBE_LIVE") != "1", reason="set LOOM_PROBE_LIVE=1 for a fresh cold read")
def test_coldreadLive_freshReader_carriesOnlyAgreedDetails() -> None:
    """One fresh cold read carries the three agreed details, in a table, and invents none."""
    claude_bin = shutil.which("claude")
    assert claude_bin, "claude CLI not found"
    reply = run_once(claude_bin, "sonnet", build_prompt(SKILL.read_text(encoding="utf-8")))
    assert score(*parse_run(reply)) == {"missing": [], "invented": [], "no_table": []}, reply


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", type=int, required=True)
    parser.add_argument("--model", default="sonnet")
    args = parser.parse_args()
    raise SystemExit(record(args.record, args.model))
