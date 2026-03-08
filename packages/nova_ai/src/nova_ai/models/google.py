"""
Google / Gemini 模型定义
"""

from typing import Dict
from .base import Model, ModelCost
from ..core.enums import KnownApi, KnownProvider


# Google / Gemini 模型定义
GOOGLE_MODELS = {
    # Gemini 2.0 系列
    "gemini-2.0-flash": Model(
        id="gemini-2.0-flash",
        name="Gemini 2.0 Flash",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.GOOGLE,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.1,
            output=0.4,
            cache_read=0.025,
            cache_write=0.0
        ),
        context_window=1048576,
        max_tokens=8192
    ),
    
    "gemini-2.0-flash-lite": Model(
        id="gemini-2.0-flash-lite",
        name="Gemini 2.0 Flash Lite",
        api=KnownApi.GOOGLE_GENERATIVE_AI,
        provider=KnownProvider.GOOGLE,
        base_url="https://generativelanguage.googleapis.com/v1beta",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.075,
            output=0.3,
            cache_read=0.01875,
            cache_write=0.0
        ),
        context_window=1048576,
        max_tokens=8192
    ),
    
    # Gemini 1.5 系列
    "gemini-1.5-pro": Model(
        id="gemini-1.5-pro",
        name="Gemini 1.5 Pro",
        api=KnownApi.GOOGLE_GENERATIVE_AI,
        provider=KnownProvider.GOOGLE,
        base_url="https://generativelanguage.googleapis.com/v1beta",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=1.25,
            output=5.0,
            cache_read=0.3125,
            cache_write=0.0
        ),
        context_window=2097152,
        max_tokens=8192
    ),
    
    "gemini-1.5-flash": Model(
        id="gemini-1.5-flash",
        name="Gemini 1.5 Flash",
        api=KnownApi.GOOGLE_GENERATIVE_AI,
        provider=KnownProvider.GOOGLE,
        base_url="https://generativelanguage.googleapis.com/v1beta",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.075,
            output=0.3,
            cache_read=0.01875,
            cache_write=0.0
        ),
        context_window=1048576,
        max_tokens=8192
    ),
    
    "gemini-1.5-flash-8b": Model(
        id="gemini-1.5-flash-8b",
        name="Gemini 1.5 Flash 8B",
        api=KnownApi.GOOGLE_GENERATIVE_AI,
        provider=KnownProvider.GOOGLE,
        base_url="https://generativelanguage.googleapis.com/v1beta",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.0375,
            output=0.15,
            cache_read=0.009375,
            cache_write=0.0
        ),
        context_window=1048576,
        max_tokens=8192
    ),
    
    # Gemini 1.0 Pro
    "gemini-1.0-pro": Model(
        id="gemini-1.0-pro",
        name="Gemini 1.0 Pro",
        api=KnownApi.GOOGLE_GENERATIVE_AI,
        provider=KnownProvider.GOOGLE,
        base_url="https://generativelanguage.googleapis.com/v1beta",
        reasoning=False,
        input_types=["text"],
        cost=ModelCost(
            input=0.5,
            output=1.5,
            cache_read=0.0,
            cache_write=0.0
        ),
        context_window=30720,
        max_tokens=2048
    ),
}


def get_google_model(model_id: str) -> Model:
    """通过ID获取Google模型"""
    if model_id not in GOOGLE_MODELS:
        raise KeyError(f"Google model not found: {model_id}")
    return GOOGLE_MODELS[model_id]


def list_google_models() -> Dict[str, Model]:
    """列出所有Google模型"""
    return GOOGLE_MODELS.copy()