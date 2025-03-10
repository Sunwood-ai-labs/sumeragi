#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ロギング設定モジュール

このモジュールはアプリケーション全体のロギング設定を管理します。
"""

import os
import sys
from loguru import logger

def setup_logging():
    """
    アプリケーションのロギング設定を初期化します。
    コンソールとファイルの両方にログを出力します。
    """
    # logsディレクトリの作成
    os.makedirs('logs', exist_ok=True)

    # デフォルトのハンドラを削除
    logger.remove()

    # コンソールへのログ出力設定
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )

    # ファイルへのログ出力設定
    logger.add(
        "logs/litellm-bot.log",
        rotation="1 day",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        compression="zip",
        level="DEBUG",
        encoding="utf-8"
    )

    return logger
