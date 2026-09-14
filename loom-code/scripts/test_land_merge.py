"""`land --accepted-by` merge preconditions, squash merge and verification
(plan W2-01, W2-02; spec REQ-1..REQ-4).

Every git and gh network call goes through `land.run_land_external`, which a
fake replaces here; waits go through `land.wait_land_interval`, recorded
instead of slept, so polling cases are instant.
"""
from __future__ import annotations

import json
import re
import stat
import subprocess
from io import StringIO
from pathlib import Path

from loom_checker.command_handlers import land

ACCEPTANCE_BLOCK = (
    "BLOCK land.merge: blind-run acceptance not recorded; "
    "pass --accepted-by <name> after the maintainer accepts\n"
)
PASS = {"name": "gate", "state": "SUCCESS", "bucket": "pass"}
MERGE_OID = "a1b2c3d" + "0" * 33
PR_TITLE = "Land merged changes"
PR_BODY = "## Summary\nLands the change.\n\n- item one\n"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def change_repository(tmp_path: Path, *, publication: str = "", prepare=None) -> Path:
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
    if prepare:
        prepare(repo)
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
        self.pr_title = PR_TITLE
        self.pr_body = PR_BODY
        self.merge_outcome: subprocess.TimeoutExpired | tuple[int, str] = (0, "")
        self.pr_states: list[dict] = [{"state": "MERGED", "mergeCommit": {"oid": MERGE_OID}}]
        self.body_file_text: str | None = None
        self.body_file_mode: int | None = None
        self.commit_message = None  # None: echo the merge subject and body file

    def merge_calls(self) -> list[list[str]]:
        return [call for call in self.calls if call[1:3] == ["pr", "merge"]]

    def __call__(self, argv, timeout, **kwargs):
        argv = [str(value) for value in argv]
        self.calls.append(argv)
        self.timeouts.append(timeout)
        if argv[1:3] == ["pr", "merge"]:
            body_file = Path(argv[argv.index("--body-file") + 1])
            self.body_file_text = body_file.read_text(encoding="utf-8")
            self.body_file_mode = stat.S_IMODE(body_file.stat().st_mode)
            if isinstance(self.merge_outcome, subprocess.TimeoutExpired):
                raise self.merge_outcome
            code, stderr = self.merge_outcome
            return subprocess.CompletedProcess(argv, code, "", stderr)
        if argv[1:2] == ["fetch"]:
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[1:2] == ["cat-file"]:
            message = self.commit_message
            if message is None:
                merge = self.merge_calls()[-1]
                message = f"{merge[merge.index('--subject') + 1]}\n\n{self.body_file_text}"
            header = "tree " + "0" * 40 + "\nauthor A <a@example.com> 1 +0000\n\n"
            return subprocess.CompletedProcess(argv, 0, header + message, "")
        if "pr" in argv and "view" in argv and "title,body" in argv:
            payload = {"title": self.pr_title, "body": self.pr_body}
            return subprocess.CompletedProcess(argv, 0, json.dumps(payload), "")
        if "pr" in argv and "view" in argv and "state,mergeCommit" in argv:
            state = self.pr_states.pop(0) if len(self.pr_states) > 1 else self.pr_states[0]
            return subprocess.CompletedProcess(argv, 0, json.dumps(state), "")
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
           configure=None, prepare=None):
    repo = change_repository(tmp_path, publication=publication, prepare=prepare)
    calls = LandCalls(git(repo, "rev-parse", "HEAD"))
    if configure:
        configure(calls)
    waits: list[float] = []
    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", calls)
    monkeypatch.setattr(land, "wait_land_interval", waits.append)
    monkeypatch.setattr(land, "_cmd_push", lambda *a, **k: 0)
    # Trunk sync and cleanup after the merge are covered by test_land_cleanup.py.
    monkeypatch.setattr(land, "_sync_and_clean", lambda *a, **k: 0)
    monkeypatch.setattr(
        land, "resolve_publish_executable",
        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh",
    )
    out, err = StringIO(), StringIO()
    rc = land.cmd_land(list(args), out, err)
    return rc, out.getvalue(), err.getvalue(), calls, waits


def no_merge(calls: LandCalls) -> bool:
    return not calls.merge_calls()


# A3 positive: originator-name-passes
def test_originator_name_passes(tmp_path: Path, monkeypatch) -> None:
    rc, out, err, calls, _ = invoke(tmp_path, monkeypatch, "--accepted-by", "kouko")

    assert rc == 0, err
    assert "Merged PR #7 as a1b2c3d\n" in out
    merge_index = calls.calls.index(calls.merge_calls()[0])
    assert set(calls.timeouts[:merge_index]) == {30}
    assert calls.timeouts[merge_index] == 300


def test_publication_authorizer_name_passes(tmp_path: Path, monkeypatch) -> None:
    rc, out, err, calls, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "Maintainer Name",
        publication="publication: automatic — authorized 2026-09-14 by Maintainer Name\n",
    )

    assert rc == 0, err
    assert "Merged PR #7 as a1b2c3d\n" in out
    assert re.search(r"^Accepted-by: Maintainer Name \d{4}-\d{2}-\d{2}$",
                     calls.body_file_text, re.MULTILINE)


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
    assert "Merged PR" not in out
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


def test_empty_checks_output_blocks(tmp_path: Path, monkeypatch) -> None:
    """gh exiting 0 with blank stdout is an unobserved check state, not 'no checks'."""
    def configure(calls: LandCalls) -> None:
        calls.checks = [" \n"]
        calls.check_returncodes = [0]

    rc, out, err, calls, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 1
    assert err == "BLOCK land.merge: checks on PR #7 could not be observed\n"
    assert "Merged PR" not in out
    assert no_merge(calls)


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
    assert "Merged PR #7 as a1b2c3d\n" in out
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


# A1 positive: accepted-green-pr-merges-with-match-head
def test_accepted_green_pr_merges_with_match_head(tmp_path: Path, monkeypatch) -> None:
    rc, out, err, calls, _ = invoke(tmp_path, monkeypatch, "--accepted-by", "kouko")

    assert rc == 0, err
    assert err == ""
    [merge] = calls.merge_calls()
    body_file = merge[merge.index("--body-file") + 1]
    assert merge == [
        "/usr/local/bin/gh", "pr", "merge", "7", "--squash",
        "--match-head-commit", calls.head,
        "--subject", f"{PR_TITLE} (#7)", "--body-file", body_file,
    ]
    assert not {"--admin", "--auto", "--delete-branch"} & set(merge)
    assert not Path(body_file).exists()
    assert out.count("Merged PR #7 as a1b2c3d\n") == 1
    assert ["/usr/bin/git", "fetch", "origin", "main"] in calls.calls
    fetch_index = calls.calls.index(["/usr/bin/git", "fetch", "origin", "main"])
    assert calls.timeouts[fetch_index] == 300
    assert ["/usr/bin/git", "cat-file", "commit", MERGE_OID] in calls.calls


# A1 negative: merge-timeout-still-open-blocks
def test_merge_timeout_still_open_blocks(tmp_path: Path, monkeypatch) -> None:
    outcomes = (
        subprocess.TimeoutExpired(["gh"], 300),
        (1, "GraphQL: Head branch was modified. Review and try the merge again."),
    )
    for index, outcome in enumerate(outcomes):
        def configure(calls: LandCalls, outcome=outcome) -> None:
            calls.merge_outcome = outcome
            calls.pr_states = [{"state": "OPEN", "mergeCommit": None}]

        rc, out, err, calls, waits = invoke(
            tmp_path / str(index), monkeypatch, "--accepted-by", "kouko", configure=configure
        )

        assert rc == 1, outcome
        assert err.startswith("BLOCK land.merge: merge not performed: "), err
        assert err.count("\n") == 1, err
        if isinstance(outcome, tuple):
            assert outcome[1] in err
        assert "Merged PR" not in out
        state_reads = [call for call in calls.calls if "state,mergeCommit" in call]
        assert len(state_reads) > 1
        assert 0 < sum(waits) <= 60
        assert not any(call[1:2] in (["fetch"], ["cat-file"]) for call in calls.calls)


def test_merge_nonzero_but_reread_merged_continues_to_verify(
    tmp_path: Path, monkeypatch
) -> None:
    def configure(calls: LandCalls) -> None:
        calls.merge_outcome = (1, "connection reset")
        calls.pr_states = [
            {"state": "OPEN", "mergeCommit": None},
            {"state": "MERGED", "mergeCommit": {"oid": MERGE_OID}},
        ]

    rc, out, err, calls, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 0, err
    assert "merge not performed" not in err
    assert "Merged PR #7 as a1b2c3d\n" in out
    assert ["/usr/bin/git", "cat-file", "commit", MERGE_OID] in calls.calls


# A4 positive: body-file-carries-body-and-accepted-by
def test_body_file_carries_body_and_accepted_by(tmp_path: Path, monkeypatch) -> None:
    rc, _, err, calls, _ = invoke(tmp_path / "plain", monkeypatch, "--accepted-by", "kouko")

    assert rc == 0, err
    assert calls.body_file_mode == 0o600
    match = re.fullmatch(
        re.escape(PR_BODY) + r"\nAccepted-by: kouko (\d{4}-\d{2}-\d{2})\n?",
        calls.body_file_text,
    )
    assert match, calls.body_file_text

    def commit_report(repo: Path) -> None:
        report = repo / "docs" / "loom" / "change" / "blind-run-report.md"
        report.write_text("# Blind run\nAll accepted.\n", encoding="utf-8")

    rc, _, err, calls, _ = invoke(
        tmp_path / "report", monkeypatch, "--accepted-by", "kouko", prepare=commit_report
    )

    assert rc == 0, err
    repo = tmp_path / "report" / "repo"
    blob = git(repo, "rev-parse", "HEAD:docs/loom/change/blind-run-report.md")
    assert calls.body_file_mode == 0o600
    assert re.fullmatch(
        re.escape(PR_BODY)
        + r"\nAccepted-by: kouko \d{4}-\d{2}-\d{2} \(blind-run-report "
        + blob[:7] + r"\)\n?",
        calls.body_file_text,
    ), calls.body_file_text


def test_body_whitespace_runs_are_normalized_in_verification(
    tmp_path: Path, monkeypatch
) -> None:
    def configure(calls: LandCalls) -> None:
        calls.commit_message = (
            f"{PR_TITLE} (#7)\n\n## Summary\n\nLands   the change.\n- item one\n"
        )

    rc, out, err, _, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 0, err
    assert "Merged PR #7 as a1b2c3d\n" in out


# A4 negative: title-only-commit-verify-blocks
def test_title_only_commit_verify_blocks(tmp_path: Path, monkeypatch) -> None:
    def configure(calls: LandCalls) -> None:
        calls.commit_message = f"{PR_TITLE} (#7)\n"

    rc, out, err, _, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 1
    assert out.endswith("Merged PR #7 as a1b2c3d\n"), out
    assert err == "BLOCK land.verify: squash commit lacks the PR body\n"


def test_body_only_commit_verify_blocks_on_title(tmp_path: Path, monkeypatch) -> None:
    def configure(calls: LandCalls) -> None:
        calls.commit_message = f"Other subject\n\n{PR_BODY}"

    rc, out, err, _, _ = invoke(
        tmp_path, monkeypatch, "--accepted-by", "kouko", configure=configure
    )

    assert rc == 1
    assert "Merged PR #7 as a1b2c3d\n" in out
    assert err == "BLOCK land.verify: squash commit lacks the PR title\n"
