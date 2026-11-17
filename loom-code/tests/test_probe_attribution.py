"""Historical execution evidence only excludes immutable prerequisite probes."""
from __future__ import annotations

import hashlib
import json

import pytest

from loom_checker.attestation import validate_attestation
from loom_checker.digest import functional_content_digest
from loom_checker.probes import check_adversarial_proportionate, graduated_probe_programs
from loom_checker.reviewers import auto_skipped_steps, committed_branch_delta, required_reviewer_count
from test_selection_finalize import (
    CHANGE, PASSING, commit_all, finalize, git, graduate, make_repo, review_input, written,
)


def prerequisite_repo(tmp_path, damage=None):
    repo = make_repo(tmp_path)
    paths = [graduate(repo, f"test_prior_{i}.py") for i in range(5)]
    prior = "2026-09-13-prior"
    intent = repo / f"docs/loom/intent/{CHANGE}.md"
    if damage == "late":
        intent.parent.mkdir(parents=True)
        intent.write_text("# Current work\n")
        commit_all(repo, "introduce current intent before evidence")
    head = git(repo, "rev-parse", "HEAD")
    record = {
        "schema": "loom-attestation/v2", "change_id": prior,
        "content_digest": functional_content_digest(repo, head, prior),
        "selection": None, "findings": [], "verdicts": PASSING,
        "executions": [{"kind": "package-tests", "command": "python3 -c pass",
                        "command_digest": hashlib.sha256(b"python3 -c pass").hexdigest(), "result": "pass"}]
        + [{"kind": "adversarial", "artifact": path, "command": f"python3 -m pytest {path}",
            "command_digest": hashlib.sha256(f"python3 -m pytest {path}".encode()).hexdigest(), "result": "pass"}
           for path in paths],
    }
    evidence = repo / f"docs/loom/{prior}/attestation.json"
    evidence.parent.mkdir(parents=True)
    if damage == "invalid":
        record["content_digest"] = "forged"
    evidence.write_text("{bad json" if damage == "malformed" else json.dumps(record))
    accepted = commit_all(repo, "accepted prerequisites")
    if damage not in {"invalid", "malformed"}:
        assert validate_attestation(repo, accepted, prior, record) == []
    if damage != "late":
        intent.parent.mkdir(parents=True)
        intent.write_text("# Current work\n")
        commit_all(repo, "introduce current intent")
    current = graduate(repo, "test_current.py")
    return repo, paths, current, evidence


def test_inherited_five_are_excluded_without_changing_scope_or_evidence(tmp_path, monkeypatch):
    repo, prior, current, evidence = prerequisite_repo(tmp_path)
    git(repo, "checkout", "-q", "main")
    (repo / "trunk.txt").write_text("unrelated trunk change\n")
    commit_all(repo, "trunk changes without prerequisite paths")
    git(repo, "checkout", "-q", "feature")
    git(repo, "merge", "--no-edit", "main")
    # Later publication metadata is not a new prerequisite boundary. The old
    # canonical revision still validates at its own historical tree.
    evidence.write_text(json.dumps({"content_digest": "later malformed metadata"}))
    commit_all(repo, "later prerequisite metadata")
    before = evidence.read_bytes()
    head = git(repo, "rev-parse", "HEAD")
    assert graduated_probe_programs(repo, head, CHANGE) == [current]
    assert check_adversarial_proportionate(repo, head, CHANGE, [current, current]) == []
    assert check_adversarial_proportionate(repo, head, CHANGE, prior + [current])
    assert set(prior) <= committed_branch_delta(repo, CHANGE, head)[2]
    assert required_reviewer_count(repo, CHANGE, head) == 2
    assert not auto_skipped_steps(repo, CHANGE, head)
    result = finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"python3 -m pytest {path}", "artifact": path} for path in [prior[0], current]
    ]))
    assert result.returncode == 0, result.stderr
    assert written(repo)["change_id"] == CHANGE
    assert [run["artifact"] for run in written(repo)["executions"]
            if run["kind"] == "adversarial"] == [prior[0], current]
    assert evidence.read_bytes() == before
    # Ordinary tests and evidence for other paths must not trigger expensive
    # historical validation, even when that history contains valid records.
    from loom_checker import attestation, probe_attribution

    def unexpected(*args, **kwargs):
        pytest.fail("unrelated input triggered historical validation")

    monkeypatch.setattr(attestation, "validate_attestation", unexpected)
    for path in prior:
        target = repo / path
        target.write_text(target.read_text().replace("# concern:", "# ordinary:"))
    head = commit_all(repo, "prior probes become ordinary tests")
    assert graduated_probe_programs(repo, head, CHANGE) == [current]
    monkeypatch.setattr(probe_attribution, "prerequisite_probe_programs", unexpected)
    target = repo / current
    target.write_text(target.read_text().replace("# concern:", "# ordinary:"))
    head = commit_all(repo, "no automatic probe candidates")
    assert graduated_probe_programs(repo, head, CHANGE) == []


@pytest.mark.parametrize("damage", ["invalid", "malformed", "late", "changed", "copy", "revert", "side-revert", "mode"])
def test_unproven_or_changed_prerequisites_stay_counted(tmp_path, damage):
    repo, prior, current, evidence = prerequisite_repo(tmp_path, damage)
    if damage in {"invalid", "malformed", "late"}:
        pass
    elif damage == "copy":
        copied = repo / "loom-code/tests/test_copy.py"
        copied.write_bytes((repo / prior[0]).read_bytes())
        current = str(copied.relative_to(repo))
        commit_all(repo, "copy")
    else:
        if damage == "side-revert":
            git(repo, "checkout", "-q", "-b", "side")
        path = repo / prior[0]
        original = path.read_text()
        if damage == "mode":
            path.chmod(0o755)
        else:
            path.write_text(original + "\n# changed\n")
        commit_all(repo, "modify prerequisite")
        if damage in {"revert", "side-revert"}:
            path.write_text(original)
            commit_all(repo, "revert prerequisite")
        if damage == "side-revert":
            git(repo, "checkout", "-q", "feature")
            git(repo, "merge", "--no-ff", "--no-edit", "side")
    head = git(repo, "rev-parse", "HEAD")
    counted = graduated_probe_programs(repo, head, CHANGE)
    assert current in counted
    if damage != "copy":
        assert prior[0] in counted
