import re
import sys

def test_ship_skill_table_guidance_present():
    """Verify that the ship skill contains guidance to use Markdown tables for list-type information."""
    with open("loom-code/skills/ship/SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Target sentence from the change
    target = "Use a Markdown table for any list‑type or comparison‑type information"

    if target in content:
        print("✅ Guidance present")
    else:
        print(f"❌ Guidance missing. Expected: {target}")
        sys.exit(1)

def test_ship_skill_no_inline_lists_guidance_present():
    """Verify that the ship skill explicitly rejects inline ①②③ lists."""
    with open("loom-code/skills/ship/SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()

    target = "Do not use inline ①②③ lists or plain‑text enumerations"

    if target in content:
        print("✅ Rejection of inline lists present")
    else:
        print(f"❌ Rejection of inline lists missing. Expected: {target}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        test_ship_skill_table_guidance_present()
        test_ship_skill_no_inline_lists_guidance_present()
        print("All probes passed.")
    except Exception as e:
        print(f"Probe failed: {e}")
        sys.exit(1)
