# 🤖 Minimal llm bot RURI

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

## 📋 必要条件

- Python 3.8以上
- Discordアカウントとボットトークン
- Gemini APIキー（Google AI Studioから取得）

## 📁 プロジェクト構成

```
minimal-llm-bot_ruri/
├── bot.py              # メインのボットコード
├── requirements.txt    # 依存パッケージリスト
├── .env.example        # 環境変数テンプレート
├── .env                # 環境変数設定ファイル（Gitで管理しない）
├── README.md           # プロジェクト説明書
└── logs/               # ログファイル保存ディレクトリ
```

## 🚀 セットアップと実行方法

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

4. `.env`ファイルの作成
```bash
cp .env.example .env
```

5. `.env`ファイルに必要なトークンを設定
```
DISCORD_TOKEN=あなたのDiscordボットトークン
GEMINI_API_KEY=あなたのGemini APIキー
```

6. ボットの起動
```bash
python bot.py
```

## 📚 使い方

1. ボットをDiscordサーバーに招待します
2. `@Bot 人工知能について教えて`のようにボットにメンションを付けてメッセージを送信します
3. ボットは新しいスレッドを作成し、Geminiモデルからの応答を表示します
4. 同じスレッド内で会話を続けることができます

## 🔧 カスタマイズ

- `.env`ファイルを編集して、ボットの設定を変更できます
- 他のLLMを使用したい場合は、`bot.py`内の`get_llm_response`関数を修正します
- loguruの設定を変更することで、ログの形式や保存方法をカスタマイズできます

## 🔑 環境変数

- `DISCORD_TOKEN`: Discord Botのトークン（必須）
- `GEMINI_API_KEY`: Gemini APIキー（必須）

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細はLICENSEファイルをご覧ください。

## 🙏 謝辞

- このプロジェクトは元のEcho Botをベースに拡張したものです
- [LiteLLM](https://github.com/BerriAI/litellm)チームの素晴らしいライブラリに感謝します
- Googleの[Gemini API](https://ai.google.dev/)を活用しています
