#!/usr/bin/env python3
"""Search agent conversations across herdr panes (read-only, stdlib only).

Live: `herdr pane list` -> each pane's agent_session id -> its transcript
(Claude / Codex JSONL, OpenCode sqlite). --history also searches transcripts
not open in any pane. Plain case-insensitive substring match; no index.
"""

import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

NOT_OPEN = "not open"


def collect_text(value, out):
    """Collect every string `text` field, and string `content`, recursively."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ("text", "content") and isinstance(item, str):
                out.append(item)
            else:
                collect_text(item, out)
    elif isinstance(value, list):
        for item in value:
            collect_text(item, out)
    return out


def snippet(text, query):
    idx = text.lower().find(query)
    if idx < 0:
        return None
    start = max(0, idx - 40)
    end = idx + len(query) + 80
    body = " ".join(text[start:end].split())
    return ("..." if start else "") + body + ("..." if end < len(text) else "")


def matches(texts, query):
    for text in texts:
        hit = snippet(text, query)
        if hit:
            yield hit


def jsonl_texts(path):
    """Return (cwd, texts) for a Claude or Codex JSONL transcript."""
    cwd, texts = "", []
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if not isinstance(record, dict):
                continue
            if not cwd:
                cwd = record.get("cwd") or (record.get("payload") or {}).get("cwd") or ""
            body = record.get("message", record.get("payload"))
            # Codex session_meta and developer items carry system prompts, not conversation.
            if record.get("type") == "session_meta" or (
                isinstance(body, dict) and body.get("role") in ("developer", "system")
            ):
                continue
            collect_text(body, texts)
    return cwd, texts


def claude_files(home):
    return sorted((home / ".claude" / "projects").glob("*/*.jsonl"))


def codex_files(home):
    return sorted((home / ".codex" / "sessions").glob("*/*/*/*.jsonl"))


def opencode_db(home):
    return home / ".local" / "share" / "opencode" / "opencode.db"


def connect_ro(path):
    con = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    con.execute("select 1").fetchone()
    return con


def table_exists(con, name):
    row = con.execute(
        "select 1 from sqlite_master where type='table' and name=?", (name,)
    ).fetchone()
    return row is not None


def opencode_rows(con, table, msg_table, where="", args=()):
    """Yield (session_id, directory, texts) from one OpenCode table pair."""
    if not (table_exists(con, table) and table_exists(con, msg_table)):
        return
    sessions = con.execute(f"select id, directory from {table} {where}", args).fetchall()
    for sid, directory in sessions:
        texts = []
        for (data,) in con.execute(
            f"select data from {msg_table} where session_id=?", (sid,)
        ):
            try:
                collect_text(json.loads(data), texts)
            except ValueError:
                continue
        yield sid, directory or "", texts


def opencode_session(con, sid):
    for table, msg in (("session_v2", "session_message"), ("session", "part")):
        for _sid, directory, texts in opencode_rows(con, table, msg, "where id=?", (sid,)):
            return directory, texts
    return None


def herdr_panes():
    try:
        proc = subprocess.run(
            ["herdr", "pane", "list"], capture_output=True, text=True, timeout=30
        )
    except FileNotFoundError:
        raise SystemExit("herdr_search: `herdr` not found on PATH") from None
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SystemExit(f"herdr_search: cannot run `herdr pane list`: {exc}") from None
    if proc.returncode != 0:
        raise SystemExit(
            f"herdr_search: `herdr pane list` failed: {proc.stderr.strip() or proc.stdout.strip()}"
        )
    try:
        panes = json.loads(proc.stdout)["result"]["panes"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit("herdr_search: `herdr pane list` did not return pane JSON") from None
    return panes if isinstance(panes, list) else []


def row(agent, cwd, text, pane=None):
    pane = pane or {}
    return {
        "workspace": pane.get("workspace_id", ""),
        "tab": pane.get("tab_id", ""),
        "pane": pane.get("pane_id", NOT_OPEN),
        "cwd": cwd,
        "agent": agent,
        "snippet": text,
    }


class Search:
    def __init__(self, home, query):
        self.home = home
        self.query = query
        self.hits = []
        self.unsearchable = []
        self._con = None
        self._con_error = None

    def opencode(self):
        if self._con is None and self._con_error is None:
            path = opencode_db(self.home)
            if not path.exists():
                self._con_error = "opencode db not found"
            else:
                try:
                    self._con = connect_ro(path)
                except sqlite3.Error as exc:
                    self._con_error = f"opencode db unreadable ({exc})"
        if self._con_error:
            raise LookupError(self._con_error)
        return self._con

    def add(self, agent, cwd, texts, pane=None):
        for hit in matches(texts, self.query):
            self.hits.append(row(agent, cwd, hit, pane))

    def live(self, pane):
        session = pane.get("agent_session") or {}
        # herdr may report agent=null (status unknown) while agent_session still names it.
        agent = session.get("agent") or pane.get("agent")
        sid = session.get("value")
        cwd = pane.get("cwd", "")
        if not sid:
            return None
        try:
            if agent == "claude":
                found = [p for p in claude_files(self.home) if p.stem == sid]
                if not found:
                    raise LookupError("claude transcript not found")
                self.add(agent, cwd, jsonl_texts(found[0])[1], pane)
            elif agent == "codex":
                found = [p for p in codex_files(self.home) if p.stem.endswith(sid)]
                if not found:
                    raise LookupError("codex transcript not found")
                self.add(agent, cwd, jsonl_texts(found[0])[1], pane)
            elif agent == "opencode":
                session = opencode_session(self.opencode(), sid)
                if session is None:
                    raise LookupError("opencode session not found")
                self.add(agent, cwd or session[0], session[1], pane)
            else:
                raise LookupError(f"unsupported agent {agent!r}")
        except (LookupError, OSError, sqlite3.Error) as exc:
            reason = exc.args[0] if isinstance(exc, LookupError) else str(exc)
            self.unsearchable.append(row(agent, cwd, f"unsearchable: {reason}", pane))
        return sid

    def history(self, open_ids):
        for path in claude_files(self.home):
            if path.stem not in open_ids:
                self.history_jsonl("claude", path)
        for path in codex_files(self.home):
            if not any(path.stem.endswith(sid) for sid in open_ids):
                self.history_jsonl("codex", path)
        try:
            con = self.opencode()
            for table, msg in (("session_v2", "session_message"), ("session", "part")):
                for sid, directory, texts in opencode_rows(con, table, msg):
                    if sid not in open_ids:
                        self.add("opencode", directory, texts)
        except LookupError as exc:
            if opencode_db(self.home).exists():
                self.unsearchable.append(row("opencode", "", f"unsearchable: {exc.args[0]}"))
        except sqlite3.Error as exc:
            self.unsearchable.append(row("opencode", "", f"unsearchable: {exc}"))

    def history_jsonl(self, agent, path):
        try:
            cwd, texts = jsonl_texts(path)
        except OSError as exc:
            self.unsearchable.append(row(agent, "", f"unsearchable: {exc}"))
            return
        self.add(agent, cwd, texts)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Search agent conversations across herdr.")
    parser.add_argument("query", help="case-insensitive substring")
    parser.add_argument("--history", action="store_true",
                        help="also search transcripts not open in herdr")
    parser.add_argument("--json", action="store_true", help="emit a JSON list of rows")
    parser.add_argument("--limit", type=int, default=20, help="maximum hit rows (default 20)")
    args = parser.parse_args(argv)
    query = args.query.lower()
    if not query:
        parser.error("query must not be empty")

    try:
        panes = herdr_panes()
    except SystemExit as exc:
        print(exc.code, file=sys.stderr)
        return 2

    search = Search(Path.home(), query)
    open_ids = {sid for sid in (search.live(p) for p in panes) if sid}
    if args.history:
        search.history(open_ids)

    rows = search.hits[: max(args.limit, 0)] + search.unsearchable
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    else:
        for r in rows:
            where = (f"workspace={r['workspace']} tab={r['tab']} pane={r['pane']}"
                     if r["pane"] != NOT_OPEN else NOT_OPEN)
            print(f"[{where}] agent={r['agent']} cwd={r['cwd']}\n  {r['snippet']}")
        if len(search.hits) > args.limit:
            print(f"({len(search.hits) - args.limit} more hits; raise --limit)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
