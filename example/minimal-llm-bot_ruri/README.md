<div align="center">

![Minimal LLM Bot RURI](assets/header.svg)

# 🤖 Minimal llm bot RURI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3.2-blue?style=flat-square)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square)](https://www.docker.com/)

</div>

## 📝 概要

minimal-llm-bot_ruriは、メンションを受け取るとLiteLLMを通じてGeminiモデルからAI応答を生成し、スレッドで返信する最小構成のDiscord Botです。シンプルながらも強力なAI機能を備えたこのボットは、ユーザーからの質問や会話に対して、自然な応答を提供します。

## ✨ 機能

- メンションを含むメッセージを受信すると、LiteLLMを使用してGeminiモデルから応答を生成
- 応答はスレッド形式で提供され、会話の継続性を確保
- 応答生成中は「考え中です...」というメッセージを表示
- ボットのステータス設定（「質問 (LiteLLM with Gemini)」をリスニング中と表示）
- エラーハンドリングとロギング機能
- loguruを使用した高度なログ機能（コンソール出力とファイル出力）

## 🛠️ 技術スタック

- Python 3.8+
- discord.py: Discord API操作用ライブラリ
- LiteLLM: 複数のLLMプロバイダーに統一インターフェースを提供するライブラリ
- Gemini API: Google提供のAIモデル
- dotenv: 環境変数管理
- loguru: 高度なロギング機能
- Docker: コンテナ化と自動デプロイメント

## 📋 必要条件

- Python 3.8以上
- Discordアカウントとボットトークン
- Gemini APIキー（Google AI Studioから取得）
- Docker（オプション）

## 📁 プロジェクト構成

```
minimal-llm-bot_ruri/
├── src/                # ソースコードディレクトリ
│   ├── __init__.py
│   ├── bot.py         # メインのボット実装
│   ├── config.py      # 設定管理
│   ├── llm_handler.py # LLM処理
│   └── logger.py      # ログ設定
├── prompts/           # プロンプトテンプレート
│   └── system.txt
├── logs/             # ログファイル保存ディレクトリ
├── bot.py            # エントリーポイント
├── requirements.txt  # 依存パッケージリスト
├── .env.example     # 環境変数テンプレート
├── .env             # 環境変数設定（Gitで管理しない）
├── Dockerfile       # Dockerイメージ定義
├── docker-compose.yml # Docker Compose設定
└── README.md        # プロジェクト説明書
```

## 🚀 セットアップと実行方法

### 通常のセットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/your-username/minimal-llm-bot_ruri.git
cd minimal-llm-bot_ruri
```

2. 仮想環境の作成と有効化（オプション）
```bash
python -m venv venv
# Windowsの場合
venv\Scripts\activate
# macOS/Linuxの場合
source venv/bin/activate
```

3. 必要なパッケージのインストール
```bash
pip install -r requirements.txt
```

4. `.env`ファイルの設定
```bash
cp .env.example .env
# .envファイルを編集して必要な情報を設定
```

5. ボットの起動
```bash
python bot.py
```

### Dockerでの実行

1. `.env`ファイルの設定（上記と同様）

2. Dockerイメージのビルドと起動
```bash
docker-compose up --build -d
```

3. ログの確認
```bash
docker logs ruri-discord-bot -f
```

## 📚 使い方

1. ボットをDiscordサーバーに招待します
2. `@Bot 人工知能について教えて`のようにボットにメンションを付けてメッセージを送信します
3. ボットは新しいスレッドを作成し、Geminiモデルからの応答を表示します
4. 同じスレッド内で会話を続けることができます

## 🔧 カスタマイズ

- `.env`ファイルを編集して、ボットの設定を変更できます
- 他のLLMを使用したい場合は、`src/llm_handler.py`を修正します
- loguruの設定を変更することで、ログの形式や保存方法をカスタマイズできます

## 🔑 環境変数

- `DISCORD_TOKEN`: Discord Botのトークン（必須）
- `GEMINI_API_KEY`: Gemini APIキー（必須）
- `MODEL_NAME`: 使用するモデル名（デフォルト: gemini/gemini-pro）
- `USE_THREAD_REPLY`: スレッドでの返信を有効にするか（デフォルト: true）

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細はLICENSEファイルをご覧ください。

## 🙏 謝辞

- [LiteLLM](https://github.com/BerriAI/litellm)チームの素晴らしいライブラリに感謝します
- Googleの[Gemini API](https://ai.google.dev/)を活用しています
