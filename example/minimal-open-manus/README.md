<div align="center">

![OpenManus](assets/header.svg)

# 🤖 minimal-open-manus FUMIZUKI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-Latest-blue?logo=discord)](https://discordpy.readthedocs.io/)
[![OpenManus](https://img.shields.io/badge/OpenManus-Latest-green)](https://github.com/mannaandpoem/OpenManus)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue?logo=docker)](https://www.docker.com/)

</div>

## 📝 概要

minimal-open-manusは、OpenManusエージェントを利用したDiscordボットの最小構成実装です。メンションを受け取ると、OpenManusエージェントに問い合わせて結果を返信します。

## ✨ 機能

- OpenManusエージェントによる高度な対話処理
- メンションに対するスレッド形式での応答
- ボットのステータス設定
- シンプルなエラーハンドリング
- loguruを使用した高度なログ機能（コンソール出力とファイル出力）

## 🛠️ 必要条件

- Python 3.8以上
- Discordアカウントとボットトークン
- OpenManusのAPI設定

## 🚀 セットアップと実行方法

### Dockerを使用する場合

1. リポジトリをクローン
```bash
git clone https://github.com/Sunwood-ai-labs/sumeragi.git
cd sumeragi/example/minimal-open-manus
```

2. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集してDiscordトークンを設定
```

3. 設定ファイルの準備
```bash
cp config/config.example.toml config/config.toml
# config/config.tomlを編集してLLMの設定を行う
```

4. Dockerコンテナの起動
```bash
docker-compose up --build -d
```

### 直接実行する場合

1. リポジトリをクローン
```bash
git clone https://github.com/Sunwood-ai-labs/sumeragi.git
cd sumeragi/example/minimal-open-manus
```

2. 仮想環境の作成と有効化（推奨）
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

4. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集してDiscordトークンを設定
```

5. 設定ファイルの準備
```bash
cp config/config.example.toml config/config.toml
# config/config.tomlを編集してLLMの設定を行う
```

6. ボットの起動
```bash
python bot.py
```

## 📚 使い方

1. ボットをDiscordサーバーに招待します
2. `@FUMIZUKI こんにちは`のようにボットにメンションを付けてメッセージを送信します
3. OpenManusエージェントが応答を生成し、必要に応じて新しいスレッドで返信します

## 🔧 設定

### 環境変数 (.env)
- `DISCORD_TOKEN_FUMIZUKI`: Discord Botのトークン（必須）
- `USE_THREAD_REPLY`: スレッドでの返信を有効にするかどうか（true/false）

### OpenManus設定 (config/config.toml)
- LLMの種類とパラメータ
- APIキーと接続設定
- その他のOpenManus固有の設定

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](../../LICENSE)ファイルをご覧ください。
