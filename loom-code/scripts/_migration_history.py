"""Resolve historical evidence IDs through the committed extraction map."""
from pathlib import Path
import re
import subprocess


def _object_exists(repo: Path, revision: str) -> bool:
    """Return whether a mapped revision is present in this checkout."""
    return subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{revision}^{{commit}}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def migration_git_args(repo, args):
    map_path = Path(repo) / "docs/migration/commit-map.tsv"
    if not args or args[0] != "git" or not map_path.is_file():
        return args
    mapping = dict(line.split() for line in map_path.read_text().splitlines()[1:])
    result = []
    for argument in args:
        match = re.fullmatch(r"([0-9a-f]{7,40})([:^~].*)?", argument)
        if not match:
            result.append(argument)
            continue
        prefix, suffix = match.groups()
        candidates = [old for old in mapping if old.startswith(prefix)]
        if len(candidates) > 1:
            raise ValueError(f"ambiguous original revision: {prefix}")
        if not candidates:
            result.append(argument)
            continue
        mapped = mapping[candidates[0]]
        # A shallow/filtered clone may carry the source evidence tag but not
        # the rewritten object.  Keep the source revision usable in that
        # case; full migration clones still resolve to the mapped object.
        result.append(mapped + (suffix or "") if _object_exists(Path(repo), mapped) else argument)
    return tuple(result)
