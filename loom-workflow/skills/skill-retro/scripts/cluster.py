"""cluster.py — pure-function clustering of memory items by cross-session evidence.

Public API
----------
cluster_memory_items(items, min_n=2) -> tuple[list[dict], list[dict]]
    Partition memory items into ``promoted`` (multi-session patterns) and
    ``pending`` (single-session / below-threshold observations).

Design notes
------------
- Normalization key: (title_norm, anchor_norm) where norm = lowercase +
  whitespace-collapse + strip leading/trailing punctuation from allowlist.
- Promotion criterion: number of *distinct* session_ids in a group >= min_n.
- Pure function: no I/O; input dicts are not mutated (copies built as needed).
- Stdlib-only: no embeddings, no third-party deps.

Locked decision Q-v0.3-1 = A (Filter):
    N=1 items go to pending (not silently dropped) so the §Cross-session
    evidence pending bucket renderer (Task 2) can surface them.
"""

import copy
import re
import string
from collections import defaultdict
from pathlib import Path

# Characters stripped from the leading/trailing positions of normalized strings.
# Internal punctuation is preserved (e.g. hyphens in compound words).
_STRIP_CHARS = set(".,;:!?'\"" + string.whitespace)


def skill_identity_from_path(path: str) -> str:
    """Return plugin:skill for source and versioned installed skill paths."""
    parts = Path(path).parts
    if "skills" not in parts:
        return ""
    index = len(parts) - 1 - parts[::-1].index("skills")
    if index < 1 or index + 1 >= len(parts) - 1:
        return ""
    plugin = parts[index - 1]
    if re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.]+)?", plugin):
        if index < 2:
            return ""
        plugin = parts[index - 2]
    return f"{plugin}:{parts[index + 1]}"


def _normalize(text: str) -> str:
    """Lowercase, collapse internal whitespace, strip leading/trailing punctuation.

    Stripping uses an allowlist of punctuation chars (.,;:!?'"") plus
    whitespace.  Internal punctuation is intentionally preserved so that
    "Read/Write" and "ReadWrite" do not accidentally merge.
    """
    # Collapse internal whitespace first, then strip boundaries.
    collapsed = " ".join(text.split())
    # Strip one character at a time from each end until no strip-chars remain.
    result = collapsed.lower()
    # lstrip / rstrip accept a *string* of chars to strip (set of chars, not substring).
    strip_str = "".join(_STRIP_CHARS)
    result = result.strip(strip_str)
    return result


def _sort_promoted_and_pending(
    promoted_entries: list[tuple[int, str, dict]],
    pending_entries: list[tuple[str, str, dict]],
) -> tuple[list[dict], list[dict]]:
    """Sort and extract promoted and pending lists from entry tuples.

    Args:
        promoted_entries:  List of (group_size, norm_title, representative) tuples.
        pending_entries:   List of (session_id, norm_title, item) tuples.

    Returns:
        (promoted, pending) tuple with proper sort order applied:
        - promoted: sorted by group size descending, then alphabetic by title.
        - pending: sorted by session_id ascending, then normalized title ascending.
    """
    promoted_entries.sort(key=lambda e: (-e[0], e[1]))
    promoted = [e[2] for e in promoted_entries]

    pending_entries.sort(key=lambda e: (e[0], e[1]))
    pending = [e[2] for e in pending_entries]

    return promoted, pending


def cluster_memory_items(
    items: list[dict],
    min_n: int = 2,
) -> tuple[list[dict], list[dict]]:
    """Partition memory items into promoted patterns and pending observations.

    Args:
        items:  Flat list of memory item dicts.  Each must contain at least
                ``title``, ``section_anchor``, and ``session_id`` keys.
        min_n:  Minimum number of *distinct* session_ids required for a group
                to be promoted.  Default 2. Must be >= 1.

    Returns:
        A ``(promoted, pending)`` tuple.

        promoted:
            One representative dict per group that reached min_n distinct
            sessions.  The representative is a shallow copy of the *first*
            item in the group (input order) with a new ``supporting_sessions``
            key added — an alphabetically-sorted list of distinct session_ids.
            Sorted by group size descending; ties broken alphabetically by
            normalized title.

        pending:
            All items whose group did not reach min_n distinct sessions,
            returned individually in their original shape (no
            ``supporting_sessions`` added).  Sorted by session_id then by
            normalized title.

    Raises:
        ValueError: if min_n < 1.

    Notes:
        - Does not mutate input dicts or the input list.
        - Items from the *same* session with the same (title, anchor) do not
          contribute more than one vote toward the distinct-session count.
    """
    if min_n < 1:
        raise ValueError(
            f"min_n must be >= 1 (minimum distinct sessions required for promotion), got {min_n}"
        )

    if not items:
        return [], []

    # -----------------------------------------------------------------------
    # Phase 1: group items by normalized (title, anchor) key.
    # Each bucket holds a list of (norm_title, item) pairs so we can sort
    # pending later without re-normalizing.
    # -----------------------------------------------------------------------
    groups: dict[tuple[str, ...], list[tuple[dict, str]]] = defaultdict(list)

    for item in items:
        norm_title = _normalize(item.get("title", ""))
        path = str(item.get("target_skill_path") or "")
        identity = skill_identity_from_path(path) or path or str(item.get("target_skill") or "")
        if item.get("issue_surface") == "plugin-integration":
            key = (
                _normalize(identity),
                "plugin-integration",
                _normalize(item.get("integration_subtype", "")),
                _normalize(item.get("failure_mechanism", "")),
            )
        else:
            key = (_normalize(identity), "skill-instructions", norm_title, _normalize(item.get("section_anchor", "")))
        item_copy = copy.copy(item)
        groups[key].append((item_copy, norm_title))

    # -----------------------------------------------------------------------
    # Phase 2: split groups into promoted / pending based on distinct sessions.
    # -----------------------------------------------------------------------
    promoted_entries: list[tuple[int, str, dict]] = []
    pending_entries: list[tuple[str, str, dict]] = []

    for key, bucket in groups.items():
        norm_title = bucket[0][1]
        seen_sessions: set[str] = set()
        for item_copy, _ in bucket:
            seen_sessions.add(item_copy.get("session_id", ""))

        if len(seen_sessions) >= min_n:
            rep = copy.copy(bucket[0][0])
            rep["supporting_sessions"] = sorted(seen_sessions)
            for field in ("source_inspections", "session_snapshots"):
                rep[field] = [copy.deepcopy(record) for item, _ in bucket
                              for record in item.get(field, [])]
            if rep.get("issue_surface") == "plugin-integration":
                rep["supporting_source_pointers"] = sorted({
                    item.get("source_pointer", "") for item, _ in bucket
                })
            promoted_entries.append((len(seen_sessions), norm_title, rep))
        else:
            for item_copy, nt in bucket:
                session_id = item_copy.get("session_id", "")
                pending_entries.append((session_id, nt, item_copy))

    # -----------------------------------------------------------------------
    # Phase 3: sort and return via helper.
    # -----------------------------------------------------------------------
    return _sort_promoted_and_pending(promoted_entries, pending_entries)
