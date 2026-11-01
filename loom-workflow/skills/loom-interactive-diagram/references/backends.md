# Backend contract

Each `backends/<module>.py` supplies `id()`, `extension()`,
`generate(path)`, `check(path)`, and `project(path)`. The command scans this
folder, so adding a backend requires only one new file. `id()` returns the
user-visible ID. `extension()` includes the dot. `generate` creates an empty
file; `check` raises `ValueError` naming the file when its structure is
invalid; `project` returns its canonical text projection.

| Backend ID | File type | Purpose |
|---|---|---|
| `drawio` | `.drawio` | Uncompressed draw.io XML |
| `demo-json` | `.json` | Small example proving registration and selection |

The projection header records the backend ID. The CLI checks that the file
extension matches that backend. The demo backend is not a replacement for a
draw.io editor.
