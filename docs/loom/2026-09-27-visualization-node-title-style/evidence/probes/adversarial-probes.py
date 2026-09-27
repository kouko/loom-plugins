import sys
from pathlib import Path
sys.path.append("/Users/kouko/.herdr/worktrees/loom-plugins/visionazation-node-title-style/loom-workflow/skills/loom-visualization/scripts")

from gen_flow import render_flow
from checks_nodes import find_issues

print("=== Probe: Width boundary ===")
# Body 1 char wide, budget very small
print("Input: title='T', body=['x'], width=1")
try:
    output = render_flow([{"title": "T", "body": ["x"]}], width=1)
    print(output)
except Exception as e:
    print(f"Exception: {e}")

print("\n=== Probe: Structured input edge - empty body ===")
print("Input: title='T', body=[]")
try:
    render_flow([{"title": "T", "body": []}])
    print("VERDICT: BROKE - Empty body should raise ValueError")
except ValueError as e:
    print(f"ValueError raised: {e}")
    print("VERDICT: HELD - Empty body raises ValueError")
except Exception as e:
    print(f"Unexpected Exception: {type(e).__name__}: {e}")
    print("VERDICT: BROKE - Wrong exception type")

print("\n=== Probe: Structured input edge - body with embedded newline ===")
print("Input: title='T', body=['a\\nb']")
try:
    output = render_flow([{"title": "T", "body": ["a\nb"]}])
    print(output)
    print("Note: Embedded newline in dict body item rendered without splitting - may be unexpected")
except Exception as e:
    print(f"Exception: {e}")

print("\n=== Probe: checks_nodes - separator with no body ===")
lines = [
    "┌───┐",
    "│ T │",
    "├───┤",
    "└───┘"
]
issues = find_issues(lines)
print(f"Issues found: {issues}")
if any("no content line after it" in issue[2] for issue in issues):
    print("VERDICT: HELD - Empty separator flagged")
else:
    print("VERDICT: BROKE - Empty separator NOT flagged")

print("\n=== Probe: checks_nodes - two content lines in title part ===")
lines = [
    "┌────┐",
    "│ T1 │",
    "│ T2 │",
    "└────┘"
]
issues = find_issues(lines)
print(f"Issues found: {issues}")
if any("two or more content lines in title part" in issue[2] for issue in issues):
    print("VERDICT: HELD - Two content lines in title flagged")
else:
    print("VERDICT: BROKE - Two content lines in title NOT flagged")

print("\n=== Probe: checks_nodes - separator at first interior line (title replaced by separator) ===")
lines = [
    "┌───┐",
    "├───┤",
    "│ B │",
    "└───┘"
]
issues = find_issues(lines)
print(f"Issues found: {issues}")
if issues:
    print("VERDICT: HELD - Separator replacing title is flagged")
else:
    print("VERDICT: BROKE - Separator replacing title NOT flagged")

print("\n=== Probe: checks_nodes - double separator ===")
lines = [
    "┌────┐",
    "│ T  │",
    "├────┤",
    "├────┤",
    "│ B  │",
    "└────┘"
]
issues = find_issues(lines)
print(f"Issues found: {issues}")
if any("no content line after it" in issue[2] for issue in issues):
    print("VERDICT: HELD - Double separator flagged")
else:
    print(f"VERDICT: {'BROKE' if issues else 'BROKE'} - Double separator not properly caught")

print("\n=== Probe: checks_nodes - double-line box (╔═╗) ===")
lines = [
    "╔════╗",
    "║ T  ║",
    "╠════╣",
    "║ B  ║",
    "╚════╝"
]
issues = find_issues(lines)
print(f"Issues found: {issues}")
print("Note: Double-line box should be checked")

print("\n=== Probe: checks_nodes - rounded box (╭─╮) ===")
lines = [
    "╭────╮",
    "│ T  │",
    "├────┤",
    "│ B  │",
    "╰────╯"
]
issues = find_issues(lines)
print(f"Issues found: {issues}")
print("Note: Rounded box corners should be checked")

print("\n=== Probe: checks_nodes - CRLF input ===")
lines = [
    "┌────┐\r",
    "│ T  │\r",
    "├────┤\r",
    "│ B  │\r",
    "└────┘\r"
]
issues = find_issues(lines)
print(f"Issues found: {issues}")

print("\n=== Probe: Backward compatibility - simple centered string ===")
print("Input: ['Hello']")
output = render_flow(["Hello"])
print(output)
# Check if centered
if "│ Hello │" in output or output.count(" ") != 0:
    print("Note: Simple string should be centered")
