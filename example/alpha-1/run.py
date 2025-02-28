#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
S.U.M.E.R.A.G.I. Discord Bot 起動スクリプト

「Synergetic Unified Machine-learning Education Resource for Artificial General Intelligence」
AIコミュニティのためのDiscord Bot
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

import discord
from discord.ext import commands

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("sumeragi-bot")

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX', '!')

# BOTのインテント設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Botのインスタンス生成
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Cogのリスト
cogs = [
    "event_manager",
    "resource_manager"
]

@bot.event
async def on_ready():
    """Botが起動した際に実行される処理"""
    logger.info(f"{bot.user.name} を起動しました（ID: {bot.user.id}）")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="AIの世界 | !help"
        )
    )
    
    # サーバー情報を表示
    guild_count = len(bot.guilds)
    guild_names = ", ".join([g.name for g in bot.guilds])
    logger.info(f"{guild_count}個のサーバーに接続中: {guild_names}")
    
    # 全コマンドを表示
    commands_list = [cmd.name for cmd in bot.commands]
    logger.info(f"登録されているコマンド: {', '.join(commands_list)}")

# Cogを読み込む
def load_cogs():
    """Cogを読み込む"""
    for cog in cogs:
        try:
            bot.load_extension(cog)
            logger.info(f"Cog '{cog}' を読み込みました")
        except Exception as e:
            logger.error(f"Cog '{cog}' の読み込みに失敗しました: {e}")

# メイン処理
def main():
    """メイン処理"""
    # Cogを読み込む
    load_cogs()
    
    # データディレクトリが存在しない場合は作成
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
        logger.info("データディレクトリを作成しました")
    
    # Botを起動
    try:
        logger.info("Botを起動しています...")
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Botの起動に失敗しました: {e}")
        print("Botの起動に失敗しました。環境変数やネットワーク接続を確認してください。")

if __name__ == "__main__":
    main()
