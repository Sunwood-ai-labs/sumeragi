<div align="center">

![Image](https://github.com/user-attachments/assets/40ba8905-a516-4088-ab39-bdac14783f71)

# 🤖 Echo Bot

</div>

## 📝 概要

Echo Botは、メンションを受け取るとそのメッセージを返信するシンプルなDiscord Botです。このボットはDiscordサーバー内でのコミュニケーションを確認するための最小構成の実装例となっています。

## ✨ 機能

- メンションを含むメッセージを受信すると、その内容をそのままオウム返しします
- ボットのステータス設定
- シンプルなエラーハンドリング
- loguruを使用した高度なログ機能（コンソール出力とファイル出力）

## 🛠️ 技術スタック

- Python 3.8+
- discord.py: Discord API操作用ライブラリ
- dotenv: 環境変数管理
- loguru: 高度なロギング機能

## 📋 必要条件

- Python 3.8以上
- Discordアカウントとボットトークン

## 🚀 セットアップと実行方法

1. リポジトリをクローン
```bash
git clone https://github.com/Sunwood-ai-labs/sumeragi.git
cd sumeragi/example/echo-bot
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

5. `.env`ファイルにDiscord Botトークンを設定
```
DISCORD_TOKEN=あなたのボットトークン
```

6. ボットの起動
```bash
python bot.py
```

## 📚 使い方

1. ボットをDiscordサーバーに招待します
2. `@Echo Bot こんにちは`のようにボットにメンションを付けてメッセージを送信します
3. ボットは「こんにちは」とオウム返しします

## 🔑 環境変数

- `DISCORD_TOKEN`: Discord Botのトークン（必須）

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](../../LICENSE)ファイルをご覧ください。
