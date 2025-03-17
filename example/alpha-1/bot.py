#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
S.U.M.E.R.A.G.I. Discord Bot

AIコミュニティ「S.U.M.E.R.A.G.I.」のためのDiscord Botの基本実装
「Synergetic Unified Machine-learning Education Resource for Artificial General Intelligence」
"""

import os
import random
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks

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

# AI関連のトピックリスト
AI_TOPICS = [
    "機械学習", "深層学習", "自然言語処理", "コンピュータビジョン",
    "強化学習", "生成AI", "AIモデル", "ニューラルネットワーク",
    "データサイエンス", "倫理的AI", "AI応用", "トランスフォーマー",
    "大規模言語モデル", "AIと社会", "自律システム"
]

# ウェルカムメッセージ
WELCOME_MESSAGES = [
    "S.U.M.E.R.A.G.I.コミュニティへようこそ！AIの学びの旅を一緒に進めましょう。",
    "新しいメンバーの参加を歓迎します！何か質問があればいつでもどうぞ。",
    "AI学習コミュニティへようこそ。あなたの参加がコミュニティに新しい価値をもたらします。"
]

# BOTの起動時の処理
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
    status_update.start()

# ステータスの定期更新
@tasks.loop(minutes=30)
async def status_update():
    """Botのステータスを定期的に更新"""
    topic = random.choice(AI_TOPICS)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.studying,
            name=f"{topic} | !help"
        )
    )

# 新規メンバー参加時のウェルカムメッセージ
@bot.event
async def on_member_join(member):
    """新しいメンバーが参加した時に実行される処理"""
    welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if welcome_channel:
        embed = discord.Embed(
            title="🌟 新メンバー参加",
            description=random.choice(WELCOME_MESSAGES),
            color=0x4a6baf
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="メンバー名", value=member.mention, inline=True)
        embed.add_field(name="参加日時", value=member.joined_at.strftime("%Y-%m-%d %H:%M"), inline=True)
        embed.set_footer(text=f"S.U.M.E.R.A.G.I. - {datetime.now().strftime('%Y-%m-%d')}")
        
        await welcome_channel.send(embed=embed)

# メッセージに反応する処理
@bot.event
async def on_message(message):
    """メッセージに反応する処理"""
    # Botからのメッセージには反応しない
    if message.author == bot.user:
        return

    # メンションされたら反応
    if bot.user in message.mentions:
        await message.channel.send(f"{message.author.mention} こんにちは！何かお手伝いできることはありますか？`!help`でコマンド一覧を確認できます。")
    
    # コマンド処理を継続
    await bot.process_commands(message)

# ヘルプコマンド
@bot.command(name="help")
async def help_command(ctx):
    """ヘルプメニューを表示するコマンド"""
    embed = discord.Embed(
        title="S.U.M.E.R.A.G.I. Bot ヘルプ",
        description="AIコミュニティのためのコマンド一覧です",
        color=0x4a6baf
    )
    
    # コマンドリスト
    commands_list = [
        {"name": f"{PREFIX}help", "value": "このヘルプメニューを表示します"},
        {"name": f"{PREFIX}about", "value": "S.U.M.E.R.A.G.I.について説明します"},
        {"name": f"{PREFIX}topic", "value": "AIに関するランダムなトピックを提案します"},
        {"name": f"{PREFIX}resources", "value": "AIの学習リソースを表示します"},
        {"name": f"{PREFIX}events", "value": "予定されているイベントを表示します"}
    ]
    
    for cmd in commands_list:
        embed.add_field(name=cmd["name"], value=cmd["value"], inline=False)
    
    embed.set_footer(text=f"S.U.M.E.R.A.G.I. - {ctx.author.name}からのリクエスト")
    await ctx.send(embed=embed)

# Aboutコマンド
@bot.command(name="about")
async def about_command(ctx):
    """S.U.M.E.R.A.G.I.についての説明を表示するコマンド"""
    embed = discord.Embed(
        title="S.U.M.E.R.A.G.I.とは",
        description="「Synergetic Unified Machine-learning Education Resource for Artificial General Intelligence」の略称です",
        color=0x4a6baf
    )
    
    # 各頭字語の説明
    explanations = [
        {"name": "**S**ynergetic", "value": "相乗的な：メンバー同士やAIシステムが協力し合って相乗効果を生み出すコミュニティ"},
        {"name": "**U**nified", "value": "統一された：様々なAI技術や知識が体系的にまとめられている"},
        {"name": "**M**achine-learning", "value": "機械学習：AIの核となる技術に焦点を当てている"},
        {"name": "**E**ducation", "value": "教育：初心者に向けた学びの場を提供"},
        {"name": "**R**esource", "value": "リソース：有益な学習材料やツール、情報を提供するプラットフォーム"},
        {"name": "**A**rtificial", "value": "人工的な：人工知能に関するコミュニティ"},
        {"name": "**G**eneral", "value": "汎用的な：特定分野だけでなく幅広いAI技術や知識を扱う"},
        {"name": "**I**ntelligence", "value": "知能：AIの「知能」という側面に焦点"}
    ]
    
    for exp in explanations:
        embed.add_field(name=exp["name"], value=exp["value"], inline=False)
    
    embed.set_footer(text="「相乗効果を生み出す統一された機械学習教育リソースを通じて汎用人工知能について学べるコミュニティ」")
    await ctx.send(embed=embed)

# トピック提案コマンド
@bot.command(name="topic")
async def topic_command(ctx):
    """AIに関するランダムなトピックを提案するコマンド"""
    topic = random.choice(AI_TOPICS)
    
    embed = discord.Embed(
        title="🧠 AIトピック提案",
        description=f"今日の学習トピック: **{topic}**",
        color=0x4a6baf
    )
    embed.set_footer(text="このトピックについて話し合ってみましょう！")
    
    await ctx.send(embed=embed)

# リソース表示コマンド
@bot.command(name="resources")
async def resources_command(ctx):
    """AIの学習リソースを表示するコマンド"""
    embed = discord.Embed(
        title="📚 AI学習リソース",
        description="AIを学ぶための厳選されたリソース一覧",
        color=0x4a6baf
    )
    
    # リソースリスト
    resources = [
        {"name": "🔰 入門者向け", "value": "[AI入門コース](https://example.com/ai-intro)\n[Python基礎](https://example.com/python-basics)"},
        {"name": "📊 データサイエンス", "value": "[データ分析入門](https://example.com/data-science)\n[統計学の基礎](https://example.com/statistics)"},
        {"name": "🤖 機械学習", "value": "[機械学習基礎](https://example.com/ml-basics)\n[実践機械学習](https://example.com/ml-practice)"},
        {"name": "🧠 深層学習", "value": "[ニューラルネットワーク入門](https://example.com/nn-intro)\n[DeepLearningチュートリアル](https://example.com/dl-tutorial)"},
        {"name": "📝 自然言語処理", "value": "[NLP入門](https://example.com/nlp-intro)\n[Transformerモデル解説](https://example.com/transformers)"}
    ]
    
    for resource in resources:
        embed.add_field(name=resource["name"], value=resource["value"], inline=False)
    
    embed.set_footer(text="定期的に更新されます。提案は #resource-suggestions チャンネルへ")
    await ctx.send(embed=embed)

# イベント表示コマンド
@bot.command(name="events")
async def events_command(ctx):
    """予定されているイベントを表示するコマンド"""
    # 仮のイベントデータ
    upcoming_events = [
        {"name": "AIモデル構築ワークショップ", "date": "2025-03-15", "desc": "PyTorchを使った基本的なAIモデルの構築方法を学びます"},
        {"name": "自然言語処理勉強会", "date": "2025-03-22", "desc": "最新のNLPモデルについて議論する勉強会です"},
        {"name": "AI倫理ディスカッション", "date": "2025-04-05", "desc": "AIの倫理的な問題について考えるオープンディスカッション"}
    ]
    
    embed = discord.Embed(
        title="📅 今後のイベント",
        description="S.U.M.E.R.A.G.I.コミュニティの予定されているイベント一覧",
        color=0x4a6baf
    )
    
    for event in upcoming_events:
        embed.add_field(
            name=f"{event['date']} - {event['name']}",
            value=event['desc'],
            inline=False
        )
    
    embed.set_footer(text="イベントは予告なく変更される場合があります。#announcements チャンネルをご確認ください")
    await ctx.send(embed=embed)

# エラーハンドリング
@bot.event
async def on_command_error(ctx, error):
    """コマンドエラー時の処理"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"コマンドが見つかりません。`{PREFIX}help`でコマンド一覧を確認できます。")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"必要な引数が不足しています。`{PREFIX}help`で使い方を確認してください。")
    else:
        logger.error(f"エラーが発生しました: {error}")
        await ctx.send("コマンド実行中にエラーが発生しました。しばらくしてからもう一度お試しください。")

# メイン処理
def main():
    """メイン処理"""
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Botの起動に失敗しました: {e}")
        print("Botの起動に失敗しました。環境変数やネットワーク接続を確認してください。")

if __name__ == "__main__":
    main()
