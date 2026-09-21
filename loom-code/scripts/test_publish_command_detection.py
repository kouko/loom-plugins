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


# The text rule this replaced matched three words anywhere in the command text.
# Built by concatenation so this file's own source carries no command such a
# rule would have matched -- which is the defect these tests pin.
MERGE = "gh" + " pr merge"


WRAPPED_MERGES = [
    "if true; then " + MERGE + " 1; fi",
    "( " + MERGE + " 1 )",
    "{ " + MERGE + " 1; }",
    "sudo -u bob " + MERGE + " 1",
    "echo 1 | xargs -n1 " + MERGE,
]


MERGE_MENTIONS = [
    "echo 'run " + MERGE + " --squash when ready'",
    "rg -n '" + MERGE + "' docs/",
    "git commit -m 'docs: explain " + MERGE + " --squash'",
    "man gh | grep -A2 'pr merge'",
    "cat > notes.md <<'EOF'\nTo land it run " + MERGE + " --squash\nEOF\n",
]


def test_a_wrapped_merge_is_recognised_structurally() -> None:
    # Only the removed text rule caught these shapes; the parse now does, so
    # dropping it costs no coverage of a merge that actually runs.
    for command in WRAPPED_MERGES:
        assert loom_checker.is_pr_merge_command(command), command


def test_text_naming_a_merge_is_not_a_merge_command() -> None:
    # A search, a printed string, a commit message and a document written
    # through a heredoc name the words without running one.
    for command in MERGE_MENTIONS:
        assert not loom_checker.is_pr_merge_command(command), command


def test_a_plain_merge_is_still_recognised() -> None:
    for command in (MERGE + " 12", MERGE + " 12 --squash", "time " + MERGE + " 1"):
        assert loom_checker.is_pr_merge_command(command), command
