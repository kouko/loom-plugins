"""Render review-only proposals from classified, source-linked session items.

Instruction items keep exact SKILL.md section anchors and draft snippets.
Plugin integration items use observed surface and source pointers instead.
Two distinct sessions are required for promotion; single-session evidence
remains pending. This module writes only the proposal output file.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from cluster import cluster_memory_items, skill_identity_from_path

# ---------------------------------------------------------------------------
# Constants.
# ---------------------------------------------------------------------------

# SequenceMatcher.ratio() threshold for "this title is essentially the same
# as that other title". 0.85 picked to tolerate punctuation / minor wording
# differences (Trace2Skill prompts produce slight variants across sessions)
# while still rejecting genuinely-different titles. Pair-wise on small N is
# fine — we never have more than O(20) Memory Items per run.
_TITLE_SIMILARITY_THRESHOLD = 0.85

# Secondary check: when two titles match by ratio, also require content
# overlap above this threshold before declaring a dedup. Prevents collapsing
# items that happen to share a generic title but describe different
# scenarios.
_CONTENT_SIMILARITY_THRESHOLD = 0.50

# ---------------------------------------------------------------------------
# Memory Item normalization.
# ---------------------------------------------------------------------------


def normalize_memory_item(raw: dict) -> dict:
    """Normalize a Memory Item dict; enforce required-field invariants.

    Required keys: ``title``, ``description``, ``content``, ``kind``, and
    ``issue_surface``. Instruction items require a real ``section_anchor``;
    integration items instead require subtype, mechanism and source pointer.

    Optional keys (with defaults): ``requires_new_reference_file`` (= False).

    Raises ``ValueError`` for an unclassified or ungrounded item.

    Returns a new dict; does not mutate ``raw``.
    """
    section_anchor_raw = raw.get("section_anchor")
    section_anchor = (
        str(section_anchor_raw).strip() if section_anchor_raw is not None else ""
    )
    surface = str(raw.get("issue_surface", "")).strip()
    if surface not in {"skill-instructions", "plugin-integration"}:
        raise ValueError("Memory Item requires issue_surface: skill-instructions or plugin-integration")
    subtype = str(raw.get("integration_subtype", "")).strip()
    pointer = str(raw.get("source_pointer", "")).strip()
    mechanism = str(raw.get("failure_mechanism", "")).strip()
    if surface == "skill-instructions" and not section_anchor:
        raise ValueError(
            "Memory Item missing required 'section_anchor' — v0.2 promoted "
            "this field to mandatory (Finding #4: dogfood showed v0.1's "
            "'Examples' default silently misfired on real SKILL.md files). "
            f"Got raw item: {raw!r}"
        )
    if surface == "plugin-integration":
        if section_anchor:
            raise ValueError("plugin-integration must not claim a SKILL.md section_anchor")
        if subtype not in {"registration", "loading", "hook", "bundled-script", "dependent-connector"}:
            raise ValueError("plugin-integration requires a known integration_subtype")
        if not pointer:
            raise ValueError("plugin-integration requires source_pointer")
        if not mechanism:
            raise ValueError("plugin-integration requires failure_mechanism")
    return {
        "title": str(raw.get("title", "")).strip(),
        "description": str(raw.get("description", "")).strip(),
        "content": str(raw.get("content", "")).strip(),
        "kind": str(raw.get("kind", "failure")).strip().lower(),
        "section_anchor": section_anchor,
        "issue_surface": surface,
        "integration_subtype": subtype,
        "source_pointer": pointer,
        "failure_mechanism": mechanism,
        "requires_new_reference_file": bool(
            raw.get("requires_new_reference_file", False)
        ),
        # Carry session context for traceability in rendered output.
        "_source_session": raw.get("_source_session", ""),
        "target_skill_path": raw.get("target_skill_path", ""),
        "target_skill": raw.get("target_skill", ""),
    }


def extract_memory_items(
    results: list[dict],
    target_skill_path: str | None = None,
) -> list[dict]:
    """Flatten subagent results into a single list of Memory Items.

    Each result entry has a ``memory_items`` array; we walk all entries and
    return one flat list with each item normalized + tagged with its source
    session id (for traceability in rendered output).

    When ``target_skill_path`` is provided (v2.7.1 hotfix), entries whose
    ``target_skill_path`` does NOT match are skipped — necessary when
    merged.json carries items for multiple target skills in one run (e.g.
    skill-retro targeted both writing-plans AND brainstorming).
    Without this filter, items intended for skill A leak into skill B's
    proposal. ``None`` default preserves backward-compat (legacy callers
    that pre-filter merged.json themselves are unaffected). An entry with an
    empty path (name-routed payload) matches when the skill part of its
    ``target_skill`` name (``plugin:skill``) matches both plugin and skill
    components of a target path under ``<plugin>/skills/<skill>/SKILL.md``.
    A path without that structure cannot safely use the name fallback.
    """
    flat: list[dict] = []
    expected_name = skill_identity_from_path(target_skill_path) if target_skill_path else ""
    for entry in results:
        if target_skill_path is not None:
            entry_path = entry.get("target_skill_path")
            entry_name = str(entry.get("target_skill") or "")
            by_name = not entry_path and bool(expected_name) and entry_name == expected_name
            if entry_path != target_skill_path and not by_name:
                continue
        session_id = entry.get("session_id", "unknown")
        for raw_item in entry.get("memory_items", []):
            item = normalize_memory_item({**raw_item, "_source_session": session_id,
                "target_skill_path": entry.get("target_skill_path", ""),
                "target_skill": entry.get("target_skill", "")})
            flat.append(item)
    return flat


# ---------------------------------------------------------------------------
# Dedup — Title + content overlap heuristic.
# ---------------------------------------------------------------------------


def _similarity(a: str, b: str) -> float:
    """SequenceMatcher.ratio() on whitespace-collapsed lowercase strings."""
    a_norm = " ".join(a.lower().split())
    b_norm = " ".join(b.lower().split())
    return difflib.SequenceMatcher(a=a_norm, b=b_norm).ratio()


def _items_are_near_duplicates(item_a: dict, item_b: dict) -> bool:
    """Two items merge when Title ratio ≥ threshold AND content overlaps.

    Title-only matching would over-aggregate when the same anti-pattern
    title shows up in two genuinely-different scenarios. Content-only
    matching is too noisy because Trace2Skill items rephrase content per
    session. Requiring BOTH keys reduces both false-positive and
    false-negative dedups.
    """
    title_ratio = _similarity(item_a["title"], item_b["title"])
    if title_ratio < _TITLE_SIMILARITY_THRESHOLD:
        return False
    content_ratio = _similarity(item_a["content"], item_b["content"])
    return content_ratio >= _CONTENT_SIMILARITY_THRESHOLD


def dedup_items(items: list[dict]) -> list[dict]:
    """Collapse near-identical Memory Items via pair-wise Title + content
    similarity.

    Greedy single-pass: for each item, check whether it merges with any
    already-kept item. If yes, drop the new item (the kept one wins —
    first-seen by input order). Order-preserving.

    Two items only merge when BOTH:
    - title SequenceMatcher ratio ≥ ``_TITLE_SIMILARITY_THRESHOLD`` (0.85)
    - content SequenceMatcher ratio ≥ ``_CONTENT_SIMILARITY_THRESHOLD`` (0.50)

    Returns a new list; does not mutate input.
    """
    kept: list[dict] = []
    for item in items:
        if any(_items_are_near_duplicates(item, k) for k in kept):
            continue
        kept.append(item)
    return kept


# ---------------------------------------------------------------------------
# v0.2 partition.
# ---------------------------------------------------------------------------


def partition_by_v02_marker(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split items into (main, v02).

    Promoted instruction items with ``requires_new_reference_file: True``
    go to v02. Integration items keep their own proposal form, because a
    plugin or connector change has no SKILL.md section anchor.
    """
    main: list[dict] = []
    v02: list[dict] = []
    for item in items:
        if item["requires_new_reference_file"] and item.get("issue_surface") != "plugin-integration":
            v02.append(item)
        else:
            main.append(item)
    return main, v02


# ---------------------------------------------------------------------------
# v0.2 anchor-mismatch partition.
# ---------------------------------------------------------------------------


def extract_skill_md_headings(skill_md: str) -> set[str]:
    """Return the set of heading texts (without leading ``#``) from a SKILL.md.

    Captures any line starting with one or more ``#`` followed by space and
    text; strips the marker + surrounding whitespace. Used for anchor-
    validation: a Memory Item whose ``section_anchor`` is not in this set
    is routed to §"Anchor mismatch — needs review" instead of being silently
    misapplied.

    Tracks fenced-code-block state via a triple-backtick toggle (v2.6.1
    hotfix): a line starting with ``` flips the in-code-block flag, and
    ``##`` lines inside a fenced block do NOT register as headings. This
    prevents a SKILL.md code example like ``` ```bash\\n## fake heading
    \\n``` ``` from yielding ``fake heading`` as a valid anchor.
    """
    headings: set[str] = set()
    in_code_block = False
    for line in skill_md.splitlines():
        # ``lstrip()`` covers indented fences (e.g. fenced blocks nested
        # inside list items); ``##`` headings themselves are NOT
        # ``lstrip()``-ed below so indented headings stay ignored — same
        # contract as before.
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not line.startswith("#"):
            continue
        stripped = line.lstrip("#").strip()
        if stripped:
            headings.add(stripped)
    return headings


def partition_by_anchor_match(
    items: list[dict], skill_headings: set[str]
) -> tuple[list[dict], list[dict]]:
    """Split items into (anchor_ok, anchor_mismatch).

    Items whose ``section_anchor`` does not exist as a heading in the target
    SKILL.md go to the mismatch bucket. Headings are matched case-sensitively
    to match the exact target heading.
    """
    anchor_ok: list[dict] = []
    anchor_mismatch: list[dict] = []
    for item in items:
        if item.get("issue_surface") == "plugin-integration":
            anchor_ok.append(item)
            continue
        if item["section_anchor"] in skill_headings:
            anchor_ok.append(item)
        else:
            anchor_mismatch.append(item)
    return anchor_ok, anchor_mismatch


# ---------------------------------------------------------------------------
# Section extraction from target SKILL.md.
# ---------------------------------------------------------------------------


def _extract_section(skill_md: str, section_anchor: str) -> str:
    """Return the body of the named section from a SKILL.md string.

    Matches ``## <section_anchor>`` (any heading level) up to the next
    heading of equal-or-lower depth. Match is CASE-SENSITIVE so the
    proposed section corresponds to the current target heading.
    Returns empty string when not found — modifications
    against missing sections still render but the diff body has only
    `+ ` lines (the draft diff
    block has no `- ` lines — that surfaces the problem rather than
    silently no-op'ing).
    """
    lines = skill_md.splitlines()
    # Find heading line.
    heading_idx = None
    heading_depth = None
    target = section_anchor.strip()
    for i, line in enumerate(lines):
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        if depth == 0 or not line.startswith("#"):
            continue
        if stripped.strip() == target:
            heading_idx = i
            heading_depth = depth
            break
    if heading_idx is None or heading_depth is None:
        return ""

    # Collect body until next heading of depth ≤ heading_depth.
    body_lines: list[str] = []
    for line in lines[heading_idx + 1:]:
        if line.startswith("#"):
            stripped = line.lstrip("#")
            other_depth = len(line) - len(stripped)
            if other_depth <= heading_depth:
                break
        body_lines.append(line)
    return "\n".join(body_lines).strip("\n") + "\n"


# ---------------------------------------------------------------------------
# Markdown rendering.
# ---------------------------------------------------------------------------


def _render_addition(item: dict, index: int) -> list[str]:
    """Render one kind=success item under §Proposed additions.

    Review heading format: ``### Addition <N> [insert into §<section>]``.
    The Memory Item's freeform Title is NOT in the heading — it
    becomes a bolded first line of the fenced block body so reviewers
    inserts it verbatim into the target section.

    ``index`` is the 1-indexed counter scoped to additions in this
    proposal (Additions and Modifications counters are independent).
    """
    body_lines: list[str] = []
    if item["title"]:
        body_lines.append(f"**{item['title']}**")
        body_lines.append("")
    if item["description"]:
        body_lines.append(f"_{item['description']}_")
        body_lines.append("")
    body_lines.append(item["content"])
    supporting = item.get("supporting_sessions")
    if supporting:
        sessions_str = ", ".join(supporting)
        body_lines.append("")
        body_lines.append(
            f"_(supported by {len(supporting)} session(s): {sessions_str})_"
        )
    elif item.get("_source_session"):
        body_lines.append("")
        body_lines.append(f"_source session: `{item['_source_session']}`_")

    lines = [
        f"### Addition {index} [insert into §{item['section_anchor']}]",
        "",
        "```",
    ]
    lines.extend(body_lines)
    lines.append("```")
    lines.append("")
    return lines


def _render_modification(item: dict, index: int, skill_md: str) -> list[str]:
    """Render one kind=failure item under §Proposed modifications.

    Review heading format: ``### Modification <N> [§<section>]``. Body
    is a fenced ``diff`` block containing only ``- `` (old line) and
    ``+ `` (new line) pairs — no unified-diff headers and no
    space-prefixed context lines (review format accepts
    ``- `` / ``+ `` / blank lines).

    The "old lines" are extracted from the named SKILL.md section
    (whole section body, each non-blank line). The "new lines"
    repeat the old lines, then append item.content as guidance — so
    A later implementation may replace the matched contiguous run with old+new
    content, which preserves the original lines while adding the new
    guidance. When the section is empty or missing, no `- ` lines
    can be emitted; we surface that by inserting a sentinel `- `
    line based on the section anchor itself, so review flags
    with a clear DiffMismatch — better than silently no-op'ing.

    ``index`` is the 1-indexed counter scoped to modifications in
    this proposal.
    """
    current_section = _extract_section(skill_md, item["section_anchor"])
    minus_lines = [ln for ln in current_section.splitlines() if ln.strip()]

    if minus_lines:
        # Replace the section's existing non-blank lines with themselves +
        # the new guidance appended (preserves prior content, adds new
        # text below).
        plus_lines = list(minus_lines)
        plus_lines.append("")
        plus_lines.append(item["content"])
    else:
        # Section is empty or missing. Emit a single sentinel `- ` line
        # so the review shows a clear missing anchor — better
        # than a silent no-op.
        minus_lines = [f"<missing or empty section: §{item['section_anchor']}>"]
        plus_lines = [item["content"]]

    lines = [
        f"### Modification {index} [§{item['section_anchor']}]",
        "",
    ]
    if item["title"] or item["description"]:
        if item["title"]:
            lines.append(f"**{item['title']}**")
        if item["description"]:
            lines.append(f"_{item['description']}_")
        lines.append("")
    lines.append("```diff")
    for ml in minus_lines:
        lines.append(f"- {ml}")
    for pl in plus_lines:
        lines.append(f"+ {pl}")
    lines.append("```")
    if item.get("_source_session"):
        lines.append("")
        lines.append(f"_source session: `{item['_source_session']}`_")
    lines.append("")
    return lines


def _render_v02_item(item: dict) -> list[str]:
    """Render one v0.2-bucket item under §Marked for v0.2."""
    lines = [
        f"### {item['title']}",
        f"_{item['description']}_" if item["description"] else "",
        "",
        f"**Target section**: §{item['section_anchor']}",
        f"**Kind**: {item['kind']}",
        "**Deferred to v0.2**: requires new reference file (per Q4 — v0.1 is SKILL.md only).",
        "",
        item["content"],
    ]
    if item.get("_source_session"):
        lines.append("")
        lines.append(f"_source session: `{item['_source_session']}`_")
    lines.append("")
    return lines


def _render_anchor_mismatch_item(item: dict, valid_headings: list[str]) -> list[str]:
    """Render one anchor-mismatched item under §Anchor mismatch — needs review.

    The reviewer needs the dead anchor named verbatim AND a list of the
    valid headings the operator can re-route to.
    """
    lines = [
        f"### {item['title']}",
    ]
    if item["description"]:
        lines.append(f"_{item['description']}_")
    lines.append("")
    lines.append(f"**Proposed anchor**: §{item['section_anchor']}  _(no matching heading in target SKILL.md)_")
    lines.append(f"**Kind**: {item['kind']}")
    lines.append("")
    if valid_headings:
        lines.append("**Valid headings in target**:")
        for heading in valid_headings:
            lines.append(f"- §{heading}")
        lines.append("")
    lines.append("**Re-route required**: assign a real heading in the source merged.json before rendering again.")
    lines.append("")
    lines.append(item["content"])
    if item.get("_source_session"):
        lines.append("")
        lines.append(f"_source session: `{item['_source_session']}`_")
    lines.append("")
    return lines


def _render_pending_item(item: dict) -> list[str]:
    """Render one pending item under §Cross-session evidence pending.

    Each entry shows the item title + content annotated with its session_id
    so the operator sees "would have clustered; only 1 session — re-run after
    more session evidence accumulates."
    """
    session_id = item.get("_source_session") or item.get("session_id") or "unknown"
    lines = [
        f"### {item['title']}",
    ]
    if item.get("description"):
        lines.append(f"_{item['description']}_")
    lines.append("")
    if item.get("requires_new_reference_file"):
        lines.append("**Requires new reference file**: still pending cross-session evidence.")
        lines.append("")
    lines.append(item["content"])
    if item.get("issue_surface") == "plugin-integration":
        lines.extend([f"**Integration surface**: {item['integration_subtype']}",
                      f"**Source pointer**: `{item['source_pointer']}`"])
    lines.append("")
    lines.append(
        f"_Observed in 1 session: `{session_id}` — re-run after more session "
        "evidence accumulates._"
    )
    lines.append("")
    return lines


def render_proposals_markdown(
    items: list[dict],
    *,
    target_skill_path: str,
    target_skill_md_content: str,
    run_date: str | None = None,
) -> str:
    """Render the full proposals markdown file as a string.

    Args:
        items: Memory Items (already normalized via ``normalize_memory_item``).
            The renderer clusters instruction items by target, title and
            anchor, and integration items by target, subtype and mechanism,
            via ``cluster_memory_items`` to identify multi-session patterns
            (N >= 2 distinct sessions → promoted) vs single-session
            observations (→ §"Cross-session evidence pending" bucket).
            Cluster subsumes the old ratio-based dedup that previously ran
            inline here; the public ``dedup_items`` helper remains available
            for callers needing the legacy behavior.
        target_skill_path: path to the target SKILL.md (rendered in header
            for human reviewers).
        target_skill_md_content: current SKILL.md text (used to compute
            unified-diff against for modifications).
        run_date: optional ``YYYY-MM-DD`` override; default = today UTC.

    Returns the markdown document as a single string.
    """
    if run_date is None:
        run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Cluster every item before applying destination buckets. In particular,
    # a reference-file request from one session is still pending evidence.
    # v0.3 cluster step: partition items into promoted (>= 2 distinct
    # sessions) and pending (1 session only).  cluster_memory_items uses the
    # ``session_id`` field; items arriving via extract_memory_items carry
    # ``_source_session`` — expose it as ``session_id`` for the clusterer
    # without mutating the original dicts.  Cluster subsumes the old
    # ``dedup_items`` role: the promoted representative is already one item
    # per (title, anchor) group; pending items are inherently single-session.
    clusterable = [
        {**it, "session_id": it.get("session_id") or it.get("_source_session", "")}
        for it in items
    ]
    promoted, pending = cluster_memory_items(clusterable, min_n=2)
    main, v02 = partition_by_v02_marker(promoted)

    # v0.2 Finding #4: items whose section_anchor doesn't match a real
    # heading in the target SKILL.md route to a third bucket instead of
    # silently producing dead-anchor proposals.
    skill_headings = extract_skill_md_headings(target_skill_md_content)
    anchor_ok, anchor_mismatch = partition_by_anchor_match(main, skill_headings)

    integration = [it for it in anchor_ok if it.get("issue_surface") == "plugin-integration"]
    additions = [it for it in anchor_ok if it.get("issue_surface") != "plugin-integration" and it["kind"] == "success"]
    modifications = [it for it in anchor_ok if it.get("issue_surface") != "plugin-integration" and it["kind"] == "failure"]

    parts: list[str] = []
    parts.append(f"# skill-retro proposals — {run_date}")
    parts.append("")
    parts.append(f"**Target SKILL.md**: `{target_skill_path}`")
    parts.append(
        f"**Counts**: {len(additions)} addition(s), "
        f"{len(modifications)} modification(s), "
        f"{len(integration)} integration proposal(s), "
        f"{len(anchor_mismatch)} anchor mismatch(es), "
        f"{len(pending)} pending cross-session evidence, "
        f"{len(v02)} deferred to v0.2."
    )
    parts.append("")
    parts.append(
        "> Review only. Send approved changes to an independent implementation workflow."
    )
    parts.append("")

    parts.append("## Proposed additions")
    parts.append("")
    if additions:
        for n, item in enumerate(additions, start=1):
            parts.extend(_render_addition(item, n))
    else:
        parts.append("_(none)_")
        parts.append("")

    parts.append("## Proposed modifications")
    parts.append("")
    if modifications:
        for n, item in enumerate(modifications, start=1):
            parts.extend(_render_modification(item, n, target_skill_md_content))
    else:
        parts.append("_(none)_")
        parts.append("")

    parts.append("## Plugin integration proposals")
    parts.append("")
    if integration:
        for item in integration:
            lines = [
                f"### {item['title']}",
                f"**Target skill**: `{target_skill_path}`",
                f"**Integration surface**: {item['integration_subtype']}",
                f"**Observed behavior**: {item['description']}",
                f"**Failure mechanism**: {item['failure_mechanism']}",
                f"**Supporting sessions**: {', '.join(f'`{s}`' for s in item['supporting_sessions'])}",
                f"**Source checks**: {', '.join(f'`{p}`' for p in item['supporting_source_pointers'])}",
                f"**Proposed outcome**: {item['content']}",
            ]
            if item.get("requires_new_reference_file"):
                lines.append("**Reference-file caveat**: A new reference file may be needed; verify its owner in the independent implementation workflow.")
            lines.extend([
                "**Uncertainty**: Confirm the cited integration source explains the observed behavior.",
                "**Verification idea**: Reproduce the activation or integration path in an independent implementation workflow.",
                "",
            ])
            parts.extend(lines)
    else:
        parts.extend(["_(none)_", ""])

    parts.append("## Anchor mismatch — needs review")
    parts.append("")
    if anchor_mismatch:
        parts.append(
            "_These items' `section_anchor` did not match any heading in the "
            "target SKILL.md. Re-assign a real heading in the source merged.json "
            "before rendering again._"
        )
        parts.append("")
        valid_headings_sorted = sorted(skill_headings)
        for item in anchor_mismatch:
            parts.extend(_render_anchor_mismatch_item(item, valid_headings_sorted))
    else:
        parts.append("_(none)_")
        parts.append("")

    parts.append("## Cross-session evidence pending")
    parts.append("")
    if pending:
        parts.append(
            "_These items were observed in only 1 session and did not reach "
            "the minimum cross-session evidence threshold (min_n=2). They are "
            "NOT auto-applied — re-run after more sessions accumulate to promote "
            "them._"
        )
        parts.append("")
        for item in pending:
            parts.extend(_render_pending_item(item))
    else:
        parts.append("_(none)_")
        parts.append("")

    parts.append("## Marked for v0.2")
    parts.append("")
    if v02:
        parts.append(
            "_These proposals require new reference files; per Q4 of the v0.1 "
            "brief, defer them to a future iteration._"
        )
        parts.append("")
        for item in v02:
            parts.extend(_render_v02_item(item))
    else:
        parts.append("_(none)_")
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def _load_subagent_results(path: Path) -> list[dict]:
    text = path.read_text()
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(
            f"expected top-level JSON list in {path}, got {type(data).__name__}"
        )
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="propose",
        description=(
            "Merge skill-retro subagent Memory Items into a markdown "
            "proposal file. Does NOT write to the target SKILL.md."
        ),
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to subagent results JSON (list of {session_id, memory_items}).",
    )
    parser.add_argument(
        "--target-skill",
        required=True,
        type=str,
        help="Path to the target SKILL.md (read-only — rendered in proposal header).",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Where to write the proposal markdown file.",
    )
    parser.add_argument(
        "--skill-content-file",
        type=Path,
        default=None,
        help=(
            "Optional override path to read the SKILL.md text from. Defaults "
            "to --target-skill. Useful for tests / dry-runs where the target "
            "path is symbolic."
        ),
    )
    parser.add_argument(
        "--run-date",
        type=str,
        default=None,
        help="Override run date (YYYY-MM-DD); default = today UTC.",
    )
    args = parser.parse_args(argv)

    results = _load_subagent_results(args.input)
    items = extract_memory_items(results, target_skill_path=args.target_skill)

    # Read SKILL.md text — from --skill-content-file if provided, else from
    # --target-skill. In production --target-skill IS the path to read; the
    # override exists for tests where target is symbolic.
    content_path = args.skill_content_file or Path(args.target_skill)
    if content_path.exists():
        skill_content = content_path.read_text()
    else:
        # Target SKILL.md may not exist yet (e.g. proposing initial content).
        # Render with empty content so modifications still produce sensible
        # diffs (current side empty → all + lines).
        skill_content = ""

    output = render_proposals_markdown(
        items,
        target_skill_path=args.target_skill,
        target_skill_md_content=skill_content,
        run_date=args.run_date,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output)
    print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover  (CLI entrypoint)
    sys.exit(main())
