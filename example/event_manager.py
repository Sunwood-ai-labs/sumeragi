#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
S.U.M.E.R.A.G.I. Discord Bot イベント管理モジュール

Discord上でのイベント管理を行うためのモジュール
"""

import os
import yaml
import logging
from datetime import datetime, timedelta
from pathlib import Path

import discord
from discord.ext import commands, tasks

# ロギングの設定
logger = logging.getLogger("sumeragi-event-manager")

# イベントデータを保存するディレクトリ
DATA_DIR = Path("data")
EVENTS_FILE = DATA_DIR / "events.yaml"

class EventManager(commands.Cog):
    """イベント管理を行うCog"""
    
    def __init__(self, bot):
        """初期化"""
        self.bot = bot
        self.events = []
        
        # データディレクトリが存在しない場合は作成
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents=True)
        
        # イベントデータをロード
        self.load_events()
        
        # イベント通知タスクを開始
        self.event_notification.start()
    
    def cog_unload(self):
        """Cogのアンロード時に呼ばれる処理"""
        self.event_notification.cancel()
    
    def load_events(self):
        """イベントデータをファイルから読み込む"""
        if not EVENTS_FILE.exists():
            logger.info(f"イベントファイルが見つかりません: {EVENTS_FILE}")
            self.events = []
            return
        
        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                self.events = yaml.safe_load(f) or []
                logger.info(f"{len(self.events)}件のイベントを読み込みました")
        except Exception as e:
            logger.error(f"イベントの読み込みに失敗しました: {e}")
            self.events = []
    
    def save_events(self):
        """イベントデータをファイルに保存"""
        try:
            with open(EVENTS_FILE, "w", encoding="utf-8") as f:
                yaml.dump(self.events, f, allow_unicode=True, default_flow_style=False)
            logger.info(f"{len(self.events)}件のイベントを保存しました")
            return True
        except Exception as e:
            logger.error(f"イベントの保存に失敗しました: {e}")
            return False
    
    @tasks.loop(hours=1)
    async def event_notification(self):
        """イベント通知を行うタスク"""
        now = datetime.now()
        
        for event in self.events:
            # イベント日時をパース
            event_date = datetime.strptime(event["date"], "%Y-%m-%d %H:%M")
            
            # イベント開始1日前と1時間前に通知
            time_diff = event_date - now
            
            # 過去のイベントはスキップ
            if time_diff.total_seconds() < 0:
                continue
                
            # 1日前の通知
            if timedelta(hours=23) < time_diff < timedelta(hours=25):
                await self.send_notification(event, "明日開催", "が明日開催されます！")
            
            # 1時間前の通知
            elif timedelta(minutes=55) < time_diff < timedelta(minutes=65):
                await self.send_notification(event, "間もなく開催", "が1時間後に開催されます！")
    
    async def send_notification(self, event, prefix, suffix):
        """イベント通知を送信"""
        # お知らせチャンネルを取得
        for guild in self.bot.guilds:
            announcement_channel = discord.utils.get(guild.text_channels, name="announcements")
            if announcement_channel:
                embed = discord.Embed(
                    title=f"📢 {prefix}: {event['name']}",
                    description=f"**{event['name']}**{suffix}",
                    color=0x4a6baf
                )
                
                embed.add_field(name="日時", value=event["date"], inline=True)
                embed.add_field(name="場所", value=event.get("location", "Discord"), inline=True)
                embed.add_field(name="詳細", value=event["description"], inline=False)
                
                if "url" in event and event["url"]:
                    embed.add_field(name="参加リンク", value=f"[こちらをクリック]({event['url']})", inline=False)
                
                embed.set_footer(text=f"S.U.M.E.R.A.G.I. イベント - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                
                await announcement_channel.send(embed=embed)
                logger.info(f"イベント通知を送信しました: {event['name']}")
    
    @commands.group(name="event", invoke_without_command=True)
    async def event_group(self, ctx):
        """イベント関連コマンドのベースグループ"""
        await ctx.send("イベント管理コマンド: `add`, `list`, `delete`, `update` があります。詳細は `!help event` で確認できます。")
    
    @event_group.command(name="add")
    @commands.has_permissions(administrator=True)
    async def add_event(self, ctx, name, date, *, description):
        """新しいイベントを追加するコマンド
        
        例: !event add "AIモデル構築ワークショップ" "2025-03-15 14:00" PyTorchを使った基本的なAIモデルの構築方法を学びます
        """
        # イベントデータの作成
        new_event = {
            "id": len(self.events) + 1,
            "name": name,
            "date": date,
            "description": description,
            "created_by": str(ctx.author.id),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # イベントリストに追加
        self.events.append(new_event)
        
        # 保存
        if self.save_events():
            embed = discord.Embed(
                title="✅ イベント追加完了",
                description=f"イベント「{name}」を追加しました",
                color=0x4a6baf
            )
            
            embed.add_field(name="日時", value=date, inline=True)
            embed.add_field(name="詳細", value=description, inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ イベントの追加に失敗しました。")
    
    @event_group.command(name="list")
    async def list_events(self, ctx):
        """登録されているイベント一覧を表示するコマンド"""
        if not self.events:
            await ctx.send("登録されているイベントはありません。")
            return
        
        # 現在の日時
        now = datetime.now()
        
        # 未来のイベントをフィルタリング
        future_events = []
        for event in self.events:
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d %H:%M")
                if event_date > now:
                    future_events.append((event, event_date))
            except ValueError:
                logger.warning(f"不正な日付形式: {event['date']}")
        
        # 日付順にソート
        future_events.sort(key=lambda x: x[1])
        
        # 最大5件表示
        embed = discord.Embed(
            title="📅 イベント一覧",
            description=f"今後予定されているイベント（{len(future_events)}件）",
            color=0x4a6baf
        )
        
        for event, event_date in future_events[:5]:
            embed.add_field(
                name=f"{event['date']} - {event['name']}",
                value=event['description'][:100] + ('...' if len(event['description']) > 100 else ''),
                inline=False
            )
        
        if len(future_events) > 5:
            embed.set_footer(text=f"他に{len(future_events) - 5}件のイベントがあります。全件表示するには「!event listall」を使用してください。")
        else:
            embed.set_footer(text=f"S.U.M.E.R.A.G.I. イベント - {datetime.now().strftime('%Y-%m-%d')}")
        
        await ctx.send(embed=embed)
    
    @event_group.command(name="delete")
    @commands.has_permissions(administrator=True)
    async def delete_event(self, ctx, event_id: int):
        """イベントを削除するコマンド"""
        # イベントの検索
        event_to_delete = None
        for event in self.events:
            if event.get("id") == event_id:
                event_to_delete = event
                break
        
        if not event_to_delete:
            await ctx.send(f"ID: {event_id} のイベントが見つかりません。")
            return
        
        # イベントの削除
        self.events.remove(event_to_delete)
        
        # 保存
        if self.save_events():
            embed = discord.Embed(
                title="🗑️ イベント削除完了",
                description=f"イベント「{event_to_delete['name']}」を削除しました",
                color=0x4a6baf
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ イベントの削除に失敗しました。")
    
    @event_group.command(name="update")
    @commands.has_permissions(administrator=True)
    async def update_event(self, ctx, event_id: int, field, *, new_value):
        """イベント情報を更新するコマンド
        
        例: !event update 1 date 2025-04-01 14:00
        例: !event update 1 description 新しい説明文をここに入力
        """
        # 有効なフィールド
        valid_fields = ["name", "date", "description", "location", "url"]
        
        if field not in valid_fields:
            await ctx.send(f"無効なフィールドです。有効なフィールド: {', '.join(valid_fields)}")
            return
        
        # イベントの検索
        event_to_update = None
        for event in self.events:
            if event.get("id") == event_id:
                event_to_update = event
                break
        
        if not event_to_update:
            await ctx.send(f"ID: {event_id} のイベントが見つかりません。")
            return
        
        # フィールドの更新
        old_value = event_to_update.get(field, "未設定")
        event_to_update[field] = new_value
        event_to_update["updated_by"] = str(ctx.author.id)
        event_to_update["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 保存
        if self.save_events():
            embed = discord.Embed(
                title="📝 イベント更新完了",
                description=f"イベント「{event_to_update['name']}」の{field}を更新しました",
                color=0x4a6baf
            )
            
            embed.add_field(name="変更前", value=old_value, inline=True)
            embed.add_field(name="変更後", value=new_value, inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ イベントの更新に失敗しました。")

# Cogのセットアップ関数
def setup(bot):
    """Cogをbotに追加する関数"""
    bot.add_cog(EventManager(bot))
