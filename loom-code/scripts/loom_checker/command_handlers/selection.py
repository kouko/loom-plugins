from __future__ import annotations

from loom_checker import selection as store
from loom_checker.command_handlers.push import read_hook_payload
from loom_checker.helpers import UsageError
from loom_checker.helpers import git_text
from loom_checker.helpers import load_manifest
from loom_checker.helpers import repo_root
from loom_checker.intent_state import remote_default_snapshot

from pathlib import Path
import argparse
import hashlib
import json
import re
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


WITHDRAW_TOKENS = frozenset({"cancel", "取消", "キャンセル", "撤回"})


def _scoped_proposals(repo: Path, branch: str, merge_base: str) -> list[tuple[str, dict, bool]]:
    """(change-id, proposal, already confirmed) for every proposal in the
    store recorded on this branch and merge base, in record order."""
    directory = store.store_dir(repo)
    found = []
    for path in sorted(directory.glob("*.jsonl")) if directory.is_dir() else []:
        scoped = [e for e in store.read_events(repo, path.stem)
                  if e.get("branch") == branch and e.get("merge_base") == merge_base]
        confirmed = {e.get("proposal_id") for e in scoped if e.get("event") == "confirmation"}
        found += [(path.stem, e, e.get("id") in confirmed)
                  for e in scoped if e.get("event") == "proposal"]
    return found


def _withdraw_targets(words: list[str], proposals) -> list[str] | None:
    """Change-ids a withdrawal prompt cancels; None when it is no withdrawal.
    A withdraw token counts only as the sole word or next to a code."""
    if len(words) == 1 and words[0].casefold() in WITHDRAW_TOKENS:
        return sorted({change for change, _, _ in proposals})
    codes = {}
    for change, proposal, _ in proposals:
        codes.setdefault(proposal["code"].upper(), set()).add(change)
    targets = set()
    for i, word in enumerate(words):
        if word.casefold() not in WITHDRAW_TOKENS:
            continue
        for neighbour in words[max(i - 1, 0):i] + words[i + 1:i + 2]:
            targets |= codes.get(neighbour.upper(), set())
    return sorted(targets) if targets else None


def _capture_prompt(repo: Path, payload: dict, out) -> None:
    prompt = payload.get("prompt")
    words = prompt.split() if isinstance(prompt, str) else []
    if not words or words[0] not in store.ENTRY_TOKENS:
        return
    prompt_ref = payload.get("prompt_id") or payload.get("turn_id")
    branch, merge_base = store.current_scope(repo)
    proposals = _scoped_proposals(repo, branch, merge_base)
    withdrawn = _withdraw_targets(words[1:], proposals)
    if withdrawn is not None:
        for change_id in withdrawn:
            store.append_event(repo, change_id, {
                "event": "cancel", "source": "user-typed", "prompt_ref": prompt_ref,
                "branch": branch, "merge_base": merge_base, "at": store.now(),
            })
        if withdrawn:
            out.write(json.dumps({"systemMessage": (
                f"Loom: selection for {', '.join(withdrawn)} withdrawn; "
                "the full process resumes.")}, ensure_ascii=False) + "\n")
        return
    pending = [(change, proposal) for change, proposal, confirmed in proposals
               if not confirmed and store.confirmation_prompt_matches(prompt, proposal["code"])]
    if not pending:
        return
    change_id, proposal = max(pending, key=lambda item: item[1].get("created_at", ""))
    store.append_event(repo, change_id, {
        "event": "confirmation", "proposal_id": proposal["id"], "code": proposal["code"],
        "source": "user-typed", "session_id": payload.get("session_id"),
        "prompt_ref": prompt_ref, "prompt_text": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "branch": branch, "merge_base": merge_base, "at": store.now(),
    })
    bound = store.effective_selection(repo, change_id)
    if not bound["bound"]:
        return
    out.write(json.dumps({"systemMessage": (
        f"Loom: selection {bound['code']} bound for {change_id}. "
        f"Run: {', '.join(bound['run']) or '(none)'}. "
        f"Skip: {', '.join(bound['skip']) or '(none)'}.")}, ensure_ascii=False) + "\n")


def _capture(repo: Path | None, args: list[str], out, err) -> int:
    """UserPromptSubmit hook only. Records what the user submitted and never
    blocks the prompt: every refusal or failure exits 0 with nothing recorded."""
    if args != ["--hook"]:
        raise UsageError("selection capture runs only as a hook: selection capture --hook.")
    try:
        payload = read_hook_payload()
        if (payload is None or payload.get("hook_event_name") != "UserPromptSubmit"
                or not (payload.get("prompt_id") or payload.get("turn_id"))):
            err.write("selection capture: not a UserPromptSubmit payload with a prompt "
                      "reference; nothing recorded.\n")
            return 0
        _capture_prompt(repo_root(Path.cwd()), payload, out)
    except Exception as exc:  # the prompt must go through whatever happens here
        err.write(f"selection capture: nothing recorded ({type(exc).__name__}: {exc}).\n")
    return 0


def _skipped_review(repo: Path, args: list[str], out, err) -> int:
    """List merged changes on the remote default branch whose attestation
    records reviewers as skipped."""
    if args:
        raise UsageError("selection skipped-review takes no arguments.")
    _ref, snapshot, error = remote_default_snapshot(repo)
    if snapshot is None:
        err.write(f"selection skipped-review: cannot resolve the remote default branch: {error}; "
                  "fetch the remote (or run `git remote set-head origin --auto`) and retry.\n")
        return 1
    template = load_manifest()["artifacts"]["attestation"]["path"]
    pattern = re.compile(
        re.escape(template).replace(re.escape("<change-id>"), r"(?P<change_id>[^/]+)"))
    listing = git_text(repo, "ls-tree", "-r", "-z", "--name-only", snapshot, "--",
                       template.split("<change-id>")[0])
    found = 0
    for path in sorted(name for name in listing.split("\0") if pattern.fullmatch(name)):
        try:
            recorded = json.loads(git_text(repo, "show", f"{snapshot}:{path}")).get("selection")
        except (UsageError, json.JSONDecodeError, AttributeError):
            err.write(f"selection skipped-review: {path} is unreadable; not listed.\n")
            continue
        if not isinstance(recorded, dict) or "reviewers" not in (recorded.get("skip") or []):
            continue
        added = git_text(repo, "log", "--first-parent", "--diff-filter=A", "--format=%h",
                         snapshot, "--", path).splitlines()
        merge = added[-1] if added else "unknown"
        out.write(f"{pattern.fullmatch(path)['change_id']} {merge} "
                  f"skipped: {', '.join(recorded['skip'])}\n")
        found += 1
    if not found:
        out.write("no merged change skipped review\n")
    return 0


SUBCOMMANDS = {
    "propose": _propose,
    "show": _show,
    "cancel": _cancel,
    "record-failure": _record_failure,
    "capture": _capture,
    "skipped-review": _skipped_review,
}


def cmd_selection(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Propose, read, withdraw and fail step selections for one change."""
    if not args or args[0] not in SUBCOMMANDS:
        raise UsageError(f"selection needs one of: {', '.join(SUBCOMMANDS)}.")
    if args[0] == "capture":  # resolves the repo inside its never-block guard
        return _capture(None, args[1:], out, err)
    return SUBCOMMANDS[args[0]](repo_root(Path.cwd()), args[1:], out, err)
