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

from width import char_width, display_width, split_lines, center, wrap_label, EMPTY_BODY, EMPTY_BODY_FROM_STRING, render_structured_node


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

    # A non-empty str body draws as its lines, exactly as the list form would
    # (str.splitlines, not split_lines: a control char draws, never raises);
    # '' keeps the empty-body error.
    steps = [
        {**s, "body": s["body"].splitlines()}
        if isinstance(s, dict) and isinstance(s.get("body"), str) and s["body"] else s
        for s in steps
    ]

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

    # A body line that would sit flush is wrapped at interior - 2, so the
    # interior must hold the widest body character plus the leading space and
    # one right pad. A body of only empty or space-only lines has no floor, so
    # an interior of 2 keeps trunk output. The +2 below already covers the title.
    def body_char_floor(step: Union[str, dict]) -> int:
        if isinstance(step, dict):
            body = step["body"]
        elif '\n' in step:
            body = split_lines(step)[1:]
        else:
            return 0
        widest_char = max((char_width(c) for ln in body for c in ln if c != " "), default=0)
        return widest_char + 2 if widest_char > 0 else 0

    interior = max(
        max(get_step_width(step) + 2, body_char_floor(step)) for step in steps
    )

    # Trunk column = the box's center display-column. Boxes start at
    # column 0; the left border "│" occupies column 0, interior starts
    # at column 1, so the interior center is at 1 + interior // 2.
    trunk_col = 1 + interior // 2
    trunk_pad = " " * trunk_col

    # The shared renderer wraps at interior - 1, which lets a line fill the
    # interior flush against the right border. Only a line that would do so is
    # pre-wrapped at interior - 2, keeping one space of right padding; every
    # other line keeps the shared renderer's breaks (wrapping all lines at
    # interior - 2 moves word/script-boundary breaks in unaffected bodies).
    # An interior of 2 has no room (wrap width 0) and keeps trunk output.
    def pad_body(body: list[str]) -> list[str]:
        if interior - 2 < 1:
            return body
        out = []
        for line in body:
            pieces = wrap_label(line, interior - 1)
            if any(display_width(p) == interior - 1 and not p.endswith(" ") for p in pieces):
                pieces = wrap_label(line, interior - 2)
            out.extend(pieces)
        return out

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
                    raise ValueError(EMPTY_BODY_FROM_STRING)

                block.extend(render_structured_node(title, pad_body(body), interior))
            else:
                # Regular string step: centered label, supports \n for multi-line
                for line in split_lines(step):
                    block.append("│" + center(line, interior) + "│")
        else:
            # Dict step: structured node with title and body
            title = step["title"]
            body = step["body"]

            # Validate body is not empty
            if not body:
                raise ValueError(EMPTY_BODY)

            block.extend(render_structured_node(title, pad_body(body), interior))

        block.append(bottom)
        blocks.append(block)

    lines: list[str] = []
    for i, block in enumerate(blocks):
        lines.extend(block)
        if i != len(blocks) - 1:
            lines.append(trunk_pad + "│")
            lines.append(trunk_pad + "▼")

    return "\n".join(lines)