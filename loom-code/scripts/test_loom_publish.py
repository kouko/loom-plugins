from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from io import StringIO
from pathlib import Path

from loom_checker.command_handlers import publish as loom_checker
from loom_checker.command_handlers import push as push_handler
from loom_checker import selection as selection_store
from loom_checker.rule_checks import push as push_rules
from loom_checker.rule_checks.push import CANONICAL_PUSH_FLAGS
from loom_checker.rule_checks.push import github_repo_from_origin
from loom_checker.rule_checks.push import render_quote_all
import pytest

CONTEXT_HEADINGS = (
    "Context", "Intended outcome", "Scope", "Decisions", "Implementation",
    "Behaviour change", "Verification", "Risks and rollback", "Follow-ups",
)
CONTEXT_CONTENT = {
    "Context": "Ship currently asks twice before publication.",
    "Intended outcome": "One informed intent decision authorizes publication.",
    "Scope": "Push, Ready PR creation, and task-local CI observation are included.",
    "Decisions": "Use a machine-readable intent field instead of prose inference.",
    "Implementation": "The publish wrapper validates and performs each outward step.",
    "Behaviour change": "After review, publication proceeds without a second prompt.",
    "Verification": "Focused race and contract regressions pass.",
    "Risks and rollback": "Disable automatic publication by omitting the intent field.",
    "Follow-ups": "None.",
}


def contextual_body(*, mermaid: bool = False, overrides: dict[str, str] | None = None) -> str:
    content = CONTEXT_CONTENT | (overrides or {})
    body = "\n\n".join(f"## {heading}\n{content[heading]}" for heading in CONTEXT_HEADINGS)
    if mermaid:
        body += "\n\n```mermaid\nflowchart LR\n  A --> B\n```"
    return body + "\n"


def trusted_executable(name: str) -> str:
    return "/usr/bin/git" if name == "git" else "/usr/local/bin/gh"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def repository(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "branch", "-M", "feature")
    git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    return repo


class ExternalCalls:
    def __init__(
        self, head: str, existing_pr: str | None = None, *, draft: bool = False
    ) -> None:
        self.head = head
        self.remote_head: str | None = None
        self.existing_pr = existing_pr
        self.move_remote_on_pr_list = False
        self.cross_repository_pr = False
        self.fail_create_once = False
        self.move_head_on_create = False
        self.move_remote_on_create = False
        self.change_pushurl_on_create = False
        self.fail_update = False
        self.fail_ready = False
        self.existing_pr_draft = draft
        self.move_head_on_update = False
        self.move_remote_on_update = False
        self.move_head_on_ready = False
        self.move_remote_on_ready = False
        self.change_pushurl_on_ready = False
        self.mutate_body_on_repo_view = False
        self.original_body: Path | None = None
        self.published_bodies: list[str] = []
        self.published_body_paths: list[Path] = []
        self.published_body_modes: list[int] = []
        self.change_pushurl_on_remote_read = False
        self.switch_branch_on_remote_read = False
        self.change_pushurl_on_pr_list = False
        self.change_uploadpack_on_final_remote_read = False
        self.remote_reads = 0
        self.required_checks = [[{"name": "gate", "state": "SUCCESS", "bucket": "pass"}]]
        self.required_check_returncodes: list[int] = []
        self.required_check_stderr: list[str] = []
        self.calls: list[list[str]] = []

    def __call__(self, argv, **kwargs):
        argv = [str(value) for value in argv]
        self.calls.append(argv)
        if "repo" in argv and "view" in argv:
            if self.mutate_body_on_repo_view:
                assert self.original_body is not None
                self.original_body.write_text("replaced after validation\n", encoding="utf-8")
            return subprocess.CompletedProcess(argv, 0, "main\n", "")
        if "ls-remote" in argv:
            self.remote_reads += 1
            if self.remote_reads == 1 and self.change_pushurl_on_remote_read:
                git(Path(kwargs["cwd"]), "config", "remote.origin.pushurl",
                    "git@github.com:attacker/project.git")
            if self.remote_reads == 1 and self.switch_branch_on_remote_read:
                git(Path(kwargs["cwd"]), "switch", "-q", "-c", "alternate")
            if self.remote_reads == 3 and self.change_uploadpack_on_final_remote_read:
                git(Path(kwargs["cwd"]), "config", "remote.origin.uploadpack",
                    "/tmp/attacker-upload-pack")
            output = f"{self.remote_head}\trefs/heads/feature\n" if self.remote_head else ""
            return subprocess.CompletedProcess(argv, 0, output, "")
        if "push" in argv:
            self.remote_head = self.head
            return subprocess.CompletedProcess(argv, 0, "", "")
        if "api" in argv and any("/pulls?" in token for token in argv):
            if self.change_pushurl_on_pr_list:
                git(Path(kwargs["cwd"]), "config", "remote.origin.pushurl",
                    "git@github.com:attacker/project.git")
            if self.move_remote_on_pr_list:
                self.remote_head = "e" * 40
            prs = []
            if self.existing_pr:
                full_name = "attacker/project" if self.cross_repository_pr else "example/project"
                prs.append({
                    "html_url": self.existing_pr,
                    "draft": self.existing_pr_draft,
                    "head": {"sha": self.head, "repo": {"full_name": full_name}},
                    "base": {"ref": "main", "repo": {"full_name": "example/project"}},
                })
            output = json.dumps(prs)
            return subprocess.CompletedProcess(argv, 0, output, "")
        if "pr" in argv and "create" in argv:
            body_path = Path(argv[argv.index("--body-file") + 1])
            self.published_bodies.append(body_path.read_text(encoding="utf-8"))
            self.published_body_paths.append(body_path)
            self.published_body_modes.append(body_path.stat().st_mode & 0o777)
            if self.fail_create_once:
                self.fail_create_once = False
                return subprocess.CompletedProcess(argv, 1, "", "temporary failure")
            if self.move_head_on_create:
                git(Path(kwargs["cwd"]), "commit", "--allow-empty", "-q", "-m", "moved")
            if self.move_remote_on_create:
                self.remote_head = "b" * 40
            if self.change_pushurl_on_create:
                git(Path(kwargs["cwd"]), "config", "remote.origin.pushurl",
                    "git@github.com:attacker/project.git")
            self.existing_pr = "https://github.com/example/project/pull/1"
            return subprocess.CompletedProcess(argv, 0, f"{self.existing_pr}\n", "")
        if "pr" in argv and "edit" in argv:
            body_path = Path(argv[argv.index("--body-file") + 1])
            self.published_bodies.append(body_path.read_text(encoding="utf-8"))
            self.published_body_paths.append(body_path)
            self.published_body_modes.append(body_path.stat().st_mode & 0o777)
            if self.fail_update:
                return subprocess.CompletedProcess(argv, 1, "", "update failed")
            if self.move_head_on_update:
                git(Path(kwargs["cwd"]), "commit", "--allow-empty", "-q", "-m", "moved")
            if self.move_remote_on_update:
                self.remote_head = "d" * 40
            return subprocess.CompletedProcess(argv, 0, "", "")
        if "pr" in argv and "ready" in argv:
            if self.fail_ready:
                return subprocess.CompletedProcess(argv, 1, "", "ready failed")
            if self.move_head_on_ready:
                git(Path(kwargs["cwd"]), "commit", "--allow-empty", "-q", "-m", "moved")
            if self.move_remote_on_ready:
                self.remote_head = "c" * 40
            if self.change_pushurl_on_ready:
                git(Path(kwargs["cwd"]), "config", "remote.origin.pushurl",
                    "git@github.com:attacker/project.git")
            self.existing_pr_draft = False
            return subprocess.CompletedProcess(argv, 0, "", "")
        if "pr" in argv and "checks" in argv:
            snapshot = self.required_checks.pop(0)
            return subprocess.CompletedProcess(
                argv,
                self.required_check_returncodes.pop(0)
                if self.required_check_returncodes else 0,
                snapshot if isinstance(snapshot, str) else json.dumps(snapshot),
                self.required_check_stderr.pop(0)
                if self.required_check_stderr else "CI observation failed",
            )
        raise AssertionError(argv)


def invoke(tmp_path: Path, monkeypatch, calls: ExternalCalls, *extra: str):
    repo = repository(tmp_path)
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    calls.original_body = body
    calls.head = git(repo, "rev-parse", "HEAD")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "_cmd_push", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        loom_checker, "resolve_publish_executable",
        trusted_executable,
    )
    out, err = StringIO(), StringIO()
    argv = [
        "--confirm-authorized", "--title", "feat(loom): publish safely",
        "--body-file", str(body), *extra,
    ]
    rc = loom_checker.cmd_publish(argv, out, err)
    return repo, rc, out.getvalue(), err.getvalue()


def publication_intent(repo: Path, *, automatic: bool, change_id: str = "change") -> Path:
    intent = repo / "docs" / "loom" / "intent" / f"{change_id}.md"
    intent.parent.mkdir(parents=True, exist_ok=True)
    publication = (
        "publication: automatic — authorized 2026-09-09 by Test\n"
        if automatic else ""
    )
    intent.write_text(
        "# Change\nstatus: confirmed 2026-09-09\n"
        f"{publication}\n## Proposed outcome\n任何語言的敘述都不控制發布授權。\n",
        encoding="utf-8",
    )
    return intent


def attestation(repo: Path, change_id: str = "change") -> Path:
    target = repo / "docs" / "loom" / change_id / "attestation.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({"change_id": change_id}), encoding="utf-8")
    return target


def test_confirmed_current_intent_publishes_without_ship_reask(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    git(repo, "branch", "main")
    intent = publication_intent(repo, automatic=True)
    attestation(repo)
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "authorize publication")
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    calls.head = git(repo, "rev-parse", "HEAD")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "_cmd_push", lambda *args, **kwargs: 0)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)

    err = StringIO()
    rc = loom_checker.cmd_publish([
        "--intent", str(intent), "--title", "feat(loom): safe",
        "--body-file", str(body),
    ], StringIO(), err)

    assert rc == 0, err.getvalue()
    assert any("push" in call for call in calls.calls)
    assert any("pr" in call and "create" in call for call in calls.calls)
    assert not any("merge" in call for call in calls.calls)


def test_legacy_intent_requires_one_publication_decision(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    git(repo, "branch", "main")
    intent = publication_intent(repo, automatic=False)
    attestation(repo)
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "legacy evidence")
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    calls.head = git(repo, "rev-parse", "HEAD")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "_cmd_push", lambda *args, **kwargs: 0)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)

    err = StringIO()
    rc = loom_checker.cmd_publish([
        "--intent", str(intent), "--title", "feat(loom): safe",
        "--body-file", str(body),
    ], StringIO(), err)

    assert rc == 2
    assert "publication decision" in err.getvalue()
    assert calls.calls == []


def test_unrelated_intent_cannot_authorize_attested_change(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    git(repo, "branch", "main")
    publication_intent(repo, automatic=False)
    unrelated = publication_intent(repo, automatic=True, change_id="unrelated")
    attestation(repo)
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "attest change")
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)

    err = StringIO()
    rc = loom_checker.cmd_publish([
        "--intent", str(unrelated), "--title", "feat(loom): safe",
        "--body-file", str(body),
    ], StringIO(), err)

    assert rc == 2
    assert "attested change" in err.getvalue()
    assert calls.calls == []


def test_untracked_or_mutated_intent_cannot_authorize(
    tmp_path: Path, monkeypatch
) -> None:
    for state in ("untracked", "mutated"):
        case = tmp_path / state
        case.mkdir()
        calls = ExternalCalls("")
        repo = repository(case)
        git(repo, "branch", "main")
        if state == "mutated":
            publication_intent(repo, automatic=False)
        attestation(repo)
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "attest change")
        intent = publication_intent(repo, automatic=True)
        body = case / "body.md"
        body.write_text(contextual_body(), encoding="utf-8")
        monkeypatch.chdir(repo)
        monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
        monkeypatch.setattr(loom_checker, "run_publish_external", calls)

        err = StringIO()
        rc = loom_checker.cmd_publish([
            "--intent", str(intent), "--title", "feat(loom): safe",
            "--body-file", str(body),
        ], StringIO(), err)

        assert rc == 2, state
        assert "committed intent" in err.getvalue(), state
        assert calls.calls == [], state


def test_publish_pushes_exact_head_and_creates_one_pr(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    repo, rc, out, err = invoke(tmp_path, monkeypatch, calls)
    head = git(repo, "rev-parse", "HEAD")
    assert rc == 0, err
    push = next(call for call in calls.calls if "push" in call)
    assert push[-2:] == ["origin", f"{head}:refs/heads/feature"]
    assert "--force" not in push and "--force-with-lease" not in push
    create = next(call for call in calls.calls if call[-2:] != [] and "create" in call)
    assert create[create.index("--base") + 1] == "main"
    assert create[create.index("--head") + 1] == "feature"
    assert "https://github.com/example/project/pull/1" in out
    assert f"Attestation validated for {head}" in out
    assert "Publication target: github.com/example/project base main" in out


def test_publish_revalidates_head_remote_and_identity_after_new_pr_creation(
    tmp_path: Path, monkeypatch
) -> None:
    cases = {
        "move_head_on_create": "live HEAD moved after PR creation",
        "move_remote_on_create": "remote branch moved after PR creation",
        "change_pushurl_on_create": "publication identity changed after PR creation",
    }
    for mutation, message in cases.items():
        case = tmp_path / mutation
        case.mkdir()
        calls = ExternalCalls("")
        setattr(calls, mutation, True)

        _, rc, _, err = invoke(case, monkeypatch, calls)

        assert rc == 1, mutation
        assert message in err, mutation
        assert not any("checks" in call for call in calls.calls)


def test_new_pr_uses_validated_body_snapshot_when_source_changes(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    calls.mutate_body_on_repo_view = True

    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    assert calls.original_body is not None
    assert calls.original_body.read_text(encoding="utf-8") == "replaced after validation\n"
    assert calls.published_bodies == [contextual_body()]
    assert calls.published_body_modes == [0o600]
    assert calls.published_body_paths != [calls.original_body]
    assert all(not path.exists() for path in calls.published_body_paths)


def test_contextual_body_gate_rejects_malformed_or_unsafe_schema() -> None:
    valid = contextual_body()
    cases = {
        "missing": valid.replace(f"## Scope\n{CONTEXT_CONTENT['Scope']}\n\n", ""),
        "duplicate": valid + "\n## Context\nAgain.\n",
        "out-of-order": valid.replace(
            f"## Context\n{CONTEXT_CONTENT['Context']}\n\n"
            f"## Intended outcome\n{CONTEXT_CONTENT['Intended outcome']}",
            f"## Intended outcome\n{CONTEXT_CONTENT['Intended outcome']}\n\n"
            f"## Context\n{CONTEXT_CONTENT['Context']}",
        ),
        "competing": valid + "\n## Memory\nLegacy.\n",
        "hidden-cot": valid.replace(CONTEXT_CONTENT["Context"], "private chain-of-thought", 1),
    }
    for name, body in cases.items():
        assert loom_checker.validate_contextual_pr_body(body) is not None, name


def test_contextual_body_gate_names_the_missing_heading() -> None:
    body = contextual_body().replace(f"## Scope\n{CONTEXT_CONTENT['Scope']}\n\n", "")

    assert loom_checker.validate_contextual_pr_body(body) == 'heading "Scope" is missing'


def test_contextual_body_gate_names_duplicated_out_of_order_and_empty_headings() -> None:
    valid = contextual_body()
    cases = {
        valid + "\n## Context\nAgain, the context repeats here.\n":
            'heading "Context" is duplicated',
        valid.replace(
            f"## Context\n{CONTEXT_CONTENT['Context']}\n\n"
            f"## Intended outcome\n{CONTEXT_CONTENT['Intended outcome']}",
            f"## Intended outcome\n{CONTEXT_CONTENT['Intended outcome']}\n\n"
            f"## Context\n{CONTEXT_CONTENT['Context']}",
        ): 'heading "Intended outcome" is out of order',
        contextual_body(overrides={"Decisions": "..."}): 'heading "Decisions" is empty',
        valid + "\n## Memory\nLegacy section kept for history.\n":
            'heading "Memory" is not one of the nine contextual headings',
        "": 'heading "Context" is missing',
    }
    for body, expected in cases.items():
        assert loom_checker.validate_contextual_pr_body(body) == expected, expected


def test_contextual_body_gate_accepts_simple_and_mermaid_bodies() -> None:
    assert loom_checker.validate_contextual_pr_body(contextual_body()) is None
    assert loom_checker.validate_contextual_pr_body(contextual_body(mermaid=True)) is None


def test_contextual_body_gate_rejects_structurally_empty_sections() -> None:
    placeholders = (
        "", "  \n\t", "...", "Evidence.", "<!-- details later -->",
        "```text\nplaceholder words inside a fence\n```",
    )
    for heading in CONTEXT_HEADINGS:
        for placeholder in placeholders:
            body = contextual_body(overrides={heading: placeholder})
            reason = loom_checker.validate_contextual_pr_body(body)
            assert reason is not None, (heading, placeholder)
            assert heading in reason, (heading, placeholder)


def test_contextual_body_gate_ignores_headings_inside_fenced_code() -> None:
    body = contextual_body(overrides={
        "Implementation": (
            "The wrapper publishes one reviewed branch.\n\n"
            "```markdown\n## Summary\nexample only\n## Example\nexample only\n```"
        ),
    })

    assert loom_checker.validate_contextual_pr_body(body) is None


def test_contextual_body_gate_accepts_substantive_chinese_and_japanese() -> None:
    for content in ("所有必要驗證均已成功完成。", "必要な検証はすべて正常に完了しました。"):
        body = contextual_body(overrides={
            heading: content for heading in CONTEXT_HEADINGS if heading != "Follow-ups"
        })
        assert loom_checker.validate_contextual_pr_body(body) is None, content


def test_contextual_body_gate_respects_commonmark_fence_length() -> None:
    body = contextual_body(overrides={
        "Implementation": (
            "The wrapper validates the exact public body.\n\n"
            "````markdown\n```\n## Summary\n```\n## Example\n````"
        ),
    })

    assert loom_checker.validate_contextual_pr_body(body) is None


def test_publish_rejects_invalid_contextual_body_before_network(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    body = tmp_path / "body.md"
    body.write_text("## Context\nIncomplete.\n", encoding="utf-8")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
    err = StringIO()

    rc = loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): safe",
        "--body-file", str(body),
    ], StringIO(), err)

    assert rc == 1
    assert "push.contextual-body" in err.getvalue()
    assert calls.calls == []


def test_publish_reuses_existing_pr_and_replaces_title_and_body(tmp_path: Path, monkeypatch) -> None:
    """Ground gh pr edit URL, --title, and --body-file.

    https://cli.github.com/manual/gh_pr_edit
    """
    calls = ExternalCalls("", "https://github.com/example/project/pull/7")
    repo = repository(tmp_path)
    calls.head = git(repo, "rev-parse", "HEAD")
    calls.remote_head = calls.head
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "_cmd_push", lambda *args, **kwargs: 0)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
    out, err = StringIO(), StringIO()
    rc = loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): safe",
        "--body-file", str(body),
    ], out, err)
    assert rc == 0, err.getvalue()
    assert not any("push" in call for call in calls.calls)
    assert not any("create" in call for call in calls.calls)
    edit = next(call for call in calls.calls if "edit" in call)
    assert edit[edit.index("--title") + 1] == "feat(loom): safe"
    assert edit[edit.index("--body-file") + 1] != str(body)
    assert calls.published_bodies == [contextual_body()]
    assert sum("checks" in call for call in calls.calls) == 1
    assert "pull/7" in out.getvalue()


def test_existing_pr_update_uses_validated_body_snapshot_when_source_changes(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("", "https://github.com/example/project/pull/7")
    calls.mutate_body_on_repo_view = True

    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    assert calls.original_body is not None
    assert calls.original_body.read_text(encoding="utf-8") == "replaced after validation\n"
    assert calls.published_bodies == [contextual_body()]
    assert calls.published_body_modes == [0o600]
    assert calls.published_body_paths != [calls.original_body]
    assert all(not path.exists() for path in calls.published_body_paths)


def test_publish_marks_matching_draft_ready_after_context_update(
    tmp_path: Path, monkeypatch
) -> None:
    """Ground gh pr ready <url>.

    https://cli.github.com/manual/gh_pr_ready
    """
    calls = ExternalCalls(
        "", "https://github.com/example/project/pull/7", draft=True
    )

    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    edit_index = next(i for i, call in enumerate(calls.calls) if "edit" in call)
    ready_index = next(i for i, call in enumerate(calls.calls) if "ready" in call)
    checks_index = next(i for i, call in enumerate(calls.calls) if "checks" in call)
    assert edit_index < ready_index < checks_index


def test_publish_blocks_existing_pr_update_and_ready_failures(
    tmp_path: Path, monkeypatch
) -> None:
    for failure in ("fail_update", "fail_ready"):
        case = tmp_path / failure
        case.mkdir()
        calls = ExternalCalls(
            "", "https://github.com/example/project/pull/7", draft=True
        )
        setattr(calls, failure, True)

        _, rc, out, err = invoke(case, monkeypatch, calls)

        assert rc == 1, failure
        assert failure.removeprefix("fail_") in err, failure
        assert "Required CI passed" not in out, failure
        assert not any("checks" in call for call in calls.calls), failure


def test_publish_revalidates_live_head_and_remote_after_existing_pr_update(
    tmp_path: Path, monkeypatch
) -> None:
    cases = {
        "move_head_on_update": "live HEAD moved after PR update",
        "move_remote_on_update": "remote branch moved after PR update",
    }
    for mutation, message in cases.items():
        case = tmp_path / mutation
        case.mkdir()
        calls = ExternalCalls(
            "", "https://github.com/example/project/pull/7", draft=True
        )
        setattr(calls, mutation, True)

        _, rc, _, err = invoke(case, monkeypatch, calls)

        assert rc == 1, mutation
        assert message in err, mutation
        assert not any("ready" in call or "checks" in call for call in calls.calls)


def test_publish_revalidates_head_remote_and_identity_after_draft_ready(
    tmp_path: Path, monkeypatch
) -> None:
    cases = {
        "move_head_on_ready": "live HEAD moved after PR readiness",
        "move_remote_on_ready": "remote branch moved after PR readiness",
        "change_pushurl_on_ready": "publication identity changed after PR readiness",
    }
    for mutation, message in cases.items():
        case = tmp_path / mutation
        case.mkdir()
        calls = ExternalCalls(
            "", "https://github.com/example/project/pull/7", draft=True
        )
        setattr(calls, mutation, True)

        _, rc, _, err = invoke(case, monkeypatch, calls)

        assert rc == 1, mutation
        assert message in err, mutation
        assert not any("checks" in call for call in calls.calls)


def test_publish_requires_authorization_and_absolute_body(tmp_path: Path, monkeypatch) -> None:
    repo = repository(tmp_path)
    monkeypatch.chdir(repo)
    out, err = StringIO(), StringIO()
    assert loom_checker.cmd_publish([], out, err) == 2
    assert loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): safe",
        "--body-file", "relative.md",
    ], out, err) == 2


def test_publish_rejects_repository_redirecting_environment(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    monkeypatch.setenv("GH_REPO", "attacker/target")
    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)
    assert rc == 2
    assert "GH_REPO" in err
    assert calls.calls == []


def test_publish_rejects_git_common_dir_before_network(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    monkeypatch.setenv("GIT_COMMON_DIR", str(tmp_path / "other.git"))
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    err_stream = StringIO()
    rc = loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): safe",
        "--body-file", str(body),
    ], StringIO(), err_stream)
    err = err_stream.getvalue()
    assert rc == 2
    assert "GIT_COMMON_DIR" in err
    assert calls.calls == []


def test_publish_does_not_replay_functional_executables(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    checked: list[list[str]] = []

    def attestation_only(args, *unused, **kwargs):
        checked.append(args)
        return 0

    repo = repository(tmp_path)
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    calls.head = git(repo, "rev-parse", "HEAD")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "_cmd_push", attestation_only)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
    assert loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): safe",
        "--body-file", str(body),
    ]) == 0
    assert checked == [["--head", calls.head, "--require-live-head"]]


def test_publish_rejects_diverged_remote_before_push(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    calls.head = git(repo, "rev-parse", "HEAD")
    calls.remote_head = "f" * 40
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "_cmd_push", lambda *args, **kwargs: 0)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
    err = StringIO()
    rc = loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): safe",
        "--body-file", str(body),
    ], StringIO(), err)
    assert rc == 1
    assert "remote branch" in err.getvalue()
    assert not any("push" in call for call in calls.calls)


def test_publish_rechecks_remote_head_before_pr_creation(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    calls.move_remote_on_pr_list = True
    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)
    assert rc == 1
    assert "remote branch moved before PR creation" in err
    assert not any("create" in call for call in calls.calls)


def test_publish_rejects_git_config_parameters_before_network(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    monkeypatch.setenv("GIT_CONFIG_PARAMETERS", "'remote.origin.pushurl'='ssh://evil/x/y'")
    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)
    assert rc == 2
    assert "GIT_CONFIG_PARAMETERS" in err
    assert calls.calls == []


def test_publish_rejects_git_redirect_config_before_push(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    redirects = {
        "remote.origin.pushurl": "git@github.com:attacker/project.git",
        "core.sshCommand": "/tmp/attacker-ssh",
        "url.https://attacker.example/.pushInsteadOf": "git@github.com:",
        "url.https://attacker.example/.insteadOf": "git@github.com:",
        "remote.origin.vcs": "attacker",
        "remote.origin.receivepack": "/tmp/attacker-receive-pack",
        "remote.origin.uploadpack": "/tmp/attacker-upload-pack",
    }
    body = tmp_path / "body.md"
    body.write_text(contextual_body(), encoding="utf-8")
    for key, value in redirects.items():
        git(repo, "config", key, value)
        calls.head = git(repo, "rev-parse", "HEAD")
        calls.calls.clear()
        monkeypatch.chdir(repo)
        monkeypatch.setattr(loom_checker, "run_publish_external", calls)
        monkeypatch.setattr(loom_checker, "_cmd_push", lambda *args, **kwargs: 0)
        monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
        err = StringIO()
        rc = loom_checker.cmd_publish([
            "--confirm-authorized", "--title", "feat(loom): safe",
            "--body-file", str(body),
        ], StringIO(), err)
        assert rc == 1, key
        assert "configuration" in err.getvalue(), key
        assert not any("push" in call for call in calls.calls), key
        git(repo, "config", "--unset-all", key)


def test_publish_revalidates_origin_and_branch_before_push(tmp_path: Path, monkeypatch) -> None:
    for mutation in ("change_pushurl_on_remote_read", "switch_branch_on_remote_read"):
        case = tmp_path / mutation
        case.mkdir()
        calls = ExternalCalls("")
        setattr(calls, mutation, True)
        _, rc, _, err = invoke(case, monkeypatch, calls)
        assert rc == 1, mutation
        assert "changed before push" in err, mutation
        assert not any("push" in call for call in calls.calls), mutation


def test_publish_revalidates_identity_around_final_remote_read(tmp_path: Path, monkeypatch) -> None:
    for mutation in ("change_pushurl_on_pr_list", "change_uploadpack_on_final_remote_read"):
        case = tmp_path / mutation
        case.mkdir()
        calls = ExternalCalls("")
        setattr(calls, mutation, True)
        _, rc, _, err = invoke(case, monkeypatch, calls)
        assert rc == 1, mutation
        assert "before PR creation" in err, mutation
        assert not any("create" in call for call in calls.calls), mutation


def test_publish_rejects_cross_repository_pr_match(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("", "https://github.com/attacker/project/pull/7")
    calls.cross_repository_pr = True
    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)
    assert rc == 1
    assert "identity" in err
    assert not any("create" in call for call in calls.calls)


def test_publish_uses_origin_bound_api_not_branch_only_pr_list(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("", "https://github.com/example/project/pull/7")
    repo, rc, _, err = invoke(tmp_path, monkeypatch, calls)
    assert rc == 0, err
    assert any("api" in call and any("/pulls?" in token for token in call) for call in calls.calls)
    assert not any("pr" in call and "list" in call for call in calls.calls)
    assert git(repo, "rev-parse", "HEAD") == calls.head


def test_executable_resolution_ignores_path_shadow(tmp_path: Path, monkeypatch) -> None:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake = fake_bin / "git"
    fake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", str(fake_bin))
    resolved = loom_checker.resolve_publish_executable("git")
    assert resolved is None or Path(resolved) != fake.resolve()


def test_retry_after_pr_creation_failure_does_not_repush(tmp_path: Path, monkeypatch) -> None:
    calls = ExternalCalls("")
    calls.fail_create_once = True
    repo, first_rc, _, first_err = invoke(tmp_path, monkeypatch, calls)
    assert first_rc == 1
    assert "temporary failure" in first_err
    first_pushes = sum("push" in call for call in calls.calls)

    body = tmp_path / "body.md"
    monkeypatch.chdir(repo)
    out, err = StringIO(), StringIO()
    second_rc = loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): publish safely",
        "--body-file", str(body),
    ], out, err)
    assert second_rc == 0, err.getvalue()
    assert sum("push" in call for call in calls.calls) == first_pushes
    assert "pull/1" in out.getvalue()


def test_publish_observes_required_ci_immediately_then_every_ten_seconds(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    calls.required_checks = [
        [{"name": "gate", "state": "IN_PROGRESS", "bucket": "pending"}],
        [{"name": "gate", "state": "SUCCESS", "bucket": "pass"}],
    ]
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append, raising=False)

    _, rc, out, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    checks = [call for call in calls.calls if "checks" in call]
    assert len(checks) == 2
    assert all("--required" in call for call in checks)
    assert waits == [10]
    assert "Required CI passed" in out
    assert "pending" not in out.casefold()


def test_publish_stops_on_required_ci_terminal_blockers(
    tmp_path: Path, monkeypatch
) -> None:
    terminal = {
        "FAILURE": "failed",
        "CANCELLED": "cancelled",
        "ACTION_REQUIRED": "requires user action",
    }
    for state, message in terminal.items():
        case = tmp_path / state.casefold()
        case.mkdir()
        calls = ExternalCalls("")
        calls.required_checks = [
            [{"name": "gate", "state": state, "bucket": "fail"}]
        ]
        waits: list[int] = []
        monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append, raising=False)

        _, rc, out, err = invoke(case, monkeypatch, calls)

        assert rc == 1, state
        assert message in err.casefold(), state
        assert waits == [], state
        assert "Required CI passed" not in out, state


def test_publish_accepts_gh_pending_exit_code_eight(tmp_path: Path, monkeypatch) -> None:
    """Ground --required, JSON fields, and pending rc=8.

    https://cli.github.com/manual/gh_pr_checks
    """
    calls = ExternalCalls("")
    calls.required_checks = [
        [{"name": "gate", "state": "IN_PROGRESS", "bucket": "pending"}],
        [{"name": "gate", "state": "SUCCESS", "bucket": "pass"}],
    ]
    calls.required_check_returncodes = [8, 0]
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    assert waits == [10]


def test_publish_blocks_unexpected_gh_checks_exit_and_malformed_json(
    tmp_path: Path, monkeypatch
) -> None:
    cases = (("exit", "[]", 2, "CI observation failed"),
             ("json", "not-json", 0, "cannot decode"))
    for name, payload, returncode, message in cases:
        case = tmp_path / name
        case.mkdir()
        calls = ExternalCalls("")
        calls.required_checks = [payload]
        calls.required_check_returncodes = [returncode]

        _, rc, _, err = invoke(case, monkeypatch, calls)

        assert rc == 1, name
        assert message.casefold() in err.casefold(), name


def test_publish_rechecks_an_initial_empty_required_set_before_pass(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    calls.required_checks = [
        [],
        [{"name": "gate", "state": "SUCCESS", "bucket": "pass"}],
    ]
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, out, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    assert waits == [10]
    assert "Required CI passed" in out


@pytest.mark.parametrize(
    "stderr",
    [
        "no checks reported on the 'feature' branch",
        "no required checks reported on the 'feature' branch",
    ],
)
def test_publish_treats_gh_exit_one_no_checks_as_registration_delay(
    tmp_path: Path, monkeypatch, stderr: str
) -> None:
    """Pin gh 2.88.1's two no-check error forms and exit-1 behavior.

    https://github.com/cli/cli/blob/v2.88.1/pkg/cmd/pr/checks/checks.go
    https://github.com/cli/cli/blob/v2.88.1/pkg/cmd/pr/checks/checks_test.go
    https://github.com/cli/cli/issues/7401
    """
    calls = ExternalCalls("")
    calls.required_checks = [
        "",
        [{"name": "gate", "state": "SUCCESS", "bucket": "pass"}],
    ]
    calls.required_check_returncodes = [1, 0]
    calls.required_check_stderr = [stderr, ""]
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, out, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    assert waits == [10]
    assert "Required CI passed" in out


@pytest.mark.parametrize("initial_output", ["", "  \n\t"])
def test_publish_rechecks_initial_successful_blank_ci_output_before_pass(
    tmp_path: Path, monkeypatch, initial_output: str
) -> None:
    calls = ExternalCalls("")
    calls.required_checks = [
        initial_output,
        [{"name": "gate", "state": "SUCCESS", "bucket": "pass"}],
    ]
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, out, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    assert waits == [10]
    assert "Required CI passed" in out


def test_publish_blocks_unexpected_ci_exit_with_blank_output(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    calls.required_checks = [""]
    calls.required_check_returncodes = [2]
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 1
    assert "required CI could not be observed" in err
    assert waits == []


@pytest.mark.parametrize(
    ("stdout", "stderr"),
    [
        ("[]", "no checks reported on the 'feature' branch"),
        ("", "no checks reported on the authentication failed branch"),
        ("", "no checks reported for feature"),
        ("", "authentication required"),
    ],
)
def test_publish_blocks_non_exact_exit_one_no_checks_responses(
    tmp_path: Path, monkeypatch, stdout: str, stderr: str
) -> None:
    calls = ExternalCalls("")
    calls.required_checks = [stdout]
    calls.required_check_returncodes = [1]
    calls.required_check_stderr = [stderr]
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, _, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 1
    assert stderr in err
    assert waits == []


@pytest.mark.parametrize("empty_snapshots", [[[], []], ["", "  \n"]])
def test_publish_reports_registration_grace_expiry_as_no_checks_registered(
    tmp_path: Path, monkeypatch, empty_snapshots: list[object]
) -> None:
    calls = ExternalCalls("")
    calls.required_checks = empty_snapshots[:1] * 7
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, out, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 0, err
    assert waits == [10] * 6
    assert "no required checks registered" in out.casefold()
    assert "Required CI passed" not in out


def test_publish_checks_appearing_at_registration_deadline_get_full_pending_budget(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    pending = [{"name": "gate", "state": "IN_PROGRESS", "bucket": "pending"}]
    calls.required_checks = ([[]] * 6) + [pending] + ([pending] * 360)
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)

    _, rc, out, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 1
    assert "after 60 minutes" in err
    assert waits == ([10] * 6) + ([10] * 360)
    assert "pending" not in out.casefold()


def test_publish_stops_permanent_pending_after_sixty_minutes_without_resume_state(
    tmp_path: Path, monkeypatch
) -> None:
    calls = ExternalCalls("")
    pending = [{"name": "gate", "state": "IN_PROGRESS", "bucket": "pending"}]
    calls.required_checks = [pending] * 361
    waits: list[int] = []
    monkeypatch.setattr(loom_checker, "wait_publish_interval", waits.append)
    before = set(tmp_path.rglob("*"))

    _, rc, out, err = invoke(tmp_path, monkeypatch, calls)

    assert rc == 1
    assert "requires user action" in err.casefold()
    assert "reliable terminal result" in err.casefold()
    assert waits == [10] * 360
    assert "pending" not in out.casefold()
    created = set(tmp_path.rglob("*")) - before
    assert not any(path.name.endswith((".pid", ".state", ".resume")) for path in created)


# --- Acceptance 5: skipped-steps disclosure (plan W2-04, spec decision 10) ---

from loom_checker.rule_checks import publish as publish_rules  # noqa: E402

SELECTION = {
    "confirmations": [
        {"code": "AB2C", "skip": ["adversarial"], "source": "user-typed",
         "at": "2026-09-13T08:00:00Z"},
        {"code": "QRST", "skip": ["reviewers", "adversarial"], "source": "user-typed",
         "at": "2026-09-14T01:02:03Z"},
    ],
    "skip": ["reviewers", "adversarial"],
    "source": "user-typed",
    "prior_failures": [
        {"step": "reviewers", "rule": "finalize.verdicts", "head_sha": "a" * 40,
         "branch": "feature", "at": "2026-09-12T23:00:00Z"},
        {"step": "finalize", "rule": "finalize.digest", "head_sha": "b" * 40,
         "branch": "feature", "at": "2026-09-13T09:00:00Z"},
    ],
}
DISCLOSURE = [
    "Skipped steps: adversarial — authority: user-typed (AB2C, 2026-09-13)",
    "Skipped steps: reviewers, adversarial — authority: user-typed (QRST, 2026-09-14)",
    "Prior failure: reviewers finalize.verdicts 2026-09-12",
    "Prior failure: finalize finalize.digest 2026-09-13",
]


def disclosed_body(lines: list[str]) -> str:
    verification = "\n".join([*lines, CONTEXT_CONTENT["Verification"]])
    return contextual_body(overrides={"Verification": verification})


def test_disclosure_renderer_matches_attestation_order() -> None:
    assert publish_rules.render_selection_disclosure({"selection": SELECTION}) == DISCLOSURE
    assert publish_rules.render_selection_disclosure({"selection": None}) == []


def test_matching_skipped_and_prior_failure_lines_publish() -> None:
    body = disclosed_body(DISCLOSURE)
    assert loom_checker.validate_contextual_pr_body(body) is None
    assert publish_rules.validate_selection_disclosure(body, {"selection": SELECTION}) is None
    # Null selection needs no line at all.
    assert publish_rules.validate_selection_disclosure(contextual_body(), {"selection": None}) is None


@pytest.mark.parametrize("name, lines", [
    ("missing everything", []),
    ("missing failure line", DISCLOSURE[:3]),
    ("missing earlier confirmation", DISCLOSURE[1:]),
    ("missing authority", [DISCLOSURE[0], "Skipped steps: reviewers, adversarial", *DISCLOSURE[2:]]),
    ("wrong authority source", [DISCLOSURE[0], DISCLOSURE[1].replace("user-typed", "agent"), *DISCLOSURE[2:]]),
    ("wrong code", [DISCLOSURE[0], DISCLOSURE[1].replace("QRST", "QRSX"), *DISCLOSURE[2:]]),
    ("wrong date", [*DISCLOSURE[:3], DISCLOSURE[3].replace("2026-09-13", "2026-09-14")]),
    ("steps reordered", [DISCLOSURE[0], DISCLOSURE[1].replace("reviewers, adversarial", "adversarial, reviewers"), *DISCLOSURE[2:]]),
    ("failures before skipped", [*DISCLOSURE[2:], *DISCLOSURE[:2]]),
    ("not first in Verification", ["Focused tests ran first.", *DISCLOSURE]),
    ("extra failure line", [*DISCLOSURE, "Prior failure: package-tests finalize.package-tests 2026-09-13"]),
])
def test_missing_authority_or_failure_line_refused(name: str, lines: list[str]) -> None:
    body = disclosed_body(lines)
    assert publish_rules.validate_selection_disclosure(body, {"selection": SELECTION}) is not None, name


def test_disclosure_elsewhere_or_false_disclosure_refused() -> None:
    # The lines must sit under Verification, not another section.
    moved = contextual_body(overrides={
        "Context": "\n".join([*DISCLOSURE, CONTEXT_CONTENT["Context"]]),
    })
    assert publish_rules.validate_selection_disclosure(moved, {"selection": SELECTION}) is not None
    # A null selection with a Skipped steps line is a false disclosure.
    for line in (DISCLOSURE[1], DISCLOSURE[2]):
        body = disclosed_body([line])
        assert publish_rules.validate_selection_disclosure(body, {"selection": None}) is not None


def selected_publication(tmp_path: Path, monkeypatch, lines: list[str]):
    calls = ExternalCalls("")
    repo = repository(tmp_path)
    git(repo, "branch", "main")
    target = attestation(repo)
    target.write_text(json.dumps({"change_id": "change", "selection": SELECTION}), encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "attested with a selection")
    body = tmp_path / "body.md"
    body.write_text(disclosed_body(lines), encoding="utf-8")
    calls.head = git(repo, "rev-parse", "HEAD")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(loom_checker, "run_publish_external", calls)
    monkeypatch.setattr(loom_checker, "_cmd_push", lambda *args, **kwargs: 0)
    monkeypatch.setattr(loom_checker, "resolve_publish_executable", trusted_executable)
    err = StringIO()
    rc = loom_checker.cmd_publish([
        "--confirm-authorized", "--title", "feat(loom): safe", "--body-file", str(body),
    ], StringIO(), err)
    return rc, err.getvalue(), calls


def test_publish_refuses_undisclosed_selection_before_network(
    tmp_path: Path, monkeypatch
) -> None:
    rc, err, calls = selected_publication(tmp_path, monkeypatch, DISCLOSURE[:3])

    assert rc == 1
    assert "push.contextual-body" in err
    assert "Prior failure: finalize finalize.digest 2026-09-13" in err
    assert calls.calls == []


def test_publish_accepts_matching_selection_disclosure(tmp_path: Path, monkeypatch) -> None:
    rc, err, calls = selected_publication(tmp_path, monkeypatch, DISCLOSURE)

    assert rc == 0, err
    assert any("pr" in call and "create" in call for call in calls.calls)


# --- Acceptance 4: the confirmed skip publishes end to end (plan W1-02) -------


def verification_section(body: str) -> list[str]:
    return body.split("## Verification\n", 1)[1].split("\n## ", 1)[0].splitlines()


def test_confirmed_skip_publishes_with_disclosure(tmp_path: Path, monkeypatch) -> None:
    """With the user-confirmed skip recorded in the attestation, publication
    pushes the selected HEAD and opens a Ready pull request whose body opens
    Verification with the attestation's own disclosure."""
    rc, err, calls = selected_publication(tmp_path, monkeypatch, DISCLOSURE)

    assert rc == 0, err
    push = next(call for call in calls.calls if "push" in call)
    assert push[-2:] == ["origin", f"{calls.head}:refs/heads/feature"]
    create = next(call for call in calls.calls if "pr" in call and "create" in call)
    # No --draft: the pull request opens Ready, so no `pr ready` call follows.
    assert "--draft" not in create
    assert not any("ready" in call for call in calls.calls)
    published = calls.published_bodies[-1]
    assert verification_section(published)[:len(DISCLOSURE)] == DISCLOSURE


def test_body_without_disclosure_refused_when_selection_bound(
    tmp_path: Path, monkeypatch
) -> None:
    """The same attestation with a body carrying no disclosure at all is refused
    before any outward call: a bound skip is never published undisclosed."""
    rc, err, calls = selected_publication(tmp_path, monkeypatch, [])

    assert rc == 1
    assert "push.contextual-body" in err
    assert DISCLOSURE[0] in err
    assert calls.calls == []


# --- push hook: the reason a blocked push names first -------------------------

MISSING_ATTESTATION = (
    "BLOCK push.attestation: branch must carry exactly one generated attestation; found 0"
    "; two legal routes, both run by the agent: run the closing-review station,"
    " which generates the attestation and needs no confirmation, so it is open"
    " in every session; or, in a session that can record a confirmation the user"
    " types and only once per change, because expert-mode allows the agent one"
    " skip proposal per change, propose a step selection"
    " (`loom_checker.py selection propose <change-id> --origin agent --skip reviewers`)"
    " that the user confirms by typing `/loom-code:expert-mode <code>`"
    " (Codex: `$expert-mode`) with the code"
    " the proposal printed, after which finalize-review drops the reviewer floor to"
    " zero and still emits an attestation recording the skip;"
    " never hand the blocked publication command to the user to run"
)
NONCANONICAL = "the entire Git push command must use canonical quote-all rendering"


def hook_repository(tmp_path: Path, *, attested: bool, monkeypatch) -> Path:
    repo = tmp_path / "hook-repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "switch", "-q", "-c", "feature")
    git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    if attested:
        attestation(repo)
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "attest")
        # Content validation is attestation.py's own contract; here only the
        # push hook's ordering and outcome are under test.
        monkeypatch.setattr(push_handler, "validate_attestation", lambda *_a, **_k: [])
    return repo


def canonical_push(repo: Path) -> str:
    head = git(repo, "rev-parse", "HEAD")
    return render_quote_all([
        "command", str(Path(shutil.which("git")).resolve()), "-C", str(repo),
        "push", *CANONICAL_PUSH_FLAGS, "origin", f"{head}:refs/heads/feature",
    ])


def run_push_hook(
    monkeypatch, repo: Path, command: str, *, payload_cwd: Path | None = None
) -> tuple[int, str]:
    """`payload_cwd` is the directory the Bash tool would run the command in.
    The hook chdirs to the repository root regardless, so the two differ
    whenever the agent works from a subdirectory of the repository."""
    payload = {
        "cwd": str(payload_cwd or repo),
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }
    monkeypatch.setattr(push_handler, "read_hook_payload", lambda: payload)
    monkeypatch.chdir(repo)
    err = StringIO()
    rc = push_handler.cmd_push(["--hook"], StringIO(), err)
    return rc, err.getvalue()


@pytest.mark.parametrize("command", [
    "git push origin feature",
    "git push -u origin feature",
])
def test_plain_push_without_attestation_reason_names_attestation(
    tmp_path: Path, monkeypatch, command: str
) -> None:
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, command)

    lines = err.splitlines()
    assert rc == 2
    assert lines[0] == MISSING_ATTESTATION
    assert any(NONCANONICAL in line for line in lines[1:])


def test_missing_attestation_names_both_routes(tmp_path: Path, monkeypatch) -> None:
    """The refusal keeps its existing reason and adds the two legal routes plus
    the rule that the blocked command is never handed to the user."""
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    reason = err.splitlines()[0]
    assert rc == 2
    assert reason.startswith(
        "BLOCK push.attestation: branch must carry exactly one generated attestation; found 0"
    )
    assert "closing-review" in reason
    assert (
        "selection propose <change-id> --origin agent --skip reviewers" in reason
    )
    assert "confirms by typing `/loom-code:expert-mode <code>`" in reason
    assert "never hand the blocked publication command to the user to run" in reason


def test_only_the_confirmation_route_is_named_conditionally(
    tmp_path: Path, monkeypatch
) -> None:
    """Route two binds only where the session records a confirmation the user
    types: a nested unattended session, a confirmation landing in a later
    session, and a host without prompt capture each leave it dead, which
    `test_probe_route_two_really_is_unavailable_there` runs. So the clause that
    names it states that condition, and route one -- which needs no
    confirmation at all -- keeps being named without one.

    The refusal is not asked to read session state to decide: that would put a
    mechanism inside a message, and PRINCIPLES.md non-negotiable 4 wants a
    declared budget exception before the net mechanism count rises. A sentence
    that is true in every session costs nothing."""
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    reason = err.splitlines()[0]
    before, separator, _after = reason.partition("propose a step selection")
    assert rc == 2
    assert separator, reason
    assert "run the closing-review station" in before
    assert "needs no confirmation" in before
    assert "record a confirmation the user types" in before


# The tail for a count greater than one. The two routes are absent: closing
# review rewrites one attestation in place and a confirmed skip emits one, so
# neither can take a branch from two attested changes down to one.
EXTRA_ATTESTED_CHANGES = (
    "BLOCK push.attestation: branch must carry exactly one generated attestation; found 2"
    "; a publication covers exactly one change, so neither route out of a missing"
    " attestation applies here: the branch delta has to end at one attested change"
    " first, by landing the other changes from their own branches or by taking"
    " their attestations out of this delta;"
    " never hand the blocked publication command to the user to run"
)


def two_attested_changes(tmp_path: Path, monkeypatch) -> Path:
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)
    attestation(repo, "change-a")
    attestation(repo, "change-b")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "attest two changes")
    return repo


def test_more_than_one_attestation_names_what_actually_helps(
    tmp_path: Path, monkeypatch
) -> None:
    """A branch attesting two changes is refused under the same rule with the
    same reason opening, and is told what reduces the count -- not the two
    routes, neither of which can."""
    repo = two_attested_changes(tmp_path, monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    assert rc == 2
    assert err.splitlines()[0] == EXTRA_ATTESTED_CHANGES
    assert "two legal routes" not in err
    assert "selection propose" not in err


def test_more_than_one_attestation_reason_stays_one_line(
    tmp_path: Path, monkeypatch
) -> None:
    """The count-greater-than-one tail obeys the same one-line contract as the
    routes: report() writes one BLOCK line per failure."""
    repo = two_attested_changes(tmp_path, monkeypatch)
    monkeypatch.chdir(repo)
    err = StringIO()

    rc = push_handler._cmd_push([], StringIO(), err)

    assert rc == 1
    assert len(err.getvalue().splitlines()) == 1, err.getvalue()


def test_one_attested_change_per_branch_clears_the_count_refusal(
    tmp_path: Path, monkeypatch
) -> None:
    """The action the reason names is one the branch can actually take: with the
    second change's attestation out of the delta, the count refusal is gone."""
    repo = two_attested_changes(tmp_path, monkeypatch)
    git(repo, "rm", "-q", "-r", "docs/loom/change-b")
    git(repo, "commit", "-q", "-m", "publish one change per branch")
    monkeypatch.chdir(repo)
    err = StringIO()

    push_handler._cmd_push([], StringIO(), err)

    assert "branch must carry exactly one generated attestation" not in err.getvalue()


def test_missing_attestation_reason_stays_one_line(tmp_path: Path, monkeypatch) -> None:
    """report() writes one line per failure, so the reason must not wrap: a
    continuation line would not carry the BLOCK prefix every caller parses."""
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)
    monkeypatch.chdir(repo)
    err = StringIO()

    rc = push_handler._cmd_push([], StringIO(), err)

    assert rc == 1
    assert len(err.getvalue().splitlines()) == 1, err.getvalue()


def test_unattested_unconfirmed_push_still_refused(tmp_path: Path, monkeypatch) -> None:
    """No attestation and no confirmed step selection: the canonical publication
    command is refused exactly as before, same rule id, same exit code."""
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, canonical_push(repo))

    lines = err.splitlines()
    assert rc == 2
    assert lines[0].startswith("BLOCK push.attestation: ")
    assert all(line.startswith("BLOCK ") for line in lines), err


def test_attested_noncanonical_push_still_blocked(tmp_path: Path, monkeypatch) -> None:
    repo = hook_repository(tmp_path, attested=True, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    assert rc == 2
    assert err.splitlines() == [f"BLOCK push.attestation: {NONCANONICAL}"]


def test_canonical_attested_push_allowed(tmp_path: Path, monkeypatch) -> None:
    repo = hook_repository(tmp_path, attested=True, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, canonical_push(repo))

    assert (rc, err) == (0, "")


# --- the hook route reaches publish's disclosure verdict (finding F5) --------


def canonical_pr_create(repo: Path, body: Path) -> str:
    """The one trusted metadata-only PR-opening command the ship station runs."""
    return render_quote_all([
        "command", str(Path(shutil.which("env")).resolve()),
        f"LOOM_REPO_ROOT={repo.resolve()}",
        f"GH_REPO={github_repo_from_origin(repo)}",
        str(Path(shutil.which("gh")).resolve()), "pr", "create",
        "--head", "feature", "--title", "feat(loom): safe", "--body-file", str(body),
    ])


def hook_repository_with_a_selection(
    tmp_path: Path, monkeypatch, selection: dict | None
) -> Path:
    """A branch whose sole attestation records this step selection, published
    through the PR-opening hook rather than through the publication command."""
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)
    attestation(repo).write_text(
        json.dumps({"change_id": "change", "selection": selection}), encoding="utf-8"
    )
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "attest")
    # Attestation content is attestation.py's own contract; the live remote-head
    # lookup is the external seam, answered with the state that holds right
    # after a successful push. Neither is what this route is under test for.
    monkeypatch.setattr(push_handler, "validate_attestation", lambda *_a, **_k: [])
    monkeypatch.setattr(push_handler, "check_pr_create_remote_head", lambda *_a, **_k: None)
    return repo


def test_hook_refuses_a_pr_body_that_hides_the_skip(tmp_path: Path, monkeypatch) -> None:
    """A skip the user typed reaches a pull request only disclosed, whichever
    route opens it: the hook refuses the very body publish refuses, under the
    same rule id and for the same reason.

    Not byte for byte: the rule renders the disclosure it expects over several
    lines, and this route writes one `BLOCK` line per failure, so the reason is
    flattened here and nowhere else. Every word of it is still the rule's own --
    the comparison is against `" ".join(expected.split("\\n"))`, not against a
    second copy of the sentence."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    body = tmp_path / "hook-body-no-disclosure.md"
    body.write_text(contextual_body(), encoding="utf-8")

    rc, err = run_push_hook(monkeypatch, repo, canonical_pr_create(repo, body))

    expected = publish_rules.validate_selection_disclosure(
        contextual_body(), {"selection": SELECTION}
    )
    assert rc == 2
    assert "\n" in expected, "premise: the rule's reason is the multi-line one"
    assert err == f"BLOCK push.contextual-body: {' '.join(expected.split(chr(10)))}\n"


def test_hook_admits_a_pr_body_that_discloses_the_skip(tmp_path: Path, monkeypatch) -> None:
    """Control: the same route with the attestation's own disclosure present is
    admitted, so the refusal above is the body being read, not the route being
    closed."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    body = tmp_path / "hook-body-disclosed.md"
    body.write_text(disclosed_body(DISCLOSURE), encoding="utf-8")

    rc, err = run_push_hook(monkeypatch, repo, canonical_pr_create(repo, body))

    assert (rc, err) == (0, "")


def test_hook_admits_an_undisclosing_body_when_nothing_was_skipped(
    tmp_path: Path, monkeypatch
) -> None:
    """An attestation recording no selection keeps behaving as it does today:
    there is nothing to disclose, so a body carrying no disclosure line passes."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, None)
    body = tmp_path / "hook-body-nothing-skipped.md"
    body.write_text(contextual_body(), encoding="utf-8")

    rc, err = run_push_hook(monkeypatch, repo, canonical_pr_create(repo, body))

    assert (rc, err) == (0, "")


def test_hook_refuses_a_false_disclosure_when_nothing_was_skipped(
    tmp_path: Path, monkeypatch
) -> None:
    """The verdict is publish's whole verdict, not just its skipped-steps half:
    a disclosure line with no selection behind it is false either way."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, None)
    body = tmp_path / "hook-body-false-disclosure.md"
    body.write_text(disclosed_body([DISCLOSURE[0]]), encoding="utf-8")

    rc, err = run_push_hook(monkeypatch, repo, canonical_pr_create(repo, body))

    assert rc == 2
    assert err.startswith("BLOCK push.contextual-body: ")


def test_hook_reads_the_body_file_gh_would_send(tmp_path: Path, monkeypatch) -> None:
    """A second `--body-file` is the file gh sends, so it is the file the gate
    reads: the disclosing one first cannot cover a hiding one after it."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    disclosed = tmp_path / "first-disclosed.md"
    disclosed.write_text(disclosed_body(DISCLOSURE), encoding="utf-8")
    hidden = tmp_path / "second-hidden.md"
    hidden.write_text(contextual_body(), encoding="utf-8")
    command = canonical_pr_create(repo, disclosed) + " " + render_quote_all(
        ["--body-file", str(hidden)]
    )

    rc, err = run_push_hook(monkeypatch, repo, command)

    assert rc == 2
    assert err.startswith("BLOCK push.contextual-body: ")


# --- the trailing-option allowlist (finding F8) -------------------------------

# The refusal every command outside the canonical form earns.
NOT_CANONICAL = (
    "BLOCK push.attestation: PR creation must use the canonical "
    "trusted-gh command from loom-code:ship\n"
)


def test_hook_refuses_the_short_body_file_spelling(tmp_path: Path, monkeypatch) -> None:
    """`-F` is not on the allowlist, so it is refused before the body is read.

    It is the one option the hook could read and resolve differently from the
    shell: `pr_create_body` resolves a relative path against the repository
    root the hook chdirs to, and the absoluteness rule covers `--body-file`
    and `--body-file=` only. Admission closes that, not a wider parser."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    body = tmp_path / "short-option.md"
    body.write_text(disclosed_body(DISCLOSURE), encoding="utf-8")
    command = render_quote_all([
        "command", str(Path(shutil.which("env")).resolve()),
        f"LOOM_REPO_ROOT={repo.resolve()}",
        f"GH_REPO={github_repo_from_origin(repo)}",
        str(Path(shutil.which("gh")).resolve()), "pr", "create",
        "--head", "feature", "--title", "feat(loom): safe", "-F", str(body),
    ])

    rc, err = run_push_hook(monkeypatch, repo, command)

    assert (rc, err) == (2, NOT_CANONICAL)


def test_hook_refuses_a_relative_body_path_the_shell_resolves_elsewhere(
    tmp_path: Path, monkeypatch
) -> None:
    """The divergence F8 names, end to end: one path, two files. The gate reads
    the disclosing copy at the repository root; the shell would read the hiding
    copy in the directory the Bash tool runs in."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    (repo / "rel.md").write_text(disclosed_body(DISCLOSURE), encoding="utf-8")
    sub = repo / "sub"
    sub.mkdir()
    (sub / "rel.md").write_text(contextual_body(), encoding="utf-8")
    command = render_quote_all([
        "command", str(Path(shutil.which("env")).resolve()),
        f"LOOM_REPO_ROOT={repo.resolve()}",
        f"GH_REPO={github_repo_from_origin(repo)}",
        str(Path(shutil.which("gh")).resolve()), "pr", "create",
        "--head", "feature", "--title", "feat(loom): safe", "-F", "rel.md",
    ])

    rc, err = run_push_hook(monkeypatch, repo, command, payload_cwd=sub)

    assert (rc, err) == (2, NOT_CANONICAL)


@pytest.mark.parametrize("trailing", [
    ["--fill"],                       # gh composes the body from the commits
    ["--editor"],                     # the body is typed in an editor
    ["--template", "PR.md"],          # gh seeds the body from a template
    ["--recover", "state.json"],      # the body is restored from saved state
    ["--web"],                        # the body is composed in a browser
    ["--assignee", "someone"],        # not body-bearing, and still not canonical
])
def test_hook_refuses_every_option_outside_the_allowlist(
    tmp_path: Path, monkeypatch, trailing: list[str]
) -> None:
    """An option the canonical form does not name is refused, whether or not it
    determines the body. Coverage of gh's body-bearing flags would have to
    track gh's release notes; admission does not."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    body = tmp_path / "allowlist-body.md"
    body.write_text(disclosed_body(DISCLOSURE), encoding="utf-8")
    command = canonical_pr_create(repo, body) + " " + render_quote_all(trailing)

    rc, err = run_push_hook(monkeypatch, repo, command)

    assert (rc, err) == (2, NOT_CANONICAL)


def test_hook_still_admits_the_allowlisted_publication_options(
    tmp_path: Path, monkeypatch
) -> None:
    """Control: the options the allowlist names are still admitted together, so
    the refusals above are the allowlist working and not the route closing."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    body = tmp_path / "allowlisted.md"
    body.write_text(disclosed_body(DISCLOSURE), encoding="utf-8")
    command = render_quote_all([
        "command", str(Path(shutil.which("env")).resolve()),
        f"LOOM_REPO_ROOT={repo.resolve()}",
        f"GH_REPO={github_repo_from_origin(repo)}",
        str(Path(shutil.which("gh")).resolve()), "pr", "create",
        "--base", "main", "--head", "feature", "--draft",
        "--title", "feat(loom): safe", "--body-file", str(body),
    ])

    rc, err = run_push_hook(monkeypatch, repo, command)

    assert (rc, err) == (0, "")


# --- the hook route runs the whole body rule it names (finding F9) ------------


def test_hook_enforces_the_structural_half_of_the_body_rule(
    tmp_path: Path, monkeypatch
) -> None:
    """The hook prints `push.contextual-body`, so it owes the whole rule: the
    nine-heading floor and the chain-of-thought ban, not the disclosure clause
    alone. This body has nothing to disclose and fails everything else."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, None)
    body = tmp_path / "naked.md"
    body.write_text(
        "no headings at all, and this body claims to expose private "
        "chain-of-thought.\n",
        encoding="utf-8",
    )

    rc, err = run_push_hook(monkeypatch, repo, canonical_pr_create(repo, body))

    assert rc == 2
    assert err == (
        "BLOCK push.contextual-body: "
        + publish_rules.validate_contextual_pr_body(body.read_text(encoding="utf-8"))
        + "\n"
    )


def test_hook_refuses_a_body_it_could_not_read_even_with_nothing_to_disclose(
    tmp_path: Path, monkeypatch
) -> None:
    """A body the gate cannot read is "", and "" has none of the nine headings.
    Every gh input the hook cannot see therefore refuses on its own, instead of
    refusing only where a recorded skip gave the disclosure clause something to
    say."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, None)
    absent = tmp_path / "absent.md"

    rc, err = run_push_hook(monkeypatch, repo, canonical_pr_create(repo, absent))

    assert rc == 2
    assert err.startswith("BLOCK push.contextual-body: ")
    assert 'heading "Context" is missing' in err


# --- the body read cannot hang or overrun the hook (finding F10) --------------


def read_body_in_a_subprocess(path: str, timeout: int = 10) -> str:
    """`pr_create_body` on one path, in a process this test can outlive: a hang
    has to fail the test rather than hang the suite. A `PreToolUse` hook has no
    timeout of its own, so a blocking read there blocks the agent."""
    command = render_quote_all([
        "command", "env", "LOOM_REPO_ROOT=/", "GH_REPO=x",
        "gh", "pr", "create", "--body-file", path,
    ])
    script = (
        "import sys; sys.path.insert(0, %r)\n"
        "from loom_checker.rule_checks.push import pr_create_body\n"
        "print(repr(pr_create_body(%r)))\n"
        % (str(Path(__file__).resolve().parent), command)
    )
    done = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=timeout
    )
    assert done.returncode == 0, done.stderr
    return done.stdout.strip()


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="needs FIFOs")
def test_body_read_does_not_block_on_a_fifo(tmp_path: Path) -> None:
    """A FIFO with no writer blocks `open` forever. The guard refuses it before
    a byte is read, so the hook answers instead of hanging."""
    fifo = tmp_path / "fifo.md"
    os.mkfifo(fifo)

    try:
        assert read_body_in_a_subprocess(str(fifo)) == "''"
    except subprocess.TimeoutExpired:
        pytest.fail("pr_create_body blocked on a FIFO")


@pytest.mark.skipif(not Path("/dev/zero").exists(), reason="needs /dev/zero")
def test_body_read_does_not_run_away_on_a_character_device(tmp_path: Path) -> None:
    """The unbounded-read variant: `/dev/zero` never ends. The same guard
    refuses it, because it is not a regular file either."""
    try:
        assert read_body_in_a_subprocess("/dev/zero") == "''"
    except subprocess.TimeoutExpired:
        pytest.fail("pr_create_body read an unbounded character device")


@pytest.mark.parametrize("path", ["-", "/dev/stdin"])
def test_body_read_refuses_the_paths_that_name_a_stream(
    tmp_path: Path, path: str
) -> None:
    """`-` is gh's spelling for stdin, which the gate cannot see: it reads ""
    rather than whatever file happens to be named `-` in the working
    directory."""
    assert read_body_in_a_subprocess(path) == "''"


def test_body_read_refuses_a_directory(tmp_path: Path) -> None:
    """A directory is not a regular file; the read fails rather than the gate."""
    assert read_body_in_a_subprocess(str(tmp_path)) == "''"


def test_body_read_still_returns_a_regular_file(tmp_path: Path) -> None:
    """Control: the guard refuses what cannot be finished, not the body."""
    body = tmp_path / "regular.md"
    body.write_text("hello\n", encoding="utf-8")

    assert read_body_in_a_subprocess(str(body)) == repr("hello\n")


# Allow (0) / block (2) outcomes pinned against commit 4e87e264, which
# introduced case-folded publisher detection (``GIT push`` blocks); the later
# reason reordering changes stderr text only, never this table.
BLOCKED_PUSH_MATRIX = [
    ("git status", 0, 0),
    ("ls -la", 0, 0),
    # Searching for the merge words is not merging. The rule was a text match
    # over the whole command and refused this; recognition is structural now.
    ("rg -n \"SEGMENT_SPLIT|publisher&&gh pr create|gh pr merge\" loom-code -g '*.py'", 0, 0),
    ("rg -n \"SEGMENT_SPLIT|publisher&&gh pr create\" loom-code -g '*.py'", 0, 0),
    ("printf '%s\\n' '$(git push origin HEAD)'", 0, 0),
    ("git push origin HEAD", 2, 2),
    ("git push origin feature", 2, 2),
    ("git push -u origin feature", 2, 2),
    ("git push --force origin main", 2, 2),
    ("'git' 'push' '-u' 'origin' 'feature'", 2, 2),
    ("zsh -c 'git push origin HEAD'", 2, 2),
    ("GIT push origin HEAD", 2, 2),
    ("cd relative && git push origin feature", 2, 2),
    ("echo \"$(git push origin HEAD)\"", 2, 2),
    ("gh pr create --fill", 2, 2),
    ("gh pr merge 123 --squash", 2, 2),
    ("eval 'gh pr create --fill'", 2, 2),
    ("<canonical>", 2, 0),
    ("<canonical-wrong-refspec>", 2, 2),
]


@pytest.mark.parametrize("attested", [False, True])
@pytest.mark.parametrize("command,unattested_rc,attested_rc", BLOCKED_PUSH_MATRIX)
def test_blocked_push_set_unchanged(
    tmp_path: Path, monkeypatch, attested: bool,
    command: str, unattested_rc: int, attested_rc: int,
) -> None:
    repo = hook_repository(tmp_path, attested=attested, monkeypatch=monkeypatch)
    if command == "<canonical>":
        command = canonical_push(repo)
    elif command == "<canonical-wrong-refspec>":
        command = canonical_push(repo).replace(":refs/heads/feature", ":refs/heads/other")

    rc, _ = run_push_hook(monkeypatch, repo, command)

    assert rc == (attested_rc if attested else unattested_rc)


# case-folded-publishers-blocked-on-every-host: publisher detection folds the
# executable basename on every host, not only on case-insensitive filesystems.
@pytest.mark.parametrize("command", [
    "GIT push origin HEAD",
    "/usr/bin/GIT push",
    "bash -c 'GIT push'",
    "GH pr create --fill",
    "Gh pr merge 1",
])
def test_case_folded_publishers_blocked_on_every_host(
    tmp_path: Path, monkeypatch, command: str
) -> None:
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, command)

    assert rc == 2
    assert "BLOCK" in err


# --- fix round: the repairs the closing review asked for ---------------------

EXPERT_MODE = Path(__file__).resolve().parents[1] / "skills" / "expert-mode" / "SKILL.md"


def test_hook_body_refusal_is_one_block_line_per_failure(
    tmp_path: Path, monkeypatch
) -> None:
    """R1: the hook route owes the same one-line-per-failure contract as every
    other refusal in the checker.

    `validate_selection_disclosure` renders the expected disclosure over several
    lines for a human reading `publish`'s output; written through the hook that
    becomes stderr lines with no `BLOCK ` prefix, which every caller that parses
    this stream -- including the adversarial module's own `_blocks()` -- reads as
    a line that is not a refusal at all."""
    repo = hook_repository_with_a_selection(tmp_path, monkeypatch, SELECTION)
    body = tmp_path / "hook-body-multiline-reason.md"
    body.write_text(contextual_body(), encoding="utf-8")

    rc, err = run_push_hook(monkeypatch, repo, canonical_pr_create(repo, body))

    assert rc == 2
    assert err.splitlines(), "the route refused and said nothing"
    for line in err.splitlines():
        assert line.startswith("BLOCK "), f"stderr line is not a BLOCK line: {line!r}"


def branch_whose_base_already_attests(
    tmp_path: Path, monkeypatch, *, trunk: str = "main"
) -> Path:
    """A branch off a base that already carries a generated attestation, adding
    nothing of its own -- the shape where closing review regenerates the bytes
    the base already holds and the attestation count never leaves zero.

    `trunk` names the branch the remote calls its default, which is not always
    `main` and is never this checker's to assume."""
    repo = tmp_path / "landed-repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    attestation(repo, "2026-09-18-already-landed")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "landed change")
    # The change landed, so the remote's default branch carries it. Both refs
    # are what `git clone` writes, and both are needed: the branch is the
    # snapshot, and `refs/remotes/origin/HEAD` is what says the remote calls
    # that branch its default. Without them the repository cannot tell this
    # branch from the finished-but-unpublished one below, and
    # `nothing_left_to_publish` answers False on that doubt.
    git(repo, "update-ref", f"refs/remotes/origin/{trunk}", "main")
    git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", f"refs/remotes/origin/{trunk}")
    git(repo, "switch", "-q", "-c", "feature")
    git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    monkeypatch.setattr(push_handler, "validate_attestation", lambda *_a, **_k: [])
    return repo


def test_a_branch_that_adds_nothing_is_not_sent_to_closing_review(
    tmp_path: Path, monkeypatch
) -> None:
    """R2: where the base already attests a change and the branch adds nothing,
    the closing-review route moves no count -- regenerating writes the same
    bytes -- so naming it loops the agent through a station forever. That state
    is told what is true of it instead."""
    repo = branch_whose_base_already_attests(tmp_path, monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    reason = err.splitlines()[0]
    assert rc == 2
    assert reason.startswith(
        "BLOCK push.attestation: branch must carry exactly one generated "
        "attestation; found 0"
    )
    assert "two legal routes" not in reason
    assert "closing-review" not in reason
    assert "selection propose" not in reason
    assert "nothing" in reason and "new intent" in reason
    assert "never hand the blocked publication command to the user to run" in reason


def test_a_branch_that_adds_work_still_gets_the_two_routes(
    tmp_path: Path, monkeypatch
) -> None:
    """Control for the branch above: the same base, a branch that carries work
    of its own. Closing review does move this count, so the routes stay -- the
    third tail is about an empty delta, not about a base that ever attested
    anything."""
    repo = branch_whose_base_already_attests(tmp_path, monkeypatch)
    (repo / "feature.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "work")

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    reason = err.splitlines()[0]
    assert rc == 2
    assert "two legal routes" in reason
    assert "run the closing-review station" in reason


def test_a_landed_branch_is_recognised_on_a_trunk_not_called_main(
    tmp_path: Path, monkeypatch
) -> None:
    """The same landed state on a remote whose default branch is `trunk`.

    Which branch a remote calls its default is the remote's to say, and git
    records the answer in `refs/remotes/origin/HEAD`. A checker that recognised
    a landed change only under two names it carries in a list would send every
    repository outside that list back into the loop the tail exists to end, and
    a third name added to the list is the same defect one repository later."""
    repo = branch_whose_base_already_attests(tmp_path, monkeypatch, trunk="trunk")

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    reason = err.splitlines()[0]
    assert rc == 2
    assert "this branch adds nothing" in reason
    assert "two legal routes" not in reason


def branch_finished_but_never_published(tmp_path: Path, monkeypatch) -> Path:
    """A branch whose work is done, reviewed and attested, with the local trunk
    fast-forwarded onto it and nothing published yet: `git branch -f main
    feature`.

    In git this is the same state as the landed branch above -- empty delta, the
    attestation in the base -- because which branch moved onto which is history,
    not content. The only witness that separates them is the published trunk,
    which here does not contain the base."""
    repo = tmp_path / "unpublished-repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "switch", "-q", "-c", "feature")
    git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    (repo / "feature.py").write_text("VALUE = 1\n", encoding="utf-8")
    attestation(repo, "2026-09-18-finished-change")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "work and its attestation")
    git(repo, "branch", "-f", "main", "feature")
    monkeypatch.setattr(push_handler, "validate_attestation", lambda *_a, **_k: [])
    return repo


def test_a_finished_branch_nobody_published_keeps_its_routes(
    tmp_path: Path, monkeypatch
) -> None:
    """R2, the state the empty-delta tail must not claim: the work is complete,
    reviewed and attested and has never been published, and the local trunk has
    been moved onto it. The two facts the third tail was built on -- an empty
    delta over an attesting base -- are both true here, so a tail that reads
    only those tells a finished change to start over from a new intent."""
    repo = branch_finished_but_never_published(tmp_path, monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    reason = err.splitlines()[0]
    assert rc == 2
    assert reason.startswith(
        "BLOCK push.attestation: branch must carry exactly one generated "
        "attestation; found 0"
    )
    assert "two legal routes" in reason
    assert "run the closing-review station" in reason
    assert "new intent" not in reason


def test_the_nothing_to_publish_tail_obeys_the_one_line_contract() -> None:
    """The third tail is appended to the same `BLOCK` line as the other two."""
    tail = push_handler.NOTHING_TO_PUBLISH
    assert tail.startswith("; ")
    assert not [character for character in tail if ord(character) < 0x20]


def test_route_two_is_named_under_the_cap_expert_mode_puts_on_it(
    tmp_path: Path, monkeypatch
) -> None:
    """R3: the station caps agent-originated skip proposals at one per change.
    A refusal that instructs `--origin agent` unconditionally tells an agent
    that has already spent it to do what the station forbids, and the effect of
    obeying is a second request that the user make a quality judgement.

    The cap is read from the station rather than remembered here, so a station
    that drops it takes this test with it."""
    station = " ".join(EXPERT_MODE.read_text(encoding="utf-8").split())
    assert "at most once per change" in station, (
        "premise: expert-mode caps agent-originated skip proposals"
    )
    repo = hook_repository(tmp_path, attested=False, monkeypatch=monkeypatch)

    rc, err = run_push_hook(monkeypatch, repo, "git push origin feature")

    reason = err.splitlines()[0]
    before, separator, _after = reason.partition("propose a step selection")
    assert rc == 2
    assert separator, reason
    assert "once per change" in before, (
        "route two instructs an agent-originated proposal, so it names the cap "
        "the station puts on that proposal"
    )


def test_an_unknown_attestation_count_names_no_count_and_no_route() -> None:
    """R5: `publication_advice(None)` served the above-one tail, which asserts a
    count nobody read and prescribes removing attestations the caller may not
    have. An unknown count gets a tail that claims neither."""
    tail = push_handler.publication_advice(None)
    assert tail.strip()
    assert tail is not push_handler.PUBLICATION_ROUTES
    assert tail is not push_handler.EXTRA_ATTESTED_CHANGES
    assert "two legal routes" not in tail
    assert "attested change first" not in tail
    assert "never hand the blocked publication command to the user to run" in tail


def test_the_pr_create_allowlist_carries_its_grounding_citations() -> None:
    """R4: `CANONICAL_PR_CREATE_OPTIONS` encodes gh's flag arities and
    `canonical_pr_create_trailing` encodes pflag's value-consumption rule. Both
    are claims about an external surface, and `check_pr_create_remote_head` in
    the same module cites its own inline -- so these carry the reference in the
    same form, where the reader meets the claim."""
    source = Path(push_rules.__file__).read_text(encoding="utf-8")
    above, _sep, _rest = source.partition("CANONICAL_PR_CREATE_OPTIONS = {")
    assert "https://cli.github.com/manual/gh_pr_create" in above.rsplit("\n\n", 1)[-1]
    trailing = source.partition("def canonical_pr_create_trailing")[2].partition("\ndef ")[0]
    assert "pflag" in trailing and "https://" in trailing


def test_the_refusal_names_both_confirmation_spellings_the_checker_accepts() -> None:
    """The refusal is what an agent reads at the moment of failure, and an agent
    on Codex reading it was shown one spelling while the ship station beside it
    gives two. Both are named here, in the station's own parenthetical form.

    Checked against `selection.ENTRY_TOKENS`, which is what decides whether a
    typed prompt binds anything -- not against the station's prose, which would
    only prove two documents agree. `ENTRY_TOKENS` accepts four spellings; the
    two the station names are the two named here, because a refusal that listed
    every accepted token would be teaching the token set rather than telling the
    user what to type."""
    forms = re.findall(r"`([^`]*expert-mode[^`]*)`", push_handler.PUBLICATION_ROUTES)
    assert [form.split()[0] for form in forms] == [
        "/loom-code:expert-mode", "$expert-mode"
    ], forms
    for form in forms:
        assert form.split()[0] in selection_store.ENTRY_TOKENS, form
