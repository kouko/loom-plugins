"""`land --accepted-by` merge preconditions (plan W2-01, spec REQ-2, REQ-3).

Every git and gh network call goes through `land.run_land_external`, which a
fake replaces here; waits go through `land.wait_land_interval`, recorded
instead of slept, so polling cases are instant.
"""
from __future__ import annotations

import json
import subprocess
from io import StringIO
from pathlib import Path

from loom_checker.command_handlers import land

ACCEPTANCE_BLOCK = (
    "BLOCK land.merge: blind-run acceptance not recorded; "
    "pass --accepted-by <name> after the maintainer accepts\n"
)
PASS = {"name": "gate", "state": "SUCCESS", "bucket": "pass"}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def change_repository(tmp_path: Path, *, publication: str = "") -> Path:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "branch", "-M", "main")
    git(repo, "switch", "-q", "-c", "feature")
    git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    intent = repo / "docs" / "loom" / "intent" / "change.md"
    intent.parent.mkdir(parents=True)
    intent.write_text(
        "# Change\noriginator: kouko\nstatus: confirmed 2026-09-14\n"
        f"{publication}\n## Proposed outcome\nLand it.\n",
        encoding="utf-8",
    )
    attestation = repo / "docs" / "loom" / "change" / "attestation.json"
    attestation.parent.mkdir(parents=True)
    attestation.write_text(json.dumps({"change_id": "change"}), encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "change")
    return repo


class LandCalls:
    def __init__(self, head: str) -> None:
        self.head = head
        self.pr_head = head
        self.checks: list[list[dict] | str] = [[PASS]]
        self.check_returncodes: list[int] = []
        self.merge_states: list[dict] = [{"mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN"}]
        self.calls: list[list[str]] = []
        self.timeouts: list[int] = []

    def __call__(self, argv, timeout, **kwargs):
        argv = [str(value) for value in argv]
        self.calls.append(argv)
        self.timeouts.append(timeout)
        if "merge" in argv:
            raise AssertionError(f"merge issued during preconditions: {argv}")
        if "repo" in argv and "view" in argv:
            return subprocess.CompletedProcess(argv, 0, "main\n", "")
        if "api" in argv and any("/pulls?" in token for token in argv):
            prs = [{
                "number": 7,
                "html_url": "https://github.com/example/project/pull/7",
                "head": {"sha": self.pr_head, "repo": {"full_name": "example/project"}},
                "base": {"ref": "main", "repo": {"full_name": "example/project"}},
            }]
            return subprocess.CompletedProcess(argv, 0, json.dumps(prs), "")
        if "pr" in argv and "checks" in argv:
            snapshot = self.checks.pop(0) if len(self.checks) > 1 else self.checks[0]
            code = self.check_returncodes.pop(0) if self.check_returncodes else 0
            text = snapshot if isinstance(snapshot, str) else json.dumps(snapshot)
            return subprocess.CompletedProcess(argv, code, text, "")
        if "pr" in argv and "view" in argv:
            state = self.merge_states.pop(0) if len(self.merge_states) > 1 else self.merge_states[0]
            return subprocess.CompletedProcess(argv, 0, json.dumps(state), "")
        raise AssertionError(argv)


def invoke(tmp_path: Path, monkeypatch, *args: str, publication: str = "",
           configure=None):
    repo = change_repository(tmp_path, publication=publication)
    calls = LandCalls(git(repo, "rev-parse", "HEAD"))
    if configure:
        configure(calls)
    waits: list[float] = []
    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", calls)
    monkeypatch.setattr(land, "wait_land_interval", waits.append)
    monkeypatch.setattr(land, "_cmd_push", lambda *a, **k: 0)
    monkeypatch.setattr(
        land, "resolve_publish_executable",
        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh",
    )
    out, err = StringIO(), StringIO()
    rc = land.cmd_land(list(args), out, err)
    return rc, out.getvalue(), err.getvalue(), calls, waits


def no_merge(calls: LandCalls) -> bool:
    return not any("merge" in call for call in calls.calls)


# A3 positive: originator-name-passes
def test_originator_name_passes(tmp_path: Path, monkeypatch) -> None:
    rc, out, err, calls, _ = invoke(tmp_path, monkeypatch, "--accepted-by", "kouko")

    assert rc == 0, err
    assert "Preconditions passed for PR #7\n" in out
    assert no_merge(calls)
    assert set(calls.timeouts) == {30}


def test_publication_authorizer_name_passes(tmp_path: Path, monkeypatch) -> None:
    rc, out, err, _, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "Maintainer Name",
        publication="publication: automatic — authorized 2026-09-14 by Maintainer Name\n",
    )

    assert rc == 0, err
    assert "Preconditions passed for PR #7\n" in out


# A3 negative: missing-or-foreign-name-blocks
def test_missing_or_foreign_name_blocks(tmp_path: Path, monkeypatch) -> None:
    for index, args in enumerate(([], ["--accepted-by", "stranger"])):
        rc, out, err, calls, _ = invoke(tmp_path / str(index), monkeypatch, *args)

        assert rc == 1, args
        assert err == ACCEPTANCE_BLOCK, args
        assert calls.calls == [], args


# A2 positive: failing-nonrequired-check-blocks
def test_failing_nonrequired_check_blocks(tmp_path: Path, monkeypatch) -> None:
    def configure(calls: LandCalls) -> None:
        calls.checks = [[
            PASS,
            {"name": "lint", "state": "FAILURE", "bucket": "fail"},
            {"name": "docs", "state": "CANCELLED", "bucket": "cancel"},
        ]]
        calls.check_returncodes = [1]

    rc, _, err, calls, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 1
    assert "BLOCK land.merge: check lint: FAILURE\n" in err
    assert "BLOCK land.merge: check docs: CANCELLED\n" in err
    assert "gate" not in err
    checks_call = next(call for call in calls.calls if "checks" in call)
    assert "--required" not in checks_call
    assert no_merge(calls)


# A2 negative: unstable-state-blocks
def test_unstable_state_blocks(tmp_path: Path, monkeypatch) -> None:
    def configure(calls: LandCalls) -> None:
        calls.merge_states = [{"mergeable": "MERGEABLE", "mergeStateStatus": "UNSTABLE"}]

    rc, out, err, calls, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 1
    assert err == "BLOCK land.merge: PR #7 is UNSTABLE\n"
    assert "Preconditions passed" not in out
    assert no_merge(calls)


def test_pending_checks_are_polled_until_they_pass(tmp_path: Path, monkeypatch) -> None:
    pending = {"name": "gate", "state": "IN_PROGRESS", "bucket": "pending"}

    def configure(calls: LandCalls) -> None:
        calls.checks = [[pending], [pending], [PASS]]
        calls.check_returncodes = [8, 8, 0]

    rc, out, err, calls, waits = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 0, err
    assert out.count("Waiting for checks on PR #7\n") == 1
    assert waits == [10, 10]
    assert sum("checks" in call for call in calls.calls) == 3


def test_unknown_merge_state_is_reread_until_mergeable(tmp_path: Path, monkeypatch) -> None:
    def configure(calls: LandCalls) -> None:
        calls.merge_states = [
            {"mergeable": "UNKNOWN", "mergeStateStatus": "UNKNOWN"},
            {"mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN"},
        ]

    rc, out, err, calls, waits = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 0, err
    assert "Preconditions passed for PR #7\n" in out
    assert len(waits) == 1


def test_unknown_merge_state_past_sixty_seconds_blocks(tmp_path: Path, monkeypatch) -> None:
    def configure(calls: LandCalls) -> None:
        calls.merge_states = [{"mergeable": "UNKNOWN", "mergeStateStatus": "UNKNOWN"}]

    rc, _, err, _, waits = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 1
    assert err == "BLOCK land.merge: PR #7 is UNKNOWN\n"
    assert sum(waits) <= 60


def test_pr_head_other_than_head_blocks(tmp_path: Path, monkeypatch) -> None:
    def configure(calls: LandCalls) -> None:
        calls.pr_head = "f" * 40

    rc, _, err, calls, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 1
    assert err.startswith("BLOCK land.merge: ")
    assert not any("checks" in call for call in calls.calls)


def test_invalid_attestation_blocks_before_github(tmp_path: Path, monkeypatch) -> None:
    repo = change_repository(tmp_path)
    calls = LandCalls(git(repo, "rev-parse", "HEAD"))
    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", calls)
    monkeypatch.setattr(land, "_cmd_push", lambda *a, **k: 1)
    monkeypatch.setattr(
        land, "resolve_publish_executable",
        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh",
    )

    rc = land.cmd_land(["--accepted-by", "kouko"], StringIO(), StringIO())

    assert rc == 1
    assert calls.calls == []
