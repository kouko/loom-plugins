"""Documented Stop framing around the same single-shot delivery observer."""
import json
import signal
from io import StringIO

from loom_checker.command_handlers import publish
from test_delivery import delivery
from test_loom_publish import git


def stop(monkeypatch, repo, **payload):
    monkeypatch.setattr(publish.sys, "stdin", StringIO(json.dumps(
        {"hook_event_name": "Stop", "cwd": str(repo), **payload})))
    out, err = StringIO(), StringIO()
    code = publish.cmd_delivery(["--hook"], out, err)
    assert code == 0
    return json.loads(out.getvalue() or "{}"), err.getvalue()


def test_premature_stop_and_repeat_disclose_actual_incompletion(delivery, monkeypatch):
    repo, _, calls, _, _ = delivery
    calls.remote_head = None
    result, _ = stop(monkeypatch, repo)
    assert result["decision"] == "block"
    assert "next:" in result["reason"] and "unpublished" in result["reason"]
    assert "If you are waiting for the user's answer or publication was withdrawn, " in result["reason"]
    assert "stop again and say so; otherwise: " in result["reason"]
    result, feedback = stop(monkeypatch, repo, stop_hook_active=True)
    assert "decision" not in result
    assert "incomplete" in feedback and "next:" in feedback


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


def test_single_total_deadline_is_unconfirmed_and_does_not_continue(delivery, monkeypatch):
    repo, _, _, _, _ = delivery
    armed = []
    original = signal.setitimer
    monkeypatch.setattr(signal, "setitimer", lambda kind, seconds, *a: (
        armed.append(seconds), original(kind, seconds, *a))[1])
    def timeout(*args, **kwargs):
        assert signal.getsignal(signal.SIGALRM) != signal.SIG_DFL
        signal.raise_signal(signal.SIGALRM)
    monkeypatch.setattr(publish.subprocess, "run", timeout)
    result, feedback = stop(monkeypatch, repo)
    assert result == {} and "unconfirmed" in feedback and "20" in feedback
    assert armed == [20, 0]

