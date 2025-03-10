#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LLM処理モジュール

LiteLLMを使用したLLMとの対話処理を管理します。
"""

import os
import re
from loguru import logger
from litellm import completion
from typing import Optional

class LLMHandler:
    """
    LLMとの対話を管理するクラス
    """
    def __init__(self, api_key: str, model_name: str):
        """
        初期化

        Args:
            api_key (str): Gemini APIキー
            model_name (str): 使用するモデル名
        """
        self.api_key = api_key
        self.model_name = model_name
        self.system_prompt = self._load_system_prompt()
        self.response_pattern = re.compile(r'<llm-response>(.*?)</llm-response>', re.DOTALL)

    def _load_system_prompt(self) -> str:
        """
        システムプロンプトをファイルから読み込みます。

        Returns:
            str: システムプロンプト
        """
        try:
            prompt_path = os.path.join('prompts', 'system.txt')
            if os.path.exists(prompt_path):
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                logger.warning('システムプロンプトファイルが見つかりません')
                return "あなたは丁寧で親切なアシスタントです。"
        except Exception as e:
            logger.error(f'システムプロンプトの読み込みに失敗しました: {e}')
            return "あなたは丁寧で親切なアシスタントです。"

    async def get_response(self, prompt: str) -> str:
        """
        プロンプトに対するLLMの応答を取得します。

        Args:
            prompt (str): ユーザーからのプロンプト

        Returns:
            str: LLMからの応答
        """
        try:
            if not self.api_key:
                return "APIキーが設定されていないため応答できません。"

            # システムプロンプトとユーザープロンプトを組み合わせる
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            # LiteLLMを使用してモデルにリクエスト送信
            response = completion(
                model=self.model_name,
                messages=messages
            )

            # レスポンスを取得し、モデル名を追加
            response_text = response.choices[0].message.content
            
            # <llm-response>タグ間のテキストを抽出
            match = self.response_pattern.search(response_text)
            if match:
                extracted_text = match.group(1).strip()
                logger.debug(f"正規表現で応答を抽出しました: {extracted_text[:100]}...")
                return f"{extracted_text}\n\n> 🤖 {self.model_name}"
            else:
                logger.warning("応答から<llm-response>タグを抽出できませんでした")
                return f"{response_text}\n\n> 🤖 {self.model_name}"
                
        except Exception as e:
            error_msg = f'LLMリクエスト中にエラーが発生しました: {e}'
            logger.error(error_msg)
            return f"応答の生成中にエラーが発生しました: {str(e)}"
