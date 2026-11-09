# concern: A same-named tag must not let ordinary commits bypass trunk protection.
"""Exercise Git's disambiguated symbolic-ref output in an isolated repository."""
import pytest

from test_native_git_protection import git, manage, setup


@pytest.mark.parametrize("branch", ["trunk", "main", "master"])
def test_native_ambiguoustag_refusescommit(tmp_path, branch):
    """A tag sharing a protected branch name must preserve commit refusal."""
    repo, _ = setup(tmp_path)
    if branch != "trunk":
        git(repo, "switch", "-c", branch)
    assert manage(repo, "--install-git-hooks").returncode == 0
    git(repo, "tag", branch)
    result = git(repo, "commit", "--allow-empty", "-m", "must be refused", ok=False)
    assert result.returncode != 0, (
        f"Ordinary commit succeeded on protected {branch} with a same-named tag: "
        f"{result.stdout} {result.stderr}"
    )
