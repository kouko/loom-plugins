"""fix:W1-05 — the package-tests runner runs one pytest session per group."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUNNER = REPO / "scripts" / "run_package_tests.py"
sys.path.insert(0, str(RUNNER.parent))
from run_package_tests import loom_family_commands, split_groups  # noqa: E402


def test_split_groups_separates_on_double_dash() -> None:
    assert split_groups(["a/", "-q", "--then", "b/", "-q"]) == [["a/", "-q"], ["b/", "-q"]]
    assert split_groups(["a/"]) == [["a/"]]
    assert split_groups(["--then", "b/"]) == [["b/"]]


def test_runner_exit_code_is_nonzero_when_a_later_group_fails(tmp_path: Path) -> None:
    ok = tmp_path / "ok"; ok.mkdir()
    (ok / "test_ok.py").write_text("def test_ok():\n    assert True\n")
    bad = tmp_path / "bad"; bad.mkdir()
    (bad / "test_bad.py").write_text("def test_bad():\n    assert False\n")
    good = subprocess.run([sys.executable, str(RUNNER), str(ok), "-q", "-p", "no:cacheprovider"], capture_output=True)
    assert good.returncode == 0, good.stdout
    mixed = subprocess.run([sys.executable, str(RUNNER), str(ok), "-q", "-p", "no:cacheprovider", "--then", str(bad), "-q", "-p", "no:cacheprovider"], capture_output=True)
    assert mixed.returncode != 0


def test_runner_with_no_groups_exits_nonzero() -> None:
    for argv in ([], ["--then"]):
        result = subprocess.run([sys.executable, str(RUNNER), *argv], capture_output=True)
        assert result.returncode == 2, argv


def test_loom_family_only_requires_a_group_name() -> None:
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--loom-family", "--only"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "--only needs a group" in result.stderr


def test_loom_family_preset_covers_every_ci_test_surface() -> None:
    commands = loom_family_commands(REPO, verbosity="-q")
    rendered = [" ".join(command) for command in commands]

    code = loom_family_commands(REPO, verbosity="-q", only="code")[0]
    assert {"tests", "loom-code/tests"} <= set(code)
    assert "scripts" not in code and ".claude/hooks" not in code
    assert "loom-code/scripts" not in code
    assert any("loom-design/tests" in command for command in rendered)
    assert any(command[3:4] == ["loom-workflow/tests"] for command in commands)
    assert any("loom-workflow/tests/test-privacy-gate-compose-commit.sh" in command for command in rendered)

    expected_skill_dirs = sorted(
        path.relative_to(REPO).as_posix()
        for path in (REPO / "loom-workflow/skills").glob("*/scripts")
        if any(path.glob("test_*.py"))
    )
    actual_skill_dirs = sorted(
        command[3] for command in commands
        if command[:3] == [sys.executable, "-m", "pytest"]
        and command[3].startswith("loom-workflow/skills/")
    )
    assert actual_skill_dirs == expected_skill_dirs


def test_workflow_mermaid_group_installs_then_validates_with_no_skip_path() -> None:
    expected = [
        ["npm", "ci", "--prefix", "loom-workflow/tests/mermaid"],
        ["node", "loom-workflow/tests/mermaid/validate_mermaid.mjs"],
        ["bash", "loom-workflow/tests/mermaid-validator-negative.sh"],
    ]
    assert loom_family_commands(REPO, verbosity="-q", only="workflow-mermaid") == expected
    full = loom_family_commands(REPO, verbosity="-q")
    assert all(command in full for command in expected)


def test_loom_family_preset_discovers_relocated_memory_skill_tests() -> None:
    commands = loom_family_commands(REPO, verbosity="-q")
    rendered = [" ".join(command) for command in commands]
    assert any("loom-workflow/skills/loom-memory/scripts" in command for command in rendered)


def test_relocated_memory_skill_tests_pass_through_the_workflow_python_command() -> None:
    commands = loom_family_commands(REPO, verbosity="-q", only="workflow-python")
    memory_command = next(
        command for command in commands
        if "loom-workflow/skills/loom-memory/scripts" in command[3]
    )
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(memory_command, capture_output=True, text=True, cwd=REPO, env=env)
    assert result.returncode == 0, result.stdout + result.stderr


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _seed_repo(repo: Path) -> None:
    """A real git repository -- the behaviour under test is git's own."""
    (repo / "loom-code" / "tests").mkdir(parents=True)
    (repo / "loom-code" / "tests" / "test_seed.py").write_text("def test_s():\n    pass\n")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")


def test_targets_unchanged_without_nested_worktree(tmp_path: Path) -> None:
    repo = tmp_path / "repo"; repo.mkdir()
    _seed_repo(repo)

    commands = loom_family_commands(repo, verbosity="-q")

    assert not any(token.startswith("--ignore") for command in commands for token in command)


def test_nested_worktree_is_ignored(tmp_path: Path) -> None:
    repo = tmp_path / "repo"; repo.mkdir()
    _seed_repo(repo)
    nested = repo / "loom-code" / "tests" / "wt"
    _git(repo, "worktree", "add", "-q", "-b", "wt-branch", str(nested))

    commands = loom_family_commands(repo, verbosity="-q")

    pytest_commands = [c for c in commands if c[:3] == [sys.executable, "-m", "pytest"]]
    assert pytest_commands
    expected = f"--ignore={nested.resolve()}"
    assert all(expected in command for command in pytest_commands)


def _collect_with_runner_ignores(repo: Path) -> str:
    """Collect `loom-code/tests/` with exactly the runner's `--ignore` tokens.

    The `--ignore=` string being present is not the property that matters;
    what matters is that pytest then collects nothing from the nested
    repository. This runs the real collection.
    """
    command = loom_family_commands(repo, verbosity="-q", only="code")[0]
    ignores = [token for token in command if token.startswith("--ignore=")]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "loom-code/tests/", "-q",
         "-p", "no:cacheprovider", "--collect-only", *ignores],
        cwd=repo, capture_output=True, text=True,
    )
    return result.stdout


def test_nested_worktree_collects_nothing_from_it(tmp_path: Path) -> None:
    repo = tmp_path / "repo"; repo.mkdir()
    _seed_repo(repo)
    nested = repo / "loom-code" / "tests" / "wt"
    _git(repo, "worktree", "add", "-q", "-b", "wt-branch", str(nested))
    (nested / "loom-code" / "tests" / "test_intruder.py").write_text(
        "def test_i():\n    assert False\n")

    assert "test_intruder" not in _collect_with_runner_ignores(repo)


def test_nested_clone_collects_nothing_from_it(tmp_path: Path) -> None:
    """A plain nested repository is not this repository's, exactly as
    `repository_files` already says -- so its tests are not ours to run."""
    repo = tmp_path / "repo"; repo.mkdir()
    _seed_repo(repo)
    inner = repo / "loom-code" / "tests" / "vendor"
    inner.mkdir(parents=True)
    (inner / "test_foreign.py").write_text("def test_foreign():\n    assert False\n")
    _git(inner, "init", "-q")
    _git(inner, "config", "user.email", "t@example.com")
    _git(inner, "config", "user.name", "T")
    _git(inner, "add", "-A")
    _git(inner, "commit", "-q", "-m", "c")

    assert "test_foreign" not in _collect_with_runner_ignores(repo)


def test_loom_family_preset_is_the_only_test_command_named_by_ci_and_kickoff() -> None:
    kickoff = (REPO / "docs/loom/KICKOFF-DEFAULTS.md").read_text(encoding="utf-8")
    assert "scripts/run_package_tests.py --loom-family" in kickoff

    for workflow in (
        REPO / ".github/workflows/loom-code-ci.yml",
        REPO / ".github/workflows/loom-design-ci.yml",
        REPO / ".github/workflows/loom-workflow-ci.yml",
    ):
        text = workflow.read_text(encoding="utf-8")
        assert "scripts/run_package_tests.py --loom-family" in text


# --- tests live in tests/ folders, and the inventory discovers them ---------


def _stray_root_tests(repo: Path) -> list[str]:
    """Test files left beside the repository-level code they test."""
    return sorted(
        path.relative_to(repo).as_posix()
        for folder in (repo / "scripts", repo / ".claude" / "hooks")
        for pattern in ("test_*.py", "test-*.sh")
        for path in folder.glob(pattern)
    )


def test_no_repository_level_test_outside_tests_folder() -> None:
    assert _stray_root_tests(REPO) == []


def test_stray_repository_level_test_is_detected(tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "test_stray.py").write_text("")
    (tmp_path / ".claude" / "hooks").mkdir(parents=True)
    (tmp_path / ".claude" / "hooks" / "test-stray.sh").write_text("")
    assert _stray_root_tests(tmp_path) == [".claude/hooks/test-stray.sh", "scripts/test_stray.py"]


def _write_test(path: Path, name: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / f"test_{name}.py").write_text(f"def test_{name}():\n    pass\n")


def _collected(repo: Path, only: str) -> str:
    """Collect every pytest command of one group exactly as the runner builds it."""
    out = []
    for command in loom_family_commands(repo, verbosity="-q", only=only):
        command = [t for t in command if t not in {"-n", "auto"}]
        result = subprocess.run(
            [*command, "-p", "no:cacheprovider", "--collect-only"],
            cwd=repo, capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        out.append(result.stdout)
    return "\n".join(out)


def test_code_group_discovers_tests_folders_and_skips_local(tmp_path: Path) -> None:
    repo = tmp_path / "repo"; repo.mkdir()
    _seed_repo(repo)
    _write_test(repo / "tests", "new_root")
    _write_test(repo / "tests" / "hooks", "hook")
    _write_test(repo / "tests" / "local", "local_only")
    _write_test(repo / "loom-code" / "tests", "new_plugin")
    _write_test(repo / "loom-code" / "tests" / "local", "plugin_local_only")

    collected = _collected(repo, "code")

    for name in ("test_new_root", "test_hook", "test_new_plugin", "test_seed"):
        assert name in collected
    assert "local_only" not in collected


def test_design_group_discovers_its_tests_folder(tmp_path: Path) -> None:
    repo = tmp_path / "repo"; repo.mkdir()
    _seed_repo(repo)
    _write_test(repo / "loom-design" / "tests", "design_new")
    _write_test(repo / "loom-design" / "tests" / "local", "design_local_only")

    collected = _collected(repo, "design")

    assert "test_design_new" in collected
    assert "local_only" not in collected


def test_workflow_tests_subfolders_run_in_their_own_sessions(tmp_path: Path) -> None:
    """Per-skill subfolders may share basenames, so each is its own session."""
    repo = tmp_path / "repo"; repo.mkdir()
    _seed_repo(repo)
    tests = repo / "loom-workflow" / "tests"
    _write_test(tests, "top")
    for skill in ("alpha", "beta"):
        _write_test(tests / skill, "dup")
    _write_test(tests / "local", "wf_local_only")

    commands = loom_family_commands(repo, verbosity="-q", only="workflow-python")
    collected = _collected(repo, "workflow-python")

    targets = [command[3] for command in commands]
    assert targets == ["loom-workflow/tests", "loom-workflow/tests/alpha", "loom-workflow/tests/beta"]
    assert collected.count("::test_dup") == 2
    assert "test_top" in collected
    assert "local_only" not in collected
