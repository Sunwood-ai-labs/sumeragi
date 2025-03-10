#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
設定モジュール

環境変数の読み込みと設定の管理を行います。
"""

import os
from dotenv import load_dotenv
from loguru import logger

class Config:
    """
    アプリケーションの設定を管理するクラス
    """
    def __init__(self):
        # スクリプトのあるフォルダの.envファイルを読み込む
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        load_dotenv(dotenv_path=env_path)
        logger.debug(f'環境変数を読み込みました: {env_path}')
        
        # Discord Token
        self.discord_token = os.getenv('DISCORD_TOKEN_RURI')
        if not self.discord_token:
            logger.error('DISCORD_TOKEN_RURIが設定されていません。.envファイルを確認してください。')
        
        # Gemini API Key
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not self.gemini_api_key:
            logger.warning('GEMINI_API_KEYが設定されていません。LLM機能は動作しません。')

        # モデル設定
        self.model_name = os.getenv('MODEL_NAME', 'gemini/gemini-pro')

        # スレッド使用設定
        self.use_thread_reply = self._parse_bool_env('USE_THREAD_REPLY', True)

    def _parse_bool_env(self, key: str, default: bool = False) -> bool:
        """
        環境変数から真偽値を取得します。

        Args:
            key (str): 環境変数のキー
            default (bool): デフォルト値

        Returns:
            bool: パースした真偽値
        """
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')

    @property
    def is_valid(self) -> bool:
        """
        設定が有効かどうかを確認します。

        Returns:
            bool: 必須の設定が揃っているかどうか
        """
        return bool(self.discord_token and self.gemini_api_key)
