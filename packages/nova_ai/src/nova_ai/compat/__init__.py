"""
兼容性配置模块
包含不同API提供商的兼容性设置
"""

from .openai import OpenAICompletionsCompat, OpenAIResponsesCompat
from .routing import OpenRouterRouting, VercelGatewayRouting

__all__ = [
    "OpenAICompletionsCompat",
    "OpenAIResponsesCompat",
    "OpenRouterRouting",
    "VercelGatewayRouting",
]