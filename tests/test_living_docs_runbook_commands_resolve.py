"""Living runbooks show no runnable command that does not resolve here.

Graduated from the 2026-11-20-stale-doc-references adversary probe.

Every `python3 <path>.py` or `bash <path>.sh` command inside a fenced
bash block of the listed living docs (at a line start or after `&&` or
`;`, the path quoted or not) must name a file that exists in this
repository, unless the same block marks the command historical or the
doc opens with a `> **Historical.**` banner directly under its title
line. A path
`$VAR/...` or `${VAR}/...` is explicitly out-of-repo and passes only when
an earlier line of the same block assigns `VAR=`. A command that only works from
another repository (for example a plugin shipped elsewhere) is not a
current reference here.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

DOCS = [
    "loom-workflow/docs/quarterly-audit-runbook.md",
    "loom-workflow/docs/skill-governance.md",
    "loom-workflow/docs/telemetry-setup.md",
]

FENCE = re.compile(r"```bash\n(.*?)```", re.S)
HISTORICAL_DOC = re.compile(r"#[^\n]*\n+> \*\*Historical\.\*\*")
CMD = re.compile(
    r"(?:^|&&|;)[ \t]*(?:python3|bash)\s+\"?([^\s\"]+\.(?:py|sh))\"?", re.M)
VAR = re.compile(r"\$\{?(\w+)\}?/")


def _unresolved(text, exists=lambda p: (ROOT / p).is_file()):
    misses = []
    if HISTORICAL_DOC.match(text):
        return misses
    for block in FENCE.findall(text):
        if re.search(r"#[^\n]*\bhistorical\b", block, re.I):
            continue
        for m in CMD.finditer(block):
            path, var = m.group(1), VAR.match(m.group(1))
            if var:
                assign = rf"^[ \t]*(?:export[ \t]+)?{var.group(1)}="
                if not re.search(assign, block[:m.start()], re.M):
                    misses.append(path)
            elif not exists(path):
                misses.append(path)
    return misses


def test_runbook_python_commands_resolve_in_repo():
    """Each current python3 command in a living runbook names an existing repo file."""
    misses = []
    for rel in DOCS:
        for path in _unresolved((ROOT / rel).read_text(encoding="utf-8")):
            misses.append(f"{rel}: {path}")
    assert not misses, "unresolved runnable paths:\n" + "\n".join(misses)


def test_unresolved_historical_block_skipped():
    """Synthetic: a missing path is reported unless its block says historical."""
    live = "```bash\npython3 gone/tool.py run\n```\n"
    old = "```bash\n# historical: removed\npython3 gone/tool.py run\n```\n"
    assert _unresolved(live, exists=lambda p: False) == ["gone/tool.py"]
    assert _unresolved(old, exists=lambda p: False) == []
    banner = "# T\n\n> **Historical.** removed\n\n## A\n" + live
    assert _unresolved(banner, exists=lambda p: False) == []
    late = "# T\n\n## A\n> **Historical.** removed\n" + live
    assert _unresolved(late, exists=lambda p: False) == ["gone/tool.py"]
    flat = "# T\n\n" + live + "\n> **Historical.** removed\n"
    assert _unresolved(flat, exists=lambda p: False) == ["gone/tool.py"]
    var = '```bash\nT="$HOME/x"\npython3 "$T/s.py" drift "$H"\n```\n'
    bare = '```bash\ncd x && python3 "$T/s.py"\nbash <d>/run.sh\n```\n'
    assert _unresolved(var, exists=lambda p: False) == []
    assert _unresolved(bare, exists=lambda p: False) == ["$T/s.py", "<d>/run.sh"]
