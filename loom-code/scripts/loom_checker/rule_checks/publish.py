from __future__ import annotations

import re


CONTEXTUAL_PR_HEADINGS = (
    "Context", "Intended outcome", "Scope", "Decisions", "Implementation",
    "Behaviour change", "Verification", "Risks and rollback", "Follow-ups",
)


# Ship's own lines. Publish refuses a `Verification status:` line that
# differs from the status it computes (`validate_stated_status`); CI still
# recomputes the status itself.
STATUS_PREFIXES = ("Verification status:", "Skipped by instruction:")


# Only `:` or `：` separates the label from its value: a table cell border
# cannot, since one line cannot tell a header row from a data row. The value
# runs from past the separators and emphasis to the next cell border.
_STATUS_CLAIM = re.compile(r"^(?:\d+ )?(?:x )?verification status ?:")
_STATUS_VALUE = re.compile(r"status[\W_]*?[:：][\s:：|*_`]*([^|]*)", re.IGNORECASE)


def _status_claim(line: str) -> bool:
    """Whether the line, with all Markdown punctuation reduced to spaces,
    opens with the `Verification status:` label."""
    normalized = re.sub(r"[^\w:]+|_", " ", line.casefold().replace("：", ":")).strip()
    return _STATUS_CLAIM.match(normalized) is not None


def validate_stated_status(body: str, status: str) -> str | None:
    """Every visible status claim, in any Markdown dress, states `status`:
    its value (past the label's separators, up to the next cell border,
    trimmed of whitespace and `*_`|`) equals it exactly; a body without such
    a claim, or a label with no value such as a table header, is not judged."""
    prefix = STATUS_PREFIXES[0]
    for line in _body_sections(body, strip_comments=True)[1]:
        stated = line.strip()
        if not _status_claim(line):
            continue
        # Detection casefolds; the raw line may not match (a ligature such
        # as "ﬆ"), and a claim whose value cannot be parsed is refused.
        parsed = _STATUS_VALUE.search(line)
        value = parsed.group(1).strip(" \t*_`|") if parsed else None
        if value is None or (value and value != status):
            return (f"PR body states '{stated}'; the body must carry exactly this "
                    f"bare line:\n{prefix} {status}")
    return None


def _visible_part(line: str, in_comment: bool) -> tuple[str, bool]:
    """The line with HTML comment text removed, and whether a comment is
    still open at its end."""
    visible = ""
    while line:
        if in_comment:
            end = line.find("-->")
            if end < 0:
                return visible, True
            line, in_comment = line[end + 3:], False
        else:
            start = line.find("<!--")
            if start < 0:
                return visible + line, False
            visible, line, in_comment = visible + line[:start], line[start + 4:], True
    return visible, in_comment


def _body_sections(
    body: str, strip_comments: bool = False
) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Top-level `## ` sections and every line outside fenced code; with
    `strip_comments`, HTML comments outside fenced code are removed first."""
    sections: list[tuple[str, list[str]]] = []
    outside_fences: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for line in body.splitlines():
        if strip_comments and fence is None:
            line, in_comment = _visible_part(line, in_comment)
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker and fence is None:
            token = marker.group(1)
            fence = (token[0], len(token))
            continue
        if marker and fence is not None:
            token, suffix = marker.group(1), marker.group(2)
            if token[0] == fence[0] and len(token) >= fence[1] and not suffix.strip():
                fence = None
            continue
        if fence is not None:
            continue
        outside_fences.append(line)
        heading = re.fullmatch(r"## ([^#\n].*)", line)
        if heading:
            sections.append((heading.group(1), []))
        elif sections:
            sections[-1][1].append(line)
    return sections, outside_fences


def _heading_fault(headings: list[str]) -> str | None:
    """The first heading that breaks "the nine, exactly once, in order"."""
    for index, found in enumerate(headings):
        if found not in CONTEXTUAL_PR_HEADINGS:
            return f'heading "{found}" is not one of the nine contextual headings'
        if found in headings[:index]:
            return f'heading "{found}" is duplicated'
        expected = CONTEXTUAL_PR_HEADINGS[index] if index < len(CONTEXTUAL_PR_HEADINGS) else None
        if found == expected:
            continue
        if expected is not None and expected not in headings:
            return f'heading "{expected}" is missing'
        return f'heading "{found}" is out of order'
    if len(headings) < len(CONTEXTUAL_PR_HEADINGS):
        return f'heading "{CONTEXTUAL_PR_HEADINGS[len(headings)]}" is missing'
    return None


def _empty(heading: str, visible: str) -> bool:
    alphanumeric_count = sum(character.isalnum() for character in visible)
    one_ascii_token = re.fullmatch(r"\s*[A-Za-z]+[.!?:;,-]*\s*", visible) is not None
    template_placeholder = re.fullmatch(r"\s*<[^>\n]+>\s*", visible) is not None
    sentinel = (
        heading == "Follow-ups"
        and re.sub(r"[\W_]+", "", visible).casefold() == "none"
    )
    return (alphanumeric_count < 8 or one_ascii_token or template_placeholder) and not sentinel


def _structure_fault(sections: list[tuple[str, list[str]]]) -> str | None:
    fault = _heading_fault([heading for heading, _content in sections])
    if fault:
        return fault
    for heading, lines in sections:
        visible = re.sub(r"<!--.*?-->", " ", "\n".join(lines), flags=re.DOTALL)
        # A link or image renders its text, never its target.
        link_text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", visible)
        if _empty(heading, visible) or _empty(heading, link_text):
            return f'heading "{heading}" is empty'
    return None


def validate_contextual_pr_body(body: str) -> str | None:
    """Recompute the structural PR-body floor; semantic truth stays review-owned.

    The body is judged as written and again as rendered (HTML comments
    removed, links read as their text); either view's fault refuses, so
    the rendered view only ever tightens the floor."""
    sections, outside_fences = _body_sections(body)
    fault = _structure_fault(sections) or _structure_fault(
        _body_sections(body, strip_comments=True)[0]
    )
    if fault:
        return fault
    visible_body = re.sub(
        r"<!--.*?-->", " ", "\n".join(outside_fences), flags=re.DOTALL
    )
    if re.search(
        r"\b(?:private|hidden)(?:\s+or\s+(?:private|hidden))?\s+chain-of-thought\b",
        visible_body,
        flags=re.IGNORECASE,
    ):
        return "PR body must not claim to expose private or hidden chain-of-thought"
    return None
