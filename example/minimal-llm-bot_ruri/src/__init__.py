"""
RURIボット パッケージ

Discord上でLiteLLMを使用してGeminiモデルと対話するボットを実装します。
"""

from .bot import main
from .config import Config
from .llm_handler import LLMHandler
from . import logger

__version__ = '0.1.0'
__author__ = 'Sunwood AI Labs'
__license__ = 'MIT'

__all__ = ['main', 'Config', 'LLMHandler', 'logger']
