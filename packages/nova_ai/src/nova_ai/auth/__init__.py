"""
认证模块
处理各个提供商的认证逻辑
"""

from .vertex import has_vertex_adc_credentials
from .bedrock import has_bedrock_credentials

__all__ = [
    "has_vertex_adc_credentials",
    "has_bedrock_credentials",
]