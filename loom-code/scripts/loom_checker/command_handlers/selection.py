from __future__ import annotations

from loom_checker import selection as store
from loom_checker.helpers import UsageError
from loom_checker.helpers import git_text
from loom_checker.helpers import load_manifest
from loom_checker.helpers import repo_root

from pathlib import Path
import argparse
import json
import sys
import uuid


class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # argparse would exit; the checker exits 2 via UsageError
        raise UsageError(f"selection: {message}")


def _names(values: list[str] | None) -> list[str]:
    """`--skip a,b --skip c` -> [a, b, c]."""
    return [part.strip() for value in values or [] for part in value.split(",") if part.strip()]


def _propose(repo: Path, args: list[str], out, err) -> int:
    parser = _Parser(prog="selection propose")
    parser.add_argument("change_id")
    parser.add_argument("--origin", choices=("user", "agent"), required=True)
    parser.add_argument("--run", action="append")
    parser.add_argument("--skip", action="append")
    ns = parser.parse_args(args)
    manifest = load_manifest()
    skip, run_named = _names(ns.skip), _names(ns.run)
    reasons = store.validate_selection(skip, run_named, manifest)
    if reasons:
        raise UsageError("selection propose refused: " + "; ".join(reasons))
    names = [s["name"] for s in store.step_vocabulary(manifest)]
    skip = [name for name in names if name in skip]
    run = [name for name in names if name not in skip]
    branch, merge_base = store.current_scope(repo)
    code = store.selection_code(ns.change_id, run, skip)
    store.append_event(repo, ns.change_id, {
        "event": "proposal", "id": uuid.uuid4().hex, "code": code, "origin": ns.origin,
        "run": run, "skip": skip, "branch": branch, "merge_base": merge_base,
        "created_at": store.now(),
    })
    out.write(f"change: {ns.change_id}  code: {code}\n")
    width = max(len(name) for name in names)
    for name in names:
        out.write(f"{name.ljust(width)}  {'skip' if name in skip else 'run'}\n")
    return 0


def _show(repo: Path, args: list[str], out, err) -> int:
    if len(args) != 1 or not args[0].strip():
        raise UsageError("selection show needs one change-id.")
    out.write(json.dumps(store.effective_selection(repo, args[0]), ensure_ascii=False, indent=2) + "\n")
    return 0


def _cancel(repo: Path, args: list[str], out, err) -> int:
    if len(args) != 1 or not args[0].strip():
        raise UsageError("selection cancel needs one change-id.")
    branch, merge_base = store.current_scope(repo)
    store.append_event(repo, args[0], {
        "event": "cancel", "source": "agent-run", "prompt_ref": None,
        "branch": branch, "merge_base": merge_base, "at": store.now(),
    })
    out.write(f"selection for {args[0]} withdrawn; the full process resumes.\n")
    return 0


def _record_failure(repo: Path, args: list[str], out, err) -> int:
    parser = _Parser(prog="selection record-failure")
    parser.add_argument("change_id")
    parser.add_argument("--step", required=True)
    parser.add_argument("--rule", required=True)
    ns = parser.parse_args(args)
    names = [s["name"] for s in store.step_vocabulary()]
    if ns.step not in names:
        raise UsageError(f"unknown step {ns.step!r} (steps: {', '.join(names)})")
    store.append_event(repo, ns.change_id, {
        "event": "failure", "step": ns.step, "rule": ns.rule,
        "head_sha": git_text(repo, "rev-parse", "HEAD"),
        "branch": git_text(repo, "rev-parse", "--abbrev-ref", "HEAD"), "at": store.now(),
    })
    out.write(f"failure recorded for {ns.change_id}: {ns.step} {ns.rule}\n")
    return 0


# Extension point: `capture` (W2-01, hook-only) and `skipped-review`
# (W2-04, ledger) register here as further entries.
SUBCOMMANDS = {
    "propose": _propose,
    "show": _show,
    "cancel": _cancel,
    "record-failure": _record_failure,
}


def cmd_selection(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Propose, read, withdraw and fail step selections for one change."""
    if not args or args[0] not in SUBCOMMANDS:
        raise UsageError(f"selection needs one of: {', '.join(SUBCOMMANDS)}.")
    return SUBCOMMANDS[args[0]](repo_root(Path.cwd()), args[1:], out, err)
