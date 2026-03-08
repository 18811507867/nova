# Compat 模块说明文档

## 概述

Compat 模块是 Nova AI SDK 的兼容性配置模块，用于处理不同 API 提供商之间的兼容性差异。该模块提供了针对不同 API 端点的兼容性设置和路由配置，确保 SDK 能够与各种 AI 服务提供商无缝集成。

## 目录结构

```
compat/
├── __init__.py          # 模块导出文件
├── openai.py           # OpenAI 兼容性配置
└── routing.py          # 路由配置（OpenRouter、Vercel Gateway）
```

## 模块导出

### 主要类

- `OpenAICompletionsCompat` - OpenAI Completions API 兼容性设置
- `OpenAIResponsesCompat` - OpenAI Responses API 兼容性设置（预留）
- `OpenRouterRouting` - OpenRouter 路由配置
- `VercelGatewayRouting` - Vercel AI Gateway 路由配置

## OpenAICompletionsCompat 类

### 类定义

```python
@dataclass
class OpenAICompletionsCompat:
    """
    OpenAI-compatible completions API 兼容性设置
    用于覆盖基于URL的自动检测
    """
```

### 属性说明

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `supports_store` | `Optional[bool]` | `None` | 是否支持 `store` 字段。默认基于URL自动检测 |
| `supports_developer_role` | `Optional[bool]` | `None` | 是否支持 `developer` 角色（vs `system`）。默认基于URL自动检测 |
| `supports_reasoning_effort` | `Optional[bool]` | `None` | 是否支持 `reasoning_effort`。默认基于URL自动检测 |
| `supports_usage_in_streaming` | `Optional[bool]` | `None` | 是否支持流式响应中的token使用统计。默认：true |
| `max_tokens_field` | `Optional[Literal["max_completion_tokens", "max_tokens"]]` | `None` | 用于max tokens的字段名。默认基于URL自动检测 |
| `requires_tool_result_name` | `Optional[bool]` | `None` | 工具结果是否需要 `name` 字段。默认基于URL自动检测 |
| `requires_assistant_after_tool_result` | `Optional[bool]` | `None` | 工具结果后的用户消息是否需要中间的助手消息。默认基于URL自动检测 |
| `requires_thinking_as_text` | `Optional[bool]` | `None` | 思考块是否需要转换为带`<thinking>`分隔符的文本块。默认基于URL自动检测 |
| `requires_mistral_tool_ids` | `Optional[bool]` | `None` | 工具调用ID是否需要规范化为Mistral格式（正好9个字母数字字符）。默认基于URL自动检测 |
| `thinking_format` | `ThinkingFormat` | `ThinkingFormat.OPENAI` | 推理/思考参数的格式。默认："openai" |
| `supports_strict_mode` | `Optional[bool]` | `None` | 是否支持工具定义中的 `strict` 字段。默认：true |

### ThinkingFormat 枚举

```python
class ThinkingFormat(str, Enum):
    """思考格式（用于不同提供商）"""
    OPENAI = "openai"      # 使用 reasoning_effort
    ZAI = "zai"            # 使用 thinking: { type: "enabled" }
    QWEN = "qwen"          # 使用 enable_thinking: boolean
```

## OpenAIResponsesCompat 类

### 类定义

```python
@dataclass
class OpenAIResponsesCompat:
    """
    OpenAI Responses API 兼容性设置
    预留供将来使用
    """
    pass
```

## OpenRouterRouting 类

### 类定义

```python
@dataclass
class OpenRouterRouting:
    """
    OpenRouter 提供商路由偏好设置
    控制OpenRouter将请求路由到哪些上游提供商
    
    @see https://openrouter.ai/docs/provider-routing
    """
```

### 属性说明

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `only` | `Optional[List[str]]` | `None` | 专门使用的提供商列表（例如 `["amazon-bedrock", "anthropic"]`） |
| `order` | `Optional[List[str]]` | `None` | 按顺序尝试的提供商列表（例如 `["anthropic", "openai"]`） |

## VercelGatewayRouting 类

### 类定义

```python
@dataclass
class VercelGatewayRouting:
    """
    Vercel AI Gateway 路由偏好设置
    控制网关将请求路由到哪些上游提供商
    
    @see https://vercel.com/docs/ai-gateway/models-and-providers/provider-options
    """
```

### 属性说明

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `only` | `Optional[List[str]]` | `None` | 专门使用的提供商列表（例如 `["bedrock", "anthropic"]`） |
| `order` | `Optional[List[str]]` | `None` | 按顺序尝试的提供商列表（例如 `["anthropic", "openai"]`） |

## 使用示例

### 基本使用

```python
from nova_ai.compat import OpenAICompletionsCompat, OpenRouterRouting

# 创建自定义兼容性配置
compat_config = OpenAICompletionsCompat(
    supports_store=True,
    supports_developer_role=False,
    thinking_format="openai",
    supports_strict_mode=True
)

# 创建路由配置
routing_config = OpenRouterRouting(
    only=["anthropic", "openai"],
    order=["anthropic", "openai"]
)
```

### 在模型配置中使用

```python
from nova_ai.models import Model, ModelCost
from nova_ai.compat import OpenAICompletionsCompat, OpenRouterRouting

# 创建带兼容性配置的模型
model = Model(
    id="custom-model",
    name="Custom Model",
    api="openai-completions",
    provider="openrouter",
    base_url="https://openrouter.ai/api/v1",
    reasoning=False,
    input_types=["text"],
    cost=ModelCost(input=1.0, output=2.0),
    context_window=8192,
    max_tokens=4096,
    compat=OpenAICompletionsCompat(
        supports_store=False,
        thinking_format="openai"
    )
)
```

## 自动检测逻辑

### 提供商检测

兼容性设置会根据模型的 `provider` 和 `base_url` 自动检测：

- **ZAI**: `provider == "zai"` 或 `"api.z.ai" in base_url`
- **Cerebras**: `provider == "cerebras"` 或 `"cerebras.ai" in base_url`
- **XAI**: `provider == "xai"` 或 `"api.x.ai" in base_url`
- **Mistral**: `provider == "mistral"` 或 `"mistral.ai" in base_url`
- **DeepSeek**: `"deepseek.com" in base_url`
- **OpenCode**: `provider == "opencode"` 或 `"opencode.ai" in base_url`

### 默认行为

| 提供商 | 支持 store | 支持 developer 角色 | 支持 reasoning_effort | max_tokens 字段 |
|--------|------------|---------------------|-----------------------|-----------------|
| OpenAI | ✅ | ✅ | ✅ | max_completion_tokens |
| ZAI | ❌ | ❌ | ❌ | max_completion_tokens |
| Cerebras | ❌ | ❌ | ✅ | max_completion_tokens |
| XAI | ❌ | ❌ | ❌ | max_completion_tokens |
| Mistral | ❌ | ❌ | ✅ | max_tokens |

## 最佳实践

1. **优先使用自动检测**: 除非有特殊需求，否则让SDK自动检测兼容性设置
2. **明确指定路由**: 对于OpenRouter和Vercel Gateway，明确指定路由偏好
3. **测试兼容性**: 在生产环境部署前，测试不同提供商的兼容性
4. **处理错误**: 准备好处理不兼容的配置导致的API错误

## 相关链接

- [OpenRouter Provider Routing](https://openrouter.ai/docs/provider-routing)
- [Vercel AI Gateway Provider Options](https://vercel.com/docs/ai-gateway/models-and-providers/provider-options)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)