# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Linear flow-diagram generator.

render_flow stacks labelled boxes vertically on a common trunk column,
joined by a centered down-arrow:

    ┌──────────┐
    │  収到訂單  │
    └──────────┘
         │
         ▼
    ┌──────────┐
    │ 驗證ユーザー │
    └──────────┘
         ...

All boxes share one interior width (= max label display width), so the
borders line up vertically and the trunk (│ / ▼) sits at one constant
display-column. Widths are measured in terminal cells via
display_width, so CJK (2 cells) and ASCII (1 cell) labels align.
"""

import pathlib
import sys
from typing import Union, Optional

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from width import display_width, split_lines, wrap_label


def _center(label: str, interior: int) -> str:
    """Pad label to `interior` display cells, label roughly centered.

    Padding is computed in display cells (not characters) so CJK labels
    are not over-padded. Extra odd cell goes to the right.
    """
    slack = interior - display_width(label)
    left = slack // 2
    right = slack - left
    return " " * left + label + " " * right


def render_flow(steps: list[Union[str, dict]], width: Optional[int] = None) -> str:
    """Render steps as vertically-stacked boxes joined by a down-arrow.

    Each step can be either:
    - A string (if contains no \n: centered label; if contains \n: treated as structured node with first line as title, remaining lines as body)
    - A dict with "title" (str) and "body" (list of str) for structured nodes
      - Title line is left-aligned
      - Followed by a separator row "├─────┤"
      - Followed by left-aligned body lines (one leading space + content)
      - Body lines are wrapped at the interior width
      - Empty body raises ValueError

    Each box interior is one space + label + one space, with all boxes
    sized to the widest label so the trunk is straight. Returns the
    multi-line diagram as a single string (no trailing newline).
    """
    if not steps:
        return ""

    # Set budget: use provided width or default 40
    budget = width if width is not None else 40

    # Interior width = max over steps of max(display_width(title), min(natural_body_width, budget)) + 2
    def get_step_width(step: Union[str, dict]) -> int:
        if isinstance(step, str):
            # For string steps, if it contains \n, treat as structured node
            if '\n' in step:
                lines = split_lines(step)
                if lines:
                    title_width = display_width(lines[0])
                    # For body lines, we need the max width of unwrapped body lines
                    if len(lines) > 1:
                        natural_body_width = max(display_width(line) for line in lines[1:])
                    else:
                        natural_body_width = 0
                else:
                    title_width = 0
                    natural_body_width = 0
                return max(title_width, min(natural_body_width, budget))
            else:
                # For string steps without \n, consider all lines from split_lines
                return max(display_width(line) for line in split_lines(step))
        else:  # dict with title and body
            title_width = display_width(step["title"])
            # Calculate natural body width (unwrapped)
            if step["body"]:
                natural_body_width = max(display_width(line) for line in step["body"])
            else:
                natural_body_width = 0  # Will be caught by empty body validation later
            return max(title_width, min(natural_body_width, budget))

    interior = max(
        get_step_width(step) for step in steps
    ) + 2

    # Trunk column = the box's center display-column. Boxes start at
    # column 0; the left border "│" occupies column 0, interior starts
    # at column 1, so the interior center is at 1 + interior // 2.
    trunk_col = 1 + interior // 2
    trunk_pad = " " * trunk_col

    top = "┌" + "─" * interior + "┐"
    bottom = "└" + "─" * interior + "┘"

    blocks = []
    for step in steps:
        block = [top]
        if isinstance(step, str):
            # String step: check if it contains \n to treat as structured node
            if '\n' in step:
                # Treat as structured node: first line as title, remaining lines as body
                lines = split_lines(step)
                if not lines:
                    # Empty string case
                    title = ""
                    body = []
                else:
                    title = lines[0]
                    body = lines[1:]

                # Validate body is not empty
                if not body:
                    raise ValueError("Body cannot be empty for structured node from string with \\n")

                # Add title line (left-aligned)
                block.append("│ " + title + " " * (interior - display_width(title) - 1) + "│")

                # Add separator line
                block.append("├" + "─" * interior + "┤")

                # Add body lines (left-aligned, wrapped at interior - 1)
                for body_line in body:
                    # Wrap the body line at interior - 1 (true content budget)
                    wrapped_lines = wrap_label(body_line, interior - 1)
                    for wrapped_line in wrapped_lines:
                        # Each wrapped line gets one leading space, then content, then padded to interior
                        block.append("│ " + wrapped_line + " " * (interior - display_width(wrapped_line) - 1) + "│")
            else:
                # Regular string step: centered label, supports \n for multi-line
                for line in split_lines(step):
                    block.append("│" + _center(line, interior) + "│")
        else:
            # Dict step: structured node with title and body
            title = step["title"]
            body = step["body"]

            # Validate body is not empty
            if not body:
                raise ValueError("Body cannot be empty for structured node")

            # Add title line (left-aligned)
            block.append("│ " + title + " " * (interior - display_width(title) - 1) + "│")

            # Add separator line
            block.append("├" + "─" * interior + "┤")

            # Add body lines (left-aligned, wrapped at interior - 1)
            for body_line in body:
                # Wrap the body line at interior - 1 (true content budget)
                wrapped_lines = wrap_label(body_line, interior - 1)
                for wrapped_line in wrapped_lines:
                    # Each wrapped line gets one leading space, then content, then padded to interior
                    block.append("│ " + wrapped_line + " " * (interior - display_width(wrapped_line) - 1) + "│")

        block.append(bottom)
        blocks.append(block)

    lines: list[str] = []
    for i, block in enumerate(blocks):
        lines.extend(block)
        if i != len(blocks) - 1:
            lines.append(trunk_pad + "│")
            lines.append(trunk_pad + "▼")

    return "\n".join(lines)