# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Classic Unicode tree / hierarchy renderer.

A node is a dict {"label": str | dict, "children": [node, ...]} (children
optional / empty). The root label sits on line 1; each descendant is
prefixed with branch glyphs that precede the label, so CJK labels do
not affect the branch columns:

    訂單系統
    ├─ 訂單服務
    └─ 庫存サービス
       └─ 預扣

Label can be:
- A plain string (current behavior): each \\n-separated line is a
  continuation line under the branch glyphs.
- A structured dict {"title": str, "body": [str, ...]}:
    - Title renders on the connector line.
    - Each body item renders as a bulleted continuation line
      "* item" on the following lines, indented to align under the
      title's text start.
    - The tree draws NO boxes, so NO separator row.
    - Empty body raises ValueError.

Per-ancestor continuation: a non-last ancestor contributes "│  ", a
last ancestor contributes "   " (three spaces). The connector for a
node itself is "├─ " unless it is its parent's last child, then "└─ ".
"""

from width import split_lines

_TEE = "├─ "
_ELBOW = "└─ "
_BAR = "│  "
_GAP = "   "


def _process_label(label: str | dict) -> list[str]:
    """Process a label (string or structured dict) into a list of physical lines.

    For string labels: uses split_lines (current behavior).
    For structured dict labels: returns [title] + body lines (each body item
    may itself contain \\n, which split_lines turns into continuation lines).
    Raises ValueError for empty body in structured nodes.
    """
    if isinstance(label, str):
        return split_lines(label)

    # Structured node: {"title": str, "body": [str, ...]}
    if not isinstance(label, dict):
        raise TypeError(f"label must be str or dict, got {type(label).__name__}")

    title = label.get("title", "")
    body = label.get("body", [])

    if not body:
        raise ValueError("Body cannot be empty for structured node")

    lines = [title]
    for item in body:
        lines.extend(split_lines(item))

    return lines


def render_tree(node: dict) -> str:
    """Render a node and its descendants as a multi-line tree string."""
    label_lines = _process_label(node["label"])
    lines = [label_lines[0]]  # root title line (no connector prefix)
    for cont in label_lines[1:]:
        lines.append(cont)  # root body continuation lines (no branch prefix)
    _render_children(node.get("children") or [], prefix="", lines=lines)
    return "\n".join(lines)


def _render_children(children: list, prefix: str, lines: list) -> None:
    last = len(children) - 1
    for i, child in enumerate(children):
        is_last = i == last
        connector = _ELBOW if is_last else _TEE
        continuation = _GAP if is_last else _BAR
        label_lines = _process_label(child["label"])

        # First line: connector + title
        lines.append(prefix + connector + label_lines[0])
        # Body continuation lines: continuation prefix + body item
        for cont in label_lines[1:]:
            lines.append(prefix + continuation + cont)

        _render_children(
            child.get("children") or [],
            prefix=prefix + continuation,
            lines=lines,
        )