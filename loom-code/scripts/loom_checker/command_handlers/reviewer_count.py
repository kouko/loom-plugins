from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import git_text
from loom_checker.helpers import repo_root
from loom_checker.reviewers import required_reviewer_count
from pathlib import Path
import sys


def cmd_reviewer_count(args: list[str], out=sys.stdout, err=sys.stderr, *, result=None) -> int:
    """Print the reviewer floor Closing Review and finalization must use."""
    if len(args) != 1 or not args[0].strip() or (result is not None and args[0] in {"--help", "-h"}):
        raise UsageError("reviewer-count needs one change-id.")
    repo = repo_root(Path.cwd())
    if git_text(repo, "status", "--porcelain"):
        raise UsageError("reviewer-count needs a clean tree with completed functional content.")
    floor = required_reviewer_count(repo, args[0])
    if result is not None:
        result["data"].update(change_id=args[0], reviewer_floor=floor)
    else:
        out.write(f"{floor}\n")
    return 0
