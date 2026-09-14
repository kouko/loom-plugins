#!/usr/bin/env bash
# test-adversarial-agy-skill-folder.sh
#
# Adversarial probes for scripts/agy-validate-skill-folder.sh (agy PreToolUse
# flat-skill-folder adapter): unnormalised paths, traversal, relative targets,
# and the side effects of the scratch mirror. A FAIL line is a finding against
# the change; a PASS line records an attack the adapter survived.
#
# Usage:
#   bash loom-workflow/tests/test-adversarial-agy-skill-folder.sh

set -u

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"

PASS_COUNT=0
FAIL_COUNT=0
pass() { echo "PASS — $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "FAIL — $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/agy-skill-folder-adv.XXXXXX")"
cleanup() { rm -rf "$TMP_ROOT"; }
trap cleanup EXIT

# Fixture: two flat skills, foo and bar, in a plain directory (no git repo).
PROJ="$TMP_ROOT/proj"
mkdir -p "$PROJ/plugin/skills/foo/assets" "$PROJ/plugin/skills/bar/assets"
printf -- '---\nname: foo\n---\n' > "$PROJ/plugin/skills/foo/SKILL.md"
printf -- '---\nname: bar\n---\n' > "$PROJ/plugin/skills/bar/SKILL.md"
# The adapter's scratch dir lands under this TMPDIR, so an escape is observable.
HOOK_TMP="$TMP_ROOT/hooktmp"
mkdir -p "$HOOK_TMP"

# run_hook <stdin> — sh -c from the plugin root, as agy runs it; sets OUT, CODE.
run_hook() {
  OUT=$(cd "$PLUGIN_DIR" && printf '%s' "$1" | TMPDIR="$HOOK_TMP" sh -c 'bash ./scripts/agy-validate-skill-folder.sh' 2>/dev/null)
  CODE=$?
}
decision() { printf '%s' "$OUT" | jq -r '.decision // empty' 2>/dev/null; }
payload() { # payload <tool> <TargetFile> <workspace-or-empty>
  jq -cn --arg t "$1" --arg p "$2" --arg w "$3" \
    '{toolCall:{name:$t,args:{TargetFile:$p}},stepIdx:1,conversationId:"c",
      workspacePaths:(if $w == "" then [] else [$w] end)}'
}

test_skillfolder_dotdot_into_sibling_nested_denies() {
  run_hook "$(payload write_to_file "$PROJ/plugin/skills/foo/../bar/assets/sub/x.md" "")"
  if [ "$CODE" -eq 0 ] && [ "$(decision)" = "deny" ]; then
    pass "test_skillfolder_dotdot_into_sibling_nested_denies"
  else
    fail "test_skillfolder_dotdot_into_sibling_nested_denies: skills/foo/../bar/assets/sub/x.md out=$OUT"
  fi
}

test_skillfolder_double_slash_nested_denies() {
  run_hook "$(payload write_to_file "$PROJ/plugin/skills//foo/assets/sub/x.md" "")"
  if [ "$(decision)" = "deny" ]; then
    pass "test_skillfolder_double_slash_nested_denies"
  else
    fail "test_skillfolder_double_slash_nested_denies: skills//foo/assets/sub/x.md out=$OUT"
  fi
}

test_skillfolder_trailing_slash_after_skills_nested_denies() {
  run_hook "$(payload write_to_file "$PROJ/plugin/skills/foo//assets//sub/x.md" "")"
  if [ "$(decision)" = "deny" ]; then
    pass "test_skillfolder_trailing_slash_after_skills_nested_denies"
  else
    fail "test_skillfolder_trailing_slash_after_skills_nested_denies: skills/foo//assets//sub/x.md out=$OUT"
  fi
}

test_skillfolder_dot_segment_nested_denies() {
  run_hook "$(payload write_to_file "$PROJ/plugin/skills/foo/./assets/sub/x.md" "")"
  if [ "$(decision)" = "deny" ]; then
    pass "test_skillfolder_dot_segment_nested_denies"
  else
    fail "test_skillfolder_dot_segment_nested_denies: skills/foo/./assets/sub/x.md out=$OUT"
  fi
}

test_skillfolder_traversal_target_creates_nothing_outside_scratch() {
  run_hook "$(payload write_to_file "$PROJ/plugin/skills/foo/../../../escaped-by-hook/a/x.md" "")"
  if [ ! -e "$HOOK_TMP/escaped-by-hook" ]; then
    pass "test_skillfolder_traversal_target_creates_nothing_outside_scratch"
  else
    fail "test_skillfolder_traversal_target_creates_nothing_outside_scratch: hook created $HOOK_TMP/escaped-by-hook (left behind after its scratch cleanup)"
  fi
}

test_skillfolder_relative_target_with_workspace_nested_denies() {
  run_hook "$(payload write_to_file "plugin/skills/foo/assets/sub/x.md" "$PROJ")"
  if [ "$(decision)" = "deny" ]; then
    pass "test_skillfolder_relative_target_with_workspace_nested_denies"
  else
    fail "test_skillfolder_relative_target_with_workspace_nested_denies: out=$OUT"
  fi
}

test_skillfolder_multi_replace_nested_denies() {
  run_hook "$(payload multi_replace_file_content "$PROJ/plugin/skills/foo/assets/sub/x.md" "")"
  if [ "$(decision)" = "deny" ]; then
    pass "test_skillfolder_multi_replace_nested_denies"
  else
    fail "test_skillfolder_multi_replace_nested_denies: out=$OUT"
  fi
}

test_skillfolder_space_and_nonascii_skill_name_nested_denies() {
  mkdir -p "$PROJ/plugin/skills/my skill 日本"
  printf -- '---\nname: x\n---\n' > "$PROJ/plugin/skills/my skill 日本/SKILL.md"
  run_hook "$(payload write_to_file "$PROJ/plugin/skills/my skill 日本/assets/sub dir/x.md" "")"
  if [ "$(decision)" = "deny" ]; then
    pass "test_skillfolder_space_and_nonascii_skill_name_nested_denies"
  else
    fail "test_skillfolder_space_and_nonascii_skill_name_nested_denies: out=$OUT"
  fi
}

test_skillfolder_hostile_stdin_exits_zero_with_json() {
  local bad=0 input
  for input in '{"toolCall":{"args":{"TargetFile":123}}}' '{"toolCall":{"args":"x"}}' '[1,2]' \
               "$(printf '{"toolCall":{"args":{"TargetFile":"%s"}}}' "$(printf 'a%.0s' $(seq 1 5000))")"; do
    run_hook "$input"
    if [ "$CODE" -ne 0 ] || [ -z "$(decision)" ]; then bad=1; fi
  done
  if [ "$bad" -eq 0 ]; then
    pass "test_skillfolder_hostile_stdin_exits_zero_with_json"
  else
    fail "test_skillfolder_hostile_stdin_exits_zero_with_json: out=$OUT code=$CODE"
  fi
}

test_skillfolder_dotdot_into_sibling_nested_denies
test_skillfolder_double_slash_nested_denies
test_skillfolder_trailing_slash_after_skills_nested_denies
test_skillfolder_dot_segment_nested_denies
test_skillfolder_traversal_target_creates_nothing_outside_scratch
test_skillfolder_relative_target_with_workspace_nested_denies
test_skillfolder_multi_replace_nested_denies
test_skillfolder_space_and_nonascii_skill_name_nested_denies
test_skillfolder_hostile_stdin_exits_zero_with_json

echo ""
echo "================================================================"
echo "Summary: ${PASS_COUNT} PASS / ${FAIL_COUNT} FAIL"
echo "================================================================"
[ "$FAIL_COUNT" -eq 0 ]
