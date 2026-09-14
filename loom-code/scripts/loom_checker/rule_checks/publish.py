from __future__ import annotations

import re


CONTEXTUAL_PR_HEADINGS = (
    "Context", "Intended outcome", "Scope", "Decisions", "Implementation",
    "Behaviour change", "Verification", "Risks and rollback", "Follow-ups",
)


DISCLOSURE_PREFIXES = ("Skipped steps:", "Prior failure:")


def _body_sections(body: str) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Top-level `## ` sections and every line outside fenced code."""
    sections: list[tuple[str, list[str]]] = []
    outside_fences: list[str] = []
    fence: tuple[str, int] | None = None
    for line in body.splitlines():
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


def validate_contextual_pr_body(body: str) -> str | None:
    """Recompute the structural PR-body floor; semantic truth stays review-owned."""
    sections, outside_fences = _body_sections(body)
    if [heading for heading, _content in sections] != list(CONTEXTUAL_PR_HEADINGS):
        return (
            "PR body must contain Ship's nine top-level contextual headings "
            "exactly once and in order, with no competing top-level heading"
        )
    for heading, lines in sections:
        content = "\n".join(lines)
        visible = re.sub(r"<!--.*?-->", " ", content, flags=re.DOTALL)
        alphanumeric_count = sum(character.isalnum() for character in visible)
        one_ascii_token = re.fullmatch(r"\s*[A-Za-z]+[.!?:;,-]*\s*", visible) is not None
        template_placeholder = re.fullmatch(r"\s*<[^>\n]+>\s*", visible) is not None
        sentinel = (
            heading == "Follow-ups"
            and re.sub(r"[\W_]+", "", visible).casefold() == "none"
        )
        if (
            (alphanumeric_count < 8 or one_ascii_token or template_placeholder)
            and not sentinel
        ):
            return f"PR body section {heading!r} has no substantive content"
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
        steps = ", ".join(confirmation.get("skip") or []) or "none"
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
    present = [line.rstrip() for line in verification if line.strip()]
    opening, rest = present[:len(expected)], present[len(expected):]
    if opening == expected and not any(line.startswith(DISCLOSURE_PREFIXES) for line in rest):
        return None
    if not expected:
        return ("PR body discloses skipped steps or prior failures, but the "
                "attestation records no step selection")
    return ("PR body section 'Verification' must start with exactly the "
            "attestation's selection disclosure and no other disclosure line:\n"
            + "\n".join(expected))
