"""Read-only delivery evidence, using the existing publication fixtures."""
import json
import subprocess
from io import StringIO

import pytest
from loom_checker.command_handlers import publish
from test_loom_publish import ExternalCalls, git, publication_intent, repository, trusted_executable


@pytest.fixture
def delivery(tmp_path, monkeypatch):
    repo = repository(tmp_path)
    git(repo, "branch", "main")
    git(repo, "update-ref", "refs/remotes/origin/main", "main")
    git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    intent = publication_intent(repo, automatic=True)
    plan = repo / "docs/loom/change/plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# Plan\n## Task DAG\n**W1-01 Work** after: none acceptance: 1\n"
                    "- Files: `file.txt`, `new,file.py`\n", encoding="utf-8")
    (repo / "delta.py").write_text("committed branch delta")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "change")
    calls = ExternalCalls(git(repo, "rev-parse", "HEAD"))
    calls.remote_head = calls.head
    pr = {"html_url": "https://github.com/example/project/pull/1", "state": "open",
          "draft": False, "merged_at": None, "merge_commit_sha": None,
          "head": {"sha": calls.head, "ref": "feature", "repo": {"full_name": "example/project"}},
          "base": {"ref": "main", "repo": {"full_name": "example/project"}}}

    def external(argv, **kwargs):
        if "api" in argv and any("/pulls?" in part for part in argv):
            calls.calls.append(argv)
            return subprocess.CompletedProcess(argv, 0, json.dumps([pr] if pr else []), "")
        return calls(argv, **kwargs)

    monkeypatch.chdir(repo)
    monkeypatch.setattr(publish, "run_publish_external", external)
    monkeypatch.setattr(publish, "resolve_publish_executable", trusted_executable)

    def observe(*args):
        out, err = StringIO(), StringIO()
        code = publish.cmd_delivery(["--json", *args], out, err)
        assert not err.getvalue()
        result = json.loads(out.getvalue())
        assert result["reason"] and result["next"] and isinstance(result["evidence"], dict)
        assert not any(set(call) & {"push", "create", "edit", "merge", "fetch"}
                       for call in calls.calls)
        return code, result

    return repo, intent, calls, pr, observe


def test_matching_remote_pr(delivery):
    repo, _, calls, pr, observe = delivery
    git(repo, "tag", "feature")
    code, result = observe()
    assert code == 0 and result["state"] == "published" and result["complete"]
    assert result["evidence"]["pr"] == pr["html_url"]
    assert sum("checks" in call for call in calls.calls) == 1
    pr.update(state="closed", merged_at="2026-11-09T00:00:00Z", merge_commit_sha="a" * 40)
    code, result = observe("--goal", "merged")
    assert code == 0 and result["state"] == "merged" and result["complete"]
    assert result["evidence"]["merge_sha"] == "a" * 40


def test_newer_local_head(delivery):
    repo, _, _, pr, observe = delivery
    pr.update(state="closed", merged_at="2026-11-09T00:00:00Z", merge_commit_sha="a" * 40)
    git(repo, "commit", "--allow-empty", "-qm", "newer local work")
    code, result = observe()
    assert code == 1 and result["state"] == "unpublished" and not result["complete"]


def test_local_without_network(delivery):
    repo, _, calls, _, observe = delivery
    (repo / "unrelated.txt").write_text("preserve me")
    code, result = observe("--goal", "local")
    assert code == 0 and result["state"] == "local" and result["complete"]
    assert calls.calls == []


def test_missing_authorization(delivery):
    repo, intent, calls, pr, observe = delivery
    intent.write_text(intent.read_text().replace(
        "publication: automatic — authorized 2026-09-09 by Test\n", ""))
    code, result = observe()
    assert code == 1 and result["state"] == "uncommitted" and not result["complete"]
    git(repo, "add", "docs/loom/intent/change.md")
    git(repo, "commit", "-qm", "legacy publication without automatic authorization")
    calls.head = calls.remote_head = pr["head"]["sha"] = git(repo, "rev-parse", "HEAD")
    code, result = observe()
    assert code == 0 and result["state"] == "published" and result["complete"]
    assert result["evidence"]["automatic_publication_authorized"] is False
    pr.update(state="closed", merged_at="2026-11-09T00:00:00Z", merge_commit_sha="a" * 40)
    code, result = observe("--goal", "merged")
    assert code == 0 and result["state"] == "merged" and result["complete"]
    assert result["evidence"]["automatic_publication_authorized"] is False
    assert "publication:" not in intent.read_text()


def test_missing_pr_without_automatic_grant(delivery):
    repo, intent, calls, pr, observe = delivery
    publication_intent(repo, automatic=False)
    git(repo, "add", "docs/loom/intent/change.md")
    git(repo, "commit", "-qm", "legacy intent")
    calls.head = calls.remote_head = git(repo, "rev-parse", "HEAD")
    pr.clear()
    code, result = observe()
    assert code == 1 and result["state"] == "missing_pr" and not result["complete"]
    assert result["evidence"]["automatic_publication_authorized"] is False
    assert "explicit user decision" in result["next"] and "otherwise" in result["next"]
    assert "--confirm-authorized" in result["next"] and "intent" not in result["next"]
    assert "publication:" not in intent.read_text()


def test_checks_pass(delivery):
    _, _, calls, _, observe = delivery
    calls.required_checks = [[]]
    code, result = observe()
    assert code == 0 and result["complete"]
    assert result["evidence"]["checks"] == "empty"
    assert "no required checks" in result["reason"].lower()


def test_failed_json(delivery):
    _, _, calls, _, observe = delivery
    calls.required_checks = [[{"name": "gate", "state": "FAILURE", "bucket": "fail"}]]
    calls.required_check_returncodes = [1]
    code, result = observe()
    assert code == 1 and result["state"] == "failed" and not result["complete"]
    assert "gate" in result["reason"] and "fix" in result["next"].lower()


def test_actionable_result(delivery):
    repo, _, calls, _, observe = delivery
    (repo / "new,file.py").write_text("untracked scoped work")
    (repo / "delta.py").unlink()
    (repo / "file.txt").write_text("staged scoped work")
    git(repo, "add", "file.txt")
    code, result = observe("--goal", "local")
    assert code == 1 and result["state"] == "uncommitted" and not result["complete"]
    assert "new,file.py" in result["evidence"]["pending_paths"]
    assert {"delta.py", "file.txt"} <= set(result["evidence"]["pending_paths"])
    assert "commit" in result["next"].lower() and calls.calls == []


def test_unavailable_remote(delivery, monkeypatch):
    def unavailable(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 30)

    monkeypatch.setattr(publish, "run_publish_external", unavailable)
    code, result = delivery[-1]()
    assert code == 1 and result["state"] == "unconfirmed" and not result["complete"]
    assert "diagnostic" in result["next"].lower()
