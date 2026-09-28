# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Shared display-width primitive for terminal-cell measurement.

Width policy, derived from the interpreter's Unicode database (unicodedata):
  - Control (Cc), combining marks (Mn, Me), format (Cf) -> 0 cells
  - East Asian Width Wide (W) / Fullwidth (F)          -> 2 cells
  - Everything else (ASCII, Ambiguous, box-drawing)    -> 1 cell

Standard library only. This agrees with terminal widths on CJK ideographs,
kana, CJK punctuation and box-drawing glyphs; it can differ on some symbols
and emoji, so keep those out of box labels. Known divergences also include
U+00AD SOFT HYPHEN: category Cf, so measured 0 cells here, while many
terminals draw it as a visible 1-cell hyphen.

Labels passed through split_lines may not contain control (Cc) characters
other than line breaks (\\n, \\r): they measure 0 cells yet move the cursor
or change rendering, so split_lines raises ValueError naming the code point.
"""

import unicodedata

_ZERO_WIDTH_CATEGORIES = frozenset(("Cc", "Mn", "Me", "Cf"))
_WIDE = frozenset(("W", "F"))
_LINE_BREAKS = frozenset("\n\r")


def char_width(c: str) -> int:
    """Return the terminal-cell width of a single character."""
    if unicodedata.category(c) in _ZERO_WIDTH_CATEGORIES:
        return 0
    return 2 if unicodedata.east_asian_width(c) in _WIDE else 1


def display_width(s: str) -> int:
    """Return the total terminal-cell width of a string."""
    return sum(char_width(c) for c in s)


def split_lines(label: str) -> list[str]:
    """Split a label into a list of >= 1 physical line, no embedded controls.

    Uses str.splitlines(), which breaks on \\n, \\r, \\r\\n (and \\v/\\f), so a
    CRLF or bare-CR label becomes real line breaks with NO embedded
    carriage-return left in any element. A bare \\r is a 0-width
    cursor-moving control char: left embedded it passes width checks yet
    silently corrupts terminal alignment, so it must become a real break.
    Empty input yields [""] (splitlines("") is [], normalized to one line).

    Any other control (Cc) character, such as a tab or an ANSI escape, raises
    ValueError naming its code point: it measures 0 cells, so a generator
    would misalign while the width checks still report clean.
    """
    for c in label:
        if c not in _LINE_BREAKS and unicodedata.category(c) == "Cc":
            raise ValueError(
                f"label {label!r} contains control character U+{ord(c):04X}; remove it"
            )
    return label.splitlines() or [""]


def wrap_label(text: str, max_width: int) -> list[str]:
    """Width-aware wrapping that breaks preferentially at ASCII spaces.

    Args:
        text: The text to wrap
        max_width: Maximum width in display cells per line

    Returns:
        List of wrapped lines
    """
    if max_width <= 0:
        raise ValueError("max_width must be positive")

    if not text:
        return [""]

    # If the whole text fits, return it as a single line
    if display_width(text) <= max_width:
        return [text]

    lines = []
    remaining = text

    while remaining:
        # If remaining fits, we're done
        if display_width(remaining) <= max_width:
            lines.append(remaining)
            break

        # Find k = max number of characters that fit
        k = 0
        width_so_far = 0
        while k < len(remaining):
            c = remaining[k]
            c_width = char_width(c)
            if width_so_far + c_width > max_width:
                break
            width_so_far += c_width
            k += 1

        # Now k characters fit, but k+1 would not (if k < len(remaining))
        if k == len(remaining):
            # The whole remaining string fits
            line = remaining
            remaining = ""
        elif remaining[k] == ' ' and ord(remaining[k]) < 128:  # ASCII space
            # Case: next character is a space -> break before the space
            line = remaining[:k]
            remaining = remaining[k:]  # includes the space and everything after
            # Strip any leading spaces (to handle multiple consecutive spaces)
            remaining = remaining.lstrip(' ')
        else:
            # Case: next character is not a space
            # Look for the last space in remaining[0:k]
            last_space_idx = -1
            for i in range(k - 1, -1, -1):
                if remaining[i] == ' ' and ord(remaining[i]) < 128:  # ASCII space
                    last_space_idx = i
                    break

            if last_space_idx >= 0:
                # Break after the last space
                line = remaining[:last_space_idx + 1]
                remaining = remaining[last_space_idx + 1:]
            else:
                # No space found, look for the last ASCII-CJK or CJK-ASCII boundary
                last_boundary_idx = -1
                for i in range(k - 1, 0, -1):  # Check from end to start, need at least 2 chars for a boundary
                    if char_width(remaining[i - 1]) != char_width(remaining[i]):
                        last_boundary_idx = i
                        break

                if last_boundary_idx >= 0:
                    # Break before the boundary character
                    line = remaining[:last_boundary_idx]
                    remaining = remaining[last_boundary_idx:]
                else:
                    # No boundary, break at k (per-character break)
                    line = remaining[:k]
                    remaining = remaining[k:]

            # Strip leading spaces (to handle cases where we broke at a space and there are multiple spaces)
            remaining = remaining.lstrip(' ')

        lines.append(line)

    return lines


# W1-01: Shared helpers for structured node rendering and single-line validation

EMPTY_BODY = "Body cannot be empty for structured node"
"""Error message for empty structured node body.

Used by gen_flow, gen_arch, and gen_tree when a structured node's body is empty.
The longer variant "Body cannot be empty for structured node from string with \n"
is specific to string-input paths and remains at those call sites.
"""


def center(label: str, interior: int) -> str:
    """Pad label to `interior` display cells, label roughly centered.

    Padding is computed in display cells (not characters) so CJK labels
    are not over-padded. Extra odd cell goes to the right.
    Negative slack (label wider than interior) yields no padding.
    """
    slack = interior - display_width(label)
    if slack < 0:
        slack = 0
    left = slack // 2
    right = slack - left
    return " " * left + label + " " * right


def require_single_line(value: str, phrase: str, *,
                        template: str = "line break not supported in {phrase}: {value!r}") -> None:
    """Raise ValueError if `value` contains a line break.

    Args:
        value: The string to validate.
        phrase: Human-readable name for the value (e.g. "participant name").
        template: Optional message template with {phrase} and {value} placeholders.
                  Default matches gen_seq.py style; gen_bar.py passes its own template.
    """
    if split_lines(value) != [value]:
        raise ValueError(template.format(phrase=phrase, value=value))


def render_structured_node(title: str, body: list[str], interior: int) -> list[str]:
    """Return the title line, separator line, and wrapped body lines for a structured node.

    This is the shared block used by gen_flow.py and gen_arch.py (4 copies).
    Does NOT validate that body is non-empty; callers own that validation.
    Returns only the inner lines (excludes box top/bottom borders).

    Args:
        title: The title string (left-aligned).
        body: List of body strings (each wrapped at interior-1).
        interior: The box interior width in display cells.

    Returns:
        List of rendered lines: [title_line, separator_line, ...wrapped_body_lines]
    """
    lines = []

    # Title line (left-aligned): "│ " + title + padding + "│"
    title_padding = interior - display_width(title) - 1
    if title_padding < 0:
        title_padding = 0
    lines.append("│ " + title + " " * title_padding + "│")

    # Separator line: "├" + "─" * interior + "┤"
    lines.append("├" + "─" * interior + "┤")

    # Body lines (left-aligned, wrapped at interior - 1)
    for body_line in body:
        wrapped_lines = wrap_label(body_line, interior - 1)
        for wrapped_line in wrapped_lines:
            body_padding = interior - display_width(wrapped_line) - 1
            if body_padding < 0:
                body_padding = 0
            lines.append("│ " + wrapped_line + " " * body_padding + "│")

    return lines
