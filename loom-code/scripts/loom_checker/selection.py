"""Step-selection record store and effective-selection resolution.

The store is append-only JSON lines at
`<git common dir>/loom/selections/<change-id>.jsonl`: untracked, shared by
every worktree of the repository, and never part of the functional digest.
Events: `proposal`, `confirmation`, `cancel`, `failure`.

Lifetimes: proposals, confirmations and cancels apply only while the current
branch AND merge base equal the ones they recorded, so a reused change-id on
another branch inherits nothing and a rebase makes a bound selection lapse.
Failures are scoped by change-id (the file) only; their `branch` is
informational, so neither a rebase nor a branch rename can drop them.
"""
from __future__ import annotations

from datetime import datetime, timezone

from loom_checker.helpers import UsageError
from loom_checker.helpers import branch_base
from loom_checker.helpers import git_text
from loom_checker.helpers import load_manifest
from loom_checker.reviewers import auto_skipped_steps
from pathlib import Path
import base64
import hashlib
import json
import os
import re


ENTRY_TOKENS = frozenset(
    {"/loom-code:expert-mode", "/expert-mode", "$expert-mode", "$loom-code:expert-mode"}
)


def step_vocabulary(manifest=None) -> list[dict]:
    """The checker-owned steps, in manifest order, each a name only."""
    manifest = manifest if manifest is not None else load_manifest()
    steps = (manifest.get("step_selection") or {}).get("steps") or []
    if not steps:
        raise UsageError("the contract manifest declares no step_selection.steps.")
    return [{"name": s["name"]} for s in steps]


def selection_code(change_id: str, run: list[str], skip: list[str]) -> str:
    """Four characters of sha256 over change-id + sorted run + sorted skip.

    Uppercase RFC 4648 base32 rather than hex: 32^4 (about one million)
    codes instead of 16^4 (65 536) for the same four keystrokes, and the
    alphabet omits 0/1/8/9, so no digit is mistaken for O, I or B."""
    payload = "\n".join([change_id, ",".join(sorted(run)), ",".join(sorted(skip))])
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    return base64.b32encode(digest).decode("ascii")[:4]


def confirmation_prompt_matches(text: str, code: str) -> bool:
    """First token is an entry-point token and the code is a standalone token."""
    tokens = (text or "").split()
    if not tokens or tokens[0] not in ENTRY_TOKENS:
        return False
    return code.upper() in (token.upper() for token in tokens[1:])


def confirmation_is_valid(event: dict, proposal: dict) -> bool:
    """The recorded prompt still hashes to its sha and still confirms the code."""
    text = event.get("prompt_text")
    if not isinstance(text, str) or event.get("code") != proposal.get("code"):
        return False
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != event.get("prompt_sha256"):
        return False
    return confirmation_prompt_matches(text, proposal["code"])


def session_matches(event: dict) -> bool:
    """A confirmation counts in this process only when it was recorded in
    the host session the process runs in (`CLAUDE_CODE_SESSION_ID`); without
    that variable (Codex, CI) every session counts."""
    current = os.environ.get("CLAUDE_CODE_SESSION_ID")
    return not current or event.get("session_id") == current


SAFE_CHANGE_ID = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+")


def store_dir(repo: Path) -> Path:
    common = Path(git_text(repo, "rev-parse", "--git-common-dir"))
    if not common.is_absolute():
        common = (repo / common).resolve()
    return common / "loom" / "selections"


def store_path(repo: Path, change_id: str) -> Path:
    """The record file for one change; a change-id that is not one safe path
    segment is refused before any path is built."""
    if not isinstance(change_id, str) or not SAFE_CHANGE_ID.fullmatch(change_id):
        raise UsageError(f"change-id {change_id!r} is not a dated kebab-case change-id.")
    return store_dir(repo) / f"{change_id}.jsonl"


def read_events(repo: Path, change_id: str) -> list[dict]:
    """Events for one change; an unsafe change-id holds none (full process)."""
    if not isinstance(change_id, str) or not SAFE_CHANGE_ID.fullmatch(change_id):
        return []
    path = store_path(repo, change_id)
    if not path.is_file():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def append_event(repo: Path, change_id: str, event: dict) -> None:
    path = store_path(repo, change_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def current_scope(repo: Path) -> tuple[str, str]:
    """(branch, merge base) a selection event must match to apply."""
    return git_text(repo, "rev-parse", "--abbrev-ref", "HEAD"), branch_base(repo)


def validate_selection(skip: list[str], run: list[str], manifest=None) -> list[str]:
    """Refusal reasons for a proposed skip list; empty when it is valid."""
    steps = step_vocabulary(manifest)
    names = [s["name"] for s in steps]
    reasons = []
    if "intent" in [*skip, *run]:
        reasons.append("the intent is always kept: landing a change requires its committed "
                       "intent, so no selection runs or skips it")
    reasons += [f"unknown step {name!r} (steps: {', '.join(names)})"
                for name in [*skip, *run] if name not in names and name != "intent"]
    reasons += [f"step {name!r} is named in both --run and --skip" for name in run if name in skip]
    return reasons


def effective_selection(repo: Path, change_id: str, manifest=None) -> dict:
    """The step set stations and gates read: full set unless a valid,
    uncancelled confirmation recorded on this branch and merge base exists.

    When no user selection is bound and the branch delta is mechanically
    narrow (is_narrow_delta), spec/plan/blind-run/adversarial are auto-skipped so
    small changes run the full ritual without a typed confirmation.
    Intent is never auto-skipped. Explicit user selections always win."""
    names = [s["name"] for s in step_vocabulary(manifest)]
    branch, merge_base = current_scope(repo)
    events = read_events(repo, change_id)
    in_scope = [e for e in events
                if e.get("branch") == branch and e.get("merge_base") == merge_base]
    proposals = {e["id"]: e for e in in_scope if e.get("event") == "proposal"}
    bound = None
    for event in in_scope:
        if event.get("event") == "cancel":
            bound = None
        elif event.get("event") == "confirmation":
            proposal = proposals.get(event.get("proposal_id"))
            if (proposal is not None and confirmation_is_valid(event, proposal)
                    and session_matches(event)):
                bound = (event, proposal)
    failures = [e for e in events if e.get("event") == "failure"]
    if bound is None:
        auto_skip = _auto_skip(repo, change_id, names)
        return {"change_id": change_id, "bound": False,
                "run": [n for n in names if n not in auto_skip],
                "skip": auto_skip, "code": None, "failures": failures}
    confirmation, proposal = bound
    user_skip = [name for name in names if name in proposal["skip"]]
    return {"change_id": change_id, "bound": True,
            "run": [name for name in names if name not in user_skip],
            "skip": user_skip, "code": proposal["code"],
            "source": confirmation.get("source"),
            "confirmed_at": confirmation.get("at"), "failures": failures}


def _auto_skip(repo: Path, change_id: str, names: list[str]) -> list[str]:
    """Mechanical auto-skip list for narrow deltas; never includes intent."""
    try:
        skipped = auto_skipped_steps(repo, change_id)
    except Exception:
        return []
    return [name for name in names if name in skipped and name != "intent"]
