"""Adversarial probes for the push hook's attestation-reason ordering.

``command_handlers/push.py`` now runs a read-only attestation check
(``attestation_reason``) before printing a refspec refusal. These probes try to
make that extra path turn a block into an allow, write into the repository,
follow a hostile ``-C`` into the wrong repository, crash, hang, or leak noise
ahead of the BLOCK lines. Subprocess probes run the real checker CLI the way a
host hook does; in-process probes reuse the attested-branch monkeypatch.
A failing probe is a finding against the change.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from io import StringIO
from pathlib import Path

import pytest

from loom_checker.command_handlers import push as push_handler

SCRIPTS = Path(__file__).resolve().parent
CHECKER = SCRIPTS / "loom_checker.py"
FOUND_ZERO = (
    "BLOCK push.attestation: branch must carry exactly one generated attestation; found 0"
    "; two legal routes, both run by the agent: run the closing-review station,"
    " which generates the attestation and needs no confirmation, so it is open"
    " in every session; or, in a session that can record a confirmation the user"
    " types, propose a step selection"
    " (`loom_checker.py selection propose <change-id> --origin agent --skip reviewers`)"
    " that the user confirms by typing `/loom-code:expert-mode <code>` with the code"
    " the proposal printed, after which finalize-review drops the reviewer floor to"
    " zero and still emits an attestation recording the skip;"
    " never hand the blocked publication command to the user to run"
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def _repo(root: Path, name: str, *, attestations: int = 0) -> Path:
    repo = root / name
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "switch", "-q", "-c", "feature")
    _git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    for index in range(attestations):
        target = repo / "docs" / "loom" / f"change{index}" / "attestation.json"
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps({"change_id": f"change{index}"}), encoding="utf-8")
    if attestations:
        _git(repo, "add", ".")
        _git(repo, "commit", "-q", "-m", "attest")
    return repo


def _hook(command: str, cwd: Path, *, env: dict | None = None, timeout: int = 60):
    payload = {"cwd": str(cwd), "hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": command}}
    result = subprocess.run([sys.executable, str(CHECKER), "push", "--hook"],
                            input=json.dumps(payload), capture_output=True, text=True,
                            cwd=str(cwd), env=env, timeout=timeout)
    return result.returncode, result.stderr


def _snapshot(repo: Path) -> tuple:
    files = sorted(str(p.relative_to(repo)) for p in repo.rglob("*")
                   if ".git" not in p.relative_to(repo).parts)
    refs = _git(repo, "for-each-ref", "--format=%(refname) %(objectname)")
    return files, refs, _git(repo, "status", "--porcelain"), _git(repo, "rev-parse", "HEAD")


HOSTILE = [
    "bash -c 'git push origin feature'",
    "env FOO=1 git push origin feature",
    "FOO=1 git push origin feature",
    "git -c core.sshCommand=true push origin feature",
    "git push --force origin feature",
    "git push --mirror origin",
    "git push origin feature main HEAD:refs/heads/x",
    "git push git@github.com:example/project.git feature",
    "GIT_DIR=/nonexistent git push origin feature",
    "git --git-dir=.git push origin feature",
    "git push origin " + "a" * 200_000,
    "git push origin \"unterminated",
    "git -C /tmp/\udcff\udcfe push origin feature",
    "git -C ../relative push origin feature",
]
# Short ids: pytest exports the node id via PYTEST_CURRENT_TEST, and Linux
# rejects any single environment string over 131072 bytes (E2BIG) for every
# child process, so a 200 KB parameter must never become part of the id.
HOSTILE_IDS = [
    "bash-c", "env-prefix", "assignment-prefix", "git-c-config", "force", "mirror",
    "multiple-refspecs", "remote-url", "git-dir-env", "git-dir-option", "200kb-refspec",
    "unterminated-quote", "non-utf8-dash-c", "relative-dash-c",
]


def test_push_reason_probe_ids_short_under_limit():
    """Every parametrize id in this file stays under 1000 characters."""
    assert len(HOSTILE_IDS) == len(HOSTILE)
    ids = []
    for value in list(globals().values()):
        for mark in getattr(value, "pytestmark", []):
            if mark.name != "parametrize":
                continue
            explicit = mark.kwargs.get("ids")
            ids.extend(explicit if explicit is not None else [str(v) for v in mark.args[1]])
    assert ids and all(len(i) < 1000 for i in ids), [len(i) for i in ids]


@pytest.mark.parametrize("command", HOSTILE, ids=HOSTILE_IDS)
def test_push_hook_hostile_variant_unattested_blocks(tmp_path, command):
    """Every hostile push variant exits 2 and every stderr line is a BLOCK line."""
    repo = _repo(tmp_path, "repo")
    rc, err = _hook(command, repo)
    assert rc == 2, err
    assert err.strip(), "a refusal must carry a reason"
    assert all(line.startswith("BLOCK ") for line in err.splitlines()), err


@pytest.mark.parametrize("command", HOSTILE, ids=HOSTILE_IDS)
def test_push_hook_hostile_variant_attested_blocks(tmp_path, monkeypatch, command):
    """With a (monkeypatched) valid attestation, no hostile variant becomes an allow."""
    repo = _repo(tmp_path, "repo", attestations=1)
    monkeypatch.setattr(push_handler, "validate_attestation", lambda *_a, **_k: [])
    payload = {"cwd": str(repo), "hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": command}}
    monkeypatch.setattr(push_handler, "read_hook_payload", lambda: payload)
    monkeypatch.chdir(repo)
    err = StringIO()
    rc = push_handler.cmd_push(["--hook"], StringIO(), err)
    assert rc == 2, err.getvalue()
    assert not err.getvalue().startswith(FOUND_ZERO)


def test_push_hook_reason_path_repository_unchanged(tmp_path):
    """The read-only reason path writes no file, ref, index entry or HEAD move."""
    repo = _repo(tmp_path, "repo", attestations=2)
    (repo / "untracked.txt").write_text("u\n", encoding="utf-8")
    before = _snapshot(repo)
    rc, err = _hook("git push origin feature", repo)
    assert rc == 2
    assert "found 2" in err.splitlines()[0]
    assert _snapshot(repo) == before


def test_push_hook_dash_c_other_repo_reports_target_repo(tmp_path):
    """-C into another repo: the reason describes the pushed repo, not the host cwd."""
    host = _repo(tmp_path, "host", attestations=2)
    target = _repo(tmp_path, "target")
    rc, err = _hook(f"git -C {target} push origin feature", host)
    lines = err.splitlines()
    assert rc == 2
    assert lines[0] == FOUND_ZERO
    assert not any("found 2" in line for line in lines)


def test_push_hook_two_repositories_single_refusal(tmp_path):
    """Pushes selecting two repositories are ambiguous: no attestation reason is guessed."""
    a = _repo(tmp_path, "a")
    b = _repo(tmp_path, "b")
    rc, err = _hook(f"git -C {a} push origin feature; git -C {b} push origin feature", a)
    assert rc == 2
    assert len(err.splitlines()) == 1 and "canonical" in err, err


@pytest.mark.parametrize("state", ["not-a-repo", "bare", "detached", "on-main", "no-commits"])
def test_push_hook_odd_repository_state_blocks_quietly(tmp_path, state):
    """Odd repository states still exit 2 with only BLOCK lines (no git noise, no traceback)."""
    if state == "not-a-repo":
        cwd = tmp_path / "plain"
        cwd.mkdir()
    elif state == "bare":
        cwd = tmp_path / "bare.git"
        subprocess.run(["git", "init", "-q", "--bare", str(cwd)], check=True)
    elif state == "no-commits":
        cwd = tmp_path / "empty"
        cwd.mkdir()
        _git(cwd, "init", "-q", "-b", "main")
    else:
        cwd = _repo(tmp_path, "repo")
        if state == "detached":
            _git(cwd, "switch", "-q", "--detach", "HEAD")
        else:
            _git(cwd, "switch", "-q", "main")
    rc, err = _hook("git push origin HEAD", cwd)
    assert rc == 2, err
    assert all(line.startswith("BLOCK ") for line in err.splitlines()), err


def test_push_hook_missing_git_blocks(tmp_path):
    """With no git on PATH the refusal stays exit 2 and the reason path adds no noise."""
    repo = _repo(tmp_path, "repo")
    empty = tmp_path / "empty-bin"
    empty.mkdir()
    env = {k: v for k, v in os.environ.items() if k != "PATH"}
    env["PATH"] = str(empty)
    rc, err = _hook("git push origin feature", repo, env=env)
    assert rc == 2, err
    assert all(line.startswith("BLOCK ") for line in err.splitlines()), err


def test_push_hook_many_segments_finishes_promptly(tmp_path):
    """A 5000-segment command cannot stall the hook through the extra cwd resolution."""
    repo = _repo(tmp_path, "repo")
    command = "; ".join(["cd " + str(repo)] * 5000) + "; git push origin feature"
    start = time.monotonic()
    rc, err = _hook(command, repo, timeout=120)
    assert rc == 2, err
    assert time.monotonic() - start < 30
