#!/usr/bin/env python3
"""Adversarial test: rounded box corners (╭─╮, ╰─╯) not recognized by checks_nodes.
The validator should recognize these as valid box corners and check them.
"""
import sys
from pathlib import Path
sys.path.append("/Users/kouko/.herdr/worktrees/loom-plugins/visionazation-node-title-style/loom-workflow/skills/loom-visualization/scripts")

from checks_nodes import find_issues

def test_rounded_box_corners():
    """Test case with rounded box corners.

    Expected: Should be recognized as a box and validated
    Actual: Not recognized at all (BROKE)
    """
    lines = [
        "╭────╮",
        "│ T  │",
        "├────┤",
        "│ B  │",
        "╰────╯"
    ]

    issues = find_issues(lines)
    print(f"Input diagram (rounded corners):")
    for line in lines:
        print(repr(line))
    print(f"\nIssues found: {issues}")

    if issues:
        print("\n✓ EXPECTED: Box recognized and validated")
        return True
    else:
        print("\n✗ BROKE: Box with rounded corners NOT recognized")
        print("The validator misses boxes using Unicode rounded corners")
        return False

def test_crlf_input():
    """Test case with CRLF line endings.

    Expected: Should be recognized as a box and validated
    Actual: Not recognized (BROKE)
    """
    lines = [
        "┌────┐\r",
        "│ T  │\r",
        "├────┤\r",
        "│ B  │\r",
        "└────┘\r"
    ]

    issues = find_issues(lines)
    print(f"\nInput diagram (CRLF):")
    for line in lines:
        print(repr(line))
    print(f"\nIssues found: {issues}")

    if issues:
        print("\n✓ EXPECTED: Box recognized and validated")
        return True
    else:
        print("\n✗ BROKE: Box with CRLF NOT recognized")
        print("The validator misses boxes with CRLF line endings")
        return False

if __name__ == "__main__":
    test_rounded_box_corners()
    test_crlf_input()