# concern: Help routing must not bypass validation, alter result streams, or grant authority.
# concern: Exact discovery must avoid handler, stdin, filesystem and subprocess work outside a repository.
"""Executable contract for `loom_checker.py`'s CLI surface (plan W0-02).

The rule-id table this asserts is a mechanism population: `--list-rules`
is the recomputable face of the checker for `docs/loom/evidence/
mechanisms.yaml` (concept-model §11), so the ids are pinned here and a
rename is a deliberate, visible edit rather than silent drift.
"""
from __future__ import annotations

import io
import json
import runpy
import socket
import subprocess
import sys
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "loom_checker.py"

EXPECTED_RULE_IDS = [
    "adversarial.proportionate",
    "ci.pr-floor",
    "contract.charter-complete",
    "contract.requires",
    "delivery.observed",
    "intake.attestation-coverage",
    "intake.commit-identity",
    "intake.confirmed",
    "intake.confirmed-behavior",
    "intake.intent-version",
    "intake.plan-boundary-tests",
    "intake.spec-ready",
    "intake.test-case-pair",
    "intent.kind-recompute",
    "intent.needs-design-reason",
    "intent.needs-design-recompute",
    "intent.product-no-identifiers",
    "intent.schema",
    "land.cleanup",
    "land.merge",
    "land.verify",
    "plan.field-caps",
    "publish.preconditions",
    "push.contextual-body",
    "review.sync",
    "spec.req-grammar",
    "spec.ui-flows-recompute",
    "standing.product-principles-reject",
    "standing.second-vendor-valid",
    "standing.silence",
    "standing.warn",
]


def run_checker(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
    )


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def make_intent_state_repo(tmp_path: Path, *, delivered: bool) -> tuple[Path, str]:
    repo = tmp_path / "intent-state-repo"
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    intent = repo / "docs/loom/intent/2026-09-09-example.md"
    intent.parent.mkdir(parents=True)
    intent.write_text(
        """# Example
originator: tester
kind: engineering
needs-design: no — fixture
status: confirmed 2026-09-09

## Problem
Fixture.

## Proposed outcome
Fixture.

## Acceptance
1. Fixture passes.

## Constraints
- none

## Out of scope
- none

## Open questions
- none
""",
        encoding="utf-8",
    )
    git(repo, "add", str(intent.relative_to(repo)))
    git(repo, "commit", "-q", "-m", "confirmed intent")
    if delivered:
        attestation = repo / "docs/loom/2026-09-09-example/attestation.json"
        attestation.parent.mkdir(parents=True)
        attestation.write_text(
            json.dumps(
                {
                    "schema": "loom-attestation/v1",
                    "change_id": "2026-09-09-example",
                    "content_digest": "historical",
                    "executions": [{
                        "kind": "package-tests", "command": "pytest", "artifact": "",
                        "result": "pass", "command_digest": "0" * 64,
                    }],
                    "verdicts": [{
                        "reviewer": "fixture", "vendor": "test", "model": "test",
                        "lens": "code", "verdict": "PASS", "findings": [],
                    }],
                    "findings": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        git(repo, "add", str(attestation.relative_to(repo)))
        git(repo, "commit", "-q", "-m", "deliver example (#123)")
    remote_head = git(repo, "rev-parse", "HEAD")
    git(repo, "update-ref", "refs/remotes/origin/trunk", remote_head)
    git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/trunk")
    git(repo, "checkout", "-q", "-b", "work")
    return repo, remote_head


def test_reviewer_count_cli_preserves_output_and_dirty_tree_error(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    (repo / "guide.md").write_text("Usage clarification.\n", encoding="utf-8")
    git(repo, "add", "guide.md")
    git(repo, "commit", "-q", "-m", "clarify usage")

    result = run_checker("reviewer-count", "2026-09-09-example", cwd=repo)
    assert (result.returncode, result.stdout, result.stderr) == (0, "1\n", "")

    (repo / "guide.md").write_text("Uncommitted change.\n", encoding="utf-8")
    result = run_checker("reviewer-count", "2026-09-09-example", cwd=repo)
    assert (result.returncode, result.stdout, result.stderr) == (
        2,
        "",
        "reviewer-count needs a clean tree with completed functional content.\n"
        'Help: "<loom-code>/scripts/loom-python" --ready reviewer-count --help '
        '(replace <loom-code> with the installed loom-code plugin directory).\n'
        'Suggested next step: Inspect the diagnostic and command help; select the intended repository, preserve outstanding work and establish a clean completed change before deliberately rerunning.\n',
    )


def test_reviewer_count_cli_preserves_argument_errors(tmp_path: Path) -> None:
    for args in [(), (" ",), ("change", "extra")]:
        result = run_checker("reviewer-count", *args, cwd=tmp_path)
        assert (result.returncode, result.stdout, result.stderr) == (
            2,
            "",
            "reviewer-count needs one change-id.\n"
            'Help: "<loom-code>/scripts/loom-python" --ready reviewer-count --help '
            '(replace <loom-code> with the installed loom-code plugin directory).\n'
            'Suggested next step: Inspect the diagnostic and command help; select the intended repository, preserve outstanding work and establish a clean completed change before deliberately rerunning.\n',
        )


def test_list_rules_exits_zero() -> None:
    assert run_checker("--list-rules").returncode == 0


def test_list_rules_emits_id_tab_description() -> None:
    lines = run_checker("--list-rules").stdout.splitlines()
    assert lines
    for line in lines:
        assert line.count("\t") == 1, line
        rule_id, description = line.split("\t")
        assert rule_id.strip() == rule_id
        assert description.strip() == description
        assert len(description.split()) >= 3, line


def test_list_rules_describes_the_closed_status_alternative() -> None:
    lines = run_checker("--list-rules").stdout.splitlines()
    confirmed_line = next(line for line in lines if line.startswith("intake.confirmed\t"))
    assert "closed" in confirmed_line
    assert "PR #" in confirmed_line
    assert "remote-default" in confirmed_line
    assert "indeterminate" in confirmed_line


def test_list_rules_covers_exactly_the_planned_population() -> None:
    ids = [line.split("\t")[0] for line in run_checker("--list-rules").stdout.splitlines()]
    assert ids == EXPECTED_RULE_IDS


def test_list_rules_is_sorted_and_stable() -> None:
    first = run_checker("--list-rules").stdout
    second = run_checker("--list-rules").stdout
    assert first == second
    ids = [line.split("\t")[0] for line in first.splitlines()]
    assert ids == sorted(ids)


def test_every_rule_id_is_area_dot_name() -> None:
    for line in run_checker("--list-rules").stdout.splitlines():
        rule_id = line.split("\t")[0]
        area, _, name = rule_id.partition(".")
        assert area in {"adversarial", "ci", "contract", "delivery", "intent", "intake", "land", "plan", "publish", "push", "review", "spec", "standing"}, rule_id
        assert name and "." not in name, rule_id


def test_unknown_subcommand_exits_2() -> None:
    result = run_checker("teleport")
    assert result.returncode == 2
    assert "teleport" in result.stderr


def test_no_arguments_exits_2() -> None:
    result = run_checker()
    assert result.returncode == 2
    assert result.stderr.strip()


def test_help_covers_commands_without_claiming_validation() -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")
    for flag in ("--help", "-h"):
        result = run_checker(flag)
        assert result.returncode == 0 and not result.stderr
        documented = {line.split()[1] for line in result.stdout.splitlines()
                      if line.strip().startswith("loom_checker.py ")}
        assert set(entry["COMMANDS"]) <= documented
        assert "plan <path-to-plan.md>" in result.stdout
        assert "intake <station> <change-id>" in result.stdout
        assert "No validation" in result.stdout
        assert '"<loom-code>/scripts/loom-python" --repair plan "<path-to-plan.md>"' in result.stdout
        assert "Replace <loom-code>" in result.stdout
        assert "push --install-git-hooks" in result.stdout
        assert "push --remove-git-hooks" in result.stdout
        assert run_checker(flag, "plan", "missing.md").returncode == 2


def test_publish_is_a_declared_cli_command() -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")

    assert entry["COMMANDS"]["publish"] is entry["cmd_publish"]
    assert "loom_checker.py publish --confirm-authorized" in entry["__doc__"]


def test_land_is_a_declared_cli_command() -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")

    assert entry["COMMANDS"]["land"] is entry["cmd_land"]
    assert "loom_checker.py land --accepted-by <name>" in entry["__doc__"]
    assert "loom_checker.py land --cleanup <branch>" in entry["__doc__"]
    assert "loom_checker.py land --sweep [--confirm <token>]" in entry["__doc__"]


def test_sync_trunk_is_a_declared_cli_command() -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")

    assert entry["COMMANDS"]["sync-trunk"] is entry["cmd_sync_trunk"]
    assert "loom_checker.py sync-trunk" in entry["__doc__"]


def test_intents_is_a_declared_cli_command() -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")

    assert entry["COMMANDS"]["intents"] is entry["cmd_intents"]
    assert "loom_checker.py intents" in entry["__doc__"]


def test_intents_lists_only_active_confirmed_intents_by_default(tmp_path: Path) -> None:
    active_repo, _ = make_intent_state_repo(tmp_path / "active", delivered=False)
    delivered_repo, _ = make_intent_state_repo(tmp_path / "delivered", delivered=True)

    active = run_checker("intents", cwd=active_repo)
    delivered = run_checker("intents", cwd=delivered_repo)

    assert active.returncode == 0
    assert active.stdout == "2026-09-09-example\tactive\n"
    assert delivered.returncode == 0
    assert delivered.stdout == ""


def test_intents_reports_one_delivered_intent_with_optional_metadata(tmp_path: Path) -> None:
    repo, remote_head = make_intent_state_repo(tmp_path, delivered=True)

    result = run_checker("intents", "2026-09-09-example", "--metadata", cwd=repo)

    assert result.returncode == 0
    assert result.stdout.startswith("2026-09-09-example\tdelivered")
    assert f"commit={remote_head}" in result.stdout
    assert "pr=#123" in result.stdout
    assert "committed_at=" in result.stdout
    assert "merged_at=" not in result.stdout


def test_intents_explains_why_one_intent_is_active(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)

    result = run_checker("intents", "2026-09-09-example", cwd=repo)

    assert result.returncode == 0
    assert result.stdout.startswith("2026-09-09-example\tactive\t")
    assert "attestation is absent" in result.stdout


def test_intents_reports_indeterminate_without_remote_default(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    git(repo, "symbolic-ref", "--delete", "refs/remotes/origin/HEAD")

    result = run_checker("intents", "2026-09-09-example", cwd=repo)

    assert result.returncode == 1
    assert "2026-09-09-example\tindeterminate" in result.stdout
    assert "refresh the selected remote-default ref" in result.stdout


def test_intents_rejects_an_unsafe_remote_name(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)

    result = run_checker("intents", "--remote", "../origin", cwd=repo)

    assert result.returncode == 2
    assert "safe literal" in result.stderr


def test_hooks_probe_is_gone() -> None:
    """`--self-test` in codex_scaffold.py owns the copy check; the reserved
    checker sub-command that never grew a body is deleted, not kept."""
    result = run_checker("hooks-probe")
    assert result.returncode == 2
    assert "unknown sub-command" in result.stderr
    assert "hooks-probe" not in CHECKER.read_text(encoding="utf-8").split('"""')[1]


def test_the_rule_population_is_thirty_one() -> None:
    assert len(run_checker("--list-rules").stdout.splitlines()) == 31


# --- contract --require (spec G) -------------------------------------------


def test_contract_require_accepts_a_met_floor() -> None:
    assert run_checker("contract", "--require", "2.0").returncode == 0


def test_contract_require_blocks_a_higher_minor() -> None:
    result = run_checker("contract", "--require", "2.99")
    assert result.returncode == 1
    assert "BLOCK contract.requires:" in result.stderr
    assert "請更新 loom-code" in result.stderr
    assert "Suggested next step: Update the plugin identified by the contract diagnostic" in result.stderr


def test_contract_require_blocks_a_different_major() -> None:
    result = run_checker("contract", "--require", "1.0")
    assert result.returncode == 1
    assert "contract.requires" in result.stderr


def test_contract_require_higher_major_still_says_update_loom_code() -> None:
    """The shipped contract (major 2) is below a higher required major (3):
    the checker itself is what's behind, so the old message direction
    ('please update loom-code') is correct and unchanged."""
    result = run_checker("contract", "--require", "3.0")
    assert result.returncode == 1
    assert "請更新 loom-code" in result.stderr


def test_contract_require_lower_major_blames_the_consuming_plugin() -> None:
    """The shipped contract (major 2) is above a lower required major (0):
    the CONSUMER declares an old contract major, not loom-code being behind
    -- the message must point at the consuming plugin, never say
    '請更新 loom-code'."""
    result = run_checker("contract", "--require", "0.5")
    assert result.returncode == 1
    assert "BLOCK contract.requires:" in result.stderr
    assert "請更新 loom-code" not in result.stderr
    assert "consuming plugin" in result.stderr
    assert "old contract major" in result.stderr
    assert "Suggested next step: Update the plugin identified by the contract diagnostic" in result.stderr


def test_contract_require_rejects_a_malformed_floor() -> None:
    assert run_checker("contract", "--require", "1").returncode == 2
    assert run_checker("contract").returncode == 2


def test_missing_operand_exits_2(tmp_path: Path) -> None:
    for argv in (["intent"], ["intake"], ["intake", "write-plan"], ["standing"]):
        result = run_checker(*argv, cwd=tmp_path)
        assert result.returncode == 2, argv
        assert result.stderr.strip(), argv


def test_internal_failure_fails_closed_with_exit_2(tmp_path: Path) -> None:
    """A path that cannot be read is an internal error, never a silent pass."""
    result = run_checker("intent", str(tmp_path / "nope.md"), cwd=tmp_path)
    assert result.returncode == 2


# --- descriptions carry the load-bearing condition (W2 re-review) ---------
#
# `--list-rules` is what a reader consults to learn what a rule actually
# recomputes. A description that stops short of the condition that blocks
# is how a reader forms the wrong model of the gate, so each one is pinned
# to the words that name its own mechanism.

LOAD_BEARING_WORDS = {
    "intake.spec-ready": ["pre-build-review", "not persisted", "ledger"],
    "intake.test-case-pair": ["Acceptance", "positive", "negative or boundary"],
    "contract.requires": ["same major", "minor"],
    "spec.ui-flows-recompute": ["visible characters", "reviewer"],
}


def test_descriptions_name_their_load_bearing_condition() -> None:
    described = dict(
        line.split("\t", 1)
        for line in run_checker("--list-rules").stdout.splitlines()
        if "\t" in line
    )
    for rule_id, words in LOAD_BEARING_WORDS.items():
        description = described[rule_id]
        missing = [word for word in words if word not in description]
        assert not missing, f"{rule_id} description omits {missing}: {description!r}"


# Self-service help is a public-entry contract, not handler-specific parsing.
def test_covered_help_is_discoverable_and_explains_inputs(tmp_path: Path) -> None:
    overall = run_checker("--help", cwd=tmp_path).stdout
    required = {
        "finalize-review": ["--input", "reviewer", "vendor", "model", "lens",
                            "verdict", "findings", "adversarial", "no_program",
                            "review_target_sha", "reviewed_sha", "diff base",
                            "skills/closing-review/SKILL.md"],
        "publish": ["--intent", "--confirm-authorized", "--title", "--body-file",
                    "## Context", "## Intended outcome", "## Scope", "## Decisions",
                    "## Implementation", "## Behaviour change", "## Verification",
                    "## Risks and rollback", "## Follow-ups", "Verification status:",
                    "skills/ship/SKILL.md"],
        "delivery": ["--goal", "local", "published", "merged", "--intent", "--json",
                     "state", "reason", "next", "evidence", "complete"],
        "plan": ["<path", "charter:", "1.1", "empty", "field", "Exit 1", "Exit 2"],
        "intake": ["write-spec", "write-plan", "change-id", "interface-surfaces",
                   "stdout", "BLOCK", "Exit 1", "Exit 2"],
        "reviewer-count": ["change-id", "clean", "committed", "floor", "two", "Exit 2",
                           "--json", "reviewer_floor", "null", "exit 86", "parseability"],
        "intent": ["--commit-msg", "stdout", "stderr", "Exit 1", "Exit 2"],
        "intents": ["--remote", "origin", "--metadata", "committer", "indeterminate"],
        "push": ["--hook", "--install-git-hooks", "--remove-git-hooks", "core.hooksPath", "three"],
        "land": ["--accepted-by", "--cleanup", "--sweep", "--confirm", "fetch", "merge"],
        "sync-trunk": ["fetch", "rebase", "merge", "WARN", "Exit 1", "Exit 2"],
        "github-rules": ["--print-setup", "advisory", "unconfirmed", "Exit 2"],
        "pr-floor": ["--body-file", "--base", "--head", "--branch", "GITHUB_STEP_SUMMARY"],
        "standing": ["PRINCIPLES.md", "DESIGN.md", "ARCHITECTURE.md", "stderr", "Exit 1"],
        "contract": ["--require", "major", "minor", "manifest", "Exit 1", "Exit 2",
                     "--json", "contract_version", "required_version", "compatible", "last --require wins"],
        "charter": ["--manifest", "table", "stdout", "BLOCK", "Exit 2"],
    }
    for command, words in required.items():
        assert f"{command} --help" in overall
        for flag in ("--help", "-h"):
            result = run_checker(command, flag, cwd=tmp_path)
            assert (result.returncode, result.stderr) == (0, "")
            assert all(word in result.stdout for word in words), result.stdout
            assert "No validation or publication" in result.stdout
            assert "Replace <loom-code>" in result.stdout
    assert not list(tmp_path.iterdir())


def test_exact_help_never_dispatches_handlers(monkeypatch, tmp_path: Path) -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")
    def forbidden(*args, **kwargs):
        raise AssertionError("help performed work")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "stdin", type("Unreadable", (), {"read": forbidden})())
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(Path, "write_text", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    for command in entry["COMMANDS"]:
        monkeypatch.setitem(entry["COMMANDS"], command, forbidden)
        for flag in ("--help", "-h"):
            out, err = io.StringIO(), io.StringIO()
            assert entry["main"]([command, flag], out, err) == 0
            assert out.getvalue() and not err.getvalue()
        out, err = io.StringIO(), io.StringIO()
        assert entry["main"]([command, "--help", "extra"], out, err) == 2
        assert not out.getvalue() and "help performed work" in err.getvalue()
    assert not list(tmp_path.iterdir())


def test_usage_and_evidence_rejections_keep_diagnostics_and_add_one_hint(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    malformed = tmp_path / "review.json"
    malformed.write_text("{", encoding="utf-8")
    cases = [
        (["finalize-review"], 2, "finalize-review needs a change-id."),
        (["finalize-review", "2026-09-09-example", "--input", str(malformed)],
         2, "cannot read review input:"),
        (["publish"], 2, "publish: --intent or --confirm-authorized is required"),
        (["delivery", "--goal", "invalid"], 2, "delivery: --goal must be local, published or merged"),
        (["plan"], 2, "plan needs a path."),
        (["plan", str(tmp_path / "absent.md")], 2, "no such plan file:"),
        (["intake"], 2, "intake needs a station and a change-id."),
        (["intake", "unknown", "example"], 2, "unknown station"),
        (["reviewer-count"], 2, "reviewer-count needs one change-id."),
    ]
    for argv, code, diagnostic in cases:
        result = run_checker(*argv, cwd=repo)
        assert result.returncode == code and not result.stdout
        assert result.stderr.startswith(diagnostic)
        assert result.stderr.count(f'--ready {argv[0]} --help') == 1
    malformed.write_text("{}", encoding="utf-8")
    result = run_checker(*cases[1][0], cwd=repo)
    assert result.returncode == 1 and not result.stdout
    assert result.stderr.startswith("BLOCK finalize.verdicts: review input has no verdicts\n")
    assert result.stderr.count("--ready finalize-review --help") == 1
    plan = tmp_path / "invalid-plan.md"
    plan.write_text("charter: 1.1\n", encoding="utf-8")
    result = run_checker("plan", str(plan), cwd=repo)
    assert result.returncode == 1 and not result.stdout
    assert result.stderr.startswith("BLOCK plan.field-caps:")
    assert result.stderr.count("--ready plan --help") == 1


def test_help_explains_outcomes_and_authority(tmp_path: Path) -> None:
    finalize = run_checker("finalize-review", "--help", cwd=tmp_path).stdout
    publish = run_checker("publish", "--help", cwd=tmp_path).stdout
    delivery = run_checker("delivery", "--help", cwd=tmp_path).stdout
    push = run_checker("push", "--help", cwd=tmp_path).stdout
    land = run_checker("land", "--help", cwd=tmp_path).stdout
    assert "original verdict" in finalize and "clean" in finalize
    assert "stage" in finalize and "overall" in finalize
    assert "authorization" in publish and "legacy" in publish
    assert "No required checks registered" in publish
    assert "remote write" in publish and "delivery" in publish
    assert "complete: false" in delivery and "exit 1" in delivery and "exit 2" in delivery
    assert "loom.protectMain=false" in push and "allows" in push
    assert "trunk not updated" in land and "exit 0" in land
    caveats = {
        "publish": ("in this order", "no other", "temporary", "upstream", "server default", "nonblank"),
        "delivery": ("action_required", "missing_pr", "No required checks", "authenticated"),
        "push": ("literal", "shared", "fast-forward", "reset/rebase"),
        "land": ("originator", "360", "10-second", "not a gate", "next: cd"),
        "github-rules": ("template not on", "before", "without --print-setup"),
        "intent": ("branch base",),
        "intake": ("branch base", "closed", "delivered", "indeterminate"),
        "contract": ("older major", "update loom-code"),
        "standing": ("existence", "product", "KICKOFF-DEFAULTS.md"),
    }
    missing = []
    for command, terms in caveats.items():
        text = run_checker(command, "--help", cwd=tmp_path).stdout
        missing.extend((command, term) for term in terms if term not in text)
    assert not missing, missing


def test_incomplete_delivery_keeps_json_stdout(tmp_path: Path) -> None:
    result = run_checker("delivery", "--goal", "local", "--json", cwd=tmp_path)
    assert result.returncode == 1
    observed = json.loads(result.stdout)
    assert set(observed) == {"state", "reason", "next", "evidence", "complete"}
    assert observed["complete"] is False and observed["state"] == "unconfirmed"
    assert result.stderr.count("--ready delivery --help") == 1


def test_dispatch_preserves_success_internal_errors_and_hooks(monkeypatch) -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")
    for command in ("finalize-review", "publish", "delivery", "push", "plan", "intake", "reviewer-count"):
        for code in (0, 1, 2):
            def handler(args, out, err):
                out.write('{"unchanged": true}\n')
                err.write("original diagnostic\n")
                return code
            monkeypatch.setitem(entry["COMMANDS"], command, handler)
            out, err = io.StringIO(), io.StringIO()
            assert entry["main"]([command, "--hook"], out, err) == code
            assert out.getvalue() == '{"unchanged": true}\n'
            hint_expected = code != 0 and command in {"finalize-review", "publish", "plan", "intake", "reviewer-count"}
            assert ("--help" in err.getvalue()) == hint_expected
            assert err.getvalue().startswith("original diagnostic\n")
        def crash(args, out, err):
            raise RuntimeError("fixture crash")
        monkeypatch.setitem(entry["COMMANDS"], command, crash)
        out, err = io.StringIO(), io.StringIO()
        assert entry["main"]([command], out, err) == 2
        expected = "loom_checker internal error: RuntimeError: fixture crash\n"
        if command == "reviewer-count":
            expected += "Suggested next step: Investigate the reported failure and preserve outstanding work; no reliable repair is known.\n"
        assert err.getvalue() == expected
        if command == "push":
            assert entry["main"]([command, "--hook"], io.StringIO(), io.StringIO()) == 0


def test_nonexact_help_forms_retain_normal_rejection(tmp_path: Path) -> None:
    for command in ("finalize-review", "publish", "delivery", "unknown", "plan", "intake", "reviewer-count"):
        for args in (("--help", "extra"), ("extra", "--help"), ("-h", "extra")):
            result = run_checker(command, *args, cwd=tmp_path)
            assert result.returncode != 0
            assert "No validation or publication" not in result.stdout
    hook = run_checker("delivery", "--hook", "--help", cwd=tmp_path)
    assert (hook.returncode, hook.stdout, hook.stderr) == (
        2, "", "delivery: use --hook alone or --hook --host claude|codex\n")


def test_planning_checks_preserve_real_success_and_conditional_stdout(tmp_path: Path, monkeypatch) -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_loom_checker_entry")
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    monkeypatch.chdir(repo)
    plan = tmp_path / "empty.md"
    plan.write_text("", encoding="utf-8")
    result = run_checker("plan", str(plan), cwd=repo)
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")
    for station in ("write-spec", "write-plan"):
        args = [station, "2026-09-09-example"]
        out, err = io.StringIO(), io.StringIO()
        code = entry["cmd_intake"](args, out, err)
        result = run_checker("intake", *args, cwd=repo)
        assert code == result.returncode == 0
        assert result.stdout == out.getvalue()
        assert result.stdout.startswith("interface-surfaces (")
        assert result.stderr == err.getvalue() == ""
    invalid = repo / "docs/loom/2026-09-09-example/plan.md"
    invalid.parent.mkdir(parents=True)
    invalid.write_text("charter: 1.1\n", encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()
    args = ["write-plan", "2026-09-09-example"]
    code = entry["cmd_intake"](args, out, err)
    result = run_checker("intake", *args, cwd=repo)
    assert code == result.returncode == 1
    assert result.stdout == out.getvalue()
    assert result.stdout.startswith("interface-surfaces (")
    assert result.stderr.startswith(err.getvalue()) and "BLOCK plan.field-caps:" in result.stderr
    assert result.stderr.count("--ready intake --help") == 1
