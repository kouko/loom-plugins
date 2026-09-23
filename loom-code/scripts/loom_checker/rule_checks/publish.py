from __future__ import annotations

import re


CONTEXTUAL_PR_HEADINGS = (
    "Context", "Intended outcome", "Scope", "Decisions", "Implementation",
    "Behaviour change", "Verification", "Risks and rollback", "Follow-ups",
)


DISCLOSURE_PREFIXES = ("Skipped steps:", "Prior failure:")


# The user reads the `Skipped steps:` line, so a step id whose meaning is not
# plain gets its user-facing name in brackets; any other id renders as is.
STEP_PLAIN_NAMES = {"acceptance-test": "acceptance-test (independent acceptance testing)"}


def plain_step_names(steps) -> str:
    """A step list as every PR line that lists steps writes it; a step id
    outside the mapping, a retired one included, reads as recorded."""
    return ", ".join(STEP_PLAIN_NAMES.get(step, step) for step in steps)


# Ship's own lines: always accepted, never validated -- the CI check recomputes
# the status, so the body's copy is a courtesy, not a claim anything trusts.
STATUS_PREFIXES = ("Verification status:", "Skipped by instruction:")


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


def render_selection_disclosure(attestation: object) -> list[str]:
    """The lines `## Verification` must open with for this attestation.

    One `Skipped steps:` line per confirmation in recorded order (newest
    last), then one `Prior failure:` line per recorded prior failure. Ship's
    prose and the publish validator both use this one renderer."""
    selected = attestation.get("selection") if isinstance(attestation, dict) else None
    if not isinstance(selected, dict):
        return []
    lines = []
    for confirmation in selected.get("confirmations") or []:
        steps = plain_step_names(confirmation.get("skip") or []) or "none"
        lines.append(
            f"Skipped steps: {steps} — authority: {confirmation.get('source')} "
            f"({confirmation.get('code')}, {str(confirmation.get('at'))[:10]})"
        )
    for failure in selected.get("prior_failures") or []:
        lines.append(
            f"Prior failure: {failure.get('step')} {failure.get('rule')} "
            f"{str(failure.get('at'))[:10]}"
        )
    return lines


def validate_selection_disclosure(body: str, attestation: object) -> str | None:
    """`## Verification` opens with exactly the rendered disclosure and carries
    no other disclosure line; with a null selection no such line may appear."""
    expected = render_selection_disclosure(attestation)
    sections, _ = _body_sections(body)
    verification = next((lines for heading, lines in sections if heading == "Verification"), [])
    present = [line.rstrip() for line in verification
               if line.strip() and not line.startswith(STATUS_PREFIXES)]
    opening, rest = present[:len(expected)], present[len(expected):]
    if opening == expected and not any(line.startswith(DISCLOSURE_PREFIXES) for line in rest):
        return None
    if not expected:
        return ("PR body discloses skipped steps or prior failures, but the "
                "attestation records no step selection")
    return ("PR body section 'Verification' must start with exactly the "
            "attestation's selection disclosure and no other disclosure line:\n"
            + "\n".join(expected))
