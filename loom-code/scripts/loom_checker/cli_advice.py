"""Optional CLI guidance, independent of checker dependencies and policy."""
from __future__ import annotations


def suggested_next(command: str, category: str) -> str | None:
    if category == "passed":
        return {
            "publish": "Review the publication evidence and await human acceptance before merging.",
            "finalize-review": "Commit the generated verification evidence, then follow the authorized publication workflow.",
        }.get(command)
    if category == "global":
        return "Inspect global --help and select a supported command before deliberately rerunning."
    if category == "internal":
        return "Investigate the reported failure and preserve outstanding work; no reliable repair is known."
    if category == "usage":
        if command == "reviewer-count":
            return "Inspect the diagnostic and command help; select the intended repository, preserve outstanding work and establish a clean completed change before deliberately rerunning."
        return "Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning."
    if category == "blocked":
        return {
            "contract": "Update the plugin identified by the contract diagnostic, then recheck supported requirements.",
            "intent": "Resolve the reported intent requirements with the intent owner; obtain any missing confirmation before continuing.",
            "intents": "Inspect the reported remote-default evidence and preserve indeterminate intent states until delivery can be confirmed.",
            "intake": "Restore the reported station prerequisites through their owning workflow and obtain any missing human confirmation before continuing.",
            "push": "Preserve existing work and hook ownership; resolve the reported protection or origin condition before deliberately rerunning.",
            "publish": "Follow the reported publication prerequisite or remedy; reconcile ambiguous remote effects with delivery before deliberately rerunning.",
            "land": "Follow the reported merge or cleanup remedy, preserve work and existing acceptance, and reconcile remote effects before deliberately rerunning.",
            "sync-trunk": "Preserve outstanding work and resolve the reported trunk condition before deliberately rerunning the existing sync workflow.",
            "standing": "Resolve the reported standing-document requirement through its owner before continuing; do not invent approval or alter waivers.",
            "charter": "Inspect the reported manifest or charter row and correct it at its source before deliberately rerunning.",
            "plan": "Resolve the reported plan requirements through the planning workflow before deliberately rerunning.",
            "pr-floor": "Correct the reported PR body requirements before deliberately rerunning; do not treat verification notices as approval.",
            "finalize-review": "Resolve the reported review or execution evidence through its owning workflow before deliberately rerunning finalization.",
        }.get(command, "Inspect the reported condition and resolve its prerequisites before deliberately rerunning.")
    return "Inspect the original diagnostic and command help; preserve outstanding work and investigate the reported condition before deliberately rerunning."


def write_suggestion(advice: str | None, stream) -> None:
    """Advice-only write failures cannot change an already determined outcome."""
    if isinstance(advice, str) and advice.strip():
        try:
            stream.write(f"Suggested next step: {advice}\n")
        except (OSError, UnicodeError):
            pass
