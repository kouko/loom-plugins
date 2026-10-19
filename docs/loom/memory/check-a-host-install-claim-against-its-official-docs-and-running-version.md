---
name: check-a-host-install-claim-against-its-official-docs-and-running-version
description: A host's interface or install claim must be checked against the host's official documentation and tried on the running version before it goes into install docs, because a key binding in the binary or a remembered UI is not evidence the user can reach it
type: gotcha
sources:
  - resource: branch engineering/2026-09-30-publish-checks-stated-verification-status (2026-09-30) — lesson from PR #70 (change 2026-09-29-opencode-v2-compatibility); TUI install route removed in commits bbf3738a / 61b46c87
---

PR #70's READMEs told OpenCode users to install through a TUI plugin
dialog opened with shift+i. The key binding exists in the OpenCode 2.0.20
binary, but no TUI screen exposes it, and the official docs
(https://opencode.ai/v2/docs/plugins/) list only `opencode plugin add` and
the `plugins` list in `opencode.json`. The maintainer caught it by trying
it; the step was removed in commits bbf3738a / 61b46c87 and the review
needed a third round.

**Why:** a binary string or a remembered UI is not evidence the user can
reach it.

**How to apply:** before writing any host install or interface step, cite
the official doc page for it and try it on the stated version. If the doc
and the binary disagree, write only what both support and disclose the
version.
