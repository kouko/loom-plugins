#!/usr/bin/env python3
"""Adversarial test: separator as first interior line (replacing title).
This should be flagged as an unstructured multi-line box but currently is not.
"""
import sys
from pathlib import Path
sys.path.append("/Users/kouko/.herdr/worktrees/loom-plugins/visionazation-node-title-style/loom-workflow/skills/loom-visualization/scripts")

from checks_nodes import find_issues

def test_separator_replaces_title():
    """Test case where separator appears as first interior line (no title line).

    Expected: Should be flagged as unstructured multi-line box
    Actual: Not flagged (BROKE)
    """
    lines = [
        "┌───┐",
        "├───┤",  # Separator replacing title
        "│ B │",
        "└───┘"
    ]

    issues = find_issues(lines)
    print(f"Input diagram:")
    for line in lines:
        print(repr(line))
    print(f"\nIssues found: {issues}")

    # Check if the expected issue is present
    expected_msg = "box interior with two or more content lines in title part and no separator row between them"
    if any(expected_msg in issue[2] for issue in issues):
        print("\n✓ EXPECTED: Issue correctly flagged")
        return True
    else:
        print("\n✗ BROKE: Expected issue NOT flagged")
        print("This demonstrates a vulnerability in checks_nodes")
        return False

if __name__ == "__main__":
    test_separator_replaces_title()