#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Botモジュール

このモジュールはDiscordボットの機能を実装します。
メンションを受け取ると、そのメッセージをオウム返しするシンプルな機能を提供します。
"""

import os
import sys
from loguru import logger
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ロギングの設定
logger.remove()  # デフォルトのハンドラを削除
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/echo-bot.log",
    rotation="1 day",
    retention="7 days",
    compression="zip",
    level="DEBUG",
    encoding="utf-8"
)

# 環境変数のロード
load_dotenv()

# ボットの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容へのアクセス権を有効化
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """
    ボットが起動して準備完了した時に呼び出されるイベントハンドラ
    """
    logger.info(f'{bot.user.name} としてログインしました')
    
    # ステータスを設定
    activity = discord.Activity(
        type=discord.ActivityType.listening, 
        name="メンション"
    )
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    """
    メッセージを受信した時に呼び出されるイベントハンドラ
    
    Args:
        message: 受信したメッセージオブジェクト
    """
    # 自分のメッセージは無視
    if message.author == bot.user:
        return
    
    # ボットがメンションされた場合
    if bot.user.mentioned_in(message):
        # メンション以外のメッセージ内容を取得
        # ユーザーメンション (<@123456789>) を除去
        content = message.content
        for mention in message.mentions:
            content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
        
        # 空白を整理
        content = content.strip()
        
        # 内容が空でなければメッセージを送信
        if content:
            try:
                await message.reply(content)
                logger.info(f'メッセージを返信しました: {content}')
            except Exception as e:
                logger.error(f'メッセージ返信中にエラーが発生しました: {e}')
                await message.channel.send('メッセージの返信中にエラーが発生しました。')
        else:
            await message.reply('こんにちは！メッセージを送ってくれればオウム返しします。')
    
    # コマンド処理を行う（ボットのコマンドを追加する場合に必要）
    await bot.process_commands(message)

def main():
    """
    メイン関数
    環境変数からトークンを取得し、ボットを起動します。
    """
    # logsディレクトリの作成
    os.makedirs('logs', exist_ok=True)
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error('DISCORD_TOKENが設定されていません。.envファイルを確認してください。')
        return
    
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        logger.error('ログインに失敗しました。トークンが正しいか確認してください。')
    except Exception as e:
        logger.error(f'ボット起動中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
