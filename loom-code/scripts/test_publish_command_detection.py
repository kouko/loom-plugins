"""Regression coverage for publication command classification."""
from __future__ import annotations

from loom_checker.rule_checks import push as loom_checker


def test_quoted_rg_pattern_is_not_a_publisher() -> None:
    command = (
        'rg -n "SEGMENT_SPLIT|publisher&&gh pr create|gh pr merge" '
        "loom-code -g '*.py'"
    )

    assert not loom_checker.is_push_command(command)
    assert not loom_checker.is_pr_create_command(command)
    assert not loom_checker.is_pr_merge_command(command)


def test_real_publishers_remain_detected() -> None:
    commands = [
        "git push origin HEAD",
        "gh pr create --fill",
        "gh pr merge 123 --squash",
        "zsh -c 'git push origin HEAD'",
        "eval 'gh pr create --fill'",
    ]

    assert all(loom_checker.is_push_command(command) for command in commands)


def test_uppercase_program_names_remain_detected() -> None:
    # A case-insensitive filesystem (default macOS) resolves GIT/GH to git/gh.
    commands = [
        "GIT push origin HEAD",
        "/usr/bin/Git push origin HEAD",
        "GH pr create --fill",
        "ENV GIT push origin HEAD",
    ]

    assert all(loom_checker.is_push_command(command) for command in commands)
    assert loom_checker.is_pr_create_command("GH pr create --fill")
    assert loom_checker.is_pr_merge_command("Gh pr merge 1")


def test_unbalanced_quote_keeps_conservative_detection() -> None:
    assert loom_checker.is_push_command("rg -n 'needle|gh pr create")


def test_dynamic_command_substitution_keeps_conservative_detection() -> None:
    assert loom_checker.is_push_command('echo "$(git push origin HEAD)"')
    assert loom_checker.is_push_command('echo "$(gh pr create --fill)"')
    assert loom_checker.is_push_command('echo "`git push origin HEAD`"')
    assert loom_checker.is_push_command('echo "`gh pr create --fill`"')


def test_single_quoted_substitutions_remain_literal() -> None:
    commands = [
        "rg -n '`true | gh pr create --fill`' docs",
        "printf '%s\\n' '$(git push origin HEAD)'",
    ]

    assert not any(loom_checker.is_push_command(command) for command in commands)
    assert not any(
        loom_checker.is_pr_create_command(command) for command in commands
    )


def test_content_heredoc_body_is_not_a_publisher() -> None:
    # `cat` writes its body to a file; that body is content, exactly as it is
    # through a file-writing tool, so no recogniser may read it as a command.
    command = "cat <<'EOF' > notes.md\ngit push origin HEAD\nEOF\n"

    assert not loom_checker.is_push_command(command)
    assert not loom_checker.is_git_push_command(command)


def test_shell_heredoc_body_is_still_a_publisher() -> None:
    # A shell interpreter executes its body, so the body stays a command.
    command = "bash <<'EOF'\ngit push origin HEAD\nEOF\n"

    assert loom_checker.is_push_command(command)
    assert loom_checker.is_git_push_command(command)


def test_every_shell_interpreter_heredoc_form_stays_recognised() -> None:
    commands = [
        "bash <<EOF\ngit push origin HEAD\nEOF\n",
        "sh <<'EOF'\ngit push origin HEAD\nEOF\n",
        "bash -s <<EOF\ngit push origin HEAD\nEOF\n",
        "zsh <<EOF\ngit push origin HEAD\nEOF\n",
        "<<EOF\ngit push origin HEAD\nEOF\n",  # no command word: the shell reads it
    ]

    assert all(loom_checker.is_push_command(command) for command in commands)


def test_content_heredoc_spellings_are_all_content() -> None:
    commands = [
        "cat <<-EOF > notes.md\n\tgit push origin HEAD\n\tEOF\n",
        'cat <<"EOF" > notes.md\ngit push origin HEAD\nEOF\n',
        "cat <<\\EOF > notes.md\ngit push origin HEAD\nEOF\n",
        # Two heredocs on one line: the bodies follow their operators' order.
        "cat <<A <<B > notes.md\ngit push origin HEAD\nA\ngh pr create\nB\n",
    ]

    assert not any(loom_checker.is_push_command(command) for command in commands)
    assert not any(
        loom_checker.is_pr_create_command(command) for command in commands
    )


def test_a_herestring_opens_no_heredoc_body() -> None:
    # `<<<` takes its word inline, so the next line is an ordinary command.
    command = "cat <<<'notes' > notes.md\ngit push origin HEAD\n"

    assert loom_checker.is_push_command(command)


def test_a_quoted_heredoc_operator_opens_no_body() -> None:
    command = "echo '<<EOF'\ngit push origin HEAD\n"

    assert loom_checker.is_push_command(command)


def test_a_heredoc_body_starts_after_the_logical_line() -> None:
    # The shell joins the continuation, so the body is empty and the push runs.
    command = "echo <<EOF \\\n&& git push origin HEAD\nEOF\n"

    assert loom_checker.is_push_command(command)


def test_an_unlocatable_terminator_judges_the_unstripped_text() -> None:
    command = "cat <<'EOF' > notes.md\ngit push origin HEAD\n"

    assert loom_checker.is_push_command(command)
