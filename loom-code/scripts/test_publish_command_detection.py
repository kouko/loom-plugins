"""The publication hook allows and reminds (plan W1-03).

Spec 2026-09-22-publication-floor-moves-to-github REQ-4 and REQ-12, Design
decisions "Hook becomes allow-only with shallow recognition" and "Reminder
content". `push --hook` never refuses a publication command. Only when the
first simple command, after leading `VAR=value` assignments, is literally
`git push`, `gh pr create` or `gh pr merge` does it print one reminder line;
every other shape is silent, and a failure while computing the reminder
allows. The line reaches Claude Code as a stdout `systemMessage` object and
Codex and a terminal on stderr.
"""
from __future__ import annotations

import json
import subprocess
import sys
from io import StringIO
from pathlib import Path

import pytest

from loom_checker.command_handlers import push as push_handler

CHECKER = Path(__file__).resolve().parent / "loom_checker.py"
CHANGE = "2026-09-22-example"

# Built by concatenation so this file's own source carries no command a text
# rule would match.
PUSH = "git" + " push"
CREATE = "gh" + " pr create"
MERGE = "gh" + " pr merge"

ABSENT = "loom: verification absent (missing: plan, attestation); publishing anyway."
UNIDENTIFIED = "loom: change not identified (no intent for this branch); publishing anyway."
OUTSIDE_LAND = ("loom: this merges outside loom_checker.py land (missing: plan, attestation); "
                "merging anyway.")
CRASHED = "loom: publication hook failed (boom); allowing."


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def _repo(root: Path, *, identified: bool = True) -> Path:
    """A branch carrying a confirmed intent and nothing else: status `absent`."""
    repo = root / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "switch", "-q", "-c", f"feat/{CHANGE}" if identified else "feature")
    if identified:
        intent = repo / "docs" / "loom" / "intent" / f"{CHANGE}.md"
        intent.parent.mkdir(parents=True)
        intent.write_text("# Example\n\noriginator: kouko\nstatus: confirmed 2026-09-22\n",
                          encoding="utf-8")
        _git(repo, "add", ".")
        _git(repo, "commit", "-q", "-m", "intent")
    return repo


def _payload(repo: Path, command: str) -> dict:
    return {"cwd": str(repo), "hook_event_name": "PreToolUse", "tool_name": "Bash",
            "tool_input": {"command": command}}


def _boom(*_a, **_k):
    raise RuntimeError("boom")


# (id, command, identified branch, attribute to patch, expected reminder line)
CASES = [
    ("direct-push", PUSH + " origin HEAD", True, None, ABSENT),
    ("assignment-push", "FOO=1 " + PUSH + " -u origin HEAD", True, None, ABSENT),
    ("direct-create", CREATE + " --fill", True, None, ABSENT),
    ("direct-merge", MERGE + " 12 --squash", True, None, OUTSIDE_LAND),
    ("unidentified-push", PUSH + " origin feature", False, None, UNIDENTIFIED),
    ("true-prefix", "true; " + PUSH + " origin HEAD", True, None, None),
    ("bash-c", "bash -c '" + PUSH + " origin HEAD'", True, None, None),
    ("pipe-into-bash", "cat <<EOF | bash\n" + PUSH + " origin HEAD\nEOF\n", True, None, None),
    ("eval", "eval '" + PUSH + " origin HEAD'", True, None, None),
    ("cd-first", "cd x && " + PUSH + " origin HEAD", True, None, None),
    ("grep-mention", "grep -rn '" + MERGE + "' .", True, None, None),
    ("echo-mention", "echo 'run " + MERGE + " --squash when ready'", True, None, None),
    ("commit-mention", "git commit -m 'docs: explain " + MERGE + "'", True, None, None),
    ("crash", PUSH + " origin HEAD", True, ("identify_change", _boom), CRASHED),
    ("valid", PUSH + " origin HEAD", True,
     ("verification_status", lambda *_a, **_k: "valid"), None),
]


@pytest.mark.parametrize("command,identified,patch,expected",
                         [case[1:] for case in CASES], ids=[case[0] for case in CASES])
def test_hook_allows_and_reminds_only_the_direct_shape(
    tmp_path, monkeypatch, command, identified, patch, expected,
):
    """A4: direct push/create reminds, wrapped shapes are silent, all exit 0.
    A12: a mention of the merge words is silent; a direct merge reminds."""
    repo = _repo(tmp_path, identified=identified)
    if patch:
        monkeypatch.setattr(push_handler, *patch)
    monkeypatch.setattr(push_handler, "read_hook_payload", lambda: _payload(repo, command))
    out, err = StringIO(), StringIO()

    assert push_handler.cmd_push(["--hook"], out, err) == 0
    assert err.getvalue() == (f"{expected}\n" if expected else "")
    assert out.getvalue() == (
        json.dumps({"systemMessage": expected}) + "\n" if expected else "")


def test_reminder_reaches_both_carriers_through_the_cli(tmp_path):
    """The host carrier contract, through the real checker process."""
    repo = _repo(tmp_path)
    result = subprocess.run([sys.executable, str(CHECKER), "push", "--hook"],
                            input=json.dumps(_payload(repo, PUSH + " origin HEAD")),
                            capture_output=True, text=True, cwd=str(repo), timeout=60)

    assert result.returncode == 0, result.stderr
    assert result.stderr == ABSENT + "\n"
    assert json.loads(result.stdout) == {"systemMessage": ABSENT}


def _checker_cli():
    """`loom_checker.py` itself (the package of the same name shadows it on import)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("loom_checker_cli", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cli_push_hook_crash_outside_guard_allows(tmp_path, monkeypatch):
    """REQ-4: an unexpected failure in `push --hook` after the guard allows."""
    repo = _repo(tmp_path)
    monkeypatch.setattr(push_handler, "read_hook_payload",
                        lambda: _payload(repo, PUSH + " origin HEAD"))
    monkeypatch.setattr(push_handler, "publication_kind", _boom)
    err = StringIO()

    assert _checker_cli().main(["push", "--hook"], StringIO(), err) == 0
    assert err.getvalue() == "loom: publication hook failed (RuntimeError: boom); allowing.\n"


def test_cli_push_hook_guard_crash_still_refuses(tmp_path, monkeypatch):
    """A guard that cannot judge never loosens selection.guard."""
    repo = _repo(tmp_path)
    monkeypatch.setattr(push_handler, "read_hook_payload",
                        lambda: _payload(repo, PUSH + " origin HEAD"))
    monkeypatch.setattr(push_handler, "selection_guard_reason", _boom)
    err = StringIO()

    assert _checker_cli().main(["push", "--hook"], StringIO(), err) == 2
    assert err.getvalue().startswith("BLOCK selection.guard: ")


def test_cli_other_subcommand_crash_keeps_exit_two(monkeypatch):
    cli = _checker_cli()
    monkeypatch.setitem(cli.COMMANDS, "intent", _boom)
    err = StringIO()

    assert cli.main(["intent"], StringIO(), err) == 2
    assert err.getvalue() == "loom_checker internal error: RuntimeError: boom\n"
