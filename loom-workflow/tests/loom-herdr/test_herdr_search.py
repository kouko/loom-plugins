"""Tests for loom-herdr's conversation search script (herdr_search.py).

A fake `herdr` on PATH serves `pane list` JSON; a temp HOME holds Claude,
Codex and OpenCode transcript stores. The script runs as a subprocess so no
bytecode lands in the skill folder.
"""

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "loom-herdr"
    / "scripts"
    / "herdr_search.py"
)

CLAUDE_ID = "11111111-aaaa-bbbb-cccc-000000000001"
CODEX_ID = "01a1f965-3a18-7832-a407-6a7a60d5cbac"
OPENCODE_ID = "ses_open1"


def _pane(pane_id, agent, session_id, cwd):
    pane = {
        "pane_id": pane_id,
        "tab_id": pane_id.replace(":p", ":t"),
        "workspace_id": pane_id.split(":")[0],
        "cwd": cwd,
        "agent": agent,
    }
    if session_id:
        pane["agent_session"] = {"agent": agent, "kind": "id", "value": session_id}
    return pane


def _write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in records))


def _claude(home, session_id, cwd, text):
    _write_jsonl(
        home / ".claude" / "projects" / "-proj" / f"{session_id}.jsonl",
        [{"type": "user", "cwd": cwd, "message": {"role": "user", "content": text}}],
    )


def _codex(home, session_id, cwd, text):
    _write_jsonl(
        home / ".codex" / "sessions" / "2026" / "11" / "21"
        / f"rollout-2026-11-21T10-00-00-{session_id}.jsonl",
        [
            {"type": "session_meta", "payload": {"id": session_id, "cwd": cwd}},
            {
                "type": "response_item",
                "payload": {"content": [{"type": "input_text", "text": text}]},
            },
        ],
    )


def _opencode(home, sessions, legacy=()):
    db = home / ".local" / "share" / "opencode" / "opencode.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    con.executescript(
        "create table session_v2 (id text primary key, directory text not null);"
        "create table session_message (id text primary key, session_id text,"
        " seq integer, data text);"
        "create table session (id text primary key, directory text not null);"
        "create table part (id text primary key, session_id text, data text);"
    )
    for sid, cwd, text in sessions:
        con.execute("insert into session_v2 values (?, ?)", (sid, cwd))
        data = {"content": [{"type": "text", "text": text}]}
        con.execute(
            "insert into session_message values (?, ?, 1, ?)",
            (sid + "-m", sid, json.dumps(data)),
        )
    for sid, cwd, text in legacy:
        con.execute("insert into session values (?, ?)", (sid, cwd))
        con.execute(
            "insert into part values (?, ?, ?)",
            (sid + "-p", sid, json.dumps({"type": "text", "text": text})),
        )
    con.commit()
    con.close()


def _herdr_env(tmp_path, panes):
    home = tmp_path / "home"
    home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    payload = tmp_path / "panes.json"
    payload.write_text(json.dumps({"id": "cli:pane:list", "result": {"panes": panes}}))
    fake = bin_dir / "herdr"
    fake.write_text(f'#!/bin/sh\ncat "{payload}"\n')
    fake.chmod(0o755)
    env = dict(os.environ, HOME=str(home), PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    return home, env


def _search(env, *args):
    proc = subprocess.run(
        [sys.executable, "-B", str(SCRIPT), *args, "--json"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _live_fixture(tmp_path):
    panes = [
        _pane("w1:p1", "claude", CLAUDE_ID, "/work/a"),
        _pane("w2:p2", "codex", CODEX_ID, "/work/b"),
        _pane("w3:p3", "opencode", OPENCODE_ID, "/work/c"),
        _pane("w4:p4", None, None, "/work/shell"),
    ]
    home, env = _herdr_env(tmp_path, panes)
    _claude(home, CLAUDE_ID, "/work/a", "please Deploy the widget")
    _codex(home, CODEX_ID, "/work/b", "codex says deploy now")
    _codex(home, "closed-codex", "/old/b", "old deploy notes")
    _claude(home, "closed-claude", "/old/a", "an earlier DEPLOY talk")
    _opencode(
        home,
        [(OPENCODE_ID, "/work/c", "opencode deploy plan"),
         ("ses_closed", "/old/c", "closed deploy session")],
        legacy=[("ses_legacy", "/old/legacy", "legacy deploy part")],
    )
    return env


def test_live_panes_claude_codex_opencode_labelled(tmp_path):
    rows = _search(_live_fixture(tmp_path), "deploy")
    by_agent = {r["agent"]: r for r in rows}
    assert set(by_agent) == {"claude", "codex", "opencode"}
    claude = by_agent["claude"]
    assert (claude["workspace"], claude["tab"], claude["pane"], claude["cwd"]) == (
        "w1", "w1:t1", "w1:p1", "/work/a")
    assert "deploy" in claude["snippet"].lower()
    assert by_agent["codex"]["pane"] == "w2:p2"
    assert by_agent["opencode"]["cwd"] == "/work/c"
    assert "opencode deploy plan" in by_agent["opencode"]["snippet"]


def test_unresolved_store_marked_unsearchable(tmp_path):
    panes = [_pane("w1:p1", "claude", "missing-id", "/work/a")]
    _home, env = _herdr_env(tmp_path, panes)
    rows = _search(env, "deploy")
    assert len(rows) == 1
    assert rows[0]["pane"] == "w1:p1"
    assert rows[0]["snippet"].startswith("unsearchable: ")


def test_history_includes_closed_sessions_marked_not_open(tmp_path):
    rows = _search(_live_fixture(tmp_path), "deploy", "--history")
    closed = {r["cwd"]: r for r in rows if r["pane"] == "not open"}
    assert set(closed) == {"/old/a", "/old/b", "/old/c", "/old/legacy"}
    assert "legacy deploy part" in closed["/old/legacy"]["snippet"]
    assert len([r for r in rows if r["pane"] != "not open"]) == 3


def test_default_excludes_history(tmp_path):
    rows = _search(_live_fixture(tmp_path), "deploy")
    assert all(r["pane"] != "not open" for r in rows)
    assert len(rows) == 3
