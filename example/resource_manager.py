#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
S.U.M.E.R.A.G.I. Discord Bot リソース管理モジュール

AIに関する学習リソースを管理・提供するためのモジュール
"""

import os
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import discord
from discord.ext import commands

# ロギングの設定
logger = logging.getLogger("sumeragi-resource-manager")

# リソースデータを保存するディレクトリ
DATA_DIR = Path("data")
RESOURCES_FILE = DATA_DIR / "resources.yaml"

class ResourceManager(commands.Cog):
    """学習リソース管理を行うCog"""
    
    def __init__(self, bot):
        """初期化"""
        self.bot = bot
        self.resources: Dict[str, List[Dict[str, Any]]] = {}
        
        # データディレクトリが存在しない場合は作成
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents=True)
        
        # リソースデータをロード
        self.load_resources()
        
        # デフォルトリソースがない場合は作成
        if not self.resources:
            self.create_default_resources()
    
    def load_resources(self):
        """リソースデータをファイルから読み込む"""
        if not RESOURCES_FILE.exists():
            logger.info(f"リソースファイルが見つかりません: {RESOURCES_FILE}")
            self.resources = {}
            return
        
        try:
            with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
                self.resources = yaml.safe_load(f) or {}
                total_resources = sum(len(cat_resources) for cat_resources in self.resources.values())
                logger.info(f"{len(self.resources)}カテゴリ、合計{total_resources}件のリソースを読み込みました")
        except Exception as e:
            logger.error(f"リソースの読み込みに失敗しました: {e}")
            self.resources = {}
    
    def save_resources(self):
        """リソースデータをファイルに保存"""
        try:
            with open(RESOURCES_FILE, "w", encoding="utf-8") as f:
                yaml.dump(self.resources, f, allow_unicode=True, default_flow_style=False)
            
            total_resources = sum(len(cat_resources) for cat_resources in self.resources.values())
            logger.info(f"{len(self.resources)}カテゴリ、合計{total_resources}件のリソースを保存しました")
            return True
        except Exception as e:
            logger.error(f"リソースの保存に失敗しました: {e}")
            return False
    
    def create_default_resources(self):
        """デフォルトのリソースデータを作成"""
        self.resources = {
            "入門者向け": [
                {
                    "id": 1,
                    "title": "AI入門コース",
                    "url": "https://example.com/ai-intro",
                    "description": "AIの基本概念を学ぶための入門コース",
                    "difficulty": "初級",
                    "tags": ["AI", "入門", "基礎"]
                },
                {
                    "id": 2,
                    "title": "Python基礎",
                    "url": "https://example.com/python-basics",
                    "description": "AIプログラミングに必要なPythonの基礎を学ぶ",
                    "difficulty": "初級",
                    "tags": ["Python", "プログラミング", "基礎"]
                }
            ],
            "データサイエンス": [
                {
                    "id": 3,
                    "title": "データ分析入門",
                    "url": "https://example.com/data-science",
                    "description": "Pandasを使ったデータ分析の基礎",
                    "difficulty": "中級",
                    "tags": ["データ分析", "Pandas", "可視化"]
                },
                {
                    "id": 4,
                    "title": "統計学の基礎",
                    "url": "https://example.com/statistics",
                    "description": "AI開発に必要な統計学の知識",
                    "difficulty": "中級",
                    "tags": ["統計", "確率", "数学"]
                }
            ],
            "機械学習": [
                {
                    "id": 5,
                    "title": "機械学習基礎",
                    "url": "https://example.com/ml-basics",
                    "description": "scikit-learnを使った機械学習の基礎",
                    "difficulty": "中級",
                    "tags": ["機械学習", "分類", "回帰"]
                },
                {
                    "id": 6,
                    "title": "実践機械学習",
                    "url": "https://example.com/ml-practice",
                    "description": "実際のデータを使った機械学習の実践",
                    "difficulty": "上級",
                    "tags": ["機械学習", "実践", "ケーススタディ"]
                }
            ],
            "深層学習": [
                {
                    "id": 7,
                    "title": "ニューラルネットワーク入門",
                    "url": "https://example.com/nn-intro",
                    "description": "ニューラルネットワークの基本概念と実装",
                    "difficulty": "中級",
                    "tags": ["ニューラルネットワーク", "深層学習", "基礎"]
                },
                {
                    "id": 8,
                    "title": "DeepLearningチュートリアル",
                    "url": "https://example.com/dl-tutorial",
                    "description": "PyTorchを使った深層学習モデルの構築",
                    "difficulty": "上級",
                    "tags": ["深層学習", "PyTorch", "CNN", "RNN"]
                }
            ],
            "自然言語処理": [
                {
                    "id": 9,
                    "title": "NLP入門",
                    "url": "https://example.com/nlp-intro",
                    "description": "自然言語処理の基礎と実践",
                    "difficulty": "中級",
                    "tags": ["NLP", "テキスト処理", "感情分析"]
                },
                {
                    "id": 10,
                    "title": "Transformerモデル解説",
                    "url": "https://example.com/transformers",
                    "description": "BERTやGPTなどのTransformerモデルについて学ぶ",
                    "difficulty": "上級",
                    "tags": ["NLP", "Transformer", "BERT", "GPT"]
                }
            ]
        }
        
        self.save_resources()
    
    def get_next_id(self) -> int:
        """次のリソースIDを取得"""
        max_id = 0
        for category in self.resources.values():
            for resource in category:
                if resource.get("id", 0) > max_id:
                    max_id = resource["id"]
        return max_id + 1
    
    def get_resource_by_id(self, resource_id: int) -> Optional[Dict[str, Any]]:
        """指定IDのリソースを取得"""
        for category, resources in self.resources.items():
            for resource in resources:
                if resource.get("id") == resource_id:
                    return resource, category
        return None
    
    @commands.group(name="resource", aliases=["r"], invoke_without_command=True)
    async def resource_group(self, ctx):
        """リソース関連コマンドのベースグループ"""
        await ctx.send("リソース管理コマンド: `list`, `add`, `search`, `delete`, `update` があります。詳細は `!help resource` で確認できます。")
    
    @resource_group.command(name="list")
    async def list_resources(self, ctx, category=None):
        """リソース一覧を表示するコマンド
        
        カテゴリを指定するとそのカテゴリのリソースを表示します
        例: !resource list 機械学習
        """
        if not self.resources:
            await ctx.send("登録されているリソースはありません。")
            return
        
        if category and category in self.resources:
            # 特定カテゴリのリソースを表示
            embed = discord.Embed(
                title=f"📚 {category}リソース一覧",
                description=f"{category}に関する学習リソース（{len(self.resources[category])}件）",
                color=0x4a6baf
            )
            
            for resource in self.resources[category]:
                embed.add_field(
                    name=f"{resource['title']} [{resource.get('difficulty', '不明')}]",
                    value=f"{resource['description'][:100]}\n[リンク]({resource['url']})",
                    inline=False
                )
            
            embed.set_footer(text=f"S.U.M.E.R.A.G.I. リソース - {ctx.author.name}からのリクエスト")
            await ctx.send(embed=embed)
            
        elif category:
            # 指定されたカテゴリが存在しない場合
            categories = ", ".join(f"`{cat}`" for cat in self.resources.keys())
            await ctx.send(f"指定されたカテゴリ `{category}` は存在しません。利用可能なカテゴリ: {categories}")
            
        else:
            # カテゴリ一覧を表示
            embed = discord.Embed(
                title="📚 リソースカテゴリ一覧",
                description="各カテゴリをクリックすると詳細が表示されます",
                color=0x4a6baf
            )
            
            for category, resources in self.resources.items():
                resource_count = len(resources)
                embed.add_field(
                    name=f"{category} ({resource_count}件)",
                    value=f"`!resource list {category}` で詳細表示",
                    inline=True
                )
            
            embed.set_footer(text=f"S.U.M.E.R.A.G.I. リソース - {datetime.now().strftime('%Y-%m-%d')}")
            await ctx.send(embed=embed)
    
    @resource_group.command(name="add")
    @commands.has_permissions(administrator=True)
    async def add_resource(self, ctx, category, title, url, *, description):
        """新しいリソースを追加するコマンド
        
        例: !resource add 機械学習 "強化学習入門" https://example.com/rl-intro 強化学習の基本概念と実装方法について学ぶ
        """
        # カテゴリが存在しない場合は作成
        if category not in self.resources:
            self.resources[category] = []
        
        # 新しいリソースを作成
        new_resource = {
            "id": self.get_next_id(),
            "title": title,
            "url": url,
            "description": description,
            "difficulty": "中級",  # デフォルト値
            "tags": [category],
            "added_by": str(ctx.author.id),
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # リソースリストに追加
        self.resources[category].append(new_resource)
        
        # 保存
        if self.save_resources():
            embed = discord.Embed(
                title="✅ リソース追加完了",
                description=f"カテゴリ「{category}」に新しいリソースを追加しました",
                color=0x4a6baf
            )
            
            embed.add_field(name="タイトル", value=title, inline=True)
            embed.add_field(name="URL", value=url, inline=True)
            embed.add_field(name="説明", value=description, inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ リソースの追加に失敗しました。")
    
    @resource_group.command(name="search")
    async def search_resources(self, ctx, *, query):
        """リソースを検索するコマンド
        
        例: !resource search 機械学習 入門
        """
        if not self.resources:
            await ctx.send("登録されているリソースはありません。")
            return
        
        query = query.lower()
        results = []
        
        # 全カテゴリから検索
        for category, resources in self.resources.items():
            for resource in resources:
                # タイトル、説明、タグを検索
                if (query in resource["title"].lower() or 
                    query in resource["description"].lower() or 
                    any(query in tag.lower() for tag in resource.get("tags", []))):
                    results.append((resource, category))
        
        if not results:
            await ctx.send(f"「{query}」に一致するリソースは見つかりませんでした。")
            return
        
        # 検索結果を表示
        embed = discord.Embed(
            title=f"🔍 「{query}」の検索結果",
            description=f"{len(results)}件のリソースが見つかりました",
            color=0x4a6baf
        )
        
        # 最大10件表示
        for resource, category in results[:10]:
            embed.add_field(
                name=f"[{category}] {resource['title']}",
                value=f"{resource['description'][:100]}\n[リンク]({resource['url']})",
                inline=False
            )
        
        if len(results) > 10:
            embed.set_footer(text=f"検索結果が多すぎるため、最初の10件のみ表示しています。検索キーワードを絞り込んでください。")
        else:
            embed.set_footer(text=f"S.U.M.E.R.A.G.I. リソース検索 - {datetime.now().strftime('%Y-%m-%d')}")
        
        await ctx.send(embed=embed)
    
    @resource_group.command(name="delete")
    @commands.has_permissions(administrator=True)
    async def delete_resource(self, ctx, resource_id: int):
        """リソースを削除するコマンド
        
        例: !resource delete 5
        """
        result = self.get_resource_by_id(resource_id)
        if not result:
            await ctx.send(f"ID: {resource_id} のリソースが見つかりません。")
            return
        
        resource, category = result
        
        # リソースの削除
        self.resources[category].remove(resource)
        
        # カテゴリが空になった場合は削除
        if not self.resources[category]:
            del self.resources[category]
        
        # 保存
        if self.save_resources():
            embed = discord.Embed(
                title="🗑️ リソース削除完了",
                description=f"リソース「{resource['title']}」を削除しました",
                color=0x4a6baf
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ リソースの削除に失敗しました。")
    
    @resource_group.command(name="update")
    @commands.has_permissions(administrator=True)
    async def update_resource(self, ctx, resource_id: int, field, *, new_value):
        """リソース情報を更新するコマンド
        
        例: !resource update 5 title 新しいタイトル
        例: !resource update 5 description 新しい説明文をここに入力
        例: !resource update 5 difficulty 上級
        """
        # 有効なフィールド
        valid_fields = ["title", "url", "description", "difficulty", "category"]
        
        if field not in valid_fields:
            await ctx.send(f"無効なフィールドです。有効なフィールド: {', '.join(valid_fields)}")
            return
        
        result = self.get_resource_by_id(resource_id)
        if not result:
            await ctx.send(f"ID: {resource_id} のリソースが見つかりません。")
            return
        
        resource, category = result
        
        # カテゴリの変更の場合
        if field == "category":
            # リソースを古いカテゴリから削除
            self.resources[category].remove(resource)
            
            # 新しいカテゴリが存在しない場合は作成
            if new_value not in self.resources:
                self.resources[new_value] = []
            
            # 新しいカテゴリに追加
            self.resources[new_value].append(resource)
            
            # カテゴリが空になった場合は削除
            if not self.resources[category]:
                del self.resources[category]
            
            old_value = category
        else:
            # その他のフィールドの更新
            old_value = resource.get(field, "未設定")
            resource[field] = new_value
            resource["updated_by"] = str(ctx.author.id)
            resource["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 保存
        if self.save_resources():
            embed = discord.Embed(
                title="📝 リソース更新完了",
                description=f"リソース「{resource['title']}」の{field}を更新しました",
                color=0x4a6baf
            )
            
            embed.add_field(name="変更前", value=old_value, inline=True)
            embed.add_field(name="変更後", value=new_value, inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ リソースの更新に失敗しました。")

# Cogのセットアップ関数
def setup(bot):
    """Cogをbotに追加する関数"""
    bot.add_cog(ResourceManager(bot))
