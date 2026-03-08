"""
Anthropic 模型定义
"""

from typing import Dict
from .base import Model, ModelCost
from ..core.enums import KnownApi, KnownProvider


# Anthropic 模型定义
ANTHROPIC_MODELS = {
    # Claude 3.5 系列
    "claude-3-5-sonnet-latest": Model(
        id="claude-3-5-sonnet-latest",
        name="Claude 3.5 Sonnet",
        api=KnownApi.ANTHROPIC_MESSAGES,
        provider=KnownProvider.ANTHROPIC,
        base_url="https://api.anthropic.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=3.0,
            output=15.0,
            cache_read=0.3,
            cache_write=3.75
        ),
        context_window=200000,
        max_tokens=8192
    ),
    
    "claude-3-5-haiku-latest": Model(
        id="claude-3-5-haiku-latest",
        name="Claude 3.5 Haiku",
        api=KnownApi.ANTHROPIC_MESSAGES,
        provider=KnownProvider.ANTHROPIC,
        base_url="https://api.anthropic.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.8,
            output=4.0,
            cache_read=0.08,
            cache_write=1.0
        ),
        context_window=200000,
        max_tokens=8192
    ),
    
    # Claude 3 系列
    "claude-3-opus-latest": Model(
        id="claude-3-opus-latest",
        name="Claude 3 Opus",
        api=KnownApi.ANTHROPIC_MESSAGES,
        provider=KnownProvider.ANTHROPIC,
        base_url="https://api.anthropic.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=15.0,
            output=75.0,
            cache_read=1.5,
            cache_write=18.75
        ),
        context_window=200000,
        max_tokens=4096
    ),
    
    "claude-3-sonnet-latest": Model(
        id="claude-3-sonnet-latest",
        name="Claude 3 Sonnet",
        api=KnownApi.ANTHROPIC_MESSAGES,
        provider=KnownProvider.ANTHROPIC,
        base_url="https://api.anthropic.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=3.0,
            output=15.0,
            cache_read=0.3,
            cache_write=3.75
        ),
        context_window=200000,
        max_tokens=4096
    ),
    
    "claude-3-haiku-latest": Model(
        id="claude-3-haiku-latest",
        name="Claude 3 Haiku",
        api=KnownApi.ANTHROPIC_MESSAGES,
        provider=KnownProvider.ANTHROPIC,
        base_url="https://api.anthropic.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.25,
            output=1.25,
            cache_read=0.03,
            cache_write=0.3
        ),
        context_window=200000,
        max_tokens=4096
    ),
}


def get_anthropic_model(model_id: str) -> Model:
    """通过ID获取Anthropic模型"""
    if model_id not in ANTHROPIC_MODELS:
        raise KeyError(f"Anthropic model not found: {model_id}")
    return ANTHROPIC_MODELS[model_id]


def list_anthropic_models() -> Dict[str, Model]:
    """列出所有Anthropic模型"""
    return ANTHROPIC_MODELS.copy()