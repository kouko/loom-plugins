#!/usr/bin/env python3
"""Adversarial test: double separator (two separators in a row).
The second separator should be flagged as having no content line after it.
"""
import sys
from pathlib import Path
sys.path.append("/Users/kouko/.herdr/worktrees/loom-plugins/visionazation-node-title-style/loom-workflow/skills/loom-visualization/scripts")

from checks_nodes import find_issues

def test_double_separator():
    """Test case with two separators consecutively.

    Expected: Second separator should be flagged as having no content after it
    Actual: Not flagged (BROKE)
    """
    lines = [
        "┌────┐",
        "│ T  │",
        "├────┤",
        "├────┤",  # Second separator - should have content after but doesn't
        "│ B  │",
        "└────┘"
    ]

    issues = find_issues(lines)
    print(f"Input diagram:")
    for line in lines:
        print(repr(line))
    print(f"\nIssues found: {issues}")

    # Check if the expected issue is present
    expected_msg = "separator row with no content line after it"
    if any(expected_msg in issue[2] for issue in issues):
        print("\n✓ EXPECTED: Issue correctly flagged")
        return True
    else:
        print("\n✗ BROKE: Expected issue NOT flagged")
        print("This demonstrates a vulnerability in checks_nodes")
        return False

if __name__ == "__main__":
    test_double_separator()