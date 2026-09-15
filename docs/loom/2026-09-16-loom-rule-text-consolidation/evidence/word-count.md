# Word-count evidence — loom rule text consolidation

Measured for W3-01 (acceptance 3): "The loom-code and loom-design rule
files, counted the same way as the audit baseline of 37,665 words, total
at least 2,000 fewer words, and loom-code's write-plan SKILL.md is under
3,750 words."

## Method

- File set: every `*.md` under `loom-code/skills`, `loom-code/agents`,
  `loom-code/references`, `loom-design/skills`, excluding any file named
  `README.md` or `CHANGELOG.md`.
- Word count per file: Python `len(text.split())`, summed across the file
  set.
- Base revision `dec4e927` was read via `git show dec4e927:<path>` for
  each path (paths listed with
  `git ls-tree -r --name-only dec4e927 -- <dirs>`) — no checkout was
  performed.
- HEAD revision measured the same way against the branch tip.
- `loom-code/skills/write-plan/SKILL.md` body: the text after the closing
  `---` of the YAML frontmatter (i.e. everything following the second
  `---` line), same `str.split()` word count, at base and HEAD.

### Script

```python
import subprocess

REPO = "/Users/kouko/GitHub/loom-plugins"
DIRS = ["loom-code/skills", "loom-code/agents", "loom-code/references", "loom-design/skills"]
EXCLUDE = {"README.md", "CHANGELOG.md"}

def git(args):
    return subprocess.run(["git", "-C", REPO] + args, capture_output=True, text=True, check=True).stdout

def list_paths(rev):
    out = git(["ls-tree", "-r", "--name-only", rev, "--"] + DIRS)
    paths = [p for p in out.splitlines() if p.endswith(".md")]
    paths = [p for p in paths if p.split("/")[-1] not in EXCLUDE]
    return sorted(paths)

def show(rev, path):
    r = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def wc(text):
    return len(text.split())

def measure(rev):
    per_file = {}
    for p in list_paths(rev):
        text = show(rev, p)
        if text is not None:
            per_file[p] = wc(text)
    return per_file

def writeplan_body(rev):
    text = show(rev, "loom-code/skills/write-plan/SKILL.md")
    if text is None:
        return None
    rest = text[4:]  # after leading "---\n"
    idx = rest.find("\n---\n")
    body = rest[idx + 5:] if idx != -1 else text
    return wc(body)

base_files = measure("dec4e927")
head_files = measure("HEAD")
print("base total", sum(base_files.values()), "files", len(base_files))
print("head total", sum(head_files.values()), "files", len(head_files))
print("write-plan body base", writeplan_body("dec4e927"))
print("write-plan body head", writeplan_body("HEAD"))
```

The base total reproduced was **37,665 words across 31 files**, matching
the expected audit baseline exactly — no discrepancy to explain.

## Per-directory results

### Base (`dec4e927`)

| Directory | Words |
|---|---|
| loom-code/agents | 4,302 |
| loom-code/references | 3,319 |
| loom-code/skills | 15,041 |
| loom-design/skills | 15,003 |
| **Total** | **37,665** (31 files) |

### HEAD (branch `docs/2026-09-16-loom-rule-text-consolidation`)

| Directory | Words |
|---|---|
| loom-code/agents | 3,214 |
| loom-code/references | 3,452 |
| loom-code/skills | 14,773 |
| loom-design/skills | 14,047 |
| **Total** | **35,486** (33 files) |

### Delta

- Total delta: **35,486 − 37,665 = −2,179 words**.
- File count changed from 31 to 33 (two new reference files were split
  out of existing skills; see per-file table below).

## write-plan SKILL.md body (post-frontmatter text)

| Revision | Words |
|---|---|
| Base (`dec4e927`) | 4,176 |
| HEAD | 3,352 |

## Per-file changes

Only files whose word count changed (new files marked NEW; none were
deleted).

| Path | Base | HEAD | Delta |
|---|---|---|---|
| loom-code/agents/adversary.md | 1,218 | 523 | −695 |
| loom-code/agents/blind-runner.md | 656 | 655 | −1 |
| loom-code/agents/implementer.md | 853 | 852 | −1 |
| loom-code/agents/reviewer.md | 1,575 | 1,184 | −391 |
| loom-code/references/dispatch-profile.md | 1,246 | 1,379 | +133 |
| loom-code/skills/build/SKILL.md | 1,081 | 882 | −199 |
| loom-code/skills/closing-review/SKILL.md | 2,209 | 1,991 | −218 |
| loom-code/skills/closing-review/references/adversarial.md | 1,045 | 1,090 | +45 |
| loom-code/skills/closing-review/references/lenses.md | 1,547 | 1,639 | +92 |
| loom-code/skills/expert-mode/SKILL.md | 720 | 768 | +48 |
| loom-code/skills/ship/SKILL.md | 1,457 | 1,394 | −63 |
| loom-code/skills/using-loom-code/SKILL.md | 232 | 221 | −11 |
| loom-code/skills/write-plan/SKILL.md | 4,205 | 3,381 | −824 |
| loom-code/skills/write-plan/references/confirm-intent.md | — | 862 | NEW |
| loom-design/skills/capture-intent/SKILL.md | 3,141 | 3,039 | −102 |
| loom-design/skills/capture-intent/references/locate-loom-code.md | — | 267 | NEW |
| loom-design/skills/design-system/SKILL.md | 1,259 | 792 | −467 |
| loom-design/skills/product-principles/SKILL.md | 1,192 | 725 | −467 |
| loom-design/skills/write-spec/SKILL.md | 3,117 | 2,930 | −187 |

## Acceptance checks

- **A3 positive `total-at-most-35665-words`**: threshold is
  37,665 − 2,000 = 35,665. HEAD total is 35,486 ≤ 35,665 → **PASS**
  (total delta −2,179, which is ≥ 2,000 fewer words as required).
- **A3 boundary `write-plan-body-below-3750`**: HEAD write-plan body is
  3,352 words < 3,750 → **PASS**.

Both A3 checks pass.
