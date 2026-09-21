# Blind Run Report for 2026-09-19-publication-hook-false-positives

## Acceptance Criteria Verification

1. The hook correctly identifies `cat <<EOF | bash\nMERGE\nEOF` as containing a merge command
   - **Result**: PASS
   - **Evidence**: `test_heredoc_piped_into_a_shell_is_seen` passes in adversarial test suite. The fix modified `_heredoc_executes_body` to consider the full pipeline, not just the command word. When `cat` pipes to `bash`, the shell executes the heredoc body.

2. The hook correctly identifies shell commands with bundled short options like `-lc`, `-euxc`, `-cl`
   - **Result**: PASS
   - **Evidence**: `test_bundled_short_options_before_c_are_seen` and `test_long_option_with_a_value_before_c_is_seen` pass. The fix modified `_shell_c_argument` to check for `c` anywhere in the bundle (`"c" in token[1:]`) rather than only at the end (`token.endswith("c")`).

3. Heredoc body execution detection considers the full pipeline, not just the command word
   - **Result**: PASS
   - **Evidence**: Multiple tests pass: `test_shell_further_down_the_pipeline_is_seen`, `test_heredoc_piped_through_tee_is_seen`, `test_quoted_delimiter_does_not_hide_the_pipe`. The `_heredoc_executes_body` function now iterates over pipeline members (`_operator_segments`) and checks each for shell programs.

4. Existing true positives (direct pushes, etc.) continue to be recognized
   - **Result**: PASS
   - **Evidence**: `test_direct_pushes_remain_refused` passes with all variants. All 2380 package tests pass (excluding known OPEN holes in adversarial tests).

5. Adversarial tests for heredoc carve-out pass
   - **Result**: PASS (for closed tests)
   - **Evidence**: 29 of 41 adversarial tests pass. The 12 failures are explicitly marked as "OPEN" in the test file, representing known holes not addressed by this fix. All "closed" tests pass.

## Impact on Existing Data

This change only modifies shell command recognition logic in the publication hook. No user data or existing functionality is affected:
- The removed text rule was a false positive generator
- All true positive detections continue to work
- No changes to user-facing features

## Decisions Made on User's Behalf

No decisions were made on the user's behalf that required dismissal of severity `important` or worse. All changes were:
- Fixes to false negative detection (heredoc pipelines, bundled flags)
- Preservation of all existing true positives
- Documentation of remaining known holes via OPEN adversarial tests

## Open Questions

None reported in the intent.