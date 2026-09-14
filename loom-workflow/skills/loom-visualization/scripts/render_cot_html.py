#!/usr/bin/env python3
"""Render a loom-visualization markdown artifact to standalone HTML.

Usage:
  python3 scripts/render_cot_html.py <report.md> [-o <out.html>] [--artifact]

The `.md` is the artifact; this HTML is derived from it. Never hand-edit
the HTML, and never let the two disagree.

**The conversion adds and removes nothing.** Headings, paragraphs, lists
and tables come out in the order and nesting the markdown put them in;
the card look and the conclusion callout are CSS applied where things
already stand. There is exactly one content transformation and it is
unavoidable: a ```mermaid fence becomes `<pre class="mermaid">` with its
body un-escaped, because mermaid node labels are raw HTML and would
otherwise reach the browser as literal text.

`--artifact` emits the Artifact build: no <!doctype>/<html>/<head>/<body>
wrapper and no mermaid CDN script, because Artifacts render
<pre class="mermaid"> natively and supply their own skeleton.

Markdown is parsed by a **standard-library** CommonMark subset (below):
the skill must run on plain Python with no third-party packages. It
reproduces the output of markdown-it-py, which this script used to
depend on, and the script test suite is the equivalence oracle. An
earlier hand-rolled converter failed its own test suite within the hour:
an unsupported `##` heading passed through unconverted *and* slipped past
the leftover check, because the check only matched line-start markdown
while the stray text had already been wrapped in `<p>`. That is why the
leftover check stays scoped to block tags and remains the backstop.
Beyond parsing, the parts worth writing here are the pipeline properties
below.

Three of those, taken from a brief about a renderer of this exact kind
that failed silently five times in five days:

  * **Fail loud, write nothing.** If markdown survives into the output the
    run exits non-zero AND no file is written. A run that fails but still
    writes leaves exactly the deliverable the check exists to stop.
  * **The check is scoped.** Mermaid blocks and <code> spans legitimately
    contain `|`, `**` and `#`. An unscoped check condemns every correct page.
  * **The output is stamped.** Every page carries the version of the copy
    that actually ran, so a page rendered by a stale copy is identifiable
    and a page with no stamp came from a pre-stamp copy. An unreadable
    manifest stamps the literal `unknown` rather than faking a version.
"""
import argparse
import hashlib
import html
import json
import re
import sys
import unicodedata
from html.entities import html5
from pathlib import Path
from urllib.parse import quote, unquote

CSS = """
:root {
  --bg: #ffffff; --fg: #1a1c1e; --muted: #5c636a; --rule: #e3e5e8;
  --card: #f8f9fa; --accent: #0c8599;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC",
          "Hiragino Sans", "Yu Gothic", sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #16181a; --fg: #e6e8ea; --muted: #9aa1a8;
    --rule: #2c3034; --card: #1e2124; --accent: #3bc9db;
  }
}
:root[data-theme="dark"] {
  --bg: #16181a; --fg: #e6e8ea; --muted: #9aa1a8;
  --rule: #2c3034; --card: #1e2124; --accent: #3bc9db;
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 2.5rem 1.25rem 5rem; background: var(--bg);
  color: var(--fg); font-family: var(--font); line-height: 1.75; font-size: 16px;
}
main { max-width: 52rem; margin: 0 auto; }
h1 { font-size: 1.75rem; line-height: 1.35; margin: 0 0 .75rem; }
/* The markdown uses the vault's heading levels: ### page section,
   #### arc, ##### node. The renderer maps those to h3/h4/h5 — do not
   "fix" these selectors to h2/h3/h4 without changing the template too. */
h3 { font-size: 1.15rem; margin: 3rem 0 1rem; padding-bottom: .4rem;
     border-bottom: 2px solid var(--rule); }
h4 { font-size: 1.05rem; margin: 2.25rem 0 .75rem; color: var(--accent); }
h5 { font-size: 1rem; margin: 1.5rem 0 .4rem; }
p { margin: 0 0 1rem; }
.meta { color: var(--muted); font-size: .85rem; margin-bottom: 2rem; }
.meta a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
.meta strong { color: #c92a2a; font-weight: 600; }
@media (prefers-color-scheme: dark) { .meta strong { color: #ff8787; } }
pre.mermaid { overflow-x: auto; background: #ffffff; border: 1px solid var(--rule);
              border-radius: 8px; padding: 1.25rem; margin: 1rem 0; }
/* Presentation only. Nothing below moves, adds, or removes content — the
   HTML's structure is the markdown's structure, so the two can be read
   against each other with no translation step.
   A node card is an h5 plus the list after it, styled where it stands. */
h5 + ul { border: 1px solid var(--rule); border-radius: 8px;
          padding: .85rem 1.25rem .85rem 2.4rem; margin: 0 0 .85rem;
          background: var(--card); list-style: disc; }
h5 { margin-bottom: .35rem; }
/* The first section's first paragraph is the one-line conclusion, styled
   in place. An earlier version lifted it to the top and deleted its
   heading — deterministic, so it looked mechanical, but it left the two
   files disagreeing about what the document contains. */
h3:first-of-type + p { font-size: 1.1rem; background: var(--card);
        border-left: 4px solid var(--accent); padding: 1rem 1.25rem;
        border-radius: 0 6px 6px 0; margin-bottom: 1.5rem; }
blockquote { margin: 0 0 1.25rem; padding: .6rem 1rem; border-left: 3px solid var(--muted);
  background: transparent; color: var(--fg); font-size: .95rem; }
blockquote p { margin: 0 0 .4rem; }
blockquote p:last-child { margin: 0; }
ul { margin: 0 0 1rem; padding-left: 1.3rem; }
li { margin-bottom: .35rem; }
table { border-collapse: collapse; width: 100%; margin: 0 0 1rem; font-size: .95rem; }
th, td { border: 1px solid var(--rule); padding: .5rem .75rem; text-align: left;
         vertical-align: top; }
th { background: var(--card); font-weight: 600; }
footer { margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--rule);
         color: var(--muted); font-size: .85rem; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
       font-size: .9em; background: var(--card); padding: .1em .35em;
       border-radius: 3px; }
""".strip()

MERMAID_CDN = """<script type="module">
  // Pinned to a release with mermaid's DOCUMENTED subgraph behaviour.
  // The pin was 11.16.0, which is the one short-lived line that honoured a
  // subgraph `direction` even when a node edge left the subgraph — the
  // layout depended on that, so the page silently required the anomaly and
  // every other renderer showed a collapsed diagram. The layout no longer
  // depends on it (rows are joined subgraph-to-subgraph), so pinning to
  // the outlier is now a liability rather than a crutch: the 11.16.x line
  // (11.16.0 and 11.16.1) is where a regression in the row-joining rule
  // would stay invisible, because it is the only line that tolerates the
  // broken form.
  //
  // Grounded, not asserted. The behaviour split was measured by rendering
  // both cross-row forms on each line and comparing node coordinates and
  // PNG bytes; the table and the method are in
  // references/mermaid-cot-spec.md's appendix, and the narrative is in
  // references/why-these-rules.md. "Latest" claims came from
  // `npm view mermaid version` / `npm view @mermaid-js/mermaid-cli version`
  // on 2026-08-19. Re-probe before moving this pin: an inherited fact about
  // an external tool is a claim with a version attached, which is the
  // mistake that produced the pin being replaced here.
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.17.0/dist/mermaid.esm.min.mjs';
  // 'antiscript', not 'loose': node labels are raw HTML by design (the
  // left-align <div>), so 'strict' would render them as literal text.
  // This is defence in depth over what mermaid itself renders, and NOT
  // the control that keeps script out of the page — the browser parses
  // <pre> content as markup before mermaid ever runs, so anything the
  // converter emits raw is live regardless of this setting. The control
  // is unescape_label_markup()'s allow-list, upstream, where the fence
  // body is turned back into markup in the first place.
  mermaid.initialize({ startOnLoad: true, theme: 'default', securityLevel: 'antiscript' });
</script>"""

# Matches ONE mermaid fence's open tag, body and close tag together, so the
# close tag of a non-mermaid fence is never rewritten. DOTALL because a
# diagram spans lines. Non-greedy so two diagrams do not merge into one.
MERMAID_FENCE = re.compile(
    r'<pre><code class="language-mermaid">(.*?)</code></pre>', re.S
)

# ------------------------------------------------------------------------
# Markdown → HTML, standard library only.
#
# A CommonMark subset plus GFM pipe tables, written to emit byte-for-byte
# what markdown-it-py ("commonmark" preset, html: False, table rule) emitted
# for the constructs a report uses: ATX and setext headings, paragraphs,
# emphasis and strong, inline code, links, images and autolinks, ordered
# and unordered lists (tight and loose, nested), block quotes, thematic
# breaks, fenced and indented code, and pipe tables. Raw HTML is never
# passed through — every `<` in text is escaped, which is what html: False
# meant. Not covered: reference-style links, raw HTML blocks, tab stops
# inside indentation. The page script suite in loom-workflow/tests/ is the
# equivalence oracle; the leftover check below is the backstop for anything
# missed.

_ASCII_PUNCT = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
_URL_SAFE = set(";/?:@&=+$,-_.!~*'()#"
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
_ESCAPABLE = re.compile(
    r"\\([!-/:-@\[-`{-~])"
    r"|(&(?:#[0-9]{1,7}|#[xX][0-9a-fA-F]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});)"
)
_ENTITY = re.compile(r"&(?:#[0-9]{1,7}|#[xX][0-9a-fA-F]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});")
_AUTOLINK = re.compile(r"<([A-Za-z][A-Za-z0-9+.\-]{1,31}:[^<>\x00-\x20]*)>")
_EMAIL = re.compile(
    r"<([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)>"
)
_BAD_PROTO = re.compile(r"^(vbscript|javascript|file|data):")
_GOOD_DATA = re.compile(r"^data:image/(gif|png|jpeg|webp);")

_FENCE_OPEN = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
_ATX = re.compile(r"^ {0,3}(#{1,6})(?=[ \t]|$)(.*)$")
_HR = re.compile(r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
_QUOTE = re.compile(r"^ {0,3}>")
_ITEM = re.compile(r"^( {0,3})([-+*]|[0-9]{1,9}[.)])(?=[ \t]|$)")
_SETEXT = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
_DELIM_CELL = re.compile(r"^:?-+:?$")


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _decode_entity(tok):
    if tok[1] == "#":
        cp = int(tok[3:-1], 16) if tok[2] in "xX" else int(tok[2:-1])
        if cp == 0 or cp > 0x10FFFF or 0xD800 <= cp <= 0xDFFF:
            return "\ufffd"
        return chr(cp)
    return html5.get(tok[1:], tok)


def _unescape_md(s):
    """Backslash escapes and entity references, in one pass."""
    return _ESCAPABLE.sub(
        lambda m: m.group(1) if m.group(1) is not None else _decode_entity(m.group(2)), s
    )


def _is_punct(ch):
    return ch in _ASCII_PUNCT or unicodedata.category(ch)[0] in "PS"


def _norm_url(url):
    out = []
    i = 0
    while i < len(url):
        c = url[i]
        if c == "%" and re.match(r"[0-9a-fA-F]{2}", url[i + 1:i + 3]):
            out.append(url[i:i + 3])
            i += 3
            continue
        out.append(c if c in _URL_SAFE else quote(c, safe=""))
        i += 1
    return "".join(out)


def _link_ok(url):
    u = url.strip().lower()
    return not _BAD_PROTO.match(u) or bool(_GOOD_DATA.match(u))


def _run_len(src, i, ch):
    j = i
    while j < len(src) and src[j] == ch:
        j += 1
    return j - i


def _code_close(src, start, k):
    """Index of a backtick run of exactly `k` at or after `start`, or None."""
    j = start
    while True:
        j = src.find("`", j)
        if j < 0:
            return None
        r = _run_len(src, j, "`")
        if r == k:
            return j
        j += r


def _skip_ws(src, i, newlines=False):
    while i < len(src) and (src[i] in " \t" or (newlines and src[i] == "\n")):
        i += 1
    return i


def _link_tail(src, i):
    """Parse `(dest "title")` starting at src[i]; (dest, title, end) or None."""
    n = len(src)
    if i >= n or src[i] != "(":
        return None
    k = _skip_ws(src, i + 1, newlines=True)
    if k >= n:
        return None
    dest = ""
    if src[k] == "<":
        j = k + 1
        while j < n and src[j] not in "\n<>":
            j += 2 if src[j] == "\\" and j + 1 < n else 1
        if j >= n or src[j] != ">":
            return None
        dest, k = _unescape_md(src[k + 1:j]), j + 1
    else:
        start, level = k, 0
        while k < n:
            c = src[k]
            if c == " " or ord(c) < 0x20 or ord(c) == 0x7F:
                break
            if c == "\\" and k + 1 < n:
                if src[k + 1] == " ":
                    break
                k += 2
                continue
            if c == "(":
                level += 1
                if level > 32:
                    return None
            elif c == ")":
                if level == 0:
                    break
                level -= 1
            k += 1
        if level:
            return None
        dest = _unescape_md(src[start:k])
    if dest and not _link_ok(_norm_url(dest)):
        return None
    after = _skip_ws(src, k, newlines=True)
    title = ""
    if after < n and after != k and src[after] in "\"'(":
        close = ")" if src[after] == "(" else src[after]
        j = after + 1
        while j < n and src[j] != close:
            if src[after] == "(" and src[j] == "(":
                j = n
                break
            j += 2 if src[j] == "\\" and j + 1 < n else 1
        if j < n:
            title = _unescape_md(src[after + 1:j])
            after = _skip_ws(src, j + 1, newlines=True)
    if after < n and src[after] == ")":
        return dest, title, after + 1
    return None


def _try_link(src, i):
    """`[text](dest "title")` starting at src[i] == '['."""
    n, j, depth = len(src), i + 1, 1
    while j < n:
        c = src[j]
        if c == "\\":
            j += 2
            continue
        if c == "`":
            k = _run_len(src, j, "`")
            close = _code_close(src, j + k, k)
            j = close + k if close is not None else j + k
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        j += 1
    if j >= n:
        return None
    tail = _link_tail(src, j + 1)
    if tail is None:
        return None
    return (src[i + 1:j],) + tail


def _emphasis(nodes):
    """CommonMark's delimiter-run algorithm over the node list, in place.

    A delimiter node is ["d", char, count, original, can_open, can_close,
    open_tags, close_tags]; it renders as close_tags, the unused
    delimiters as literal text, then open_tags.
    """
    stack = [k for k, nd in enumerate(nodes) if nd[0] == "d"]
    bottom = {}
    ci = 0
    while ci < len(stack):
        cl = nodes[stack[ci]]
        if not cl[5]:
            ci += 1
            continue
        key = (cl[1], cl[4], cl[3] % 3)
        floor = bottom.get(key, -1)
        found = -1
        oi = ci - 1
        while oi >= 0 and stack[oi] > floor:
            op = nodes[stack[oi]]
            if op[1] == cl[1] and op[4]:
                odd = ((op[5] or cl[4]) and (op[3] + cl[3]) % 3 == 0
                       and not (op[3] % 3 == 0 and cl[3] % 3 == 0))
                if not odd:
                    found = oi
                    break
            oi -= 1
        if found < 0:
            bottom[key] = stack[ci - 1] if ci > 0 else -1
            if not cl[4]:
                del stack[ci]
            else:
                ci += 1
            continue
        op = nodes[stack[found]]
        use = 2 if op[2] >= 2 and cl[2] >= 2 else 1
        tag = "strong" if use == 2 else "em"
        op[2] -= use
        cl[2] -= use
        op[6].insert(0, f"<{tag}>")
        cl[7].append(f"</{tag}>")
        del stack[found + 1:ci]
        ci = found + 1
        if op[2] == 0:
            del stack[found]
            ci -= 1
        if cl[2] == 0:
            del stack[ci]


def _inline(src):
    nodes, buf = [], []
    n, i = len(src), 0

    def flush():
        if buf:
            nodes.append(["t", _esc("".join(buf))])
            buf.clear()

    def emit(markup):
        flush()
        nodes.append(["t", markup])

    while i < n:
        c = src[i]
        if c == "\\":
            if i + 1 < n and src[i + 1] == "\n":
                emit("<br />\n")
                i = _skip_ws(src, i + 2)
            elif i + 1 < n and src[i + 1] in _ASCII_PUNCT:
                buf.append(src[i + 1])
                i += 2
            else:
                buf.append(c)
                i += 1
        elif c == "`":
            k = _run_len(src, i, "`")
            close = _code_close(src, i + k, k)
            if close is None:
                buf.append("`" * k)
                i += k
                continue
            code = src[i + k:close].replace("\n", " ")
            if len(code) >= 2 and code[0] == " " and code[-1] == " " and code.strip(" "):
                code = code[1:-1]
            emit(f"<code>{_esc(code)}</code>")
            i = close + k
        elif c == "<":
            m = _AUTOLINK.match(src, i)
            e = None if m else _EMAIL.match(src, i)
            if m and _link_ok(_norm_url(m.group(1))):
                url = m.group(1)
                emit(f'<a href="{_esc(_norm_url(url))}">{_esc(unquote(url))}</a>')
                i = m.end()
            elif e:
                url = e.group(1)
                emit(f'<a href="{_esc(_norm_url("mailto:" + url))}">{_esc(url)}</a>')
                i = e.end()
            else:
                buf.append(c)
                i += 1
        elif c == "&":
            m = _ENTITY.match(src, i)
            if m:
                buf.append(_decode_entity(m.group(0)))
                i = m.end()
            else:
                buf.append(c)
                i += 1
        elif c in "![" and (c == "[" or (i + 1 < n and src[i + 1] == "[")):
            image = c == "!"
            link = _try_link(src, i + 1 if image else i)
            if link is None:
                buf.append(c)
                i += 1
                continue
            text, dest, title, end = link
            href = _esc(_norm_url(dest))
            t_attr = f' title="{_esc(title)}"' if title else ""
            if image:
                alt = re.sub(r"<[^>]*>", "", _inline(text))
                emit(f'<img src="{href}" alt="{alt}"{t_attr} />')
            else:
                emit(f'<a href="{href}"{t_attr}>{_inline(text)}</a>')
            i = end
        elif c in "*_":
            k = _run_len(src, i, c)
            before = src[i - 1] if i > 0 else " "
            after = src[i + k] if i + k < n else " "
            bw, aw = before.isspace(), after.isspace()
            bp, ap = _is_punct(before), _is_punct(after)
            left = not aw and (not ap or bw or bp)
            right = not bw and (not bp or aw or ap)
            if c == "*":
                can_open, can_close = left, right
            else:
                can_open = left and (not right or bp)
                can_close = right and (not left or ap)
            flush()
            nodes.append(["d", c, k, k, can_open, can_close, [], []])
            i += k
        elif c == "\n":
            spaces = 0
            while buf and buf[-1] == " ":
                buf.pop()
                spaces += 1
            emit("<br />\n" if spaces >= 2 else "\n")
            i = _skip_ws(src, i + 1)
        else:
            buf.append(c)
            i += 1
    flush()
    _emphasis(nodes)
    return "".join(
        nd[1] if nd[0] == "t" else "".join(nd[7]) + nd[1] * nd[2] + "".join(nd[6])
        for nd in nodes
    )


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _fence_open(line):
    m = _FENCE_OPEN.match(line)
    if m and not (m.group(2)[0] == "`" and "`" in m.group(3)):
        return m
    return None


def _split_row(line):
    s = line.strip()
    cells, cur, i = [], [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if s[i] == "|":
            cells.append("".join(cur))
            cur = []
        else:
            cur.append(s[i])
        i += 1
    cells.append("".join(cur))
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return cells


def _table_head(lines, i):
    if i + 1 >= len(lines):
        return None
    head, delim = lines[i], lines[i + 1]
    if _indent(head) >= 4 or _indent(delim) >= 4 or "|" not in head:
        return None
    d = delim.strip()
    lead = delim.lstrip(" ")
    if not d or d[0] not in "|-:" or set(d) - set("|-: \t") or len(lead) < 2:
        return None
    # `- ` opens a list item, not a delimiter row — the same ambiguity rule
    # markdown-it applies.
    if lead[0] == "-" and lead[1] in " \t":
        return None
    parts = d.split("|")
    aligns = []
    for k, part in enumerate(parts):
        t = part.strip()
        if not t:
            if k in (0, len(parts) - 1):
                continue
            return None
        if not _DELIM_CELL.match(t):
            return None
        aligns.append("center" if t[0] == ":" and t[-1] == ":"
                      else "right" if t[-1] == ":"
                      else "left" if t[0] == ":" else "")
    header = _split_row(head)
    if not header or len(header) != len(aligns):
        return None
    return header, aligns


def _starts_block(lines, j):
    """Would lines[j] interrupt a paragraph?"""
    line = lines[j]
    if _indent(line) >= 4:
        return False
    if _fence_open(line) or _ATX.match(line) or _HR.match(line) or _QUOTE.match(line):
        return True
    m = _ITEM.match(line)
    if m and line[m.end():].strip():
        marker = m.group(2)
        if marker in "-+*" or int(marker[:-1]) == 1:
            return True
    return _table_head(lines, j) is not None


def _lazy_ok(item_lines):
    """May an unindented line continue the item's last paragraph?"""
    last = item_lines[-1]
    if not last.strip() or _ATX.match(last) or _HR.match(last) or _fence_open(last):
        return False
    fences = sum(1 for ln in item_lines if _fence_open(ln) and _indent(ln) < 4)
    return fences % 2 == 0


def _table(lines, i, head):
    header, aligns = head

    def cell(tag, k, text):
        style = f' style="text-align:{aligns[k]}"' if aligns[k] else ""
        return f"<{tag}{style}>{_inline(text.strip())}</{tag}>\n"

    out = ["<table>\n<thead>\n<tr>\n"]
    out += [cell("th", k, h) for k, h in enumerate(header)]
    out.append("</tr>\n</thead>\n")
    j, rows = i + 2, []
    while j < len(lines):
        line = lines[j]
        if not line.strip() or _indent(line) >= 4 or _starts_block(lines, j):
            break
        rows.append(_split_row(line))
        j += 1
    if rows:
        out.append("<tbody>\n")
        for row in rows:
            out.append("<tr>\n")
            out += [cell("td", k, row[k] if k < len(row) else "")
                    for k in range(len(aligns))]
            out.append("</tr>\n")
        out.append("</tbody>\n")
    out.append("</table>\n")
    return "".join(out), j


def _list(lines, i):
    n = len(lines)
    first = _ITEM.match(lines[i]).group(2)
    ordered = first[-1] in ".)"
    kind = first[-1] if ordered else first
    items, loose, j = [], False, i
    while j < n:
        m = _ITEM.match(lines[j])
        if not m or _HR.match(lines[j]):
            break
        marker = m.group(2)
        if (marker[-1] if marker[-1] in ".)" else marker) != kind:
            break
        rest = lines[j][m.end():]
        spaces = _indent(rest)
        if not rest.strip():
            width, item = m.end() + 1, [""]
        elif spaces >= 5:
            width, item = m.end() + 1, [rest[1:]]
        else:
            width, item = m.end() + spaces, [rest[spaces:]]
        j += 1
        while j < n:
            line = lines[j]
            if not line.strip():
                if item == [""]:
                    break
                item.append("")
            elif _indent(line) >= width:
                item.append(line[width:])
            elif (item[-1].strip() and not _ITEM.match(line)
                  and not _starts_block(lines, j) and _lazy_ok(item)):
                item.append(line.lstrip(" "))
            else:
                break
            j += 1
        trailing = 0
        while len(item) > 1 and not item[-1].strip():
            item.pop()
            trailing += 1
        blocks, gap = _blocks(item)
        items.append(blocks)
        loose = loose or gap
        k = j
        while k < n and not lines[k].strip():
            k += 1
        nxt = _ITEM.match(lines[k]) if k < n else None
        same = (nxt and not _HR.match(lines[k])
                and (nxt.group(2)[-1] if nxt.group(2)[-1] in ".)" else nxt.group(2)) == kind)
        if same:
            loose = loose or trailing > 0 or k > j
            j = k
        else:
            j -= trailing
            break
    tag = "ol" if ordered else "ul"
    start = int(first[:-1]) if ordered else 1
    out = [f'<{tag} start="{start}">\n' if start != 1 else f"<{tag}>\n"]
    for blocks in items:
        li = "<li>"
        for k, (kind_k, payload) in enumerate(blocks):
            tight_p = kind_k == "p" and not loose
            if k == 0 and not tight_p:
                li += "\n"
            elif k > 0 and blocks[k - 1][0] == "p" and not loose:
                li += "\n"
            li += payload if tight_p else _block_html(kind_k, payload)
        out.append(li + "</li>\n")
    out.append(f"</{tag}>\n")
    return "".join(out), j


def _block_html(kind, payload):
    return f"<p>{payload}</p>\n" if kind == "p" else payload


def _blocks(lines):
    """Parse block structure: ([(kind, payload)], blank-line-between-blocks)."""
    out, gap, pending_blank = [], False, False
    n, i = len(lines), 0
    while i < n:
        line = lines[i]
        if not line.strip():
            pending_blank = bool(out)
            i += 1
            continue
        if pending_blank:
            gap = True
            pending_blank = False

        head = _table_head(lines, i)
        if head:
            html_, i = _table(lines, i, head)
            out.append(("b", html_))
            continue

        if _indent(line) >= 4:
            body, j = [], i
            while j < n and (not lines[j].strip() or _indent(lines[j]) >= 4):
                body.append(lines[j][4:] if _indent(lines[j]) >= 4 else lines[j].lstrip(" "))
                j += 1
            while body and not body[-1].strip():
                body.pop()
                j -= 1
            out.append(("b", "<pre><code>" + _esc("".join(b + "\n" for b in body))
                        + "</code></pre>\n"))
            i = j
            continue

        m = _fence_open(line)
        if m:
            indent, mark = len(m.group(1)), m.group(2)
            info = _unescape_md(m.group(3)).strip()
            closer = re.compile(r"^ {0,3}" + re.escape(mark[0]) + "{%d,}[ \t]*$" % len(mark))
            body, j = [], i + 1
            while j < n and not closer.match(lines[j]):
                body.append(lines[j][min(indent, _indent(lines[j])):])
                j += 1
            lang = info.split()[0] if info else ""
            cls = f' class="language-{_esc(lang)}"' if lang else ""
            out.append(("b", f"<pre><code{cls}>" + _esc("".join(b + "\n" for b in body))
                        + "</code></pre>\n"))
            i = j + 1
            continue

        if _QUOTE.match(line):
            inner, j = [], i
            while j < n:
                cur = lines[j]
                if _QUOTE.match(cur):
                    s = cur.lstrip(" ")[1:]
                    inner.append(s[1:] if s.startswith(" ") else s)
                elif cur.strip() and inner and inner[-1].strip() and not _starts_block(lines, j):
                    inner.append(cur)
                else:
                    break
                j += 1
            blocks, _ = _blocks(inner)
            out.append(("b", "<blockquote>\n"
                        + "".join(_block_html(*b) for b in blocks) + "</blockquote>\n"))
            i = j
            continue

        if _HR.match(line):
            out.append(("b", "<hr />\n"))
            i += 1
            continue

        if _ITEM.match(line):
            html_, i = _list(lines, i)
            out.append(("b", html_))
            continue

        m = _ATX.match(line)
        if m:
            level = len(m.group(1))
            text = re.sub(r"(?:^|[ \t]+)#+[ \t]*$", "", m.group(2).strip()).strip()
            out.append(("b", f"<h{level}>{_inline(text)}</h{level}>\n"))
            i += 1
            continue

        para, j, level = [line], i + 1, 0
        while j < n and lines[j].strip():
            setext = _SETEXT.match(lines[j])
            if setext:
                level = 1 if setext.group(1)[0] == "=" else 2
                break
            if _starts_block(lines, j):
                break
            para.append(lines[j])
            j += 1
        text = "\n".join(p.lstrip(" \t") for p in para).strip()
        if level:
            out.append(("b", f"<h{level}>{_inline(text)}</h{level}>\n"))
            i = j + 1
        else:
            out.append(("p", _inline(text)))
            i = j
    return out, gap


def version():
    """Version of the copy of this script that is actually running.

    Read from the plugin manifest located relative to this file, not to a
    working directory: a stale copy then stamps its own older number, and
    that mismatch is the entire point of stamping.
    """
    try:
        manifest = Path(__file__).resolve().parents[3] / ".claude-plugin" / "plugin.json"
        v = json.loads(manifest.read_text(encoding="utf-8")).get("version")
        return v if isinstance(v, str) and v else "unknown"
    except Exception:
        return "unknown"


def split_front_matter(text):
    # `\r?\n` throughout: a markdown file edited on Windows, or pasted
    # through a tool that normalises to CRLF, otherwise fails to match at
    # all — and the failure is silent, since an unmatched frontmatter is
    # indistinguishable here from a file that has none.
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if km and km.group(2):
            meta[km.group(1)] = km.group(2)
    return meta, m.group(2)


def body_sha(body):
    """Fingerprint of the page body — must match verify_cot_html.source_sha.

    The gate stamp carries the first twelve characters of this, so the
    page can tell whether the body it is showing is the body the gate
    judged. Without it `verified: "pass"` survives any later edit and the
    page keeps advertising a result for text the gate never saw — the
    exact staleness this tool exists to catch, reintroduced on the field
    that reports the catching.

    It is also emitted into the page as <meta name="cot-body-sha">, which
    is what lets the verifier prove the HTML it just judged was built
    from the markdown it is about to stamp. Without that link the gate
    reads one file and fingerprints another.
    """
    # Normalised, so CRLF and LF copies of the same body hash alike —
    # must stay identical to verify_cot_html.source_sha, which a test
    # pins across six frontmatter shapes.
    return hashlib.sha256(body.replace("\r\n", "\n").encode("utf-8")).hexdigest()


# The only tags a mermaid label may contain. Applied first, while their
# `&gt;` is still distinguishable from an arrow's.
LABEL_TAGS = [
    ("&lt;div style='text-align:left'&gt;", "<div style='text-align:left'>"),
    ("&lt;/div&gt;", "</div>"),
    ("&lt;br/&gt;", "<br/>"),
    ("&lt;br&gt;", "<br>"),
]


def unescape_label_markup(fence_body):
    """Un-escape what mermaid needs, and no tag outside the allow-list.

    A blanket `html.unescape` here is a cross-site scripting hole, and the
    review that found it is the reason this function exists. The renderer
    passes no raw HTML through, so every `<` in the document is escaped and
    the page is safe — except inside this fence, where the label syntax
    genuinely needs `<div>` and `<br/>` to arrive as markup. Unescaping
    the whole body to get them also delivers `<script>` and
    `<img onerror=…>`, live, from whatever source document was
    summarised.

    mermaid's own `securityLevel` cannot save this. The browser parses
    `<pre>` content as markup at load time, before mermaid initializes —
    the sanitizer sits downstream of the injection point. A control
    placed after the thing it guards is not a control.

    The cut is **`<`, not `>`**. A lone `>` cannot open a tag, and the
    diagram is full of legitimate ones: `-->`, `==>`, `-.->` are arrows
    and mermaid will not parse them escaped. So `&gt;` is restored
    everywhere, while `&lt;` is restored only as part of a tag in
    LABEL_TAGS. Everything else keeps its `&lt;` and renders as text —
    `<script>` included, which is the point.

    Order is load-bearing: the allowed tags first, while their `&gt;` is
    still an entity and can be told from an arrow's; then the `&lt;`
    neutralisation; then `&gt;` and the quote that delimits labels.

    `&amp;` is deliberately NOT restored. Left alone it decodes to `&`
    exactly once, at the browser stage, which is what the reader should
    see — and restoring it would undo the `&lt;` neutralisation above and
    reconstitute numeric character references like `&#60;` into a second
    route to the same hole.
    """
    for escaped, raw in LABEL_TAGS:
        fence_body = fence_body.replace(escaped, raw)

    # THERE ARE TWO DECODE STAGES, and this is the one that is easy to
    # miss. The browser decodes the <pre> to get textContent, mermaid
    # takes that textContent as the diagram source, and then inserts each
    # label with innerHTML — which decodes a SECOND time. So a `&lt;` here
    # becomes the character `<` in textContent and is parsed as a tag by
    # the innerHTML pass, arriving at mermaid's own sanitizer as real
    # markup. Defending only the first stage leaves the second one relying
    # on a downstream control, which is the posture this file rejects.
    #
    # Anything meant to READ as text therefore needs one extra level of
    # escaping, so that exactly one decode is consumed at each stage.
    # `&amp;lt;` → textContent `&lt;` → innerHTML → the character `<`,
    # displayed. Correct for fidelity as well as safety: a `<div>` written
    # in the source is text the reader should see, not an element that
    # silently disappears into the label.
    fence_body = fence_body.replace("&lt;", "&amp;lt;")
    fence_body = fence_body.replace("&gt;", ">")
    return fence_body.replace("&quot;", '"')


def render_body(md_text):
    lines = md_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks, _ = _blocks(lines)
    out = "".join(_block_html(kind, payload) for kind, payload in blocks)

    # The renderer escapes fence bodies. Mermaid node labels are raw HTML
    # (<div style='text-align:left'>) and must reach the browser as
    # markup, so the allowed tags — and only those — are un-escaped here.
    out = MERMAID_FENCE.sub(
        lambda m: '<pre class="mermaid">\n'
        + unescape_label_markup(m.group(1))
        + "</pre>",
        out,
    )

    return out


def leftover_markdown(rendered):
    """Markdown that survived conversion, ignoring where it is legitimate.

    Mermaid blocks and <code> spans really do contain `|`, `**` and `#`.

    The anchor is a BLOCK-tag open, not a bare `>`. Unconverted text ends
    up inside a tag, where a line-start-only check cannot see it — that
    hole let a stray `##` through during development — but `>` alone also
    matches the close of any inline tag, so `<em>x</em> - 說明` and
    `<strong>A</strong> | B` were condemned as survived markdown. Both
    are ordinary prose, and the policy here writes no file at all, so a
    false accusation is a hard stop on a correct page.

    `**` cannot be anchored that way, because unconverted bold appears
    mid-paragraph. It needs the PAIR instead: a lone `**` is arithmetic
    (`2**3`), a pair opening at a word boundary is markdown that did not
    convert.
    """
    scoped = re.sub(r'<pre class="mermaid">.*?</pre>', "", rendered, flags=re.S)
    # `<code[^>]*>` and not `<code>`: the renderer tags a fence's inner code
    # element with the language (`<code class="language-bash">`), so a bare
    # `<code>` scope leaves every language-tagged fence in the text being
    # searched — and a ```bash block holding `# install …` is then reported
    # as an unconverted heading. The check condemned legitimate content.
    scoped = re.sub(r"<code[^>]*>.*?</code>", "", scoped, flags=re.S)
    block = r"(?:^|<(?:p|li|td|th|div|h[1-6])[^>]*>)\s*"
    found = []
    # The pair must open on a non-space and close on a non-space, as
    # markdown itself requires — otherwise `2 ** 3 ** 4` in prose matches
    # and hard-stops a correct page.
    if re.search(r"(?:^|[\s>])\*\*\S[^*\n]{0,200}\S\*\*", scoped, re.M):
        found.append("literal ** (bold marker)")
    if re.search(block + r"-\s+\S", scoped, re.M):
        found.append("literal `- ` list rows")
    if re.search(block + r"\|.*\|", scoped, re.M):
        found.append("literal | table rows")
    if re.search(block + r"#{1,6}\s", scoped, re.M):
        found.append("literal # headings")
    if "```" in scoped:
        found.append("literal ``` fences")
    if re.search(r"\{\{[A-Z][A-Z_]*\}\}", scoped):
        found.append("unreplaced {{PLACEHOLDER}}")
    return found


def path_link(value, artifact=False):
    """Render a path as a clickable file:// link when that can work.

    Only an absolute path is linked. A relative one has no defined base
    once the page leaves the directory it was written in, and guessing a
    root would produce links that look right and go nowhere — worse than
    plain text.

    The Artifact build neither links nor prints an absolute path. It is
    served over https, where browsers refuse file:// navigation, so the
    link would be dead — and printing the path as plain text still hands
    the author's directory layout to everyone the page is shared with,
    which was the other half of the reason for not linking. The file name
    alone identifies the source to anyone who has it and discloses
    nothing to anyone who does not.
    """
    if artifact:
        return html.escape(Path(value).name if value.startswith("/") else value)
    if not value.startswith("/"):
        return html.escape(value)
    return (f'<a href="file://{html.escape(quote(value))}">'
            f"{html.escape(value)}</a>")


def build(md_text, artifact=False, out_dir=None):
    meta, body = split_front_matter(md_text)
    rendered = render_body(body)
    ver = version()

    title = meta.get("title") or meta.get("source") or "CoT Explain"
    stamp = f"loom-workflow:loom-visualization/{ver}"

    # Every frontmatter key reaches the full page's <head> (the Artifact
    # build has no <head> of its own, so it carries none). The markdown carried
    # nineteen and an earlier version forwarded two, one of which it read
    # under a name the template had since changed — so the date rendered
    # blank and nothing said so. Whatever the artifact records, the
    # derived file records too.
    head_meta = "\n".join(
        f'<meta name="cot-{html.escape(k)}" content="{html.escape(v)}">'
        for k, v in meta.items()
    )

    # verified / fidelity_checked are deliberately shown even when empty.
    # A page that ran no checks must say so: silence reads as "fine", and
    # this whole tool exists because a silent artifact was mistaken for a
    # good one. `verified` additionally carries the fingerprint of the
    # body the gate judged, so a stale result reads as stale rather than
    # as a pass.
    verified_raw = meta.get("verified", "").strip()
    vm_gate = re.match(r"^(.*?)\s*@\s*([0-9a-f]{6,64})$", verified_raw)
    if not verified_raw:
        verified_shown = "<strong>閘：未執行</strong>"
    elif not vm_gate:
        verified_shown = (
            "<strong>閘：stale — 這筆結果沒有頁面指紋，無法證明它判的是這份內容"
            "（重跑 verify --stamp）</strong>"
        )
    elif not body_sha(body).startswith(vm_gate.group(2)):
        verified_shown = (
            "<strong>閘：stale — 檢查之後頁面被改過，這筆結果不適用"
            "（重跑 verify --stamp）</strong>"
        )
    else:
        verified_shown = f"閘：{html.escape(vm_gate.group(1))}"

    fidelity_raw = meta.get("fidelity_checked", "").strip()
    fm = re.match(r"^(PASS|FAIL)\s*\((.+)\)$", fidelity_raw)
    if fm and out_dir:
        target = str(Path(out_dir).resolve() / fm.group(2))
        fidelity_shown = f"{fm.group(1)} ({path_link(target, artifact)})"
    else:
        fidelity_shown = html.escape(fidelity_raw)

    meta_line = "　·　".join([
        f'來源：{path_link(meta.get("source", "—"), artifact)}',
        f'產出：{html.escape(meta.get("processed_at") or meta.get("date", "—"))}',
        html.escape(stamp),
        verified_shown,
        (f"忠實度檢查：{fidelity_shown}" if fidelity_shown
         else "<strong>忠實度檢查：未執行</strong>"),
    ])
    parts = [
        f"<h1>{html.escape(title)}</h1>",
        f'<p class="meta">{meta_line}</p>',
        rendered,
        f'<footer class="stamp">{html.escape(stamp)} — rendered from the '
        f"markdown artifact; do not hand-edit this file.</footer>",
    ]
    inner = "\n".join(p for p in parts if p)

    leftovers = leftover_markdown(inner)
    if leftovers:
        return None, leftovers

    if artifact:
        return f"<style>\n{CSS}\n</style>\n<main>\n{inner}\n</main>\n", []
    return (
        "<!doctype html>\n"
        '<html lang="zh-TW">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<meta name="generator" content="{html.escape(stamp)}">\n'
        f'<meta name="cot-body-sha" content="{body_sha(body)}">\n'
        f"{head_meta}\n"
        f"<title>{html.escape(title)}</title>\n<style>\n{CSS}\n</style>\n</head>\n"
        f"<body>\n<main>\n{inner}\n</main>\n{MERMAID_CDN}\n</body>\n</html>\n"
    ), []


def main():
    ap = argparse.ArgumentParser(description="Render loom-visualization markdown to HTML.")
    ap.add_argument("markdown")
    ap.add_argument("-o", "--out")
    ap.add_argument("--artifact", action="store_true")
    args = ap.parse_args()

    src = Path(args.markdown)
    out = Path(args.out) if args.out else src.with_suffix(".html")
    doc, leftovers = build(
        src.read_text(encoding="utf-8"), args.artifact, out.parent
    )

    if leftovers:
        msg = (
            "FAIL: markdown survived conversion — " + "; ".join(leftovers)
            + "\nNo file written. A run that fails but still writes leaves "
              "exactly the broken deliverable this check exists to stop."
        )
        # Writing nothing is not the same as leaving nothing. A page from
        # an earlier good run sits there looking current, for a source
        # that no longer converts — say so, or the silence reads as "the
        # file on disk is fine".
        if out.exists():
            msg += (
                f"\nWARNING: {out} is still on disk from an earlier run and "
                "is now STALE — it does not reflect the current markdown."
            )
        print(msg, file=sys.stderr)
        return 1

    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out}  ({version()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
