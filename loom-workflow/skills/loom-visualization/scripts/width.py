# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Shared display-width primitive for terminal-cell measurement.

Width policy, derived from the interpreter's Unicode database (unicodedata):
  - Control (Cc), combining marks (Mn, Me), format (Cf) -> 0 cells
  - East Asian Width Wide (W) / Fullwidth (F)          -> 2 cells
  - Everything else (ASCII, Ambiguous, box-drawing)    -> 1 cell

Standard library only. This agrees with terminal widths on CJK ideographs,
kana, CJK punctuation and box-drawing glyphs; it can differ on some symbols
and emoji, so keep those out of box labels.
"""

import unicodedata

_ZERO_WIDTH_CATEGORIES = frozenset(("Cc", "Mn", "Me", "Cf"))
_WIDE = frozenset(("W", "F"))


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
    """
    return label.splitlines() or [""]
