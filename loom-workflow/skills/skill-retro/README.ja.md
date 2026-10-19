# skill-retro

[English](README.md) | **日本語** | [繁體中文](README.zh-TW.md)

複数の Claude Code と Codex セッションを分析し、インストール済み skill で繰り返し起きる問題を調べます。提案対象は指示、または対象 skill に直接関係する plugin の登録、読み込み、hook、同梱スクリプト、依存 connector です。振り返りはレビュー用の成果物だけを作り、採用した変更は別の実装フローに渡します。

旧コマンド名 `distill-sessions` は `skill-retro` に変更されました。運用上の規則は [SKILL.md](SKILL.md) を参照してください。

## 処理の流れ

1. `scripts/main.py` が対応するローカル記録を読み、観測できる摩擦の兆候を順位付けします。JSON は `top.json`、人が読むプレビューは stderr に出力します。
2. 選んだセッション由来の文章を外部の分析エージェントへ送る前に、明示的な同意を得ます。分析結果を `merged.json` に集め、元の session と対象 skill を保持します。
3. `scripts/propose.py` が対象ごとの提案を作ります。昇格には異なる二つの session が必要で、一つだけの観察は保留します。指示の項目には実在する SKILL.md 見出しが必要です。連携の項目には直接関係するソース位置が必要で、見出しを捏造しません。
4. 提案を確認し、選んだ変更を別の実装フローに渡します。この振り返りは変更を適用しません。

収集形式とホスト別の派遣手順は [runtime protocol](references/runtime-protocol.md) を参照してください。

## Installation

この skill は `loom-workflow` plugin に同梱されています。`loom` marketplace からインストールします。

```sh
# Claude Code
claude plugin marketplace add https://github.com/kouko/loom-plugins.git
claude plugin install loom-workflow@loom

# Codex
codex plugin marketplace add https://github.com/kouko/loom-plugins.git
codex plugin add loom-workflow@loom
```

改名を含むバージョンをインストールした後、Claude Code では `loom-workflow:skill-retro` を呼び、Codex では `skill-retro` の使用を指示します。旧名は呼び出し可能な別名ではありません。Python スクリプトは標準ライブラリのみを使用し、Python 3.11 以降が必要です。

## Quick start

repository のルートからローカルプレビューを実行します。この段階ではセッションデータを分析エージェントへ送信しません。

```sh
python3 loom-workflow/skills/skill-retro/scripts/main.py \
  --target-skill-pattern 'loom-code:*' > top.json
```

順位付けされた概要は stderr に表示されます。対象を確認し、分析エージェントへ渡す記録を明示的に承認します。[runtime protocol](references/runtime-protocol.md) に従って結果を `merged.json` に集め、レビュー用の文書を作ります。

```sh
python3 loom-workflow/skills/skill-retro/scripts/propose.py \
  --input merged.json \
  --target-skill /path/to/target/SKILL.md \
  --output proposals.md
```

`propose.py` は対象の SKILL.md を読み、`proposals.md` だけを書き込みます。連携のソースがない観察は `merged.json` に入れず、調査候補として示します。単一セッションの項目は保留します。

## Configuration

`main.py` は `--config /path/to/thresholds.json` で部分的な JSON 閾値設定を読み込みます。六つの閾値と意味は [runtime protocol](references/runtime-protocol.md#configuration-meanings) を参照してください。主な引数は次のとおりです。

- `--target-skill-pattern`（既定値 `loom-code:*`）
- `--top-n`（既定値 `5`）
- `--max-trajectories-per-skill`（既定値 `5`、派遣数で計算）
- `--project-root`（Claude のプロジェクト記録フォルダーを変更、主にテスト用）
- `--facets-root`（Claude `/insights` の facet フォルダーを変更、主にテスト用）

## ライセンス

この skill は [loom-plugins](https://github.com/kouko/loom-plugins) repository に含まれ、[MIT ライセンス](https://github.com/kouko/loom-plugins/blob/main/LICENSE) の対象です。

### 第三者帰属

`agents/` の失敗・成功分析 prompt は、Apache 2.0 で公開された [Trace2Skill](https://github.com/Qwen-Applications/Trace2Skill)（[論文](https://arxiv.org/abs/2603.25158)）を改作したものです。再配布時には上流の帰属を保持してください。
