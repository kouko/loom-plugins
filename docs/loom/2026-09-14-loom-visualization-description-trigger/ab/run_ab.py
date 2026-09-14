#!/usr/bin/env python3
"""A/B the loom-visualization description on Loom station reporting prompts.

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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHANGE_DIR = HERE.parent
REPO = CHANGE_DIR.parents[2]
EVIDENCE = CHANGE_DIR / "evidence"
PROTOCOL = HERE / "protocol.md"
RESULTS = HERE / "results.md"
SCRATCH = Path(os.environ.get(
    "AB_SCRATCH",
    "/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-loom-visualization/"
    "30f9cf4e-fddc-43dd-84bf-3c3c97261377/scratchpad/ab-desc",
))
BASE_REF = "6ad80799"
PLUGINS = ("loom-code", "loom-design", "loom-workflow")
SKILL_REL = "loom-workflow/skills/loom-visualization/SKILL.md"
SKILL_NAMES = {"loom-visualization", "loom-workflow:loom-visualization"}
MAX_STREAM_BYTES = 2 * 1024 * 1024

DESCRIPTION_A = (
    "Show comparisons, flows, decisions, states or reasoning chains as tables, "
    "ASCII or Mermaid in coding chat; not Obsidian notes."
)
DESCRIPTION_B = (
    "Show comparisons, flows, decisions, states or reasoning chains as tables, "
    "ASCII or Mermaid in coding chat, including when a Loom station reports to "
    "the user (intent restatement, choices, blind-run results); not Obsidian notes."
)
DESCRIPTION_B_SHA256 = "e98a3ed165415900bf405fe07209dde634cd465ff035fbea4ac2c73f57f6fd45"

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


def decide(a_count: int, b_count: int) -> str:
    return "SHIP" if b_count > a_count else "HOLD"


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
    return argv + ["--settings", settings_json]


def parse_stream(path: Path) -> dict:
    invoked, result, failed = False, None, False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
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
    return {"invoked": invoked, "table": bool(TABLE.search(text)),
            "diagram": bool(DIAGRAM.search(text)), "error": result is None or failed}


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
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
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


def report(runs: int) -> None:
    rows, dropped, counts = [], [], {"A": 0, "B": 0}
    for variant in ("A", "B"):
        for pid, _ in prompts():
            for r in range(1, runs + 1):
                stream = EVIDENCE / f"ab-{variant}" / f"{pid}-run{r}.jsonl"
                got = parse_stream(stream)
                counts[variant] += got["invoked"]
                rows.append((variant, pid, r, got))
                if stream.stat().st_size > MAX_STREAM_BYTES:
                    dropped.append(f"{stream.relative_to(CHANGE_DIR)} ({stream.stat().st_size} bytes)")
                    stream.unlink()
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    total = len(rows) // 2
    lines = [
        "# A/B results — loom-visualization description on Loom station reporting prompts",
        "",
        f"Protocol: [protocol.md](protocol.md). Runs per prompt per variant: {runs} "
        f"({total} sessions per variant, {len(rows)} total).",
        "",
        "| variant | prompt | run | invoked | table | diagram | error |",
        "|---|---|---|---|---|---|---|",
        *[f"| {v} | {p} | {r} | {yn(g['invoked'])} | {yn(g['table'])} | {yn(g['diagram'])} | {yn(g['error'])} |"
          for v, p, r, g in rows],
        "",
        "## Totals",
        "",
        "| variant | invoked | table | diagram | error |",
        "|---|---|---|---|---|",
        *[f"| {v} | {counts[v]}/{total} | {sum(g['table'] for x, _, _, g in rows if x == v)}/{total} "
          f"| {sum(g['diagram'] for x, _, _, g in rows if x == v)}/{total} "
          f"| {sum(g['error'] for x, _, _, g in rows if x == v)} |" for v in ("A", "B")],
        "",
        "## Decision",
        "",
        f"**{decide(counts['A'], counts['B'])}** — rule: SHIP B only if B's invocation count "
        f"({counts['B']}) is strictly greater than A's ({counts['A']}).",
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
