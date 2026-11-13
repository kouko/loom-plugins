---
title: "Can CI prepare agy for local plugin validation without model credentials?"
type: loom-research
status: concluded
created: 2026-11-13
updated: 2026-11-13
change: 2026-11-13-retired-test-skips
tags:
  - loom/research
---

# agy installation for CI validation

## Question and scope
Can an Ubuntu GitHub runner install real Antigravity CLI and execute the existing local plugin validators without opening an agent session, supplying credentials, or making model requests? The local reference binary reports 1.3.3; the official installer serves a moving release.

## Method and rationale
Inspect official documentation and the actual Unix bootstrapper, then trace the repository test entry. This bounded feasibility check addresses installation support and separates it from unverified credential-free Linux execution. English and Japanese discovery queries led to the same official documentation; no third-party assertions are used.

## Findings
- Documented: Google provides a macOS/Linux CLI bootstrapper. Plugin validation is a shell command; marketplace installation is separately documented as requiring sign-in.
- Installer source observed on 2026-11-13: selects the Linux architecture manifest, requires a download URL and SHA512, verifies the payload before copying, and accepts `--dir`. There is no version-selection argument. Its final native shell setup command is followed by `|| true`, so exit zero alone does not establish readiness.
- Repository source: the three live validators invoke only `agy plugin validate <local-plugin-path>` and check exit status plus processed skill count. They do not open agent sessions.
- Official manifest observed: Linux amd64 version 1.5.8 has a fixed versioned payload URL and SHA512 below. Prefer this pinned artifact over executing the mutable bootstrapper; explicitly export PATH, inspect the version and execute the real local validator. No model credentials are justified.

## Evidence
- [Official quickstart](https://antigravity.google/docs/getting-started?tab=cli), CLI download section: supported bootstrap command and default binary path.
- [Official plugins documentation](https://antigravity.google/docs/plugins?tab=cli), CLI shell subcommands: local validation and separate marketplace sign-in condition.
- [Official installer source](https://antigravity.google/cli/install.sh), read as data, not executed. Snapshot at `/private/tmp/loom-agy-official-install.sh`, SHA256 `62966c07365423bd4dc209355060744058fb30d60f5323e2d360e39de64e5042`; relevant sections: argument parsing, platform manifest, checksum verification, native setup handoff.
- [Existing validator tests](../../../../tests/test_sync_codex_manifests.py), `test_agy_plugin_validate_accepts_committed_plugin`, inspected at confirmation commit ecddb23b175a133fc0d904aa8b557c844ba36d0a.
- Observed local command: `agy --version` returned `1.3.3`. No fresh Linux installation or credential-free Linux validator execution was performed during planning.

## Decision impact
Download the fixed official Linux amd64 1.5.8 artifact, verify its recorded SHA512 before extraction, explicitly export PATH and verify actual executable readiness before tests. Do not install the desktop application, authenticate, or open an agent session. Keep installation failures fatal; do not replace the CLI with a stub. A failed credential-free live run remains a reported limitation and an implementation decision to resolve from evidence.

The [official Linux amd64 manifest](https://antigravity-cli-auto-updater-974169037036.us-central1.run.app/manifests/linux_amd64.json), fetched 2026-11-13, identifies payload `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.5.8-4602374149505024/linux-x64/cli_linux_x64.tar.gz` and SHA512 `f08faaee588327dba8722bdc60f26a14f6915a8f2d756ed7959cde0a706d4e62fd9f831ab1a077dace5f947caaa6e851457df5023180bb8d3f54386804a3787f`. The payload was not downloaded or executed during planning. An initial guessed linux_x64 manifest returned 404; source inspection corrected the platform key to linux_amd64.

## Limitations and open questions
The latest manifest can change; the plan instead pins the observed versioned artifact and publisher SHA512. Record the observed version in CI logs; updates require explicit pin maintenance. Official documentation does not prove credential-free validation on this runner; actual CI must establish it. The temporary source snapshot is supporting local evidence, not a portable committed dependency.
