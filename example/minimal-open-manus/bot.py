#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Botモジュール

このモジュールはDiscordボットの機能を実装します。
メンションを受け取ると、Manusエージェントに問い合わせて結果を返信します。
"""

import os
import sys
import asyncio
from loguru import logger
import discord
from discord.ext import commands
from distutils.util import strtobool
from dotenv import load_dotenv

# Manusモジュールのインポート
from app.agent.manus import Manus

# ロギングの設定
logger.remove()  # デフォルトのハンドラを削除
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/manus-bot.log",
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

# Manusエージェントのインスタンスを作成
manus_agent = Manus()

@bot.event
async def on_ready():
    """
    ボットが起動して準備完了した時に呼び出されるイベントハンドラ
    """
    logger.info(f'{bot.user.name} としてログインしました')
    
    # ステータスを設定
    activity = discord.Activity(
        type=discord.ActivityType.listening, 
        name="OpenManus Minimal エージェント"
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
        use_thread = bool(strtobool(os.getenv('USE_THREAD_REPLY', 'true')))
        
        for mention in message.mentions:
            content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
        
        # 空白を整理
        content = content.strip()
        
        # 内容が空でなければメッセージを送信
        if content:
            try:
                # 処理中のメッセージを送信
                processing_msg = await message.channel.send("🔄 Manusに問い合わせ中です...")
                
                # スレッドの作成または取得
                if use_thread and not isinstance(message.channel, discord.Thread):
                    thread = await message.create_thread(
                        name=f"Manus: {content[:50]}",  # スレッド名は最初の50文字を使用
                        auto_archive_duration=60  # 60分で自動アーカイブ
                    )
                    target_channel = thread
                    logger.info(f'新しいスレッドを作成しました: {content[:50]}')
                else:
                    target_channel = message.channel
                
                # Manusエージェントを実行
                logger.info(f'Manusエージェントに問い合わせ: {content}')
                
                # Manusエージェントを実行して応答を取得
                try:
                    response = await manus_agent.run(content)
                except Exception as e:
                    logger.error(f'Manusエージェント実行中にエラー: {e}')
                    response = f"エラーが発生しました: {str(e)}"
                
                # 処理中メッセージを削除
                await processing_msg.delete()
                
                # 応答があれば送信
                if response:
                    # Discord APIのメッセージ長の制限（2000文字）を考慮
                    if len(response) <= 2000:
                        await target_channel.send(response)
                    else:
                        # 長いメッセージを分割して送信
                        chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                        for chunk in chunks:
                            await target_channel.send(chunk)
                            # 連続送信による制限回避のため少し待機
                            await asyncio.sleep(1)
                    
                    logger.info(f'Manusの回答を送信しました')
                else:
                    await target_channel.send("Manusから応答がありませんでした。")
                    logger.warning('Manusから空の応答が返されました')
                
            except Exception as e:
                error_msg = f'メッセージ処理中にエラーが発生しました: {e}'
                logger.error(error_msg)
                try:
                    await message.channel.send('メッセージの処理中にエラーが発生しました。')
                except:
                    logger.error('エラーメッセージの送信にも失敗しました。')
        else:
            await message.reply('こんにちは！Manusに質問したいことを送ってください。' + (' (スレッドモード有効)' if use_thread else ''))

def main():
    """
    メイン関数
    環境変数からトークンを取得し、ボットを起動します。
    """
    # logsディレクトリの作成
    os.makedirs('logs', exist_ok=True)
    
    token = os.getenv('DISCORD_TOKEN_FUMIZUKI')
    if not token:
        logger.error('DISCORD_TOKEN_FUMIZUKIが設定されていません。.envファイルを確認してください。')
        return
    
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        logger.error('ログインに失敗しました。トークンが正しいか確認してください。')
    except Exception as e:
        logger.error(f'ボット起動中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
