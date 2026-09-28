#!/usr/bin/env python3
"""A/B the loom-visualization description on Loom station reporting prompts.

Variant A is the description at --base-ref; variant B is the description in the
current working tree. Both plugin copies are `git archive HEAD` and differ only
in that description (A's is swapped in). Streams and results.md go to --out,
which may not lie inside this 2026-09-14 change directory.

Rerun for the current description (from the repo root; stdlib only). Needs the
`claude` CLI on PATH, logged in, with quota for 9 prompts x --runs x 2 variants
sessions (36 at the default --runs 2; 18 at --runs 1):

  AB=docs/loom/2026-09-14-loom-visualization-description-trigger/ab/run_ab.py
  OUT=docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/ab-rerun
  export AB_SCRATCH=<scratch dir outside the repo>
  python3 $AB build  --base-ref 6ad80799
  python3 $AB run    --prompts $OUT/protocol.md --out $OUT --runs 2
  python3 $AB report --prompts $OUT/protocol.md --out $OUT --runs 2

`run` skips sessions whose stream is already complete, so it can be repeated
(or capped with --limit N) until every session has a result.
"""

from __future__ import annotations

import argparse
import filecmp
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
PROTOCOL = REPO / "docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/ab-rerun/protocol.md"
EVIDENCE: Path | None = None  # set from --out
RESULTS: Path | None = None


def scratch_dir(env) -> Path:
    return Path(env.get("AB_SCRATCH") or Path(tempfile.gettempdir()) / "loom-ab-desc")


SCRATCH = scratch_dir(os.environ)
PLUGINS = ("loom-code", "loom-design", "loom-workflow")
SKILL_REL = "loom-workflow/skills/loom-visualization/SKILL.md"
SKILL_NAMES = {"loom-visualization", "loom-workflow:loom-visualization"}
MAX_STREAM_BYTES = 2 * 1024 * 1024

sys.path.insert(0, str(REPO / "tests"))
from test_loom_skill_description_catalog import _render_description  # noqa: E402

TABLE = re.compile(r"^\s*\|.*\|\s*\n\s*\|\s*:?-{3,}", re.MULTILINE)
DIAGRAM = re.compile(r"[─-╿]|```mermaid")
PROMPT_LINE = re.compile(r"^- \*\*(?P<id>[abc]\d-[a-z0-9-]+)\*\*：(?P<text>.+)$", re.MULTILINE)


def current_description() -> str:
    return _render_description((REPO / SKILL_REL).read_text(encoding="utf-8"))


def set_output(out: Path) -> Path:
    """Point streams and results.md at `out`; refuse the old change directory."""
    global EVIDENCE, RESULTS
    out = Path(out).resolve()
    for p in (out, *out.parents):  # samefile: a case variant on a case-insensitive disk is the same dir
        if p == CHANGE_DIR or (p.exists() and os.path.samefile(p, CHANGE_DIR)):
            raise SystemExit(f"refusing --out inside the 2026-09-14 change: {out}")
    EVIDENCE, RESULTS = out, out / "results.md"
    return out


def decide(a_count: int, b_count: int, errors: int = 0) -> str:
    if errors:
        return "INCOMPLETE"  # an unmeasured session leaves the comparison undecided
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
    invoked, result, failed, corrupt = False, None, False, False
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
    text_a = (a / SKILL_REL).read_text(encoding="utf-8")
    text_b = (b / SKILL_REL).read_text(encoding="utf-8")
    da, db = _render_description(text_a), _render_description(text_b)
    if db != current_description():
        raise ValueError("rendered B is not the current SKILL.md description")
    if da == db:
        raise ValueError("A and B render the same description")
    if text_a.replace(da, "") != text_b.replace(db, ""):
        raise ValueError("SKILL.md differs outside the description text")


def build(base_ref: str) -> None:
    for variant in ("A", "B"):
        dest = SCRATCH / variant
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        archive = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD", *PLUGINS],
                                 check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)
    old = subprocess.run(["git", "-C", str(REPO), "show", f"{base_ref}:{SKILL_REL}"],
                         check=True, capture_output=True, text=True).stdout
    desc_a, desc_b = _render_description(old), current_description()
    skill = SCRATCH / "A" / SKILL_REL
    text = skill.read_text(encoding="utf-8")
    if text.count("  " + desc_b + "\n") != 1:
        raise ValueError("the HEAD description is not a single block line")
    skill.write_text(text.replace("  " + desc_b + "\n", "  " + desc_a + "\n"), encoding="utf-8")
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
                counts[variant] += got["invoked"] and not got["error"]
                rows.append((variant, pid, r, got))
                if stream.stat().st_size > MAX_STREAM_BYTES:
                    dropped.append(f"{stream.relative_to(EVIDENCE)} ({stream.stat().st_size} bytes)")
                    stream.unlink()
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    total = len(rows) // 2
    lines = [
        "# A/B results — loom-visualization description on Loom station reporting prompts",
        "",
        f"Protocol: [{PROTOCOL.name}]({os.path.relpath(PROTOCOL, RESULTS.parent)}). "
        f"Runs per prompt per variant: {runs} ({total} sessions per variant, {len(rows)} total).",
        "",
        f"B (current SKILL.md description): `{current_description()}`",
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
        f"**{decide(counts['A'], counts['B'], sum(g['error'] for *_, g in rows))}** — rule: "
        f"SHIP B only if no session errored and B's invocation count "
        f"({counts['B']}) is strictly greater than A's ({counts['A']}). "
        "B is already the shipped text, so this is a re-measurement: SHIP means the current "
        "description still out-invokes A; HOLD or INCOMPLETE is a finding for review, not a revert.",
        "",
        "## Dropped streams (> 2 MB)",
        "",
        *([f"- {d}" for d in dropped] or ["- none"]),
        "",
    ]
    RESULTS.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


def main() -> None:
    global PROTOCOL
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_build = sub.add_parser("build", help="extract A/B plugin copies from HEAD, verify they differ only in the description")
    p_build.add_argument("--base-ref", required=True, help="git ref whose description is variant A")
    for name, text in (("run", "run every prompt --runs times per variant"),
                       ("report", "parse streams, write <out>/results.md")):
        p = sub.add_parser(name, help=text)
        p.add_argument("--prompts", type=Path, required=True, help="protocol.md holding the 9 prompts")
        p.add_argument("--out", type=Path, required=True, help="output dir (not inside the 2026-09-14 change)")
        p.add_argument("--runs", type=int, default=2)
        if name == "run":
            p.add_argument("--workers", type=int, default=4)
            p.add_argument("--limit", type=int, default=None,
                           help="run at most N pending sessions (keeps one call under a tool timeout)")
    args = parser.parse_args()
    if args.command == "build":
        build(args.base_ref)
        return
    PROTOCOL = args.prompts.resolve()
    set_output(args.out)
    if args.command == "run":
        run(args.runs, args.workers, args.limit)
    else:
        report(args.runs)


if __name__ == "__main__":
    main()
