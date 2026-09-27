# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Node-structure checks for ASCII/Unicode boxed diagrams.

Checks that every box follows the structured format:
  ┌──────┐
  │title │
  ├──────┤
  │* item│
  │* item│
  └──────┘

Flags exactly two deviations:
  a. Unstructured multi-line box: two or more content lines in title part without separator
  b. Empty-separator padding: separator immediately followed by bottom border
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from glyphs import BOX_BORDER, CORNERS, TEES
from width import display_width


def _is_top_border(line: str) -> bool:
    """True if line is a box top border (┌─┐ / ┏━┓ / ╔═╗ etc.)."""
    stripped = line.strip()
    return (
        len(stripped) >= 2
        and stripped[0] in CORNERS
        and stripped[-1] in CORNERS
        and all(c in BOX_BORDER for c in stripped[1:-1])
    )


def _is_bottom_border(line: str) -> bool:
    """True if line is a box bottom border (└─┘ / ┗━┛ / ╚═╝ etc.)."""
    stripped = line.strip()
    return (
        len(stripped) >= 2
        and stripped[0] in CORNERS
        and stripped[-1] in CORNERS
        and all(c in BOX_BORDER for c in stripped[1:-1])
    )


def _is_separator(line: str) -> bool:
    """True if line is a box separator row (├───┤ / ┣━┫ / ╠═╣ etc.)."""
    stripped = line.strip()
    return (
        len(stripped) >= 2
        and stripped[0] in TEES
        and stripped[-1] in TEES
        and all(c in BOX_BORDER for c in stripped[1:-1])
    )


def _is_content_line(line: str) -> bool:
    """True if line is a box content line (│ text │), ignoring blank lines."""
    stripped = line.strip()
    return (
        len(stripped) >= 2
        and stripped[0] == '│'
        and stripped[-1] == '│'
        and any(c != ' ' for c in stripped[1:-1])  # non-blank content
    )


def _is_blank_interior(line: str) -> bool:
    """True if line is a blank interior (│      │)."""
    stripped = line.strip()
    return (
        len(stripped) >= 2
        and stripped[0] == '│'
        and stripped[-1] == '│'
        and all(c == ' ' for c in stripped[1:-1])
    )


def find_issues(lines: list[str]) -> list[tuple[int, int, str]]:
    """Find node-structure deviations in ASCII/Unicode diagrams.

    Returns list of (1-based line number, display-column, message) tuples.
    """
    issues = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # Look for top border of a box
        if _is_top_border(line):
            # Find the matching bottom border
            top_left_col, top_right_col = _get_frame_columns(line)
            j = i + 1

            # Scan downward for bottom border with matching frame
            while j < n:
                if _is_bottom_border(lines[j]):
                    bot_left_col, bot_right_col = _get_frame_columns(lines[j])
                    if bot_left_col == top_left_col and bot_right_col == top_right_col:
                        # Found matching box: [i] top border to [j] bottom border
                        box_top, box_bottom = i, j

                        # Check box interior for deviations
                        issues.extend(_check_box_interior(lines, box_top, box_bottom))
                        i = j + 1  # Continue after the box
                        break
                elif _is_top_border(lines[j]):
                    # Found another top border before bottom border - malformed, but not our concern
                    break
                j += 1
            else:
                # No matching bottom border found - not our concern
                i += 1
        else:
            i += 1

    return issues


def _get_frame_columns(line: str) -> tuple[int, int]:
    """Return (left, right) display-columns of the line's frame glyphs."""
    if not line:
        return (0, 0)

    # Find left frame column
    left_col = 0
    for ch in line:
        if ch in BOX_BORDER:
            left_col = display_width(line[:line.index(ch)])
            break

    # Find right frame column
    right_col = 0
    for ch in reversed(line):
        if ch in BOX_BORDER:
            right_col = display_width(line[:len(line) - line[::-1].index(ch)])
            break

    return (left_col, right_col)


def _check_box_interior(lines: list[str], box_top: int, box_bottom: int) -> list[tuple[int, int, str]]:
    """Check the interior of a box for node-structure deviations.
    """
    issues = []

    has_seen_separator = False
    seen_content_in_title = False
    prev_line_was_separator = False

    for line_idx in range(box_top + 1, box_bottom):
        line = lines[line_idx]

        if _is_separator(line):
            # Defect 1: separator as first interior line (no title content before it)
            if not has_seen_separator and not seen_content_in_title:
                issues.append((
                    line_idx + 1,
                    _get_display_col_of_separator(line),
                    "separator row with no content line before it (missing title)"
                ))

            # Defect 2: two consecutive separators (no content between them)
            if prev_line_was_separator:
                issues.append((
                    line_idx + 1,
                    _get_display_col_of_separator(line),
                    "separator row with no content line after it before box's bottom border"
                ))

            has_seen_separator = True
            prev_line_was_separator = True

            # Check if this separator is immediately followed by bottom border (no content after)
            # Find next content line or bottom border
            found_content_after = False
            for k in range(line_idx + 1, box_bottom):
                if _is_content_line(lines[k]):
                    found_content_after = True
                    break
                elif _is_bottom_border(lines[k]):
                    break

            if not found_content_after:
                issues.append((
                    line_idx + 1,
                    _get_display_col_of_separator(line),
                    "separator row with no content line after it before box's bottom border"
                ))

        elif _is_content_line(line):
            prev_line_was_separator = False
            if not has_seen_separator:
                # We are in the Title part. Only ONE content line allowed.
                if seen_content_in_title:
                    issues.append((
                        line_idx + 1,
                        _get_display_col_of_content(line),
                        "box interior with two or more content lines in title part and no separator row between them"
                    ))
                seen_content_in_title = True
            else:
                # We are in the Body part. Multiple lines allowed.
                pass

        elif _is_blank_interior(line):
            prev_line_was_separator = False
            pass

    return issues


def _get_display_col_of_content(line: str) -> int:
    """Get display-column of first non-space character in content line."""
    stripped = line.lstrip()
    if not stripped or stripped[0] != '│':
        return 0
    # Find first non-space after the left border
    content_start = len(line) - len(stripped) + 1  # after '│'
    return display_width(line[:content_start])


def _get_display_col_of_separator(line: str) -> int:
    """Get display-column of first non-space character in separator line."""
    stripped = line.lstrip()
    if not stripped:
        return 0
    # Find first non-space after left border
    content_start = len(line) - len(stripped)
    return display_width(line[:content_start])