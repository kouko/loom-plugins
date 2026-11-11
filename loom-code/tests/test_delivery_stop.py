"""Documented Stop framing around the same single-shot delivery observer."""
import json
import signal
import shlex
from io import StringIO
from pathlib import Path
import pytest

from loom_checker.command_handlers import publish
from test_delivery import delivery
from test_loom_publish import git


def stop(monkeypatch, repo, host=None, **payload):
    monkeypatch.setattr(publish.sys, "stdin", StringIO(json.dumps(
        {"hook_event_name": "Stop", "cwd": str(repo), **payload})))
    out, err = StringIO(), StringIO()
    code = publish.cmd_delivery(["--hook"] + (["--host", host] if host else []), out, err)
    assert code == 0
    return json.loads(out.getvalue() or "{}"), err.getvalue()


@pytest.mark.parametrize("host", [None, "claude", "codex"])
def test_premature_stop_and_repeat_disclose_actual_incompletion(delivery, monkeypatch, host):
    repo, _, calls, _, _ = delivery
    calls.remote_head = None
    result, feedback = stop(monkeypatch, repo, host=host)
    assert feedback == ""
    if host == "claude":
        assert set(result) == {"hookSpecificOutput"}
        assert result["hookSpecificOutput"]["hookEventName"] == "Stop"
        reason = result["hookSpecificOutput"]["additionalContext"]
    else:
        assert result["decision"] == "block"
        reason = result["reason"]
    assert "next:" in reason and "unpublished" in reason
    assert "If you are waiting for the user's answer or publication was withdrawn, " in reason
    assert "stop again and say so; otherwise: " in reason


@pytest.mark.parametrize("host", ["claude", "codex"])
def test_pause_metadata_only_suppresses_valid_pauses(delivery, monkeypatch, host):
    repo, _, calls, _, _ = delivery
    calls.remote_head = None
    original = publish.resolve_publish_executable
    def unexpected_lookup(*args):
        pytest.fail("paused Stop must not resolve tools or inspect delivery")
    monkeypatch.setattr(publish, "resolve_publish_executable", unexpected_lookup)
    assert stop(monkeypatch, repo, host=host, stop_hook_active=True) == ({}, "")
    for field in ("background_tasks", "session_crons"):
        if host == "claude":
            assert stop(monkeypatch, repo, host=host, **{field: [{"id": "task-1"}]}) == ({}, "")
    monkeypatch.setattr(publish, "resolve_publish_executable", original)
    for payload in ({"stop_hook_active": "true"}, {"stop_hook_active": 1},
                    *({field: value} for field in ("background_tasks", "session_crons")
                      for value in (None, [], {}, "task", [1], [{}], [{"id": ""}], [{"id": 1}], [{"id": "ok"}, None])),
                    *([{"background_tasks": [{"id": "task"}]}, {"session_crons": [{"id": "cron"}]}] if host == "codex" else [])):
        assert stop(monkeypatch, repo, host=host, **payload)[0]


def test_user_boundaries_and_irrelevant_hooks_can_stop(delivery, monkeypatch):
    repo, intent, calls, _, _ = delivery
    assert stop(monkeypatch, repo)[0] == {}  # published, awaiting acceptance
    before = len(calls.calls)
    for payload in ({"agent_id": "child"}, {"hook_event_name": "SubagentStop"}):
        assert stop(monkeypatch, repo, **payload)[0] == {}
    assert len(calls.calls) == before
    intent.write_text(intent.read_text().replace("publication:", "withdrawn:"))
    assert stop(monkeypatch, repo)[0] == {}
    git(repo, "restore", str(intent.relative_to(repo)))
    intent.write_text(intent.read_text().replace("# Change\n", "# Change\nkind: product\n"))
    spec = repo / "docs/loom/change/spec.md"
    spec.write_text("# Specification\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "product awaiting behavior confirmation")
    assert stop(monkeypatch, repo)[0] == {}


@pytest.mark.parametrize("host", ["claude", "codex"])
@pytest.mark.parametrize("failure", ["deadline", "unconfirmed", "exception"])
def test_single_total_deadline_is_unconfirmed_and_does_not_continue(delivery, monkeypatch, host, failure):
    repo, _, _, _, _ = delivery
    armed = []
    original = signal.setitimer
    monkeypatch.setattr(signal, "setitimer", lambda kind, seconds, *a: (
        armed.append(seconds), original(kind, seconds, *a))[1])
    def timeout(*args, **kwargs):
        assert signal.getsignal(signal.SIGALRM) != signal.SIG_DFL
        signal.raise_signal(signal.SIGALRM)
    if failure == "deadline":
        monkeypatch.setattr(publish.subprocess, "run", timeout)
    elif failure == "unconfirmed":
        monkeypatch.setattr(publish, "observe_delivery", lambda *a, **kw:
                            publish.DeliveryResult("unconfirmed", "missing evidence", "recover", {}))
    else:
        monkeypatch.setattr(publish, "observe_delivery", lambda *a, **kw: (_ for _ in ()).throw(OSError("missing")))
    result, feedback = stop(monkeypatch, repo, host=host)
    assert feedback == "" and set(result) == {"systemMessage"}
    feedback = result["systemMessage"]
    assert "unconfirmed" in feedback
    if failure == "deadline":
        assert "20" in feedback
    assert armed == [20, 0]
    if failure == "unconfirmed":
        assert "recover" in feedback
        return
    recovery = shlex.split(feedback.split("run ")[-1].split(" before claiming completion.")[0])
    assert Path(recovery[0]).is_absolute() and Path(recovery[0]).is_file()
    assert recovery[1:] == ["--ready", "delivery", "--json"]


@pytest.mark.parametrize("args", [["--host", "claude"], ["--hook", "--host", "unknown"],
                                  ["--hook", "--host"], ["--hook", "--json"]])
def test_invalid_host_mode_does_not_read_stdin(monkeypatch, args):
    monkeypatch.setattr(publish.sys, "stdin", None)
    out, err = StringIO(), StringIO()
    assert publish.cmd_delivery(args, out, err) == 2
    assert not out.getvalue() and err.getvalue()

