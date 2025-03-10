#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Discord Bot メインモジュール

Discordボットのメイン処理を実装します。
"""

import discord
from discord.ext import commands
from . import logger
from .config import Config
from .llm_handler import LLMHandler

# ロギングの設定
log = logger.setup_logging()

class RuriBot:
    """
    Discordボットのメインクラス
    """
    def __init__(self):
        """
        ボットの初期化
        """
        # 設定の読み込み
        self.config = Config()
        
        # Discordクライアントの設定
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        # LLMハンドラーの初期化
        self.llm = LLMHandler(
            api_key=self.config.gemini_api_key,
            model_name=self.config.model_name
        )
        
        # イベントハンドラーの設定
        self._setup_events()

    def _setup_events(self):
        """
        Discordイベントハンドラーを設定
        """
        @self.bot.event
        async def on_ready():
            """
            ボット起動時の処理
            """
            log.info(f'{self.bot.user.name} としてログインしました')
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name=f"質問受付中...  ({self.config.model_name})"
            )
            await self.bot.change_presence(activity=activity)

        @self.bot.event
        async def on_message(message):
            """
            メッセージ受信時の処理
            """
            # 自分のメッセージは無視
            log.debug(f'メッセージを受信: channel={message.channel.name}, author={message.author}, content={message.content}')
            if message.author == self.bot.user:
                log.debug('自身のメッセージなので無視します')
                return

            # メンションチェック
            is_mentioned = (
                self.bot.user.mentioned_in(message) or  # ユーザーメンション
                any(role.id == 1348600999094255659 for role in message.role_mentions)  # 特定のロールメンション
            )
            
            if is_mentioned and message.content.strip():
                log.debug(f'メンションを検出: channel_type={type(message.channel)}, is_thread={isinstance(message.channel, discord.Thread)}')
                await self._handle_mention(message)

            # コマンド処理
            await self.bot.process_commands(message)

    async def _handle_mention(self, message):
        """
        メンション時の処理
        """
        # メンション以外のメッセージ内容を取得
        content = message.content
        log.debug(f'元のメッセージ: {content}')
        
        # メンションの除去
        for mention in message.mentions:
            # ユーザーメンションを除去
            content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
        # ロールメンションを除去
        for role in message.role_mentions:
            content = content.replace(f'<@&{role.id}>', '')
            
        log.debug(f'メンション除去後: {content}')
        content = content.strip()

        if not content:
            await message.reply(f'こんにちは！質問や会話したいことを送ってください。LiteLLMを使って{self.config.model_name}が回答します。')
            return

        try:
            # 待機メッセージを送信
            log.debug('待機メッセージを送信します')
            waiting_msg = await message.reply("考え中です...しばらくお待ちください。")

            # LLMからの応答を取得
            log.debug('LLMに応答を要求します')
            llm_response = await self.llm.get_response(content)

            if isinstance(message.channel, discord.Thread):
                # スレッド内のメッセージの場合
                log.debug('スレッド内での応答を送信します')
                await message.channel.send(llm_response)
                log.info(f'スレッド内でLLM応答を送信しました: {content[:100]}...')
            elif self.config.use_thread_reply:
                # スレッド外かつスレッド返信が有効な場合
                thread = await message.create_thread(
                    name=f"Q: {content[:50]}",
                    auto_archive_duration=1440
                )
                await thread.send(llm_response)
                log.info(f'新しいスレッドを作成し応答を送信しました: {content[:100]}...')
            else:
                log.debug('チャンネルに直接応答を送信します')
                await message.channel.send(llm_response)
                log.info(f'チャンネルに直接応答を送信しました: {content[:100]}...')

            # 待機メッセージを削除
            await waiting_msg.delete()
            log.debug('待機メッセージを削除しました')

        except Exception as e:
            error_msg = f'メッセージ応答中にエラーが発生しました: {e}'
            log.error(error_msg)
            try:
                await message.channel.send('メッセージの応答中にエラーが発生しました。')
            except:
                log.error('エラーメッセージの送信にも失敗しました。')

    def run(self):
        """
        ボットを起動
        """
        if not self.config.is_valid:
            log.error('必要な設定が不足しているため、ボットを起動できません。')
            return

        try:
            self.bot.run(self.config.discord_token)
        except discord.errors.LoginFailure:
            log.error('ログインに失敗しました。トークンが正しいか確認してください。')
        except Exception as e:
            log.error(f'ボット起動中にエラーが発生しました: {e}')

def main():
    """
    メイン関数
    """
    bot = RuriBot()
    bot.run()

if __name__ == '__main__':
    main()
