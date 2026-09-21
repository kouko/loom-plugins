"""Adversarial probes against the structural publication recognisers.

Every test here is one attempt to get a real publication -- a `git push` or a
`gh pr merge` that a real bash actually executes -- past the PreToolUse hook.

Two verdicts are recorded:

* **closed** -- the hook refuses it, and the test asserts that refusal, so the
  hole stays shut.
* **OPEN** -- the hook allows it and a real shell runs the publication. The
  test asserts the refusal the hook owes, so it fails today. That failure is
  the hole; it turns green when the hole is closed and cannot silently reopen.

Every OPEN command was checked twice: the hook was run on it (`push --hook`
with a PreToolUse payload, exit 0 = allowed), and bash was run on it with `gh`
and `git` replaced by a reporter stub, which printed the publication. The
`sudo` arity used below is sudo's own, from `sudo --help`: `-u`/`-g` take a
value, `-n`/`-s`/`-E` do not.
"""
from __future__ import annotations

from loom_checker.command_handlers import push as handlers
from loom_checker.rule_checks import push as recognisers

MERGE = "gh pr merge 1"
PUSH = "git push origin HEAD"


# --------------------------------------------------------------------------
# 1. The heredoc carve-out. A body nothing in its pipeline executes is dropped
#    before recognition and reaches no rule at all.
# --------------------------------------------------------------------------


def test_cat_heredoc_body_is_document_content() -> None:
    """closed -- `cat <<EOF` prints its body; nothing is published. This is the
    false positive the change exists to remove."""
    assert not handlers.contains_pr_merge(f"cat <<EOF\n{MERGE}\nEOF")
    assert not handlers.contains_pr_merge(f"cat <<EOF > /tmp/doc.md\n{MERGE}\nEOF")


def test_heredoc_piped_into_a_shell_is_seen() -> None:
    """closed -- `cat` does not execute the body but the pipe hands it to bash,
    which does."""
    assert handlers.contains_pr_merge(f"cat <<EOF | bash\n{MERGE}\nEOF")
    assert recognisers.is_push_command(f"cat <<EOF | bash\n{PUSH}\nEOF")


def test_shell_further_down_the_pipeline_is_seen() -> None:
    """closed -- the executing member need not be the second."""
    command = f"cat <<EOF | tr a-z a-z | bash\n{MERGE}\nEOF"

    assert handlers.contains_pr_merge(command)


def test_heredoc_piped_through_tee_is_seen() -> None:
    """closed -- any non-shell command word in front of the pipe."""
    command = f"tee /dev/null <<EOF | bash\n{MERGE}\nEOF"

    assert handlers.contains_pr_merge(command)


def test_quoted_delimiter_does_not_hide_the_pipe() -> None:
    """closed -- `EO'F'` is the literal EOF to a shell."""
    command = f"cat <<EO'F' | bash\n{MERGE}\nEOF"

    assert handlers.contains_pr_merge(command)


def test_source_dev_stdin_executes_its_heredoc_body() -> None:
    """OPEN -- `source` is not in SHELL_PROGRAMS, and no pipeline member is, so
    the body is carved out as document content. Real bash runs the merge."""
    command = f"source /dev/stdin <<EOF\n{MERGE}\nEOF"

    assert handlers.contains_pr_merge(command)


def test_dot_dev_stdin_executes_its_heredoc_body() -> None:
    """OPEN -- the `.` spelling of the same builtin."""
    command = f". /dev/stdin <<EOF\n{MERGE}\nEOF"

    assert handlers.contains_pr_merge(command)


def test_source_dev_stdin_executes_a_push() -> None:
    """OPEN -- and it carries a push just as well."""
    command = f"source /dev/stdin <<EOF\n{PUSH}\nEOF"

    assert recognisers.is_push_command(command)


def test_wrapper_value_options_before_a_shell_heredoc_are_spent() -> None:
    """closed -- the prefix is read with the wide `_strip_merge_prefix`, so
    `sudo -u <user>` and `nice -n <level>` do not hide the shell behind them."""
    assert handlers.contains_pr_merge(f"sudo -u me sh <<EOF\n{MERGE}\nEOF")
    assert handlers.contains_pr_merge(f"nice -n 10 bash <<EOF\n{MERGE}\nEOF")


def test_plain_wrappers_before_a_shell_heredoc_are_seen() -> None:
    """closed."""
    assert handlers.contains_pr_merge(f"env bash <<EOF\n{MERGE}\nEOF")
    assert handlers.contains_pr_merge(f"xargs bash <<EOF\n{MERGE}\nEOF")


def test_bare_shell_heredoc_is_seen() -> None:
    """closed -- the plain executing form, merge and push."""
    assert handlers.contains_pr_merge(f"bash <<EOF\n{MERGE}\nEOF")
    assert recognisers.is_push_command(f"bash <<EOF\n{PUSH}\nEOF")


def test_bare_heredoc_with_no_command_word_stays_conservative() -> None:
    """OPEN as the branch's own suite defines it -- `_heredoc_executes_body` is
    now handed the whole logical line, so for `<<EOF` the command word it reads
    is the `<<EOF` operator itself rather than the empty string that used to
    mean "no command word, the shell reads it". This is what makes the branch's
    existing `test_every_shell_interpreter_heredoc_form_stays_recognised` fail.

    A real bash runs nothing here (`<<EOF\\ncmd\\nEOF` is a redirection with no
    command, verified), so the fix may be either restoring the conservative read
    or amending that test -- but the two cannot both stand as they are."""
    command = f"<<EOF\n{PUSH}\nEOF\n"

    assert recognisers.is_push_command(command)


def test_heredoc_inside_command_substitution_fails_closed() -> None:
    """closed -- the prefix is an assignment, which reads as executing."""
    command = f"x=$(bash <<EOF\n{MERGE}\nEOF\n)"

    assert handlers.contains_pr_merge(command)


def test_command_substitution_around_a_cat_heredoc_fails_closed() -> None:
    """closed -- `eval "$(cat <<EOF ...)"` does run the body."""
    command = f'eval "$(cat <<EOF\n{MERGE}\nEOF\n)"'

    assert handlers.contains_pr_merge(command)


def test_dash_heredoc_stripping_tabs_is_seen() -> None:
    """closed -- `<<-` strips tabs, exactly as a shell does."""
    command = f"bash <<-EOF\n\t{MERGE}\n\tEOF"

    assert handlers.contains_pr_merge(command)


def test_dash_heredoc_indented_with_spaces_fails_closed() -> None:
    """closed -- a shell finds no terminator either (only tabs are stripped),
    and an unterminated body makes the whole pass fail toward judging."""
    command = f"bash <<-EOF\n  {MERGE}\n  EOF"

    assert handlers.contains_pr_merge(command)


def test_unterminated_heredoc_fails_closed() -> None:
    """closed -- no terminator line, so nothing is carved."""
    assert handlers.contains_pr_merge(f"cat <<EOF\n{MERGE}\n")


def test_crlf_heredoc_fails_closed() -> None:
    """closed -- the carriage return lands in the delimiter on both sides."""
    command = f"cat <<EOF | bash\r\n{MERGE}\r\nEOF\r\n"

    assert handlers.contains_pr_merge(command)


def test_heredoc_operator_inside_quotes_is_literal_text() -> None:
    """closed -- a shell opens no heredoc inside quotes, and neither does the
    carve-out; the text is judged as the argument it is."""
    assert not handlers.contains_pr_merge('echo "a << EOF b"')


def test_two_heredocs_on_one_line_are_read_in_order() -> None:
    """closed -- the non-executing body is dropped and the executing one is
    judged, in the order a shell reads them."""
    command = f"cat <<A; bash <<B\ndocument text\nA\n{MERGE}\nB"

    assert handlers.contains_pr_merge(command)


def test_a_documenting_heredoc_beside_a_script_heredoc_stays_content() -> None:
    """closed -- resolving each body against its own pipeline, not the whole
    line, keeps the `cat` body content while the `bash` body is judged."""
    command = (
        "cat <<A > /tmp/doc.md; bash <<B\n"
        "we merged the pr with gh\nA\necho ok\nB"
    )

    assert not handlers.contains_pr_merge(command)


def test_python_heredoc_printing_the_words_is_not_a_merge() -> None:
    """closed -- python prints the string; no shell runs it."""
    command = f"python3 - <<EOF\nprint('{MERGE}')\nEOF"

    assert not handlers.contains_pr_merge(command)


# --------------------------------------------------------------------------
# 2. Herestrings. `<<<` is skipped by the carve-out, and no recogniser reads
#    the string a shell interpreter runs from it.
# --------------------------------------------------------------------------


def test_herestring_into_a_shell_still_merges() -> None:
    """OPEN -- `bash <<<'<merge>'` runs the merge; the hook sees no script."""
    assert handlers.contains_pr_merge(f"bash <<<'{MERGE}'")
    assert handlers.contains_pr_merge(f"sh -s <<<'{MERGE}'")


def test_herestring_into_a_shell_still_pushes() -> None:
    """OPEN, but pre-existing -- main allows this one too."""
    assert recognisers.is_push_command(f"bash <<<'{PUSH}'")


# --------------------------------------------------------------------------
# 3. `_shell_c_argument` and the `-c` script.
# --------------------------------------------------------------------------


def test_shell_c_with_end_of_options_still_merges() -> None:
    """OPEN -- bash reads `--` as end-of-options and runs the *next* word as
    the `-c` script; `_shell_c_argument` returns the `--` itself and recurses
    into it."""
    assert handlers.contains_pr_merge(f"bash -c -- '{MERGE}'")
    assert handlers.contains_pr_merge(f"sh -c -- '{MERGE}'")


def test_shell_c_with_end_of_options_still_pushes() -> None:
    """OPEN, but pre-existing -- main allows this one too."""
    assert recognisers.is_push_command(f"bash -c -- '{PUSH}'")


def test_bundled_short_options_before_c_are_seen() -> None:
    """closed -- this is what `_shell_c_argument` was widened for."""
    assert handlers.contains_pr_merge(f"bash -lc '{MERGE}'")
    assert handlers.contains_pr_merge(f"bash -euxc '{MERGE}'")


def test_long_option_with_a_value_before_c_is_seen() -> None:
    """closed -- `--rcfile` is skipped as a long option, so the `-c` after it
    is the one found."""
    command = f"bash --rcfile /dev/null -c '{MERGE}'"

    assert handlers.contains_pr_merge(command)


def test_shell_c_as_the_last_token_names_no_script() -> None:
    """closed -- nothing to recurse into, and nothing runs."""
    assert not handlers.contains_pr_merge("bash -c")


# --------------------------------------------------------------------------
# 4. `_strip_merge_prefix` and the wrapper option table.
# --------------------------------------------------------------------------


def test_sudo_non_interactive_still_merges() -> None:
    """OPEN -- `WRAPPER_VALUE_OPTIONS` is one table applied to every wrapper,
    so xargs's `-n <count>` makes sudo's valueless `-n` eat the `gh`."""
    assert handlers.contains_pr_merge(f"sudo -n {MERGE}")


def test_sudo_shell_flag_still_merges() -> None:
    """OPEN -- the same collision between xargs's `-s <size>` and sudo's `-s`."""
    assert handlers.contains_pr_merge(f"sudo -s {MERGE}")


def test_sudo_with_its_real_value_option_is_seen() -> None:
    """closed -- `sudo -u <user>` really does spend two tokens."""
    assert handlers.contains_pr_merge(f"sudo -u me {MERGE}")


def test_sudo_preserve_env_is_seen() -> None:
    """closed -- `-E` is in no wrapper table, so it spends one token."""
    assert handlers.contains_pr_merge(f"sudo -E {MERGE}")


def test_xargs_and_nice_wrappers_are_seen() -> None:
    """closed -- the wrappers the widening was written for."""
    assert handlers.contains_pr_merge(f"xargs -n1 {MERGE}")
    assert handlers.contains_pr_merge(f"nice -n 10 {MERGE}")


def test_shell_grammar_does_not_hide_a_merge() -> None:
    """closed -- grammar words and grouping are skipped."""
    assert handlers.contains_pr_merge(f"if true; then {MERGE}; fi")
    assert handlers.contains_pr_merge(f"({MERGE})")
    assert handlers.contains_pr_merge(f"{{ {MERGE}; }}")


def test_backslash_continuation_is_joined() -> None:
    """closed -- the shell joins it before reading a command word."""
    assert handlers.contains_pr_merge("gh pr \\\nmerge 1")


# --------------------------------------------------------------------------
# 5. `_merge_word`.
# --------------------------------------------------------------------------


def test_ansi_c_and_locale_quoting_resolve_to_merge() -> None:
    """closed."""
    assert handlers.contains_pr_merge("gh pr $'merge' 1")
    assert handlers.contains_pr_merge('gh pr $"merge" 1')


def test_case_folding_resolves_to_merge() -> None:
    """closed -- gh matches its own subcommands case-insensitively, and a
    case-insensitive filesystem runs GH as gh."""
    assert handlers.contains_pr_merge("GH PR MERGE 1")


def test_an_expansion_named_merge_fails_closed() -> None:
    """closed -- `_merge_word` drops the leading `$`, so a variable that happens
    to be spelled `merge` lands on the word and refuses."""
    assert handlers.contains_pr_merge("gh pr $merge 1")


def test_an_expansion_under_any_other_name_still_merges() -> None:
    """OPEN, but pre-existing -- `m=merge; gh pr $m 1` runs the merge in a real
    bash, and both this branch and main allow it. `_merge_word`'s docstring
    claims an expansion in the subcommand slot is the fail-closed direction;
    that holds only for the one name `merge`. Recorded because the claim is
    wider than the behaviour, not because the change caused it."""
    assert handlers.contains_pr_merge("m=merge; gh pr $m 1")


def test_naming_a_merge_is_not_merging_one() -> None:
    """closed -- the false positives the change exists to remove; none of these
    publishes anything."""
    assert not handlers.contains_pr_merge("echo 'gh pr merge is blocked'")
    assert not handlers.contains_pr_merge("grep -r 'gh pr merge' .")
    assert not handlers.contains_pr_merge("git commit -m 'gh pr merge notes'")


# --------------------------------------------------------------------------
# 6. The push recognisers, which the change was meant to leave alone.
# --------------------------------------------------------------------------


def test_direct_pushes_remain_refused() -> None:
    """closed."""
    for command in (
        PUSH,
        f"eval '{PUSH}'",
        f"zsh -c '{PUSH}'",
        "GIT push origin HEAD",
        "env GIT_DIR=/x git push origin HEAD",
    ):
        assert recognisers.is_push_command(command), command


def test_sudo_non_interactive_push_was_already_allowed() -> None:
    """OPEN, but pre-existing -- main allows this too, because the push
    recognisers keep the narrow `_strip_prefix` on purpose. Recorded so the
    hole is not mistaken for something this change introduced."""
    assert recognisers.is_push_command(f"sudo -n {PUSH}")
