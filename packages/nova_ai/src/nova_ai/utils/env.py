"""
环境变量工具函数
处理API密钥和认证信息的获取
"""

import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path

from ..core.enums import KnownProvider
from ..auth.vertex import has_vertex_adc_credentials
from ..auth.bedrock import has_bedrock_credentials


def get_env_api_key(provider: str) -> Optional[str]:
    """
    从已知的环境变量获取提供商的API密钥
    
    对于需要OAuth令牌的提供商不会返回API密钥
    
    Args:
        provider: 提供商名称
        
    Returns:
        API密钥或None
    """
    # GitHub Copilot 特殊处理
    if provider == "github-copilot":
        return (os.environ.get("COPILOT_GITHUB_TOKEN") or 
                os.environ.get("GH_TOKEN") or 
                os.environ.get("GITHUB_TOKEN"))
    
    # Anthropic: ANTHROPIC_OAUTH_TOKEN 优先于 ANTHROPIC_API_KEY
    if provider == "anthropic":
        return os.environ.get("ANTHROPIC_OAUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
    
    # Vertex AI 使用 Application Default Credentials，不是API密钥
    # 认证通过 `gcloud auth application-default login` 配置
    if provider == "google-vertex":
        if has_vertex_adc_credentials():
            has_project = bool(os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT"))
            has_location = bool(os.environ.get("GOOGLE_CLOUD_LOCATION"))
            
            if has_project and has_location:
                return "<authenticated>"
        return None
    
    # Amazon Bedrock 支持多种认证源
    if provider == "amazon-bedrock":
        if has_bedrock_credentials():
            return "<authenticated>"
        return None
    
    # 标准API密钥映射
    env_map = {
        "openai": "OPENAI_API_KEY",
        "azure-openai-responses": "AZURE_OPENAI_API_KEY",
        "google": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "cerebras": "CEREBRAS_API_KEY",
        "xai": "XAI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "vercel-ai-gateway": "AI_GATEWAY_API_KEY",
        "zai": "ZAI_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "minimax": "MINIMAX_API_KEY",
        "minimax-cn": "MINIMAX_CN_API_KEY",
        "huggingface": "HF_TOKEN",
        "opencode": "OPENCODE_API_KEY",
        "kimi-coding": "KIMI_API_KEY",
    }
    
    env_var = env_map.get(provider)
    return os.environ.get(env_var) if env_var else None


def get_env_api_key_typed(provider: KnownProvider) -> Optional[str]:
    """类型化的 get_env_api_key 版本"""
    return get_env_api_key(provider.value if hasattr(provider, 'value') else provider)


def get_all_env_api_keys() -> Dict[str, Optional[str]]:
    """获取所有已知提供商的环境变量值"""
    providers = [
        "github-copilot", "anthropic", "google-vertex", "amazon-bedrock",
        "openai", "azure-openai-responses", "google", "groq", "cerebras",
        "xai", "openrouter", "vercel-ai-gateway", "zai", "mistral",
        "minimax", "minimax-cn", "huggingface", "opencode", "kimi-coding"
    ]
    
    result = {}
    for provider in providers:
        value = get_env_api_key(provider)
        if value:
            # 隐藏实际密钥值，只显示是否存在
            result[provider] = "<set>" if value != "<authenticated>" else value
        else:
            result[provider] = None
    
    return result