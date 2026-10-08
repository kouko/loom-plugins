from __future__ import annotations

from loom_checker.artifact_types import _TEST_NAME_RE
from loom_checker.digest import functional_content_digest
from loom_checker.helpers import TRUNK_BRANCH_NAMES
from loom_checker.helpers import UsageError
from loom_checker.helpers import _is_host_plumbing
from loom_checker.helpers import branch_base
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_ok
from loom_checker.helpers import git_text
from loom_checker.helpers import is_program_path
from loom_checker.helpers import tree_programs
from loom_checker.rule_checks.publish import _body_sections
from pathlib import Path
import hashlib
import re
import yaml


_LOW_RISK_DOC_EXTENSIONS = frozenset({".md", ".mdx", ".rst", ".txt"})
_OUTSIDE_FAMILIES = {"claude": "anthropic", "codex": "openai", "gemini": "google"}
_DOC_DIMENSIONS = frozenset({
    "omission", "ambiguity", "inconsistency", "incorrect-fact",
    "missing-population", "deletion-first",
})
_REVIEW_DIMENSIONS = {
    "docs": _DOC_DIMENSIONS,
    "skill": _DOC_DIMENSIONS | {"user-judgment-leak"},
    "spec": _DOC_DIMENSIONS | {"spec-conformance", "design-conformance",
                               "principles-conformance", "user-judgment-leak"},
    "spec+adversarial": _DOC_DIMENSIONS | {"spec-conformance", "design-conformance",
                                           "principles-conformance", "user-judgment-leak"},
    "code": frozenset({
        "security", "architecture", "correctness", "naming", "tests",
        "refactoring", "cross-task-coherence", "external-surface-grounding",
        "principles-conformance", "architecture-conformance",
        "deliberate-simplification", "deletion-first",
    }),
    "design": frozenset({"design-conformance"}),
    "principles": frozenset({"principles-conformance"}),
    "plan": frozenset({"deletion-first"}),
}


def _review_yaml_failure(parsed: object, verdict: dict) -> str | None:
    """Check the required owning-reviewer fields before accepting outside YAML."""
    if not isinstance(parsed, dict):
        return "selected outside execution lacks required reviewer YAML"
    if any(parsed.get(key) != verdict.get(key) for key in ("verdict", "lens", "findings")):
        return "selected outside execution output differs from its verdict"
    lens = verdict.get("lens")
    expected = _REVIEW_DIMENSIONS.get(lens) if isinstance(lens, str) else None
    scores = parsed.get("dimension_scores")
    if (expected is None or not isinstance(scores, dict) or set(scores) != expected or
            any(not isinstance(score, str) or
                (score not in {"PASS", "PASS_WITH_NOTES", "NEEDS_REVISION"}
                 and not re.fullmatch(r"N/A — .+", score))
                for score in scores.values()) or
            not isinstance(parsed.get("reviewed_sha"), str) or
            not parsed["reviewed_sha"].strip() or
            parsed["reviewed_sha"] != verdict.get("reviewed_sha") or
            parsed.get("review_target_sha") != verdict.get("review_target_sha") or
            not isinstance(parsed.get("review_target_sha"), str)):
        return "selected outside execution lacks required reviewer YAML"
    findings = parsed.get("findings")
    if not isinstance(findings, list):
        return "selected outside execution lacks required reviewer YAML"
    for finding in findings:
        if (not isinstance(finding, dict) or
                finding.get("severity") not in {"fatal", "important", "nit"} or
                not isinstance(finding.get("dimension"), str) or
                finding["dimension"] not in expected or
                not isinstance(finding.get("anchor"), str) or
                not re.search(r":\d+$| :: .+", finding["anchor"]) or
                not isinstance(finding.get("text"), str) or
                not re.match(r"^(praise|nitpick|suggestion|issue|todo|question|thought|chore|note)(?:\s*\([^)]*\))?:", finding["text"]) or
                not isinstance(finding.get("fix"), str) or not finding["fix"].strip()):
            return "selected outside execution has malformed reviewer findings"
    notes = parsed.get("notes", [])
    if not isinstance(notes, list) or len(notes) > 3 or any(not isinstance(n, str) for n in notes):
        return "selected outside execution has malformed reviewer notes"
    severity = [finding["severity"] for finding in findings]
    if ("NEEDS_REVISION" in scores.values() or "fatal" in severity or
            severity.count("important") >= 2):
        expected_verdict = "NEEDS_REVISION"
    elif "PASS_WITH_NOTES" in scores.values() or "important" in severity:
        expected_verdict = "PASS_WITH_NOTES"
    else:
        expected_verdict = "PASS"
    if parsed.get("verdict") != expected_verdict:
        return "selected outside execution overall verdict contradicts scores or findings"
    return None


def selected_outside_family(repo: Path, change_id: str, head_sha: str | None = None) -> str | None:
    """Read an explicit outside selection from the committed review inputs."""
    head = head_sha or git_maybe(repo, "rev-parse", "HEAD")
    if not head:
        return None

    def selection_in(record: str, section: str) -> str | None:
        for heading, lines in _body_sections(record, strip_comments=True)[0]:
            if heading.rstrip(" \t") != section:
                continue
            matches = [match.group(1) for line in lines if (match := re.fullmatch(
                r"(?:(?:-|[0-9]+\.)[ \t]+)?user-decided — second-vendor "
                r"selection-confirmed: (claude|codex|gemini)[ \t]*", line,
            ))]
            return matches[-1] if matches else None
        return None

    plan = git_maybe(repo, "show", f"{head}:docs/loom/{change_id}/plan.md") or ""
    selected = selection_in(plan, "Risks")
    if selected is None:
        intent = git_maybe(repo, "show", f"{head}:docs/loom/intent/{change_id}.md") or ""
        selected = selection_in(intent, "Constraints")
    if selected is not None:
        return _OUTSIDE_FAMILIES[selected]
    defaults = git_maybe(repo, "show", f"{head}:docs/loom/KICKOFF-DEFAULTS.md") or ""
    match = re.search(
        r"(?m)^- second-vendor:\s*(claude|codex|gemini)(?:\s+—|\s*$)", defaults,
    )
    return _OUTSIDE_FAMILIES[match.group(1)] if match else None


def outside_verdict_failure(
    verdicts: list[dict], family: str | None, head_sha: str, *,
    repo: Path | None = None, change_id: str | None = None,
    content_digest: str | None = None, manifest: dict | None = None,
) -> str | None:
    """A selected outside opinion must coexist with an incumbent opinion."""
    if family is None:
        return None
    vendors = {str(v.get("vendor", "")).casefold() for v in verdicts}
    aliases = {"anthropic": {"anthropic", "claude"},
               "openai": {"openai", "codex"}, "google": {"google", "gemini"}}
    outside = aliases[family]
    if not vendors.intersection(outside):
        return "selected outside vendor has no reviewer verdict"
    if not vendors.difference(outside):
        return "outside verdict has no distinct incumbent vendor verdict"
    lenses = {str(v.get("lens", "")).strip() for v in verdicts}
    if len(lenses) != 1 or not next(iter(lenses)):
        return "outside and incumbent verdicts must use the same review lens"
    matched = [v for v in verdicts if str(v.get("vendor", "")).casefold() in outside]
    if len(matched) != 1:
        return "selected outside execution needs exactly one attributed verdict"
    verdict = matched[0]
    target = verdict.get("review_target_sha")
    if not isinstance(target, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", target):
        return "selected outside execution has no concrete review target SHA"
    receipt = verdict.get("external_review")
    if not isinstance(receipt, dict) or set(receipt) != {
        "status", "executor", "model", "effort", "family", "evidence_level",
        "observed_model", "observed_effort", "output_digest", "reviewer",
        "review_target_sha",
    }:
        return "selected outside execution receipt is missing or malformed"
    if receipt["review_target_sha"] != target:
        return "selected outside execution review target differs from its receipt"
    if repo is None:
        if target != head_sha:
            return "selected outside execution review target does not match finalization HEAD"
    elif (change_id is None or content_digest is None or
          not git_ok(repo, "merge-base", "--is-ancestor", target, head_sha) or
          functional_content_digest(repo, target, change_id, manifest) != content_digest):
        return "selected outside execution review target is stale or outside validation ancestry"
    if (receipt["status"] != "completed" or receipt["family"] != family or
            receipt["model"] != verdict.get("model") or
            receipt["reviewer"] != verdict.get("reviewer") or
            receipt["executor"] not in {"codex", "claude", "agy"} or
            not isinstance(receipt["effort"], str) or not receipt["effort"] or
            receipt["evidence_level"] not in {
                "observed-model-and-effort", "accepted-explicit-settings"
            } or not re.fullmatch(r"[0-9a-f]{64}", str(receipt["output_digest"]))):
        return "selected outside execution receipt does not match its verdict"
    # Reuse the runner's model-family classifier; a receipt is caller supplied
    # evidence and must not claim observations that its executor cannot emit.
    from external_review import EFFORTS, claude_model_matches, provider_family

    executor = receipt["executor"]
    model = receipt["model"]
    effort = receipt["effort"]
    observed_model = receipt["observed_model"]
    observed_effort = receipt["observed_effort"]
    if (not isinstance(model, str) or provider_family(model) != family or
            effort not in EFFORTS):
        return "selected outside execution receipt has an impossible model profile"
    if executor == "codex":
        valid = (family == "openai" and
                 receipt["evidence_level"] == "observed-model-and-effort" and
                 observed_model == model and observed_effort == effort)
    elif executor == "claude":
        valid = (family == "anthropic" and
                 receipt["evidence_level"] == "accepted-explicit-settings" and
                 isinstance(observed_model, str) and
                 provider_family(observed_model) == family and
                 claude_model_matches(model, observed_model) and
                 observed_effort is None)
    else:  # Antigravity lists the selected model but does not report effective settings.
        valid = (receipt["evidence_level"] == "accepted-explicit-settings" and
                 observed_model is None and observed_effort is None)
    if not valid:
        return "selected outside execution receipt has impossible executor evidence"
    return None


def attach_outside_receipt(
    verdicts: list[dict], family: str | None, head_sha: str,
) -> tuple[list[dict], str | None]:
    """Verify the runner output and keep only a digest-bound receipt."""
    if family is None:
        return verdicts, None
    prepared = [item.copy() for item in verdicts]
    aliases = {"anthropic": {"anthropic", "claude"},
               "openai": {"openai", "codex"}, "google": {"google", "gemini"}}
    outside = [v for v in prepared if str(v.get("vendor", "")).casefold() in aliases[family]]
    if len(outside) != 1:
        return prepared, "selected outside execution needs exactly one attributed verdict"
    verdict = outside[0]
    result = verdict.get("external_review")
    if not isinstance(result, dict):
        return prepared, "selected outside execution result is missing"
    output = result.get("review_output")
    if not isinstance(output, str) or not output.strip():
        return prepared, "selected outside execution has no raw review output"
    try:
        parsed = yaml.safe_load(output)
    except yaml.YAMLError:
        return prepared, "selected outside execution output is invalid YAML"
    yaml_failure = _review_yaml_failure(parsed, verdict)
    if yaml_failure:
        return prepared, yaml_failure
    if result.get("status") != "completed" or result.get("reason") is not None:
        return prepared, "selected outside execution did not complete"
    verdict["external_review"] = {
        "status": result["status"], "executor": result.get("executor"),
        "model": result.get("requested_model"),
        "effort": result.get("requested_effort"),
        "family": result.get("requested_family"),
        "evidence_level": result.get("evidence_level"),
        "observed_model": result.get("observed_model"),
        "observed_effort": result.get("observed_effort"),
        "output_digest": hashlib.sha256(output.encode("utf-8")).hexdigest(),
        "reviewer": verdict.get("reviewer"),
        "review_target_sha": verdict.get("review_target_sha"),
    }
    return prepared, outside_verdict_failure(prepared, family, head_sha)


_REVIEW_PROTECTED_PARTS = frozenset(
    {"agents", "api", "cli", "commands", "contract", "hooks", "skills", "templates"}
)


_REVIEW_PROTECTED_NAMES = frozenset(
    {"agents.md", "architecture.md", "claude.md", "design.md", "kickoff-defaults.md", "principles.md", "skill.md"}
)


# Steps that a narrow delta auto-skips. Intent always stays (cannot be skipped).
_NARROW_AUTO_SKIP_STEPS = frozenset(
    {"spec", "plan", "acceptance-test", "adversarial"}
)


def _is_test_path(path: Path) -> bool:
    """True for a file the suite collects, or anything under a `tests` tree."""
    return bool(_TEST_NAME_RE.fullmatch(path.name)) or "tests" in {
        part.casefold() for part in path.parts
    }


def reviewer_floor_for_paths(
    paths: set[str], change_id: str, deleted: frozenset[str] | set[str] = frozenset()
) -> int:
    """Return one only for a complete, narrow, mechanically low-risk delta.

    This is a positive allowlist. Anything not recognized here, including a
    mixed delta with one protected path, keeps the default floor of two.

    ``deleted`` is the subset of ``paths`` the delta removes. Adding a test is
    low risk; removing one is the delta that deletes the evidence a later
    reviewer would read, so it keeps the default floor whatever else the
    delta touches.
    """
    if not paths:
        return 2
    for path in deleted:
        if _is_test_path(Path(path)):
            return 2
    intent_path = f"docs/loom/intent/{change_id}.md"
    change_store = f"docs/loom/{change_id}/"
    evidence_store = "docs/loom/evidence/"
    for path in paths:
        pure = Path(path)
        if pure.is_absolute() or ".." in pure.parts:
            return 2
        parts = {part.casefold() for part in pure.parts}
        name = pure.name.casefold()
        if parts.intersection(_REVIEW_PROTECTED_PARTS) or name in _REVIEW_PROTECTED_NAMES:
            return 2
        if path == intent_path or path.startswith(change_store):
            continue
        if path.startswith(evidence_store):
            continue
        if _is_test_path(pure):
            continue
        if (
            pure.suffix.casefold() in _LOW_RISK_DOC_EXTENSIONS
            and not path.startswith("docs/loom/")
        ):
            continue
        return 2
    return 1


def is_narrow_delta(
    paths: set[str], change_id: str, deleted: frozenset[str] | set[str] = frozenset(),
    executable: frozenset[str] | set[str] = frozenset(),
) -> bool:
    """Return True when the diff is narrow enough to auto-skip the steps in
    ``_NARROW_AUTO_SKIP_STEPS``.

    A narrow delta contains only the intent, plan, evidence and low-risk docs
    (`.md`/`.rst`/`.txt` outside `docs/loom/`) — no production code, no
    protected surface, no interface-surface glob, and **no file anything
    executes**, wherever it sits.

    ``adversarial`` is auto-skipped here as well, and the program test is what
    makes that safe: the justification for skipping it is that the delta
    carries no executed behaviour a probe program could make fail, so a delta
    that carries an executed file — a test, a script, a probe program under
    this change's own store, which `finalize-review` runs as a subprocess —
    is not one the justification covers. A delta that removes a test is not
    narrow either: what it changes is what the repository can still check.

    Narrowness is therefore strictly stronger than reviewer floor 1: every
    narrow delta gets floor 1, but a delta that only adds a test file gets
    floor 1 without being narrow.

    ``executable`` carries the paths a caller has already resolved against the
    tree — `helpers.tree_programs` reads git's 100755 mode and a `#!` first
    line, which is how `evidence/probes/run` says it is a program without
    taking a suffix. The name test here is the cheap half of that same
    question, and a caller with a commit in hand passes the other half in;
    `auto_skipped_steps` always does.
    """
    if any(is_program_path(path) or path in executable for path in paths):
        return False
    return reviewer_floor_for_paths(paths, change_id, deleted) == 1


def committed_branch_delta(
    repo: Path, change_id: str, head_sha: str | None = None
) -> tuple[set[str], set[str], set[str]] | None:
    """The committed branch delta as (all paths, removed, added), or None.

    This is the single path source for every rule that reasons about the
    branch's committed content: the reviewer floor, the auto-skip list, and
    anything else that must agree on the same delta. Working-tree and staged
    edits are deliberately excluded — they are not yet part of the change
    that reviewers and finalize-review will see.

    ``None`` means the delta could not be computed at all, which is not the
    same fact as an empty delta and must not be read as one. A checkout that
    holds only the branch — the ordinary CI fetch — resolves no trunk, so
    every caller has to decide for itself what "cannot tell" means for it.

    Working on the trunk is not that case. There the delta is computable and
    empty by construction, which `branch_base` refuses precisely because it
    would pass every recomputed rule; that stays an empty delta here, so the
    rules keep failing closed on it.
    """
    try:
        selected = head_sha or git_text(repo, "rev-parse", "HEAD")
        base = branch_base(repo)
        status = git_text(
            repo, "diff", "--name-status", "--no-renames", base, selected
        )
    except (OSError, UsageError):
        current = git_maybe(repo, "rev-parse", "--abbrev-ref", "HEAD") or ""
        if current in TRUNK_BRANCH_NAMES or current == "HEAD":
            return set(), set(), set()
        return None
    paths: set[str] = set()
    removed: set[str] = set()
    added: set[str] = set()
    for line in status.splitlines():
        code, _, name = line.partition("\t")
        name = name.strip()
        if not name or _is_host_plumbing(name):
            continue
        paths.add(name)
        letter = code.strip().upper()[:1]
        if letter == "D":
            removed.add(name)
        elif letter == "A":
            added.add(name)
    return paths, removed, added


def committed_branch_paths(
    repo: Path, change_id: str, head_sha: str | None = None
) -> set[str]:
    """The committed branch-delta paths; empty when the delta cannot be read."""
    delta = committed_branch_delta(repo, change_id, head_sha)
    return delta[0] if delta else set()


def auto_skipped_steps(
    repo: Path, change_id: str, head_sha: str | None = None
) -> set[str]:
    """Steps the committed delta skips with no typed confirmation.

    Recomputed from the delta itself, so finalize-review, the attestation
    validator read the same answer without a
    recorded event to consult.

    That recomputation is the reason an unreadable delta returns the whole
    auto-skip set rather than nothing. The set is not a demand, it is the
    list of steps nobody has to account for; answering "nothing was skipped"
    where the delta cannot be read turns a checkout that lacks the trunk —
    a single-branch CI clone validating an attestation finalize already
    wrote — into a refusal of evidence that was correct when it was made.
    An empty but readable delta is a different fact and stays not narrow.

    That permissive answer is only ever correct for a caller re-reading
    evidence that already exists and is bound to the commit's content, which
    is `attestation.validate_attestation` and nothing else. The caller that
    MAKES the evidence, `finalize-review`, refuses an unreadable delta before
    it ever reaches this function: there, "cannot tell" read as "everything
    is skipped" let a change touching production code finalize with no
    adversarial execution at all.
    """
    delta = committed_branch_delta(repo, change_id, head_sha)
    if delta is None:
        return set(_NARROW_AUTO_SKIP_STEPS)
    paths, removed, _added = delta
    selected = head_sha or git_maybe(repo, "rev-parse", "HEAD") or ""
    executable = tree_programs(repo, selected, paths) if selected else set()
    narrow = is_narrow_delta(paths, change_id, removed, executable)
    return set(_NARROW_AUTO_SKIP_STEPS) if narrow else set()


def required_reviewer_count(
    repo: Path, change_id: str, head_sha: str | None = None
) -> int:
    """Compute the reviewer floor from the selected branch delta, failing closed.

    Unlike the auto-skip list this one fails closed on an unreadable delta:
    the reviewer count is checked against verdicts the attestation itself
    records, so demanding two costs an honest change nothing.
    """
    delta = committed_branch_delta(repo, change_id, head_sha)
    if delta is None:
        return 2
    paths, removed, _added = delta
    floor = reviewer_floor_for_paths(paths, change_id, removed)
    return max(floor, 2) if selected_outside_family(repo, change_id, head_sha) else floor
