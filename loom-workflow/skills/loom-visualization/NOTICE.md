# Third-party notices

The loom-visualization skill includes or follows work from the projects below.

## ascii-graph-toolkit v0.6.0

The ASCII engine in `scripts/` (`width.py`, `glyphs.py`, `align.py`,
`checks_seam.py`, `checks_table.py`, `checks_kink.py`, `generate.py` and the
`gen_*.py` generators, with their tests) is ported from ascii-graph-toolkit
v0.6.0, monkey-skills commit e5b978e0. Each ported file records that source in
its header. `width.py` was reimplemented on Python's `unicodedata` in place of
the `wcwidth` package.

MIT License. Copyright (c) 2026 kouko.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Mermaid syntax conventions

The Mermaid forms in `templates/` follow the diagram syntax documented by
mermaid-js/mermaid (https://github.com/mermaid-js/mermaid), MIT License. No
Mermaid source code is included; the templates were written for this skill.

## Diagon ASCII conventions

The hand-authored box-drawing forms in `templates/` follow the ASCII diagram
conventions of ArthurSonzogni/Diagon (https://github.com/ArthurSonzogni/Diagon),
MIT License. No Diagon source code is included.

## C4 model

The one-level-per-diagram rule in `templates/08-system-architecture.md` uses
the context, container and component levels of the C4 model by Simon Brown
(https://c4model.com), licensed under Creative Commons Attribution 4.0
International (CC BY 4.0).
