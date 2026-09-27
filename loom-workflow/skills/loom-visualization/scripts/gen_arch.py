# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Layered-architecture diagram generator.

render_arch stacks one INDEPENDENT box per layer, vertically, with no
connector arrows between them. Each box is:

    ┌────────────────────────────────────┐   top border
    │            Presentation            │   centered layer name
    ├──────────┬────────────┬────────────┤   separator (┬ per cell seam)
    │ Web App  │ Mobile App │ Desktop    │   component-cell row
    └──────────┴────────────┴────────────┘   bottom border (┴ per seam)

All layer boxes share ONE outer interior width = max over all layers of
(that layer's natural component-row width, and the layer-name display
width). The component seams use ├ … ┬ … ┤ / └ … ┴ … ┘ junctions so the
vertical column seams are legitimate (keeps align.py's kink check happy).

Widths are measured in terminal cells via display_width, so CJK (2 cells)
and ASCII (1 cell) labels align in a monospace terminal.
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


def _cell_width(label: str) -> int:
    """Display width of a (possibly multi-line) cell: one pad space each
    side of the WIDEST physical line + that widest line."""
    return max(display_width(ln) for ln in split_lines(label)) + 2


def _cell_height(label: str) -> int:
    """Number of physical lines in a (possibly multi-line) cell."""
    return len(split_lines(label))


def _row_natural_width(components: list[str]) -> int:
    """Interior display width of a component row with no extra slack.

    Each cell is sized to its widest physical line + 2 pad cells; adjacent
    cells are joined by a single `│` seam, so N cells contribute (N - 1)
    seam columns.
    """
    cells_width = sum(_cell_width(c) for c in components)
    seams = max(len(components) - 1, 0)
    return cells_width + seams


def render_arch(layers: list[dict], width: Optional[int] = None) -> str:
    """Render layers as vertically-stacked independent boxes.

    `layers` is a list of dicts. Each dict has:
    - "components": [str, ...] (list of component strings, unchanged)
    - "name": either a string (current behavior: centered) or a dict with
      "title" (str) and "body" (list of str) for structured nodes

    For string name: current behavior (centered label)
    For dict name:
      - Title line is left-aligned
      - Followed by a separator row "├─────┤"
      - Followed by left-aligned body lines (one leading space + content)
      - Body lines are wrapped at the interior width
      - Empty body raises ValueError

    Returns the multi-line diagram as a single string (no trailing newline).
    """
    if not layers:
        return ""

    # Set budget: use provided width or default 40
    budget = width if width is not None else 40

    def _name_width(name: Union[str, dict]) -> int:
        if isinstance(name, str):
            return max(display_width(ln) for ln in split_lines(name))
        else:  # dict with title and body
            return display_width(name["title"])

    def _body_width(name: Union[str, dict]) -> int:
        if isinstance(name, str):
            return 0
        else:  # dict with title and body
            if not name["body"]:
                return 0
            return max(display_width(ln) for ln in name["body"])

    # Shared outer interior width = max over all layers of:
    # max(display_width(name), min(_row_natural_width(component), budget))
    def get_layer_width(layer: dict) -> int:
        name_width = _name_width(layer["name"])
        # For dict name, apply budget to body width; for string name, body width is 0
        body_width = _body_width(layer["name"])
        bounded_body_width = min(body_width, budget) if layer["name"] and isinstance(layer["name"], dict) else 0
        # For dict name, the effective name width is max(title width, bounded body width)
        if isinstance(layer["name"], dict):
            effective_name_width = max(name_width, bounded_body_width)
        else:
            effective_name_width = name_width
        component_width = _row_natural_width(layer["components"])
        return max(effective_name_width, component_width)

    interior = max(
        get_layer_width(layer) for layer in layers
    )

    lines: list[str] = []
    for layer in layers:
        components = layer["components"]

        # Distribute the difference between this layer's natural row width and
        # the shared interior EVENLY across the cells: each cell gets a `base`
        # number of extra spaces, and the integer `remainder` is spread one
        # cell at a time so the per-cell widths differ by at most one. The
        # leftover (the remainder) lands on the trailing cells — keeping the
        # last cell as the tie-break sink, deterministic for a given input.
        # This replaces dumping all slack on the last cell, which left skinny
        # cells beside one bloated tail.
        #
        # We compute each cell's final DISPLAY WIDTH (not its rendered text):
        # a cell may be multi-line, so a single padded string can't represent
        # it. The widths drive both the per-row line rendering and the seam
        # placement, which stay constant across every physical row line.
        if components:
            slack = interior - _row_natural_width(components)
            base, remainder = divmod(slack, len(components))
            n = len(components)
            cell_widths = [
                _cell_width(c) + base + (1 if i >= n - remainder else 0)
                for i, c in enumerate(components)
            ]
            # Row height = the tallest cell's physical line count; all cells
            # TOP-align into this many rows (blank-padded below).
            row_height = max(_cell_height(c) for c in components)
        else:
            # Degenerate empty-row case: one empty cell padded to interior.
            components = [""]
            cell_widths = [interior]
            row_height = 1

        # Pre-split each cell into top-aligned physical lines, each padded
        # (one pad space + line + filler) to its cell width.
        def _pad_line(line: str, width: int) -> str:
            # interior width = width; one leading pad space, label, then
            # trailing spaces to fill. Mirrors the old ` label ` + slack.
            return " " + line + " " * (width - display_width(line) - 1)

        cell_line_grids = []
        for comp, width in zip(components, cell_widths):
            phys = split_lines(comp)
            padded = [_pad_line(ln, width) for ln in phys]
            blank = " " * width
            padded += [blank] * (row_height - len(padded))
            cell_line_grids.append(padded)

        # Top border + bottom border: ─ across the whole interior, with ┬
        # / ┴ junctions at each inter-cell seam so the column seams are
        # legitimate corners. Seam columns derive from cell WIDTHS, constant
        # across every physical row line.
        seam_cols = []
        col = 0
        for width in cell_widths[:-1]:
            col += width
            seam_cols.append(col)
            col += 1  # the seam character itself

        def border(left: str, junction: str, right: str) -> str:
            chars = ["─"] * interior
            for sc in seam_cols:
                chars[sc] = junction
            return left + "".join(chars) + right

        top = "┌" + "─" * interior + "┐"
        name = layer["name"]
        if isinstance(name, str):
            # String name: if contains \n, treat as structured node (first line
            # title, remaining lines body); otherwise centered label.
            if '\n' in name:
                lines_split = split_lines(name)
                title = lines_split[0]
                body = lines_split[1:]
                if not body:
                    raise ValueError("Body cannot be empty for structured node from string with \\n")

                # Add title line (left-aligned)
                name_lines = [
                    "│ " + title + " " * (interior - display_width(title) - 1) + "│"
                ]

                # Add separator line
                name_lines.append("├" + "─" * interior + "┤")

                # Add body lines (left-aligned, wrapped at interior - 1)
                for body_line in body:
                    wrapped_lines = wrap_label(body_line, interior - 1)
                    for wrapped_line in wrapped_lines:
                        name_lines.append("│ " + wrapped_line + " " * (interior - display_width(wrapped_line) - 1) + "│")
            else:
                # String name without \n: current behavior (centered)
                name_lines = [
                    "│" + _center(nl, interior) + "│"
                    for nl in split_lines(name)
                ]
        else:
            # Dict name: structured node with title and body
            title = name["title"]
            body = name["body"]

            # Validate body is not empty
            if not body:
                raise ValueError("Body cannot be empty for structured node")

            # Add title line (left-aligned)
            name_lines = [
                "│ " + title + " " * (interior - display_width(title) - 1) + "│"
            ]

            # Add separator line
            name_lines.append("├" + "─" * interior + "┤")

            # Add body lines (left-aligned, wrapped at interior - 1)
            for body_line in body:
                # Wrap the body line at interior - 1 (true content budget)
                wrapped_lines = wrap_label(body_line, interior - 1)
                for wrapped_line in wrapped_lines:
                    # Each wrapped line gets one leading space, then content, then padded to interior
                    name_lines.append("│ " + wrapped_line + " " * (interior - display_width(wrapped_line) - 1) + "│")

        separator = border("├", "┬", "┤")
        row_lines = [
            "│" + "│".join(grid[r] for grid in cell_line_grids) + "│"
            for r in range(row_height)
        ]
        bottom = border("└", "┴", "┘")

        lines.append(top)
        lines.extend(name_lines)
        lines.append(separator)
        lines.extend(row_lines)
        lines.append(bottom)

    return "\n".join(lines)