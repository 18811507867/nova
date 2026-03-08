"""
OpenAI 模型定义
"""

from typing import Dict, Any
from .base import Model, ModelCost
from ..core.enums import KnownApi, KnownProvider


# OpenAI 模型定义
OPENAI_MODELS = {
    # GPT-4.1 系列
    "gpt-4.1": Model(
        id="gpt-4.1",
        name="GPT-4.1",
        api=KnownApi.OPENAI_RESPONSES,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=2.0,
            output=8.0,
            cache_read=0.5,
            cache_write=0.0
        ),
        context_window=1047576,
        max_tokens=32768
    ),
    
    "gpt-4.1-mini": Model(
        id="gpt-4.1-mini",
        name="GPT-4.1 Mini",
        api=KnownApi.OPENAI_RESPONSES,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.4,
            output=1.6,
            cache_read=0.1,
            cache_write=0.0
        ),
        context_window=1047576,
        max_tokens=32768
    ),
    
    "gpt-4.1-nano": Model(
        id="gpt-4.1-nano",
        name="GPT-4.1 Nano",
        api=KnownApi.OPENAI_RESPONSES,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=False,
        input_types=["text", "image"],
        cost=ModelCost(
            input=0.1,
            output=0.4,
            cache_read=0.025,
            cache_write=0.0
        ),
        context_window=1047576,
        max_tokens=32768
    ),
    
    # GPT-4 系列
    "gpt-4": Model(
        id="gpt-4",
        name="GPT-4",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=False,
        input_types=["text"],
        cost=ModelCost(
            input=30.0,
            output=60.0,
            cache_read=0.0,
            cache_write=0.0
        ),
        context_window=8192,
        max_tokens=4096
    ),
    
    "gpt-4-turbo": Model(
        id="gpt-4-turbo",
        name="GPT-4 Turbo",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=False,
        input_types=["text"],
        cost=ModelCost(
            input=10.0,
            output=30.0,
            cache_read=0.0,
            cache_write=0.0
        ),
        context_window=128000,
        max_tokens=4096
    ),
    
    # GPT-3.5 系列
    "gpt-3.5-turbo": Model(
        id="gpt-3.5-turbo",
        name="GPT-3.5 Turbo",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=False,
        input_types=["text"],
        cost=ModelCost(
            input=0.5,
            output=1.5,
            cache_read=0.0,
            cache_write=0.0
        ),
        context_window=16385,
        max_tokens=4096
    ),
    
    # o1 系列（推理模型）
    "o1": Model(
        id="o1",
        name="O1",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=True,
        input_types=["text"],
        cost=ModelCost(
            input=15.0,
            output=60.0,
            cache_read=0.0,
            cache_write=0.0
        ),
        context_window=200000,
        max_tokens=100000
    ),
    
    "o1-mini": Model(
        id="o1-mini",
        name="O1 Mini",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=True,
        input_types=["text"],
        cost=ModelCost(
            input=3.0,
            output=12.0,
            cache_read=0.0,
            cache_write=0.0
        ),
        context_window=128000,
        max_tokens=65536
    ),
    
    "o3-mini": Model(
        id="o3-mini",
        name="O3 Mini",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.OPENAI,
        base_url="https://api.openai.com/v1",
        reasoning=True,
        input_types=["text"],
        cost=ModelCost(
            input=1.0,
            output=4.0,
            cache_read=0.0,
            cache_write=0.0
        ),
        context_window=200000,
        max_tokens=100000
    ),
}


def get_openai_model(model_id: str) -> Model:
    """通过ID获取OpenAI模型"""
    if model_id not in OPENAI_MODELS:
        raise KeyError(f"OpenAI model not found: {model_id}")
    return OPENAI_MODELS[model_id]


def list_openai_models() -> Dict[str, Model]:
    """列出所有OpenAI模型"""
    return OPENAI_MODELS.copy()