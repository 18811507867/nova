"""
OpenAI 模型定义
"""

from typing import Dict, Any
from .base import Model, ModelCost
from ..core.enums import KnownApi, KnownProvider


# OpenAI 模型定义
VOLCENGINE_MODELS = {
    "deepseek-v3-2-251201": Model(
        id="deepseek-v3-2-251201",
        name="Deepseek-v3-2",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.VOLCENGINE,
        base_url="https://ark.cn-beijing.volces.com/api/v3/",
        reasoning=False,
        input_types=["text"],
        cost=ModelCost(
            input=2.0,
            output=8.0,
            cache_read=0.5,
            cache_write=0.0
        ),
        context_window=1047576,
        max_tokens=32768
    ),
    "deepseek-r1-250528": Model(
        id="deepseek-r1-250528",
        name="Deepseek-R1",
        api=KnownApi.OPENAI_COMPLETIONS,
        provider=KnownProvider.VOLCENGINE,
        base_url="https://ark.cn-beijing.volces.com/api/v3/",
        reasoning=True,
        input_types=["text"],
        cost=ModelCost(
            input=2.0,
            output=8.0,
            cache_read=0.5,
            cache_write=0.0
        ),
        context_window=1047576,
        max_tokens=32768
    ),
}


def get_volcengine_model(model_id: str) -> Model:
    """通过ID获取VOLCENGINE模型"""
    if model_id not in VOLCENGINE_MODELS:
        raise KeyError(f"OpenAI model not found: {model_id}")
    return VOLCENGINE_MODELS[model_id]


def list_volcengine_models() -> Dict[str, Model]:
    """列出所有VOLCENGINE模型"""
    return VOLCENGINE_MODELS.copy()