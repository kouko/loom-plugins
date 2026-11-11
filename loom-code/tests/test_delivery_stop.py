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
import test_verification_status as verification_fixtures


@pytest.fixture
def reviewed_delivery(delivery, monkeypatch):
    repo, _, calls, pr, _ = delivery
    monkeypatch.setattr(verification_fixtures, "CHANGE", "change")
    verification_fixtures.write(repo, "src.py", "VALUE = 1\n")
    verification_fixtures.write(repo, "docs/loom/KICKOFF-DEFAULTS.md",
                                "- package-tests: python3 -m pytest -q — fixture (2026-09-22)\n")
    verification_fixtures.commit(repo, "reviewed work")
    verification_fixtures.commit_attestation(repo, verification_fixtures.attestation(repo),
                                            "docs/loom/change/attestation.json")
    assert publish.verification_status(repo, "change") == "valid"
    calls.head = calls.remote_head = pr["head"]["sha"] = git(repo, "rev-parse", "HEAD")
    return delivery


def stop(monkeypatch, repo, host=None, **payload):
    monkeypatch.setattr(publish.sys, "stdin", StringIO(json.dumps(
        {"hook_event_name": "Stop", "cwd": str(repo), **payload})))
    out, err = StringIO(), StringIO()
    code = publish.cmd_delivery(["--hook"] + (["--host", host] if host else []), out, err)
    assert code == 0
    return json.loads(out.getvalue() or "{}"), err.getvalue()


@pytest.mark.parametrize("host", [None, "claude", "codex"])
def test_premature_stop_and_repeat_disclose_actual_incompletion(reviewed_delivery, monkeypatch, host):
    repo, _, calls, _, _ = reviewed_delivery
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
def test_pause_metadata_only_suppresses_valid_pauses(reviewed_delivery, monkeypatch, host):
    repo, _, calls, _, _ = reviewed_delivery
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


def test_user_boundaries_and_irrelevant_hooks_can_stop(reviewed_delivery, monkeypatch):
    repo, intent, calls, _, _ = reviewed_delivery
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
def test_single_total_deadline_is_unconfirmed_and_does_not_continue(reviewed_delivery, monkeypatch, host, failure):
    repo, _, _, _, _ = reviewed_delivery
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


@pytest.mark.parametrize("host", ["claude", "codex"])
@pytest.mark.parametrize("state", ["absent", "skip", "stale", "pending"])
def test_unready_work_stops_before_remote(reviewed_delivery, monkeypatch, host, state):
    repo, _, calls, _, _ = reviewed_delivery
    calls.remote_head = None
    if state in {"absent", "skip"}:
        (repo / "docs/loom/change/attestation.json").unlink()
        if state == "skip":
            plan = repo / "docs/loom/change/plan.md"
            plan.write_text(plan.read_text() + "\nskipped-by-instruction: closing-review 2026-11-11\n")
        verification_fixtures.commit(repo, "no verification")
    else:
        (repo / "src.py").write_text("VALUE = 2\n")
        if state == "stale":
            verification_fixtures.commit(repo, "new unreviewed work")
    assert publish.verification_status(repo, "change").startswith(
        "valid" if state == "pending" else "stale" if state == "stale" else "absent")
    assert stop(monkeypatch, repo, host=host) == ({}, "")
    assert calls.calls == []


@pytest.mark.parametrize("host", ["claude", "codex"])
@pytest.mark.parametrize("phase", ["verification", "local", "published", "pending"])
def test_changed_head_cannot_continue(reviewed_delivery, monkeypatch, host, phase):
    repo, _, calls, _, _ = reviewed_delivery
    calls.remote_head = None
    name = "verification_status" if phase == "verification" else "observe_delivery"
    original = getattr(publish, name)
    def change_after_read(*args, **kwargs):
        if phase == "pending" and kwargs["goal"] == "published":
            (repo / "src.py").write_text("VALUE = 2\n")
        result = original(*args, **kwargs)
        if phase == "verification" or kwargs["goal"] == phase:
            (repo / "src.py").write_text("VALUE = 2\n")
            verification_fixtures.commit(repo, "concurrent work")
        return result
    monkeypatch.setattr(publish, name, change_after_read)
    result, feedback = stop(monkeypatch, repo, host=host)
    if phase == "pending":
        assert (result, feedback) == ({}, "")
        return
    assert not feedback and set(result) == {"systemMessage"}
    assert "unconfirmed" in result["systemMessage"]
    if phase != "published":
        assert calls.calls == []


@pytest.mark.parametrize("args", [["--host", "claude"], ["--hook", "--host", "unknown"],
                                  ["--hook", "--host"], ["--hook", "--json"]])
def test_invalid_host_mode_does_not_read_stdin(monkeypatch, args):
    monkeypatch.setattr(publish.sys, "stdin", None)
    out, err = StringIO(), StringIO()
    assert publish.cmd_delivery(args, out, err) == 2
    assert not out.getvalue() and err.getvalue()

