"""Native hooks operate independently of the shell command spelling."""
import subprocess
import sys
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts/loom_checker.py"


def git(repo, *args, ok=True):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if ok:
        assert result.returncode == 0, result.stderr
    return result


def setup(tmp_path):
    origin = tmp_path / "origin"
    origin.mkdir()
    git(origin, "init", "--bare", "-b", "trunk")
    repo = tmp_path / "repo"
    git(tmp_path, "clone", str(origin), str(repo))
    git(repo, "config", "user.name", "T")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "commit", "--allow-empty", "-m", "initial")
    git(repo, "push", "origin", "trunk")
    git(repo, "remote", "set-head", "origin", "-a")
    return repo, origin


def manage(repo, option):
    return subprocess.run([sys.executable, str(CHECKER), "push", option], cwd=repo,
                          capture_output=True, text=True)


def test_feature_commit_and_trunk_sync(tmp_path):
    repo, origin = setup(tmp_path)
    assert manage(repo, "--install-git-hooks").returncode == 0
    assert manage(repo, "--install-git-hooks").returncode == 0
    git(repo, "switch", "-c", "feature")
    git(repo, "commit", "--allow-empty", "-m", "feature")
    git(repo, "push", "origin", "feature")
    linked = tmp_path / "linked"
    git(repo, "worktree", "add", "-b", "linked", str(linked))
    git(linked, "commit", "--allow-empty", "-m", "linked")
    git(repo, "config", "loom.protectMain", "false")
    for branch in ("main", "master"):
        git(linked, "switch", "-c", branch)
        assert git(linked, "commit", "--allow-empty", "-m", "blocked", ok=False).returncode != 0
    git(linked, "switch", "linked")
    git(repo, "switch", "trunk")
    git(repo, "pull", "--ff-only")
    # Fast-forward/history edits do not invoke these hooks; server rules remain necessary.
    git(repo, "merge", "--ff-only", "feature")
    git(repo, "reset", "--hard", "origin/trunk")
    git(repo, "symbolic-ref", "--delete", "refs/remotes/origin/HEAD")
    assert manage(repo, "--remove-git-hooks").returncode == 0


def test_compound_main_commit_and_push(tmp_path):
    repo, _ = setup(tmp_path)
    assert manage(repo, "--install-git-hooks").returncode == 0
    result = subprocess.run(["sh", "-c", "true; git commit --allow-empty -m blocked"],
                            cwd=repo, capture_output=True, text=True)
    assert result.returncode != 0
    assert "trunk" in result.stderr and "branch" in result.stderr
    git(repo, "switch", "-c", "feature")
    git(repo, "commit", "--allow-empty", "-m", "feature")
    assert git(repo, "push", "origin", "HEAD:trunk", ok=False).returncode != 0
    git(repo, "switch", "trunk")
    assert git(repo, "merge", "--no-ff", "feature", ok=False).returncode != 0
    git(repo, "merge", "--abort")


def test_protection_remedy(tmp_path):
    repo, _ = setup(tmp_path)
    assert manage(repo, "--install-git-hooks").returncode == 0
    git(repo, "switch", "-c", "feature")
    git(repo, "symbolic-ref", "--delete", "refs/remotes/origin/HEAD")
    result = git(repo, "commit", "--allow-empty", "-m", "blocked", ok=False)
    assert result.returncode != 0 and "remote set-head" in result.stderr
    assert "no-verify" not in result.stderr


def test_foreign_hooks_unchanged(tmp_path):
    repo, _ = setup(tmp_path)
    hooks = repo / ".git/hooks"
    foreign = hooks / "pre-push"
    foreign.write_text("foreign\n")
    before = {p.name: p.read_bytes() for p in hooks.iterdir()}
    result = manage(repo, "--install-git-hooks")
    assert result.returncode != 0 and "Foreign" in result.stderr
    assert {p.name: p.read_bytes() for p in hooks.iterdir()} == before
    foreign.unlink()
    git(repo, "config", "core.hooksPath", str(hooks))
    assert manage(repo, "--install-git-hooks").returncode != 0
    git(repo, "config", "--unset", "core.hooksPath")
    external = tmp_path / "shared-hooks"
    hooks.rename(external)
    hooks.symlink_to(external, target_is_directory=True)
    assert manage(repo, "--install-git-hooks").returncode != 0
    hooks.unlink()
    external.rename(hooks)
    git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/trunk")
    git(repo, "update-ref", "refs/remotes/origin/feature", "HEAD")
    git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/feature")
    result = manage(repo, "--install-git-hooks")
    assert result.returncode != 0 and "conflicts" in result.stderr
    assert not (hooks / "pre-commit").exists()
    git(repo, "remote", "set-head", "origin", "-a")
    assert manage(repo, "--install-git-hooks").returncode == 0
    foreign.write_bytes(foreign.read_bytes() + b"# edited\n")
    before = {p.name: p.read_bytes() for p in hooks.iterdir()}
    assert manage(repo, "--remove-git-hooks").returncode != 0
    assert {p.name: p.read_bytes() for p in hooks.iterdir()} == before
