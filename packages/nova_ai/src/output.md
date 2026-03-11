# 代码文件汇总

- **项目根目录**: `/root/nova/packages/nova_ai/src/nova_ai`
- **文件总数**: 37
- **生成时间**: 2026-03-09 15:49:32

## 目录结构

```
nova_ai/
```

## 文件内容

### 1. __init__.py

**路径**: `__init__.py`

**大小**: 6.1 KB

```python
"""
Assistant Message 模块
提供助手消息相关的类型定义和事件流处理
"""

# 重新导出core模块
from .core.enums import (
    Api, KnownApi, Provider, KnownProvider, StopReason,
    ThinkingLevel, CacheRetention, Transport, ThinkingFormat
)
from .core.content import TextContent, ThinkingContent, ToolCall, ImageContent
from .core.usage import Usage, Cost
from .core.messages import (
    UserMessage, AssistantMessage, ToolResultMessage,
    Message, MessageUnion, Tool, Context
)

# 重新导出streaming模块
from .streaming import (
    # 事件类型
    AssistantMessageEvent,
    StartEvent, TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallDeltaEvent, ToolCallEndEvent,
    DoneEvent, ErrorEvent,
    
    # 事件流
    EventStream, AssistantMessageEventStream,
    create_assistant_message_event_stream,
    
    # 主要API函数
    stream, complete, stream_simple, complete_simple,
)

# 重新导出registry模块
from .registry import (
    # API注册表
    ApiProvider, ApiProviderRecord, ApiProviderRegistry,
    register_api_provider, get_api_provider, list_api_providers,
    unregister_api_provider, has_api_provider, clear_api_providers,
    
    # 模型注册表
    ModelRegistry, ModelProvider,
    register_model, get_model, get_models_by_provider,
    list_providers, list_all_models, find_model_by_id,
    register_models_from_dict,
    
    # 内置注册
    register_builtin_api_providers, register_builtin_models,
    register_all_builtins, reset_registry,
)

# 重新导出providers模块
from .providers import (
    # 各个提供者的流式函数（可选）
    stream_openai_completions, stream_simple_openai_completions, OpenAICompletionsOptions
)

# 重新导出utils模块
from .utils import (
    # 环境变量
    get_env_api_key, get_env_api_key_typed, get_all_env_api_keys,
    
    # Copilot
    infer_copilot_initiator, has_copilot_vision_input,
    build_copilot_dynamic_headers, build_copilot_headers_from_messages,
    
    # JSON解析
    parse_streaming_json,
    
    # 字符串处理
    sanitize_surrogates,
    
    # 流选项
    build_base_options, clamp_reasoning, adjust_max_tokens_for_thinking,
    ThinkingBudgets, StreamOptions, SimpleStreamOptions,
    
    # 消息转换
    transform_messages,
    
    # HTTP代理
    setup_http_proxy, get_http_proxy, get_https_proxy,
    configure_http_client_proxy, is_node_environment,
)

# 重新导出compat模块
from .compat import (
    OpenAICompletionsCompat, OpenAIResponsesCompat,
    OpenRouterRouting, VercelGatewayRouting
)

# 重新导出auth模块
from .auth import (
    has_vertex_adc_credentials, has_bedrock_credentials,
)

# 重新导出models模块（仅数据）
from .models import (
    Model, ModelCost,
    OPENAI_MODELS, ANTHROPIC_MODELS, GOOGLE_MODELS,
    get_openai_model, get_anthropic_model, get_google_model,
    list_openai_models, list_anthropic_models, list_google_models,
)

# 初始化
from .utils.http_proxy import setup_http_proxy
setup_http_proxy()

# 注册所有内置组件
from .registry import register_all_builtins
register_all_builtins()

__all__ = [
    # core.enums
    "Api", "KnownApi", "Provider", "KnownProvider", "StopReason",
    "ThinkingLevel", "CacheRetention", "Transport", "ThinkingFormat",
    
    # core.content
    "TextContent", "ThinkingContent", "ToolCall", "ImageContent",
    
    # core.usage
    "Usage", "Cost",
    
    # core.messages
    "UserMessage", "AssistantMessage", "ToolResultMessage",
    "Message", "MessageUnion", "Tool", "Context",
    
    # core.models
    "Model", "ModelCost",
    
    # streaming.events
    "AssistantMessageEvent",
    "StartEvent", "TextStartEvent", "TextDeltaEvent", "TextEndEvent",
    "ThinkingStartEvent", "ThinkingDeltaEvent", "ThinkingEndEvent",
    "ToolCallStartEvent", "ToolCallDeltaEvent", "ToolCallEndEvent",
    "DoneEvent", "ErrorEvent",
    
    # streaming.event_stream
    "EventStream", "AssistantMessageEventStream",
    "create_assistant_message_event_stream",
    
    # streaming.api
    "stream", "complete", "stream_simple", "complete_simple",
    
    # registry.api_registry
    "ApiProvider", "ApiProviderRecord", "ApiProviderRegistry",
    "register_api_provider", "get_api_provider", "list_api_providers",
    "unregister_api_provider", "has_api_provider", "clear_api_providers",
    
    # registry.model_registry
    "ModelRegistry", "ModelProvider",
    "register_model", "get_model", "get_models_by_provider",
    "list_providers", "list_all_models", "find_model_by_id",
    "register_models_from_dict",
    
    # registry.builtins
    "register_builtin_api_providers", "register_builtin_models",
    "register_all_builtins", "reset_registry",
    
    # providers (可选)
    "stream_openai_completions", "stream_simple_openai_completions", "OpenAICompletionsOptions",
    
    # utils.env
    "get_env_api_key", "get_env_api_key_typed", "get_all_env_api_keys",
    
    # utils.copilot
    "infer_copilot_initiator", "has_copilot_vision_input",
    "build_copilot_dynamic_headers", "build_copilot_headers_from_messages",
    
    # utils.json_parser
    "parse_streaming_json",
    
    # utils.surrogate
    "sanitize_surrogates",
    
    # utils.stream_options
    "build_base_options", "clamp_reasoning", "adjust_max_tokens_for_thinking",
    "ThinkingBudgets", "StreamOptions", "SimpleStreamOptions",
    
    # utils.message_transformer
    "transform_messages",
    
    # utils.http_proxy
    "setup_http_proxy", "get_http_proxy", "get_https_proxy",
    "configure_http_client_proxy", "is_node_environment",
    
    # compat
    "OpenAICompletionsCompat", "OpenAIResponsesCompat",
    "OpenRouterRouting", "VercelGatewayRouting",
    
    # auth
    "has_vertex_adc_credentials", "has_bedrock_credentials",
    "is_vertex_fully_configured", "get_vertex_adc_path",
    "get_bedrock_credentials_type", "get_bedrock_region",
    
    # models.data
    "OPENAI_MODELS", "ANTHROPIC_MODELS", "GOOGLE_MODELS",
    "get_openai_model", "get_anthropic_model", "get_google_model",
    "list_openai_models", "list_anthropic_models", "list_google_models",
]
```

### 2. auth/__init__.py

**路径**: `auth/__init__.py`

**大小**: 230.0 B

```python
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
```

### 3. auth/bedrock.py

**路径**: `auth/bedrock.py`

**大小**: 2.5 KB

```python
"""
Amazon Bedrock 认证处理
"""

import os
from typing import Optional


def has_bedrock_credentials() -> bool:
    """
    检查是否存在Amazon Bedrock凭据
    
    Amazon Bedrock 支持多种凭据源:
    1. AWS_PROFILE - ~/.aws/credentials 中的命名配置
    2. AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY - 标准IAM密钥
    3. AWS_BEARER_TOKEN_BEDROCK - Bedrock API密钥（bearer token）
    4. AWS_CONTAINER_CREDENTIALS_RELATIVE_URI - ECS任务角色
    5. AWS_CONTAINER_CREDENTIALS_FULL_URI - ECS任务角色（完整URI）
    6. AWS_WEB_IDENTITY_TOKEN_FILE - IRSA (IAM Roles for Service Accounts)
    
    Returns:
        是否存在有效凭据
    """
    # 检查AWS_PROFILE（命名配置）
    if os.environ.get("AWS_PROFILE"):
        return True
    
    # 检查标准IAM密钥对
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        return True
    
    # 检查Bedrock API密钥
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return True
    
    # 检查ECS容器凭据
    if os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"):
        return True
    
    if os.environ.get("AWS_CONTAINER_CREDENTIALS_FULL_URI"):
        return True
    
    # 检查IRSA (IAM Roles for Service Accounts)
    if os.environ.get("AWS_WEB_IDENTITY_TOKEN_FILE"):
        return True
    
    # 检查默认的AWS配置文件
    from pathlib import Path
    aws_config_path = Path.home() / ".aws" / "credentials"
    if aws_config_path.exists():
        # 简单检查文件是否存在，实际使用中需要解析文件
        return True
    
    return False


def get_bedrock_credentials_type() -> Optional[str]:
    """获取当前使用的Bedrock凭据类型"""
    if os.environ.get("AWS_PROFILE"):
        return "profile"
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        return "iam_keys"
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return "bearer_token"
    if os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"):
        return "ecs_relative_uri"
    if os.environ.get("AWS_CONTAINER_CREDENTIALS_FULL_URI"):
        return "ecs_full_uri"
    if os.environ.get("AWS_WEB_IDENTITY_TOKEN_FILE"):
        return "irsa"
    
    from pathlib import Path
    if (Path.home() / ".aws" / "credentials").exists():
        return "aws_config_file"
    
    return None


def get_bedrock_region() -> Optional[str]:
    """获取Bedrock配置的AWS区域"""
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
```

### 4. auth/vertex.py

**路径**: `auth/vertex.py`

**大小**: 2.5 KB

```python
"""
Vertex AI 认证处理
"""

import os
from pathlib import Path
from typing import Optional
import sys
import importlib.util


# 懒加载Node.js模块的替代：使用Python的os.path
def _get_home_dir() -> Path:
    """获取用户主目录"""
    return Path.home()


def _get_default_adc_path() -> Path:
    """获取默认的Application Default Credentials路径"""
    return _get_home_dir() / ".config" / "gcloud" / "application_default_credentials.json"


# 缓存ADC凭据存在性检查结果
_cached_vertex_adc_credentials_exists: Optional[bool] = None


def has_vertex_adc_credentials() -> bool:
    """
    检查是否存在Vertex AI Application Default Credentials
    
    检查顺序:
    1. GOOGLE_APPLICATION_CREDENTIALS 环境变量指向的文件
    2. 默认的ADC路径: ~/.config/gcloud/application_default_credentials.json
    
    Returns:
        是否存在有效凭据
    """
    global _cached_vertex_adc_credentials_exists
    
    if _cached_vertex_adc_credentials_exists is not None:
        return _cached_vertex_adc_credentials_exists
    
    # 检查 GOOGLE_APPLICATION_CREDENTIALS 环境变量
    gac_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if gac_path:
        _cached_vertex_adc_credentials_exists = Path(gac_path).exists()
        return _cached_vertex_adc_credentials_exists
    
    # 检查默认ADC路径
    default_path = _get_default_adc_path()
    _cached_vertex_adc_credentials_exists = default_path.exists()
    
    return _cached_vertex_adc_credentials_exists


def get_vertex_project() -> Optional[str]:
    """获取Vertex AI项目ID"""
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")


def get_vertex_location() -> Optional[str]:
    """获取Vertex AI位置"""
    return os.environ.get("GOOGLE_CLOUD_LOCATION")


def is_vertex_fully_configured() -> bool:
    """
    检查Vertex AI是否完全配置
    
    需要:
    - 有效的ADC凭据
    - 项目ID
    - 位置
    """
    return (has_vertex_adc_credentials() and 
            get_vertex_project() is not None and 
            get_vertex_location() is not None)


def get_vertex_adc_path() -> Optional[Path]:
    """获取ADC凭据文件路径（如果存在）"""
    gac_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if gac_path and Path(gac_path).exists():
        return Path(gac_path)
    
    default_path = _get_default_adc_path()
    if default_path.exists():
        return default_path
    
    return None
```

### 5. compat/__init__.py

**路径**: `compat/__init__.py`

**大小**: 329.0 B

```python
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
```

### 6. compat/openai.py

**路径**: `compat/openai.py`

**大小**: 2.4 KB

```python
"""
OpenAI兼容性配置
"""

from typing import Optional, Literal
from dataclasses import dataclass, field

from ..core.enums import ThinkingFormat
from .routing import OpenRouterRouting, VercelGatewayRouting

@dataclass
class OpenAICompletionsCompat:
    """
    OpenAI-compatible completions API 兼容性设置
    用于覆盖基于URL的自动检测
    """
    # 是否支持 `store` 字段。默认：基于URL自动检测
    supports_store: Optional[bool] = None
    
    # 是否支持 `developer` 角色（vs `system`）。默认：基于URL自动检测
    supports_developer_role: Optional[bool] = None
    
    # 是否支持 `reasoning_effort`。默认：基于URL自动检测
    supports_reasoning_effort: Optional[bool] = None
    
    # 是否支持 `stream_options: { include_usage: true }` 用于流式响应中的token使用统计。默认：true
    supports_usage_in_streaming: Optional[bool] = None
    
    # 用于max tokens的字段名。默认：基于URL自动检测
    max_tokens_field: Optional[Literal["max_completion_tokens", "max_tokens"]] = None
    
    # 工具结果是否需要 `name` 字段。默认：基于URL自动检测
    requires_tool_result_name: Optional[bool] = None
    
    # 工具结果后的用户消息是否需要中间的助手消息。默认：基于URL自动检测
    requires_assistant_after_tool_result: Optional[bool] = None
    
    # 思考块是否需要转换为带<thinking>分隔符的文本块。默认：基于URL自动检测
    requires_thinking_as_text: Optional[bool] = None
    
    # 工具调用ID是否需要规范化为Mistral格式（正好9个字母数字字符）。默认：基于URL自动检测
    requires_mistral_tool_ids: Optional[bool] = None
    
    # 推理/思考参数的格式。默认："openai"
    thinking_format: ThinkingFormat = ThinkingFormat.OPENAI
    
    # 是否支持工具定义中的 `strict` 字段。默认：true
    supports_strict_mode: Optional[bool] = None
    
    # 新增字段：OpenRouter-specific routing preferences. Only used when baseUrl points to OpenRouter.
    open_router_routing: Optional[OpenRouterRouting] = None
    
    # 新增字段：Vercel AI Gateway routing preferences. Only used when baseUrl points to Vercel AI Gateway.
    vercel_gateway_routing: Optional[VercelGatewayRouting] = None


@dataclass
class OpenAIResponsesCompat:
    """
    OpenAI Responses API 兼容性设置
    预留供将来使用
    """
    pass
```

### 7. compat/routing.py

**路径**: `compat/routing.py`

**大小**: 1.0 KB

```python
"""
路由配置
用于OpenRouter和Vercel AI Gateway等代理服务
"""

from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class OpenRouterRouting:
    """
    OpenRouter 提供商路由偏好设置
    控制OpenRouter将请求路由到哪些上游提供商
    
    @see https://openrouter.ai/docs/provider-routing
    """
    # 专门使用的提供商列表（例如 ["amazon-bedrock", "anthropic"]）
    only: Optional[List[str]] = None
    
    # 按顺序尝试的提供商列表（例如 ["anthropic", "openai"]）
    order: Optional[List[str]] = None


@dataclass
class VercelGatewayRouting:
    """
    Vercel AI Gateway 路由偏好设置
    控制网关将请求路由到哪些上游提供商
    
    @see https://vercel.com/docs/ai-gateway/models-and-providers/provider-options
    """
    # 专门使用的提供商列表（例如 ["bedrock", "anthropic"]）
    only: Optional[List[str]] = None
    
    # 按顺序尝试的提供商列表（例如 ["anthropic", "openai"]）
    order: Optional[List[str]] = None
```

### 8. core/__init__.py

**路径**: `core/__init__.py`

**大小**: 731.0 B

```python
"""
核心类型模块
包含所有基础数据类型定义
"""

from .enums import Api, KnownApi, Provider, KnownProvider, StopReason
from .content import TextContent, ThinkingContent, ToolCall, ImageContent, ContentUnion
from .usage import Usage, Cost
from .messages import (
    AssistantMessage,
    UserMessage,
    ToolResultMessage,
    Message,
    MessageUnion
)

__all__ = [
    # 枚举
    "Api", "KnownApi", "Provider", "KnownProvider", "StopReason",
    
    # 内容类型
    "TextContent", "ThinkingContent", "ToolCall", "ImageContent", "ContentUnion",
    
    # 使用统计
    "Usage", "Cost",
    
    # 消息类型
    "AssistantMessage", "UserMessage", "ToolResultMessage",
    "Message", "MessageUnion",
]
```

### 9. core/content.py

**路径**: `core/content.py`

**大小**: 1.3 KB

```python
"""
内容类型定义
"""

from typing import Literal, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class TextContent:
    """文本内容"""
    type: Literal["text"] = "text"
    text: str = ""
    text_signature: Optional[str] = None  # 例如OpenAI响应中的消息ID


@dataclass
class ThinkingContent:
    """思考过程内容（推理过程）"""
    type: Literal["thinking"] = "thinking"
    thinking: str = ""
    thinking_signature: Optional[str] = None  # 例如OpenAI响应中的推理项ID
    redacted: bool = False  # 当为True时，表示思考内容被安全过滤器屏蔽
    
    def __post_init__(self):
        """加密的载荷存储在thinking_signature中，以便在多轮对话中传回API"""
        pass


@dataclass
class ToolCall:
    """工具调用"""
    type: Literal["toolCall"] = "toolCall"
    id: str = ""
    name: str = ""
    arguments: Dict[str, Any] = field(default_factory=dict)
    thought_signature: Optional[str] = None  # Google专用：重用思考上下文的签名


@dataclass
class ImageContent:
    """图像内容（用于用户消息和工具结果）"""
    type: Literal["image"] = "image"
    data: str = ""  # base64 encoded image data
    mime_type: str = ""


# 内容联合类型
ContentUnion = TextContent | ThinkingContent | ToolCall | ImageContent
```

### 10. core/enums.py

**路径**: `core/enums.py`

**大小**: 2.4 KB

```python
"""
枚举类型定义
"""

from typing import Union, Literal
from enum import Enum


class KnownApi(str, Enum):
    """已知的 API 类型"""
    OPENAI_COMPLETIONS = "openai-completions"
    OPENAI_RESPONSES = "openai-responses"
    AZURE_OPENAI_RESPONSES = "azure-openai-responses"
    OPENAI_CODEX_RESPONSES = "openai-codex-responses"
    ANTHROPIC_MESSAGES = "anthropic-messages"
    BEDROCK_CONVERSE_STREAM = "bedrock-converse-stream"
    GOOGLE_GENERATIVE_AI = "google-generative-ai"
    GOOGLE_GEMINI_CLI = "google-gemini-cli"
    GOOGLE_VERTEX = "google-vertex"


# 允许任意字符串值的 API 类型
Api = Union[KnownApi, str]


class KnownProvider(str, Enum):
    """已知的服务提供商类型"""
    AMAZON_BEDROCK = "amazon-bedrock"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GOOGLE_GEMINI_CLI = "google-gemini-cli"
    GOOGLE_ANTIGRAVITY = "google-antigravity"
    GOOGLE_VERTEX = "google-vertex"
    OPENAI = "openai"
    AZURE_OPENAI_RESPONSES = "azure-openai-responses"
    OPENAI_CODEX = "openai-codex"
    GITHUB_COPILOT = "github-copilot"
    XAI = "xai"
    GROQ = "groq"
    CEREBRAS = "cerebras"
    OPENROUTER = "openrouter"
    VERCEL_AI_GATEWAY = "vercel-ai-gateway"
    ZAI = "zai"
    MISTRAL = "mistral"
    MINIMAX = "minimax"
    MINIMAX_CN = "minimax-cn"
    HUGGINGFACE = "huggingface"
    OPENCODE = "opencode"
    KIMI_CODING = "kimi-coding"
    VOLCENGINE = "volcengine"


# 允许任意字符串值的 Provider 类型
Provider = Union[KnownProvider, str]


class StopReason(str, Enum):
    """停止原因"""
    STOP = "stop"       # 正常结束
    LENGTH = "length"   # 达到长度限制
    TOOL_USE = "toolUse"  # 触发工具调用
    ERROR = "error"     # 发生错误
    ABORTED = "aborted"  # 被中止


class ThinkingLevel(str, Enum):
    """思考级别"""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    XHIGH = "xhigh"


class CacheRetention(str, Enum):
    """缓存保留策略"""
    NONE = "none"
    SHORT = "short"
    LONG = "long"


class Transport(str, Enum):
    """传输协议"""
    SSE = "sse"
    WEBSOCKET = "websocket"
    AUTO = "auto"


class ThinkingFormat(str, Enum):
    """思考格式（用于不同提供商）"""
    OPENAI = "openai"      # 使用 reasoning_effort
    ZAI = "zai"            # 使用 thinking: { type: "enabled" }
    QWEN = "qwen"          # 使用 enable_thinking: boolean
```

### 11. core/messages.py

**路径**: `core/messages.py`

**大小**: 2.0 KB

```python
"""
核心消息类型定义
"""

from typing import List, Optional, Union, Literal, Dict, Any, TypeVar, Generic
from dataclasses import dataclass, field

from .enums import Api, Provider, StopReason
from .content import TextContent, ThinkingContent, ToolCall, ImageContent, ContentUnion
from .usage import Usage


@dataclass
class UserMessage:
    """用户消息（用于上下文理解）"""
    role: Literal["user"] = "user"
    content: Union[str, List[Union[TextContent, ImageContent]]] = field(default_factory=list)
    timestamp: int = 0


@dataclass
class AssistantMessage:
    """助手消息"""
    role: Literal["assistant"] = "assistant"
    content: List[Union[TextContent, ThinkingContent, ToolCall]] = field(default_factory=list)
    api: Api = ""                      # 使用的API类型
    provider: Provider = ""             # 服务提供商
    model: str = ""                      # 模型名称
    usage: Usage = field(default_factory=Usage)  # 令牌使用统计
    stop_reason: StopReason = StopReason.STOP    # 停止原因
    error_message: Optional[str] = None           # 错误信息（如果有）
    timestamp: int = 0                            # Unix时间戳（毫秒）


@dataclass
class ToolResultMessage:
    """工具结果消息（用于上下文理解）"""
    role: Literal["toolResult"] = "toolResult"
    tool_call_id: str = ""
    tool_name: str = ""
    content: List[Union[TextContent, ImageContent]] = field(default_factory=list)
    details: Optional[Dict[str, Any]] = None
    is_error: bool = False
    timestamp: int = 0


# 消息联合类型
Message = Union[UserMessage, AssistantMessage, ToolResultMessage]
MessageUnion = Message


T = TypeVar('T')


@dataclass
class Tool(Generic[T]):
    """工具定义"""
    name: str = ""
    description: str = ""
    parameters: Optional[T] = None  # 应该是 TypeBox TSchema 的对应物


@dataclass
class Context:
    """上下文"""
    system_prompt: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    tools: Optional[List[Tool]] = None
```

### 12. core/usage.py

**路径**: `core/usage.py`

**大小**: 746.0 B

```python
"""
使用统计类型定义
"""

from dataclasses import dataclass, field


@dataclass
class Cost:
    """成本明细"""
    input: float = 0.0          # 输入成本
    output: float = 0.0         # 输出成本
    cache_read: float = 0.0     # 缓存读取成本
    cache_write: float = 0.0    # 缓存写入成本
    total: float = 0.0          # 总成本


@dataclass
class Usage:
    """令牌使用统计"""
    input: int = 0               # 输入令牌数
    output: int = 0              # 输出令牌数
    cache_read: int = 0          # 缓存读取令牌数
    cache_write: int = 0         # 缓存写入令牌数
    total_tokens: int = 0        # 总令牌数
    cost: Cost = field(default_factory=Cost)  # 成本明细
```

### 13. models/__init__.py

**路径**: `models/__init__.py`

**大小**: 1023.0 B

```python
"""
模型模块
包含所有提供商模型的定义和注册表
"""

from .base import Model, ModelCost, calculate_cost, supports_xhigh_thinking
from .openai import OPENAI_MODELS, get_openai_model, list_openai_models
from .anthropic import ANTHROPIC_MODELS, get_anthropic_model, list_anthropic_models
from .google import GOOGLE_MODELS, get_google_model, list_google_models
from .volcengine import VOLCENGINE_MODELS, get_volcengine_model, list_volcengine_models

__all__ = [
    # 基础
    "Model",
    "ModelCost",
    "calculate_cost",
    "supports_xhigh_thinking",
    
    # 按提供商分组的模型
    "MODELS_BY_PROVIDER",
    
    # OpenAI
    "OPENAI_MODELS",
    "get_openai_model",
    "list_openai_models",
    
    # Anthropic
    "ANTHROPIC_MODELS",
    "get_anthropic_model",
    "list_anthropic_models",
    
    # Google
    "GOOGLE_MODELS",
    "get_google_model",
    "list_google_models",

    # Volcengine
    "VOLCENGINE_MODELS",
    "get_volcengine_model",
    "list_volcengine_models"

    
]
```

### 14. models/anthropic.py

**路径**: `models/anthropic.py`

**大小**: 3.1 KB

```python
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
```

### 15. models/base.py

**路径**: `models/base.py`

**大小**: 2.8 KB

```python
"""
基础模型类型定义
"""

from typing import Optional, Dict, List, Literal, Union, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum

from ..core.usage import Usage,Cost

from ..core.enums import Api, Provider, KnownApi, KnownProvider
from ..compat.openai import OpenAICompletionsCompat, OpenAIResponsesCompat


@dataclass
class ModelCost:
    """模型成本（$/百万tokens）"""
    input: float = 0.0
    output: float = 0.0
    cache_read: float = 0.0
    cache_write: float = 0.0


@dataclass
class Model:
    """模型定义"""
    id: str
    name: str
    api: Api
    provider: Provider
    base_url: str
    reasoning: bool
    input_types: List[Literal["text", "image"]]
    cost: ModelCost
    context_window: int
    max_tokens: int
    headers: Optional[Dict[str, str]] = None
    compat: Optional[Union[OpenAICompletionsCompat, OpenAIResponsesCompat]] = None
    
    def __post_init__(self):
        """根据API类型设置兼容性配置"""
        if self.compat is None:
            if self.api == KnownApi.OPENAI_COMPLETIONS:
                self.compat = OpenAICompletionsCompat()
            elif self.api == KnownApi.OPENAI_RESPONSES:
                self.compat = OpenAIResponsesCompat()


# 类型别名
TApi = TypeVar('TApi', bound=Api)
ModelType = Model  # 在Python中，我们可以使用类型检查

def calculate_cost(model: Model, usage: Usage) -> Cost:
    """
    根据模型和用量计算成本
    
    Args:
        model: 模型对象
        usage: 使用统计
        
    Returns:
        成本明细（直接修改并返回usage.cost）
    """
    # 成本计算：模型成本是$/M tokens，需要除以1,000,000得到每token成本
    usage.cost.input = (model.cost.input / 1000000) * usage.input
    usage.cost.output = (model.cost.output / 1000000) * usage.output
    usage.cost.cache_read = (model.cost.cache_read / 1000000) * usage.cache_read
    usage.cost.cache_write = (model.cost.cache_write / 1000000) * usage.cache_write
    usage.cost.total = (
        usage.cost.input + 
        usage.cost.output + 
        usage.cost.cache_read + 
        usage.cost.cache_write
    )
    
    return usage.cost

def supports_xhigh_thinking(model: Model) -> bool:
    """
    检查模型是否支持xhigh思考级别
    
    当前支持的模型:
    - GPT-5.2 / GPT-5.3 模型家族
    - Anthropic Messages API Opus 4.6 模型 (xhigh 映射到 adaptive effort "max")
    
    Args:
        model: 模型对象
        
    Returns:
        是否支持xhigh思考级别
    """
    # GPT-5.2 / GPT-5.3 系列
    if "gpt-5.2" in model.id or "gpt-5.3" in model.id:
        return True
    
    # Anthropic Opus 4.6 系列
    if model.api == "anthropic-messages":
        return "opus-4-6" in model.id or "opus-4.6" in model.id
    
    return False
```

### 16. models/google.py

**路径**: `models/google.py`

**大小**: 3.6 KB

```python
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
```

### 17. models/openai.py

**路径**: `models/openai.py`

**大小**: 4.7 KB

```python
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
```

### 18. models/volcengine.py

**路径**: `models/volcengine.py`

**大小**: 1.5 KB

```python
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
```

### 19. providers/__init__.py

**路径**: `providers/__init__.py`

**大小**: 373.0 B

```python
"""
API提供者模块
"""
# 导出各个提供者的流式函数
from .openai_completions import stream_openai_completions, stream_simple_openai_completions, OpenAICompletionsOptions
from .options import ProviderStreamOptions
__all__ = [
    "stream_openai_completions",
    "stream_simple_openai_completions",
    "OpenAICompletionsOptions",
    "ProviderStreamOptions"
]
```

### 20. providers/openai_completions.py

**路径**: `providers/openai_completions.py`

**大小**: 32.5 KB

```python
"""
OpenAI Completions API 流式处理实现
"""

import json
import time
from typing import List, Dict, Optional, Any, Union
import asyncio
from copy import deepcopy
from dataclasses import dataclass

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionChunk,
    ChatCompletionMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
)

from ..core.enums import StopReason
from ..core.messages import (
    Message, UserMessage, AssistantMessage, ToolResultMessage,
    Context, Tool
)
from ..core.content import (
    TextContent, ThinkingContent, ToolCall,
)
from ..models import Model
from ..core.usage import Usage, Cost
from ..utils.env import get_env_api_key
from ..utils.json_parser import parse_streaming_json
from ..utils.surrogate import sanitize_surrogates
from ..utils.copilot import (
    has_copilot_vision_input,
    build_copilot_dynamic_headers
)
from ..utils.stream_options import (
    build_base_options,
    clamp_reasoning,
    StreamOptions,
    SimpleStreamOptions,
)
from ..utils.message_transformer import transform_messages
from ..models import calculate_cost, supports_xhigh_thinking
from ..streaming import (
    AssistantMessageEventStream,
    StartEvent, TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallDeltaEvent, ToolCallEndEvent,
    DoneEvent, ErrorEvent
)
from ..compat.openai import OpenAICompletionsCompat

@dataclass
class OpenAICompletionsOptions(StreamOptions):
    """OpenAI Completions 特定选项"""
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    reasoning_effort: Optional[str] = None


def normalize_mistral_tool_id(id: str) -> str:
    """
    规范化工具调用ID以适应Mistral
    
    Mistral要求工具ID正好是9个字母数字字符（a-z, A-Z, 0-9）
    """
    # 移除非字母数字字符
    normalized = ''.join(c for c in id if c.isalnum())
    
    # Mistral要求正好9个字符
    if len(normalized) < 9:
        # 基于原始ID使用确定性字符填充以确保匹配
        padding = "ABCDEFGHI"
        normalized = normalized + padding[:9 - len(normalized)]
    elif len(normalized) > 9:
        normalized = normalized[:9]
    
    return normalized


def has_tool_history(messages: List[Message]) -> bool:
    """
    检查对话消息是否包含工具调用或工具结果
    
    因为Anthropic（通过代理）要求在消息包含tool_calls或tool角色消息时
    必须提供tools参数
    """
    for msg in messages:
        if msg.role == "toolResult":
            return True
        if msg.role == "assistant":
            if any(block.type == "toolCall" for block in msg.content):
                return True
    return False


def map_stop_reason(reason: Optional[str]) -> StopReason:
    """映射OpenAI的finish_reason到标准StopReason"""
    if reason is None:
        return StopReason.STOP
    
    if reason == "stop":
        return StopReason.STOP
    elif reason == "length":
        return StopReason.LENGTH
    elif reason in ["function_call", "tool_calls"]:
        return StopReason.TOOL_USE
    elif reason == "content_filter":
        return StopReason.ERROR
    else:
        raise ValueError(f"Unhandled stop reason: {reason}")


def detect_compat(model: Model) -> OpenAICompletionsCompat:
    """
    从提供商和baseUrl检测兼容性设置
    
    提供商优先于基于URL的检测，因为它是显式配置的
    """
    provider = model.provider
    base_url = model.base_url
    
    is_zai = provider == "zai" or "api.z.ai" in base_url
    
    is_non_standard = (
        provider == "volcengine" or
        "volces.com" in base_url or
        "googleapis.com" in base_url or
        provider == "cerebras" or
        "cerebras.ai" in base_url or
        provider == "xai" or
        "api.x.ai" in base_url or
        provider == "mistral" or
        "mistral.ai" in base_url or
        "chutes.ai" in base_url or
        "deepseek.com" in base_url or
        is_zai or
        provider == "opencode" or
        "opencode.ai" in base_url
    )
    
    use_max_tokens = (
        provider == "mistral" or
        "mistral.ai" in base_url or
        "chutes.ai" in base_url
    )
    
    is_grok = provider == "xai" or "api.x.ai" in base_url
    
    is_mistral = provider == "mistral" or "mistral.ai" in base_url
    
    return OpenAICompletionsCompat(
        supports_store=not is_non_standard,
        supports_developer_role=not is_non_standard,
        supports_reasoning_effort=not (is_grok or is_zai),
        supports_usage_in_streaming=True,
        max_tokens_field="max_tokens" if use_max_tokens else "max_completion_tokens",
        requires_tool_result_name=is_mistral,
        requires_assistant_after_tool_result=False,
        requires_thinking_as_text=is_mistral,
        requires_mistral_tool_ids=is_mistral,
        thinking_format="zai" if is_zai else "openai",
        open_router_routing={},
        vercel_gateway_routing={},
        supports_strict_mode=True,
    )


def get_compat(model: Model) -> OpenAICompletionsCompat:
    """
    获取模型的解析后兼容性设置
    
    如果提供了model.compat则使用，否则自动检测
    """
    detected = detect_compat(model)
    if model.compat is None:
        return detected
    
    compat = model.compat
    
    return OpenAICompletionsCompat(
        supports_store=compat.supports_store if compat.supports_store is not None else detected.supports_store,
        supports_developer_role=compat.supports_developer_role if compat.supports_developer_role is not None else detected.supports_developer_role,
        supports_reasoning_effort=compat.supports_reasoning_effort if compat.supports_reasoning_effort is not None else detected.supports_reasoning_effort,
        supports_usage_in_streaming=compat.supports_usage_in_streaming if compat.supports_usage_in_streaming is not None else detected.supports_usage_in_streaming,
        max_tokens_field=compat.max_tokens_field or detected.max_tokens_field,
        requires_tool_result_name=compat.requires_tool_result_name if compat.requires_tool_result_name is not None else detected.requires_tool_result_name,
        requires_assistant_after_tool_result=compat.requires_assistant_after_tool_result if compat.requires_assistant_after_tool_result is not None else detected.requires_assistant_after_tool_result,
        requires_thinking_as_text=compat.requires_thinking_as_text if compat.requires_thinking_as_text is not None else detected.requires_thinking_as_text,
        requires_mistral_tool_ids=compat.requires_mistral_tool_ids if compat.requires_mistral_tool_ids is not None else detected.requires_mistral_tool_ids,
        thinking_format=compat.thinking_format or detected.thinking_format,
        open_router_routing=compat.open_router_routing or detected.open_router_routing,
        vercel_gateway_routing=compat.vercel_gateway_routing or detected.vercel_gateway_routing,
        supports_strict_mode=compat.supports_strict_mode if compat.supports_strict_mode is not None else detected.supports_strict_mode,
    )


def maybe_add_openrouter_anthropic_cache_control(
    model: Model,
    messages: List[ChatCompletionMessageParam]
) -> None:
    """为OpenRouter上的Anthropic模型添加缓存控制"""
    if model.provider != "openrouter" or not model.id.startswith("anthropic/"):
        return
    
    for i in range(len(messages) - 1, -1, -1):
        msg = messages[i]
        if msg["role"] not in ["user", "assistant"]:
            continue
        
        content = msg.get("content")
        if isinstance(content, str):
            msg["content"] = [
                {
                    "type": "text",
                    "text": content,
                    "cache_control": {"type": "ephemeral"}
                }
            ]
            return
        
        if not isinstance(content, list):
            continue
        
        for j in range(len(content) - 1, -1, -1):
            part = content[j]
            if isinstance(part, dict) and part.get("type") == "text":
                part["cache_control"] = {"type": "ephemeral"}
                return


def convert_messages(
    model: Model,
    context: Context,
    compat: OpenAICompletionsCompat
) -> List[ChatCompletionMessageParam]:
    """将标准消息转换为OpenAI格式"""
    params: List[ChatCompletionMessageParam] = []
    
    def normalize_tool_call_id(id: str) -> str:
        """规范化工具调用ID"""
        if compat.requires_mistral_tool_ids:
            return normalize_mistral_tool_id(id)
        
        if "|" in id:
            call_id = id.split("|")[0]
            import re
            return re.sub(r'[^a-zA-Z0-9_-]', '_', call_id)[:40]
        
        if model.provider == "openai":
            return id[:40] if len(id) > 40 else id
        return id
    
    transformed_messages = transform_messages(
        context.messages,
        model,
        lambda id, m, src: normalize_tool_call_id(id)
    )
    
    if context.system_prompt:
        use_developer_role = model.reasoning and compat.supports_developer_role
        role = "developer" if use_developer_role else "system"
        params.append({
            "role": role,
            "content": sanitize_surrogates(context.system_prompt)
        })
    
    last_role: Optional[str] = None
    
    i = 0
    while i < len(transformed_messages):
        msg = transformed_messages[i]
        
        if (compat.requires_assistant_after_tool_result and 
            last_role == "toolResult" and 
            msg.role == "user"):
            params.append({
                "role": "assistant",
                "content": "I have processed the tool results."
            })
        
        if msg.role == "user":
            user_msg = msg
            if isinstance(user_msg.content, str):
                params.append({
                    "role": "user",
                    "content": sanitize_surrogates(user_msg.content)
                })
            else:
                content = []
                for item in user_msg.content:
                    if item.type == "text":
                        content.append({
                            "type": "text",
                            "text": sanitize_surrogates(item.text)
                        })
                    elif item.type == "image":
                        content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{item.mime_type};base64,{item.data}"
                            }
                        })
                if "image" not in model.input_types:
                    content = [c for c in content if c.get("type") != "image_url"]
                
                if content:
                    params.append({
                        "role": "user",
                        "content": content
                    })
        
        elif msg.role == "assistant":
            assistant_msg = msg
            
            assistant_param: ChatCompletionAssistantMessageParam = {
                "role": "assistant",
                "content": "" if compat.requires_assistant_after_tool_result else None
            }
            
            text_blocks = [b for b in assistant_msg.content if b.type == "text"]
            non_empty_text = [b for b in text_blocks if b.text and b.text.strip()]
            
            if non_empty_text:
                if model.provider == "github-copilot":
                    assistant_param["content"] = "".join(
                        sanitize_surrogates(b.text) for b in non_empty_text
                    )
                else:
                    assistant_param["content"] = [
                        {"type": "text", "text": sanitize_surrogates(b.text)}
                        for b in non_empty_text
                    ]
            
            thinking_blocks = [b for b in assistant_msg.content if b.type == "thinking"]
            non_empty_thinking = [b for b in thinking_blocks if b.thinking and b.thinking.strip()]
            
            if non_empty_thinking:
                if compat.requires_thinking_as_text:
                    thinking_text = "\n\n".join(b.thinking for b in non_empty_thinking)
                    if isinstance(assistant_param["content"], list):
                        assistant_param["content"].insert(0, {"type": "text", "text": thinking_text})
                    else:
                        assistant_param["content"] = [{"type": "text", "text": thinking_text}]
                else:
                    signature = non_empty_thinking[0].thinking_signature
                    if signature:
                        assistant_param[signature] = "\n".join(b.thinking for b in non_empty_thinking)
            
            tool_calls = [b for b in assistant_msg.content if b.type == "toolCall"]
            if tool_calls:
                assistant_param["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments)
                        }
                    }
                    for tc in tool_calls
                ]
                
                reasoning_details = []
                for tc in tool_calls:
                    if tc.thought_signature:
                        try:
                            reasoning_details.append(json.loads(tc.thought_signature))
                        except:
                            pass
                if reasoning_details:
                    assistant_param["reasoning_details"] = reasoning_details
            
            content = assistant_param.get("content")
            has_content = (
                content is not None and
                ((isinstance(content, str) and len(content) > 0) or
                 (isinstance(content, list) and len(content) > 0))
            )
            if not has_content and "tool_calls" not in assistant_param:
                i += 1
                continue
            
            params.append(assistant_param)
        
        elif msg.role == "toolResult":
            tool_msg = msg
            image_blocks = []
            
            j = i
            while j < len(transformed_messages) and transformed_messages[j].role == "toolResult":
                curr = transformed_messages[j]
                
                text_result = "\n".join(
                    c.text for c in curr.content if c.type == "text"
                )
                has_images = any(c.type == "image" for c in curr.content)
                
                has_text = len(text_result) > 0
                tool_result_param: ChatCompletionToolMessageParam = {
                    "role": "tool",
                    "content": sanitize_surrogates(text_result if has_text else "(see attached image)"),
                    "tool_call_id": curr.tool_call_id
                }
                if compat.requires_tool_result_name and curr.tool_name:
                    tool_result_param.name = curr.tool_name
                
                params.append(tool_result_param)
                
                if has_images and "image" in model.input_types:
                    for block in curr.content:
                        if block.type == "image":
                            image_blocks.append({
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{block.mime_type};base64,{block.data}"
                                }
                            })
                
                j += 1
            
            i = j - 1
            
            if image_blocks:
                if compat.requires_assistant_after_tool_result:
                    params.append({
                        "role": "assistant",
                        "content": "I have processed the tool results."
                    })
                
                params.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Attached image(s) from tool result:"},
                        *image_blocks
                    ]
                })
                last_role = "user"
            else:
                last_role = "toolResult"
            
            i += 1
            continue
        
        last_role = msg.role
        i += 1
    
    return params


def convert_tools(
    tools: List[Tool],
    compat: OpenAICompletionsCompat
) -> List[Dict[str, Any]]:
    """转换工具定义为OpenAI格式"""
    result = []
    for tool in tools:
        tool_dict = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        }
        if compat.supports_strict_mode is not False:
            tool_dict["function"]["strict"] = False
        
        result.append(tool_dict)
    
    return result


def create_client(
    model: Model,
    context: Context,
    api_key: Optional[str] = None,
    options_headers: Optional[Dict[str, str]] = None
) -> AsyncOpenAI:
    """创建OpenAI客户端"""
    if not api_key:
        api_key = get_env_api_key(model.provider)
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass it as an argument."
            )
    
    headers = {}
    if model.headers:
        headers.update(model.headers)
    
    if model.provider == "github-copilot":
        has_images = has_copilot_vision_input(context.messages)
        copilot_headers = build_copilot_dynamic_headers(context.messages, has_images)
        headers.update(copilot_headers)
    
    if options_headers:
        headers.update(options_headers)
    
    return AsyncOpenAI(
        api_key=api_key,
        base_url=model.base_url,
        default_headers=headers
    )


def build_params(
    model: Model,
    context: Context,
    options: Optional[OpenAICompletionsOptions] = None
) -> Dict[str, Any]:
    """构建OpenAI API参数"""
    compat = get_compat(model)
    messages = convert_messages(model, context, compat)
    maybe_add_openrouter_anthropic_cache_control(model, messages)
    
    params: Dict[str, Any] = {
        "model": model.id,
        "messages": messages,
        "stream": True,
    }
    
    if compat.supports_usage_in_streaming is not False:
        params["stream_options"] = {"include_usage": True}
    
    if compat.supports_store:
        params["store"] = False
    
    if options and options.max_tokens:
        if compat.max_tokens_field == "max_tokens":
            params["max_tokens"] = options.max_tokens
        else:
            params["max_completion_tokens"] = options.max_tokens
    
    if options and options.temperature is not None:
        params["temperature"] = options.temperature
    
    if context.tools:
        params["tools"] = convert_tools(context.tools, compat)
    elif has_tool_history(context.messages):
        params["tools"] = []
    
    if options and options.tool_choice:
        params["tool_choice"] = options.tool_choice
    
    if compat.thinking_format in ["zai", "qwen"] and model.reasoning:
        params["enable_thinking"] = bool(options and options.reasoning_effort)
    elif (options and options.reasoning_effort and 
          model.reasoning and compat.supports_reasoning_effort):
        params["reasoning_effort"] = options.reasoning_effort
    
    if "openrouter.ai" in model.base_url and model.compat and model.compat.open_router_routing:
        params["provider"] = model.compat.open_router_routing
    
    if ("ai-gateway.vercel.sh" in model.base_url and 
        model.compat and model.compat.vercel_gateway_routing):
        routing = model.compat.vercel_gateway_routing
        if routing.only or routing.order:
            gateway_options = {}
            if routing.only:
                gateway_options["only"] = routing.only
            if routing.order:
                gateway_options["order"] = routing.order
            params["providerOptions"] = {"gateway": gateway_options}
    
    return params


async def stream_openai_completions(
    model: Model,
    context: Context,
    options: Optional[OpenAICompletionsOptions] = None
) -> AssistantMessageEventStream:
    """OpenAI Completions 流式处理主函数"""
    stream = AssistantMessageEventStream()
    
    async def process_stream():
        output = AssistantMessage(
            role="assistant",
            content=[],
            api=model.api,
            provider=model.provider,
            model=model.id,
            usage=Usage(
                input=0,
                output=0,
                cache_read=0,
                cache_write=0,
                total_tokens=0,
                cost=Cost()
            ),
            stop_reason=StopReason.STOP,
            timestamp=int(time.time() * 1000)
        )
        
        # try:
        api_key = options.api_key if options else None
        client = create_client(model, context, api_key, options.headers if options else None)
        params = build_params(model, context, options)
        
        if options and options.on_payload:
            options.on_payload(params)
        
        openai_stream = await client.chat.completions.create(**params)
        
        stream.push(StartEvent(partial=deepcopy(output)))
        
        current_block = None
        current_block_index = -1
        
        def finish_current_block(block=None):
            nonlocal current_block, current_block_index
            if block:
                if block.type == "text":
                    stream.push(TextEndEvent(
                        content_index=current_block_index,
                        content=block,
                        partial=deepcopy(output)
                    ))
                elif block.type == "thinking":
                    stream.push(ThinkingEndEvent(
                        content_index=current_block_index,
                        content=block,
                        partial=deepcopy(output)
                    ))
                elif block.type == "toolCall":
                    block.arguments = parse_streaming_json(block.partial_args)
                    if hasattr(block, "partial_args"):
                        del block.partial_args
                    stream.push(ToolCallEndEvent(
                        content_index=current_block_index,
                        tool_call=ToolCall(
                            id=block.id,
                            name=block.name,
                            arguments=block.arguments,
                            thought_signature=block.thought_signature if hasattr(block, "thought_signature") else None
                        ),
                        partial=deepcopy(output)
                    ))
            current_block = None
            current_block_index = -1
        
        async for chunk in openai_stream:
            if chunk.usage:
                cached_tokens = getattr(chunk.usage.prompt_tokens_details, 'cached_tokens', 0) if chunk.usage.prompt_tokens_details else 0
                reasoning_tokens = getattr(chunk.usage.completion_tokens_details, 'reasoning_tokens', 0) if chunk.usage.completion_tokens_details else 0
                
                input_tokens = (chunk.usage.prompt_tokens or 0) - cached_tokens
                output_tokens = (chunk.usage.completion_tokens or 0) + reasoning_tokens
                
                output.usage.input = input_tokens
                output.usage.output = output_tokens
                output.usage.cache_read = cached_tokens
                output.usage.cache_write = 0
                output.usage.total_tokens = input_tokens + output_tokens + cached_tokens
                
                calculate_cost(model, output.usage)
            
            if not chunk.choices:
                continue
            
            choice = chunk.choices[0]
            
            if choice.finish_reason:
                output.stop_reason = map_stop_reason(choice.finish_reason)
            
            if choice.delta:
                delta = choice.delta
                
                if delta.content and len(delta.content) > 0:
                    if not current_block or current_block.type != "text":
                        finish_current_block(current_block)
                        current_block = TextContent(
                            type = "text", 
                            text = ""
                                                    
                        )
                        output.content.append(current_block)
                        current_block_index = len(output.content) - 1
                        stream.push(TextStartEvent(
                            content_index=current_block_index,
                            partial=deepcopy(output)
                        ))
                    
                    if current_block.type == "text":
                        current_block.text += delta.content
                        stream.push(TextDeltaEvent(
                            content_index=current_block_index,
                            delta=delta.content,
                            partial=deepcopy(output)
                        ))
                
                delta_dict = delta.model_dump() if hasattr(delta, 'model_dump') else {}
                reasoning_fields = ["reasoning_content", "reasoning", "reasoning_text"]
                found_reasoning = None
                
                for field in reasoning_fields:
                    if field in delta_dict and delta_dict[field] and len(delta_dict[field]) > 0:
                        found_reasoning = field
                        break
                
                if found_reasoning:
                    if not current_block or current_block.type != "thinking":
                        finish_current_block(current_block)
                        current_block = ThinkingContent(
                            type = "thinking",
                            thinking = "",
                            thinking_signature = found_reasoning
                        )
                        output.content.append(current_block)
                        current_block_index = len(output.content) - 1
                        stream.push(ThinkingStartEvent(
                            content_index=current_block_index,
                            partial=deepcopy(output)
                        ))
                    
                    if current_block.type == "thinking":
                        delta_text = delta_dict[found_reasoning]
                        current_block.thinking += delta_text
                        stream.push(ThinkingDeltaEvent(
                            content_index=current_block_index,
                            delta=delta_text,
                            partial=deepcopy(output)
                        ))
                
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        if (not current_block or 
                            current_block.type != "toolCall" or
                            (tool_call.id and current_block.id != tool_call.id)):
                            finish_current_block(current_block)
                            current_block = ToolCall(
                                type="toolCall",
                                id=tool_call.id or "",
                                name=tool_call.function.name if tool_call.function else "",
                                arguments={},
                            )
                            current_block.partial_args=""
                            output.content.append(current_block)
                            current_block_index = len(output.content) - 1
                            stream.push(ToolCallStartEvent(
                                content_index=current_block_index,
                                partial=deepcopy(output)
                            ))
                        
                        if current_block.type == "toolCall":
                            if tool_call.id:
                                current_block.id = tool_call.id
                            if tool_call.function and tool_call.function.name:
                                current_block.name = tool_call.function.name
                            
                            delta_args = ""
                            if tool_call.function and tool_call.function.arguments:
                                delta_args = tool_call.function.arguments
                                current_block.partial_args = current_block.partial_args + delta_args
                                current_block.arguments = parse_streaming_json(current_block.partial_args)
                            
                            stream.push(ToolCallDeltaEvent(
                                content_index=current_block_index,
                                delta=delta_args,
                                partial=deepcopy(output)
                            ))
                
                if "reasoning_details" in delta_dict and delta_dict["reasoning_details"]:
                    reasoning_details = delta_dict["reasoning_details"]
                    if isinstance(reasoning_details, list):
                        for detail in reasoning_details:
                            if (isinstance(detail, dict) and 
                                detail.get("type") == "reasoning.encrypted" and
                                detail.get("id") and detail.get("data")):
                                for block in output.content:
                                    if (block.type == "toolCall" and 
                                        block.id == detail.id):
                                        block.thought_signature = json.dumps(detail)
                                        break
        
        finish_current_block(current_block)
        
        if options and options.signal and hasattr(options.signal, 'aborted') and options.signal.aborted:
            raise Exception("Request was aborted")
        
        if output.stop_reason in [StopReason.ABORTED, StopReason.ERROR]:
            raise Exception("An unknown error occurred")
        
        stream.push(DoneEvent(
            reason=output.stop_reason,
            message=deepcopy(output)
        ))
        stream.end()
            
        # except Exception as e:
        #     for block in output.content:
        #         if "partial_args" in block:
        #             del block.partial_args
            
        #     output.stop_reason = StopReason.ABORTED if (options and options.signal and options.signal.aborted) else StopReason.ERROR
        #     output.error_message = str(e)
            
        #     if hasattr(e, 'error') and hasattr(e.error, 'metadata') and hasattr(e.error.metadata, 'raw'):
        #         output.error_message += f"\n{e.error.metadata.raw}"
            
        #     stream.push(ErrorEvent(
        #         reason=output.stop_reason,
        #         error=deepcopy(output)
        #     ))
        #     stream.end()
    
    asyncio.create_task(process_stream())
    return stream


async def stream_simple_openai_completions(
    model: Model,
    context: Context,
    options: Optional[SimpleStreamOptions] = None
) -> AssistantMessageEventStream:
    """简化的OpenAI Completions流式处理"""
    api_key = options.api_key if options else None
    if not api_key:
        api_key = get_env_api_key(model.provider)
    
    if not api_key:
        raise ValueError(f"No API key for provider: {model.provider}")
    
    base = build_base_options(model, options, api_key)
    
    reasoning_effort = None
    if supports_xhigh_thinking(model) and options and options.reasoning:
        reasoning_effort = options.reasoning.value
    elif options and options.reasoning:
        clamped = clamp_reasoning(options.reasoning)
        reasoning_effort = clamped.value if clamped else None
    
    tool_choice = getattr(options, 'tool_choice', None) if options else None
    
    openai_options = OpenAICompletionsOptions(
        temperature=base.temperature,
        max_tokens=base.max_tokens,
        signal=base.signal,
        api_key=base.api_key,
        transport=base.transport,
        cache_retention=base.cache_retention,
        session_id=base.session_id,
        headers=base.headers,
        on_payload=base.on_payload,
        max_retry_delay_ms=base.max_retry_delay_ms,
        metadata=base.metadata,
        tool_choice=tool_choice,
        reasoning_effort=reasoning_effort
    )
    
    # 等待协程执行完成
    return await stream_openai_completions(model, context, openai_options)
```

### 21. providers/options.py

**路径**: `providers/options.py`

**大小**: 137.0 B

```python
from typing import Union
from .openai_completions import OpenAICompletionsOptions
ProviderStreamOptions = Union[OpenAICompletionsOptions]
```

### 22. registry/__init__.py

**路径**: `registry/__init__.py`

**大小**: 1.2 KB

```python
"""
注册模块
包含所有注册相关的逻辑
"""

from .api_registry import (
    ApiProvider,
    ApiProviderRecord,
    ApiProviderRegistry,
    register_api_provider,
    get_api_provider,
    list_api_providers,
    unregister_api_provider,
    has_api_provider,
    clear_api_providers,
)

from .model_registry import (
    ModelRegistry,
    ModelProvider,
    register_model,
    get_model,
    get_models_by_provider,
    list_providers,
    list_all_models,
    find_model_by_id,
    register_models_from_dict,
)

from .builtins import (
    register_builtin_api_providers,
    register_builtin_models,
    register_all_builtins,
    reset_registry,
)

__all__ = [
    # API注册表
    "ApiProvider", "ApiProviderRecord", "ApiProviderRegistry",
    "register_api_provider", "get_api_provider", "list_api_providers",
    "unregister_api_provider", "has_api_provider", "clear_api_providers",
    
    # 模型注册表
    "ModelRegistry", "ModelProvider",
    "register_model", "get_model", "get_models_by_provider",
    "list_providers", "list_all_models", "find_model_by_id",
    "register_models_from_dict",
    
    # 内置注册
    "register_builtin_api_providers", "register_builtin_models",
    "register_all_builtins", "reset_registry",
]
```

### 23. registry/api_registry.py

**路径**: `registry/api_registry.py`

**大小**: 4.5 KB

```python
"""
API注册表
管理不同API类型的提供者
"""

from typing import Dict, Optional, List, Callable, Awaitable, Union, Protocol
from dataclasses import dataclass
from ..core.enums import Api, KnownApi
from ..models import Model
from ..core.messages import Context
from ..streaming.event_stream import AssistantMessageEventStream
from ..utils.stream_options import StreamOptions, SimpleStreamOptions


class ApiProvider(Protocol):
    """
    API提供者接口协议
    
    每个API类型（如openai-completions, anthropic-messages等）都需要注册一个提供者
    """
    
    def stream(
        self,
        model: Model,
        context: Context,
        options: Optional[StreamOptions] = None
    ) -> AssistantMessageEventStream:
        """流式调用"""
        ...
    
    def stream_simple(
        self,
        model: Model,
        context: Context,
        options: Optional[SimpleStreamOptions] = None
    ) -> AssistantMessageEventStream:
        """简化的流式调用"""
        ...


@dataclass
class ApiProviderRecord:
    """API提供者记录"""
    api: str
    stream: Callable
    stream_simple: Callable


class ApiProviderRegistry:
    """API提供者注册表"""
    
    def __init__(self):
        self._providers: Dict[str, ApiProviderRecord] = {}
    
    def register(self, provider: Union[ApiProviderRecord, dict]) -> None:
        """
        注册API提供者
        
        Args:
            provider: 提供者记录，可以是ApiProviderRecord或包含api, stream, stream_simple的字典
        """
        if isinstance(provider, dict):
            provider = ApiProviderRecord(
                api=provider["api"],
                stream=provider["stream"],
                stream_simple=provider["stream_simple"]
            )
        self._providers[provider.api] = provider
    
    def get(self, api: Union[Api, str]) -> Optional[ApiProviderRecord]:
        """
        获取API提供者
        
        Args:
            api: API类型
            
        Returns:
            提供者记录，如果未注册则返回None
        """
        api_str = api.value if hasattr(api, 'value') else api
        return self._providers.get(api_str)
    
    def list(self) -> List[str]:
        """列出所有已注册的API类型"""
        return list(self._providers.keys())
    
    def unregister(self, api: Union[Api, str]) -> Optional[ApiProviderRecord]:
        """
        注销API提供者
        
        Args:
            api: API类型
            
        Returns:
            被注销的提供者记录，如果未注册则返回None
        """
        api_str = api.value if hasattr(api, 'value') else api
        return self._providers.pop(api_str, None)
    
    def has_provider(self, api: Union[Api, str]) -> bool:
        """检查是否已注册指定API的提供者"""
        api_str = api.value if hasattr(api, 'value') else api
        return api_str in self._providers
    
    def clear(self) -> None:
        """清空所有注册的提供者"""
        self._providers.clear()


# 全局注册表实例
_registry = ApiProviderRegistry()


def register_api_provider(provider: Union[ApiProviderRecord, dict]) -> None:
    """
    注册API提供者（便捷函数）
    
    Args:
        provider: 提供者记录
    """
    _registry.register(provider)


def get_api_provider(api: Union[Api, str]) -> Optional[ApiProviderRecord]:
    """
    获取API提供者（便捷函数）
    
    Args:
        api: API类型
        
    Returns:
        提供者记录，如果未注册则返回None
    """
    return _registry.get(api)


def list_api_providers() -> List[str]:
    """列出所有已注册的API类型（便捷函数）"""
    return _registry.list()


def unregister_api_provider(api: Union[Api, str]) -> Optional[ApiProviderRecord]:
    """
    注销API提供者（便捷函数）
    
    Args:
        api: API类型
        
    Returns:
        被注销的提供者记录
    """
    return _registry.unregister(api)


def has_api_provider(api: Union[Api, str]) -> bool:
    """
    检查是否已注册指定API的提供者
    
    Args:
        api: API类型
        
    Returns:
        是否已注册
    """
    return _registry.has_provider(api)


def clear_api_providers() -> None:
    """清空所有注册的API提供者"""
    _registry.clear()


__all__ = [
    "ApiProvider",
    "ApiProviderRecord",
    "ApiProviderRegistry",
    "register_api_provider",
    "get_api_provider",
    "list_api_providers",
    "unregister_api_provider",
    "has_api_provider",
    "clear_api_providers",
]
```

### 24. registry/builtins.py

**路径**: `registry/builtins.py`

**大小**: 2.4 KB

```python
"""
内置组件注册
集中注册所有内置的API提供者和模型
"""

from .api_registry import clear_api_providers, register_api_provider
from .model_registry import clear_model_registry, register_models_from_dict
from ..core.enums import KnownApi, KnownProvider

# 导入API提供者

try:
    from ..providers.openai_completions import stream_openai_completions, stream_simple_openai_completions
    HAS_OPENAI_COMPLETIONS = True
except ImportError:
    HAS_OPENAI_COMPLETIONS = False


# 导入模型数据
try:
    from ..models.openai import OPENAI_MODELS
    HAS_OPENAI_MODELS = True
except ImportError:
    HAS_OPENAI_MODELS = False

try:
    from ..models.anthropic import ANTHROPIC_MODELS
    HAS_ANTHROPIC_MODELS = True
except ImportError:
    HAS_ANTHROPIC_MODELS = False

try:
    from ..models.google import GOOGLE_MODELS
    HAS_GOOGLE_MODELS = True
except ImportError:
    HAS_GOOGLE_MODELS = False

try:
    from ..models.volcengine import VOLCENGINE_MODELS
    HAS_VOLCENGINE_MODELS = True
except ImportError:
    HAS_VOLCENGINE_MODELS = False


def register_builtin_api_providers() -> None:
    """注册所有内置的API提供者"""
    
    # OpenAI Completions
    if HAS_OPENAI_COMPLETIONS:
        register_api_provider({
            "api": KnownApi.OPENAI_COMPLETIONS,
            "stream": stream_openai_completions,
            "stream_simple": stream_simple_openai_completions,
        })


def register_builtin_models() -> None:
    """注册所有内置的模型"""
    
    # OpenAI 模型
    if HAS_OPENAI_MODELS:
        register_models_from_dict(KnownProvider.OPENAI, OPENAI_MODELS)
    
    # Anthropic 模型
    if HAS_ANTHROPIC_MODELS:
        register_models_from_dict(KnownProvider.ANTHROPIC, ANTHROPIC_MODELS)
    
    # Google 模型
    if HAS_GOOGLE_MODELS:
        register_models_from_dict(KnownProvider.GOOGLE, GOOGLE_MODELS)

    # Volcengine 模型
    if HAS_VOLCENGINE_MODELS:
        register_models_from_dict(KnownProvider.VOLCENGINE, VOLCENGINE_MODELS)


def register_all_builtins() -> None:
    """注册所有内置组件（API提供者和模型）"""
    register_builtin_api_providers()
    register_builtin_models()


def reset_registry() -> None:
    """重置所有注册表"""
    clear_api_providers()
    clear_model_registry()
    register_all_builtins()


__all__ = [
    "register_builtin_api_providers",
    "register_builtin_models",
    "register_all_builtins",
    "reset_registry",
]
```

### 25. registry/model_registry.py

**路径**: `registry/model_registry.py`

**大小**: 6.1 KB

```python
"""
模型注册表
管理模型注册和查询
"""

from typing import Dict, Optional, List, Union, Any
from ..models import Model
from ..core.enums import KnownProvider


class ModelProvider:
    """模型提供者信息"""
    
    def __init__(self, name: str, models: Dict[str, Model] = None):
        self.name = name
        self.models = models or {}


class ModelRegistry:
    """模型注册表"""
    
    def __init__(self):
        self._providers: Dict[str, ModelProvider] = {}
    
    def register_model(self, provider: str, model: Model) -> None:
        """
        注册单个模型
        
        Args:
            provider: 提供商名称
            model: 模型对象
        """
        if provider not in self._providers:
            self._providers[provider] = ModelProvider(provider)
        
        self._providers[provider].models[model.id] = model
    
    def register_models(self, provider: str, models: Dict[str, Model]) -> None:
        """
        注册多个模型
        
        Args:
            provider: 提供商名称
            models: 模型字典
        """
        if provider not in self._providers:
            self._providers[provider] = ModelProvider(provider)
        
        self._providers[provider].models.update(models)
    
    def get_model(self, provider: str, model_id: str) -> Optional[Model]:
        """
        通过提供商和模型ID获取模型（双key查找）
        
        Args:
            provider: 提供商名称
            model_id: 模型ID
            
        Returns:
            找到的模型，如果不存在则返回None
        """
        if provider in self._providers:
            return self._providers[provider].models.get(model_id)
        return None
    
    
    def get_models_by_provider(self, provider: str) -> Dict[str, Model]:
        """获取指定提供商的所有模型"""
        if provider in self._providers:
            return self._providers[provider].models.copy()
        return {}
    
    def list_providers(self) -> List[str]:
        """列出所有提供商"""
        return list(self._providers.keys())
    
    def list_all_models(self) -> Dict[str, Dict[str, Model]]:
        """
        列出所有模型，按提供商分组
        
        Returns:
            按提供商分组的模型字典
        """
        result = {}
        for provider_name, provider in self._providers.items():
            result[provider_name] = provider.models.copy()
        return result
    
    def list_all_models_flat(self) -> Dict[str, Model]:
        """
        列出所有模型，扁平化返回
        注意：如果多个提供商有相同ID的模型，后面的会覆盖前面的
        
        Returns:
            模型ID到模型的映射字典
        """
        result = {}
        for provider in self._providers.values():
            result.update(provider.models)
        return result
    
    def find_model(self, model_id: str) -> Optional[Model]:
        """通过ID查找模型（同get_model_by_id）"""
        return self.get_model_by_id(model_id)
    
    def remove_model(self, provider: str, model_id: str) -> bool:
        """
        移除指定模型
        
        Args:
            provider: 提供商名称
            model_id: 模型ID
            
        Returns:
            是否成功移除
        """
        if provider in self._providers:
            if model_id in self._providers[provider].models:
                del self._providers[provider].models[model_id]
                # 如果提供商没有模型了，可以选择是否移除该提供商
                return True
        return False
    
    def remove_provider(self, provider: str) -> bool:
        """
        移除指定提供商及其所有模型
        
        Args:
            provider: 提供商名称
            
        Returns:
            是否成功移除
        """
        if provider in self._providers:
            del self._providers[provider]
            return True
        return False
    
    def clear(self) -> None:
        """清空注册表"""
        self._providers.clear()


# 全局注册表实例
_model_registry = ModelRegistry()


def register_model(provider: str, model: Model) -> None:
    """注册模型"""
    _model_registry.register_model(provider, model)


def register_models_from_dict(provider: str, models: Dict[str, Model]) -> None:
    """从字典注册模型"""
    _model_registry.register_models(provider, models)


def get_model(provider: str, model_id: str) -> Optional[Model]:
    """通过提供商和模型ID获取模型"""
    return _model_registry.get_model(provider, model_id)


def get_model_by_id(model_id: str) -> Optional[Model]:
    """通过ID在所有提供商中查找模型"""
    return _model_registry.get_model_by_id(model_id)


def get_models_by_provider(provider: str) -> Dict[str, Model]:
    """获取指定提供商的所有模型"""
    return _model_registry.get_models_by_provider(provider)


def list_providers() -> List[str]:
    """列出所有提供商"""
    return _model_registry.list_providers()


def list_all_models() -> Dict[str, Dict[str, Model]]:
    """列出所有模型（按提供商分组）"""
    return _model_registry.list_all_models()


def list_all_models_flat() -> Dict[str, Model]:
    """列出所有模型（扁平化）"""
    return _model_registry.list_all_models_flat()


def find_model_by_id(model_id: str) -> Optional[Model]:
    """通过ID查找模型"""
    return _model_registry.find_model(model_id)


def remove_model(provider: str, model_id: str) -> bool:
    """移除指定模型"""
    return _model_registry.remove_model(provider, model_id)


def remove_provider(provider: str) -> bool:
    """移除指定提供商及其所有模型"""
    return _model_registry.remove_provider(provider)


def clear_model_registry() -> None:
    """清空模型注册表"""
    _model_registry.clear()


__all__ = [
    "ModelRegistry", "ModelProvider",
    "register_model", "get_model", 
    "get_models_by_provider", "list_providers", 
    "list_all_models", "list_all_models_flat", "find_model_by_id",
    "register_models_from_dict", "remove_model", "remove_provider",
    "clear_model_registry",
]
```

### 26. streaming/__init__.py

**路径**: `streaming/__init__.py`

**大小**: 1.1 KB

```python
"""
流式处理核心模块
只包含流式处理的核心机制，不包含注册逻辑
"""

# 事件类型
from .events import (
    AssistantMessageEvent,
    StartEvent, TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallDeltaEvent, ToolCallEndEvent,
    DoneEvent, ErrorEvent
)

# 事件流
from .event_stream import (
    EventStream,
    AssistantMessageEventStream,
    create_assistant_message_event_stream
)

# 主要API函数
from .api import (
    stream,
    complete,
    stream_simple,
    complete_simple,
)

__all__ = [
    # 事件类型
    "AssistantMessageEvent",
    "StartEvent", "TextStartEvent", "TextDeltaEvent", "TextEndEvent",
    "ThinkingStartEvent", "ThinkingDeltaEvent", "ThinkingEndEvent",
    "ToolCallStartEvent", "ToolCallDeltaEvent", "ToolCallEndEvent",
    "DoneEvent", "ErrorEvent",
    
    # 事件流
    "EventStream", "AssistantMessageEventStream",
    "create_assistant_message_event_stream",
    
    # 主要API函数
    "stream", "complete", "stream_simple", "complete_simple",
]
```

### 27. streaming/api.py

**路径**: `streaming/api.py`

**大小**: 3.3 KB

```python
"""
主要API函数
提供统一的流式和非流式调用接口
"""

import asyncio
from typing import Optional, TypeVar

from ..core.enums import Api
from ..models import Model
from ..core.messages import Context, AssistantMessage
from .event_stream import AssistantMessageEventStream
from ..utils.stream_options import StreamOptions, SimpleStreamOptions
from ..providers import ProviderStreamOptions
from ..utils.env import get_env_api_key
from ..registry.api_registry import get_api_provider


TApi = TypeVar('TApi', bound=Api)


def resolve_api_provider(api: Api):
    """
    解析API提供者
    
    Args:
        api: API类型
        
    Returns:
        API提供者实例
        
    Raises:
        ValueError: 如果没有注册对应的API提供者
    """
    provider = get_api_provider(api)
    if provider is None:
        raise ValueError(f"No API provider registered for api: {api}")
    return provider


def stream(
    model: Model,
    context: Context,
    options: Optional[ProviderStreamOptions] = None
) -> AssistantMessageEventStream:
    """
    流式调用模型
    
    Args:
        model: 模型对象
        context: 上下文
        options: 流式选项
        
    Returns:
        助手消息事件流
    """
    provider = resolve_api_provider(model.api)
    
    stream_options = None
    if options:
        stream_options = ProviderStreamOptions(
            temperature=options.temperature,
            max_tokens=options.max_tokens,
            signal=options.signal,
            api_key=options.api_key,
            transport=options.transport,
            cache_retention=options.cache_retention,
            session_id=options.session_id,
            headers=options.headers,
            on_payload=options.on_payload,
            max_retry_delay_ms=options.max_retry_delay_ms,
            metadata=options.metadata,
        )
    
    return provider.stream(model, context, stream_options)


async def complete(
    model: Model,
    context: Context,
    options: Optional[ProviderStreamOptions] = None
) -> AssistantMessage:
    """
    完成调用模型（非流式）
    
    Args:
        model: 模型对象
        context: 上下文
        options: 流式选项
        
    Returns:
        完整的助手消息
    """
    event_stream = stream(model, context, options)
    return await event_stream.result()


def stream_simple(
    model: Model,
    context: Context,
    options: Optional[SimpleStreamOptions] = None
) -> AssistantMessageEventStream:
    """
    简化的流式调用
    
    Args:
        model: 模型对象
        context: 上下文
        options: 简化选项
        
    Returns:
        助手消息事件流
    """
    provider = resolve_api_provider(model.api)
    return provider.stream_simple(model, context, options)


async def complete_simple(
    model: Model,
    context: Context,
    options: Optional[SimpleStreamOptions] = None
) -> AssistantMessage:
    """
    简化的完成调用
    
    Args:
        model: 模型对象
        context: 上下文
        options: 简化选项
        
    Returns:
        完整的助手消息
    """
    event_stream = stream_simple(model, context, options)
    return await event_stream.result()


__all__ = [
    "stream",
    "complete",
    "stream_simple",
    "complete_simple",
    "resolve_api_provider",
]
```

### 28. streaming/event_stream.py

**路径**: `streaming/event_stream.py`

**大小**: 3.4 KB

```python
"""
事件流处理
"""

from typing import TypeVar, Generic, AsyncIterator, Optional
import asyncio
from asyncio import Queue

from ..core.messages import AssistantMessage
from .events import AssistantMessageEvent, DoneEvent, ErrorEvent


T = TypeVar('T')
R = TypeVar('R')


class EventStream(Generic[T, R]):
    """
    通用事件流类，支持异步迭代
    """

    def __init__(self, is_complete_func, extract_result_func):
        self._queue: asyncio.Queue[T] = asyncio.Queue()
        self._done = False
        self._final_result_future: asyncio.Future[R] = asyncio.Future()
        self._is_complete = is_complete_func
        self._extract_result = extract_result_func

    def push(self, event: T) -> None:
        """推送事件到流中"""
        if self._done:
            return

        if self._is_complete(event):
            self._done = True
            try:
                result = self._extract_result(event)
                if not self._final_result_future.done():
                    self._final_result_future.set_result(result)
            except Exception as e:
                if not self._final_result_future.done():
                    self._final_result_future.set_exception(e)

        # 将事件放入队列
        try:
            loop = asyncio.get_running_loop()
            loop.call_soon_threadsafe(lambda: self._queue.put_nowait(event))
        except RuntimeError:
            # 没有运行中的事件循环，直接放入
            self._queue.put_nowait(event)

    def end(self, result: Optional[R] = None) -> None:
        """结束流"""
        self._done = True
        if result is not None and not self._final_result_future.done():
            self._final_result_future.set_result(result)
        elif not self._final_result_future.done():
            self._final_result_future.set_exception(
                StopAsyncIteration("Stream ended without result")
            )

    async def __aiter__(self) -> AsyncIterator[T]:
        """异步迭代器"""
        while True:
            try:
                # 如果队列为空且已完成，则停止
                if self._queue.empty() and self._done:
                    break
                
                # 获取下一个事件
                try:
                    event = await asyncio.wait_for(self._queue.get(), timeout=0.1)
                    yield event
                except asyncio.TimeoutError:
                    continue
                    
            except Exception as e:
                break

    async def result(self) -> R:
        """获取最终结果"""
        return await self._final_result_future


class AssistantMessageEventStream(EventStream[AssistantMessageEvent, AssistantMessage]):
    """
    助手消息事件流
    """

    def __init__(self):
        def is_complete(event: AssistantMessageEvent) -> bool:
            return event.type in ["done", "error"]

        def extract_result(event: AssistantMessageEvent) -> AssistantMessage:
            if event.type == "done":
                return event.message
            elif event.type == "error":
                return event.error
            raise ValueError(f"Unexpected event type for final result: {event.type}")

        super().__init__(is_complete, extract_result)


def create_assistant_message_event_stream() -> AssistantMessageEventStream:
    """
    创建助手消息事件流的工厂函数（用于扩展）
    """
    return AssistantMessageEventStream()
```

### 29. streaming/events.py

**路径**: `streaming/events.py`

**大小**: 3.2 KB

```python
"""
事件类型定义
"""

from typing import Union, Literal
from dataclasses import dataclass, field

from ..core.messages import AssistantMessage
from ..core.content import ToolCall


@dataclass
class StartEvent:
    """流开始事件"""
    type: Literal["start"] = "start"
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class TextStartEvent:
    """文本内容开始事件"""
    type: Literal["text_start"] = "text_start"
    content_index: int = 0
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class TextDeltaEvent:
    """文本内容增量事件"""
    type: Literal["text_delta"] = "text_delta"
    content_index: int = 0
    delta: str = ""
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class TextEndEvent:
    """文本内容结束事件"""
    type: Literal["text_end"] = "text_end"
    content_index: int = 0
    content: str = ""
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class ThinkingStartEvent:
    """思考内容开始事件"""
    type: Literal["thinking_start"] = "thinking_start"
    content_index: int = 0
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class ThinkingDeltaEvent:
    """思考内容增量事件"""
    type: Literal["thinking_delta"] = "thinking_delta"
    content_index: int = 0
    delta: str = ""
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class ThinkingEndEvent:
    """思考内容结束事件"""
    type: Literal["thinking_end"] = "thinking_end"
    content_index: int = 0
    content: str = ""
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class ToolCallStartEvent:
    """工具调用开始事件"""
    type: Literal["toolcall_start"] = "toolcall_start"
    content_index: int = 0
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class ToolCallDeltaEvent:
    """工具调用增量事件"""
    type: Literal["toolcall_delta"] = "toolcall_delta"
    content_index: int = 0
    delta: str = ""
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class ToolCallEndEvent:
    """工具调用结束事件"""
    type: Literal["toolcall_end"] = "toolcall_end"
    content_index: int = 0
    tool_call: ToolCall = field(default_factory=ToolCall)
    partial: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class DoneEvent:
    """完成事件"""
    type: Literal["done"] = "done"
    reason: Literal["stop", "length", "toolUse"] = "stop"
    message: AssistantMessage = field(default_factory=AssistantMessage)


@dataclass
class ErrorEvent:
    """错误事件"""
    type: Literal["error"] = "error"
    reason: Literal["aborted", "error"] = "error"
    error: AssistantMessage = field(default_factory=AssistantMessage)


# 助手消息事件联合类型
AssistantMessageEvent = Union[
    StartEvent,
    TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallDeltaEvent, ToolCallEndEvent,
    DoneEvent,
    ErrorEvent
]
```

### 30. utils/__init__.py

**路径**: `utils/__init__.py`

**大小**: 1.5 KB

```python
"""
工具函数模块
"""

from .env import (
    get_env_api_key,
    get_env_api_key_typed,
    get_all_env_api_keys
)

from .copilot import (
    infer_copilot_initiator,
    has_copilot_vision_input,
    build_copilot_dynamic_headers,
    build_copilot_headers_from_messages
)

from .json_parser import parse_streaming_json

from .surrogate import sanitize_surrogates

from .stream_options import (
    build_base_options,
    clamp_reasoning,
    adjust_max_tokens_for_thinking,
    ThinkingBudgets,
    StreamOptions,
    SimpleStreamOptions,
)

from .message_transformer import transform_messages

from .http_proxy import (
    setup_http_proxy,
    get_http_proxy,
    get_https_proxy,
    configure_http_client_proxy,
    is_node_environment,
)

__all__ = [
    # env
    "get_env_api_key",
    "get_env_api_key_typed",
    "get_all_env_api_keys",
    
    # copilot
    "infer_copilot_initiator",
    "has_copilot_vision_input",
    "build_copilot_dynamic_headers",
    "build_copilot_headers_from_messages",
    
    # json_parser
    "parse_streaming_json",
    
    # surrogate
    "sanitize_surrogates",
    
    # stream_options
    "build_base_options",
    "clamp_reasoning",
    "adjust_max_tokens_for_thinking",
    "ThinkingBudgets",
    "StreamOptions",
    "SimpleStreamOptions",
    
    # message_transformer
    "transform_messages",
    
    # http_proxy
    "setup_http_proxy",
    "get_http_proxy",
    "get_https_proxy",
    "configure_http_client_proxy",
    "is_node_environment",
]
```

### 31. utils/copilot.py

**路径**: `utils/copilot.py`

**大小**: 2.5 KB

```python
"""
Copilot 特定的工具函数
用于处理 GitHub Copilot 请求的头部信息
"""

from typing import List, Dict, Literal
from ..core.messages import Message


def infer_copilot_initiator(messages: List[Message]) -> Literal["user", "agent"]:
    """
    推断 Copilot 请求的发起者
    
    Copilot 期望 X-Initiator 头部指示请求是用户发起还是代理发起
    （例如：在助手/工具消息后的后续请求）
    
    Args:
        messages: 消息列表
        
    Returns:
        "user" 或 "agent"
    """
    if not messages:
        return "user"
    
    last = messages[-1]
    # 如果最后一条消息不是用户消息，则是代理发起
    return "agent" if last.role != "user" else "user"


def has_copilot_vision_input(messages: List[Message]) -> bool:
    """
    检查消息中是否包含图像输入
    
    Copilot 在发送图像时需要 Copilot-Vision-Request 头部
    
    Args:
        messages: 消息列表
        
    Returns:
        是否包含图像输入
    """
    for msg in messages:
        # 检查用户消息中的图像
        if msg.role == "user" and isinstance(msg.content, list):
            for content in msg.content:
                if hasattr(content, 'type') and content.type == "image":
                    return True
        
        # 检查工具结果中的图像
        elif msg.role == "toolResult" and isinstance(msg.content, list):
            for content in msg.content:
                if hasattr(content, 'type') and content.type == "image":
                    return True
    
    return False


def build_copilot_dynamic_headers(
    messages: List[Message],
    has_images: bool
) -> Dict[str, str]:
    """
    构建 Copilot 动态请求头部
    
    Args:
        messages: 消息列表
        has_images: 是否包含图像
        
    Returns:
        Copilot 请求头部字典
    """
    headers = {
        "X-Initiator": infer_copilot_initiator(messages),
        "Openai-Intent": "conversation-edits",
    }
    
    if has_images:
        headers["Copilot-Vision-Request"] = "true"
    
    return headers


# 备用：直接检查消息中的图像而不需要外部参数
def build_copilot_headers_from_messages(messages: List[Message]) -> Dict[str, str]:
    """
    直接从消息构建 Copilot 请求头部
    
    Args:
        messages: 消息列表
        
    Returns:
        Copilot 请求头部字典
    """
    return build_copilot_dynamic_headers(
        messages=messages,
        has_images=has_copilot_vision_input(messages)
    )
```

### 32. utils/env.py

**路径**: `utils/env.py`

**大小**: 3.4 KB

```python
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
        "volcengine": "VOLCENGINE_API_KEY",
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
```

### 33. utils/http_proxy.py

**路径**: `utils/http_proxy.py`

**大小**: 2.8 KB

```python
"""
HTTP代理配置
根据环境变量为基于`fetch`的SDK设置HTTP代理
"""

import os
import sys
import platform


def is_node_environment() -> bool:
    """
    检查是否在Node.js环境中
    
    Python中我们检查是否在支持undici的环境中
    """
    # 检查是否在Node.js（通过进程名）
    if platform.system() == "Windows":
        return False
    
    # 检查是否在Bun环境
    if "bun" in sys.executable or os.environ.get("BUN_INSTALL"):
        return True
    
    # 检查是否在Node环境（通过环境变量）
    if os.environ.get("NODE_ENV") or os.environ.get("npm_config_user_agent"):
        return True
    
    return False


def setup_http_proxy() -> None:
    """
    根据环境变量设置HTTP代理
    
    在Node.js环境中，这应该被任何需要为fetch()提供代理支持的代码早期导入。
    ES模块会被缓存，所以多次导入是安全的 - 设置只运行一次。
    """
    if not is_node_environment():
        return
    
    try:
        # 在Python中，我们可以配置urllib3或requests的代理
        # 这里我们只是读取代理环境变量，供其他模块使用
        http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
        https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        
        if http_proxy or https_proxy:
            # 设置环境变量供其他库使用
            if http_proxy and not os.environ.get("HTTP_PROXY"):
                os.environ["HTTP_PROXY"] = http_proxy
            if https_proxy and not os.environ.get("HTTPS_PROXY"):
                os.environ["HTTPS_PROXY"] = https_proxy
            
            # 这里可以导入并配置urllib3或aiohttp的代理
            # 但为了保持简单，我们只设置环境变量
            pass
            
    except Exception:
        # 静默失败，不影响主要功能
        pass


def get_http_proxy() -> str | None:
    """获取HTTP代理配置"""
    return os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")


def get_https_proxy() -> str | None:
    """获取HTTPS代理配置"""
    return os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")


def configure_http_client_proxy(client_kwargs: dict) -> None:
    """
    配置HTTP客户端代理
    
    Args:
        client_kwargs: 客户端参数字典
    """
    http_proxy = get_http_proxy()
    https_proxy = get_https_proxy()
    
    if http_proxy or https_proxy:
        proxies = {}
        if http_proxy:
            proxies["http://"] = http_proxy
        if https_proxy:
            proxies["https://"] = https_proxy
        
        client_kwargs["proxies"] = proxies


__all__ = [
    "setup_http_proxy",
    "get_http_proxy",
    "get_https_proxy",
    "configure_http_client_proxy",
    "is_node_environment",
]
```

### 34. utils/json_parser.py

**路径**: `utils/json_parser.py`

**大小**: 1.0 KB

```python
"""
JSON解析工具
用于解析流式响应中的部分JSON
"""

import json
from typing import TypeVar, Any, Union, Dict, List
from json_repair import repair_json

T = TypeVar('T')


def parse_streaming_json(json_str: str | None) -> Union[Dict[str, Any], List[Any]]:
    """
    解析流式响应中的部分JSON
    
    始终返回一个有效的对象，即使JSON不完整。
    
    Args:
        json_str: 流式响应中的部分JSON字符串
        
    Returns:
        解析后的对象，如果解析失败则返回空对象
    """
    if not json_str or json_str.strip() == "":
        return {}
    
    # 首先尝试标准解析（对于完整JSON最快）
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # 使用 json_repair 修复并解析
    try:
        repaired = repair_json(json_str)
        if repaired:
            return json.loads(repaired)
    except Exception:
        pass
    
    # 如果所有解析都失败，返回空对象
    return {}
```

### 35. utils/message_transformer.py

**路径**: `utils/message_transformer.py`

**大小**: 12.6 KB

```python
"""
消息转换工具
用于跨提供商兼容性的消息转换
"""

from typing import List, Dict, Optional, Set, Callable, Union, Any
import time
from copy import deepcopy

from ..core.messages import (
    Message, UserMessage, AssistantMessage, ToolResultMessage,
    MessageUnion
)
from ..core.content import (
    TextContent, ThinkingContent, ToolCall, ImageContent, ContentUnion
)
from ..models import Model
from ..core.enums import StopReason, Api


def transform_messages(
    messages: List[Message],
    model: Model,
    normalize_tool_call_id: Optional[Callable[[str, Model, AssistantMessage], str]] = None
) -> List[Message]:
    """
    转换消息以实现跨提供商兼容性
    
    Args:
        messages: 原始消息列表
        model: 目标模型
        normalize_tool_call_id: 可选的工具调用ID规范化函数
        
    Returns:
        转换后的消息列表
    """
    # 构建原始工具调用ID到规范化ID的映射
    tool_call_id_map: Dict[str, str] = {}
    
    # 第一遍：转换消息（思考块、工具调用ID规范化）
    transformed: List[Message] = []
    
    for msg in messages:
        # 用户消息保持不变
        if msg.role == "user":
            transformed.append(msg)
            continue
        
        # 处理 toolResult 消息 - 如果有映射则规范化 toolCallId
        if msg.role == "toolResult":
            tool_result = msg
            normalized_id = tool_call_id_map.get(tool_result.tool_call_id)
            if normalized_id and normalized_id != tool_result.tool_call_id:
                # 创建新的 toolResult 消息，更新 toolCallId
                new_tool_result = ToolResultMessage(
                    role="toolResult",
                    tool_call_id=normalized_id,
                    tool_name=tool_result.tool_name,
                    content=tool_result.content,
                    details=tool_result.details,
                    is_error=tool_result.is_error,
                    timestamp=tool_result.timestamp
                )
                transformed.append(new_tool_result)
            else:
                transformed.append(msg)
            continue
        
        # 助手消息需要转换检查
        if msg.role == "assistant":
            assistant_msg = msg
            is_same_model = (
                assistant_msg.provider == model.provider and
                assistant_msg.api == model.api and
                assistant_msg.model == model.id
            )
            
            transformed_content: List[ContentUnion] = []
            
            for block in assistant_msg.content:
                if block.type == "thinking":
                    thinking_block = block
                    
                    # 被屏蔽的思考是加密的不透明内容，仅对同一模型有效
                    # 跨模型时删除以避免API错误
                    if thinking_block.redacted:
                        if is_same_model:
                            transformed_content.append(thinking_block)
                        continue
                    
                    # 对于同一模型：保留带有签名的思考块（用于重放）
                    # 即使思考文本为空（OpenAI加密推理）
                    if is_same_model and thinking_block.thinking_signature:
                        transformed_content.append(thinking_block)
                        continue
                    
                    # 跳过空的思考块，其他转换为纯文本
                    if not thinking_block.thinking or thinking_block.thinking.strip() == "":
                        continue
                    
                    if is_same_model:
                        transformed_content.append(thinking_block)
                    else:
                        # 转换为文本块
                        transformed_content.append(
                            TextContent(
                                type="text",
                                text=thinking_block.thinking
                            )
                        )
                
                elif block.type == "text":
                    text_block = block
                    if is_same_model:
                        transformed_content.append(text_block)
                    else:
                        # 保留文本内容
                        transformed_content.append(
                            TextContent(
                                type="text",
                                text=text_block.text,
                                text_signature=text_block.text_signature if is_same_model else None
                            )
                        )
                
                elif block.type == "toolCall":
                    tool_call = block
                    normalized_tool_call = deepcopy(tool_call)
                    
                    # 跨模型时删除 thought_signature
                    if not is_same_model and tool_call.thought_signature:
                        normalized_tool_call.thought_signature = None
                    
                    # 规范化工具调用ID
                    if not is_same_model and normalize_tool_call_id:
                        normalized_id = normalize_tool_call_id(
                            tool_call.id, 
                            model, 
                            assistant_msg
                        )
                        if normalized_id != tool_call.id:
                            tool_call_id_map[tool_call.id] = normalized_id
                            normalized_tool_call.id = normalized_id
                    
                    transformed_content.append(normalized_tool_call)
                
                else:
                    # 其他类型保持不变
                    transformed_content.append(block)
            
            # 创建新的助手消息
            new_assistant_msg = AssistantMessage(
                role="assistant",
                content=transformed_content,
                api=assistant_msg.api,
                provider=assistant_msg.provider,
                model=assistant_msg.model,
                usage=assistant_msg.usage,
                stop_reason=assistant_msg.stop_reason,
                error_message=assistant_msg.error_message,
                timestamp=assistant_msg.timestamp
            )
            transformed.append(new_assistant_msg)
            continue
        
        # 其他类型保持不变
        transformed.append(msg)
    
    # 第二遍：为孤立的工具调用插入合成的空工具结果
    # 这可以保留思考签名并满足API要求
    result: List[Message] = []
    pending_tool_calls: List[ToolCall] = []
    existing_tool_result_ids: Set[str] = set()
    
    for i, msg in enumerate(transformed):
        
        if msg.role == "assistant":
            assistant_msg = msg
            
            # 如果有待处理的孤立工具调用，现在插入合成结果
            if pending_tool_calls:
                for tc in pending_tool_calls:
                    if tc.id not in existing_tool_result_ids:
                        result.append(
                            ToolResultMessage(
                                role="toolResult",
                                tool_call_id=tc.id,
                                tool_name=tc.name,
                                content=[TextContent(type="text", text="No result provided")],
                                is_error=True,
                                timestamp=int(time.time() * 1000)  # 当前时间戳（毫秒）
                            )
                        )
                pending_tool_calls = []
                existing_tool_result_ids = set()
            
            # 跳过错误/中止的助手消息
            # 这些是不完整的历史记录，不应该重放：
            # - 可能有部分内容（推理而没有消息，不完整的工具调用）
            # - 重放它们可能导致API错误（例如OpenAI "reasoning without following item"）
            # - 模型应该从最后一个有效状态重试
            if assistant_msg.stop_reason in [StopReason.ERROR, StopReason.ABORTED]:
                continue
            
            # 跟踪此助手消息中的工具调用
            tool_calls = [
                block for block in assistant_msg.content 
                if block.type == "toolCall"
            ]
            if tool_calls:
                pending_tool_calls = tool_calls
                existing_tool_result_ids = set()
            
            result.append(msg)
        
        elif msg.role == "toolResult":
            tool_result = msg
            existing_tool_result_ids.add(tool_result.tool_call_id)
            result.append(msg)
        
        elif msg.role == "user":
            # 用户消息中断工具流 - 为孤立调用插入合成结果
            if pending_tool_calls:
                for tc in pending_tool_calls:
                    if tc.id not in existing_tool_result_ids:
                        result.append(
                            ToolResultMessage(
                                role="toolResult",
                                tool_call_id=tc.id,
                                tool_name=tc.name,
                                content=[TextContent(type="text", text="No result provided")],
                                is_error=True,
                                timestamp=int(time.time() * 1000)
                            )
                        )
                pending_tool_calls = []
                existing_tool_result_ids = set()
            result.append(msg)
        
        else:
            result.append(msg)
    
    return result


def normalize_openai_tool_call_id(
    tool_call_id: str,
    model: Model,
    source_msg: AssistantMessage
) -> str:
    """
    OpenAI工具调用ID规范化函数
    
    OpenAI Responses API生成的ID长达450+字符，包含`|`等特殊字符。
    Anthropic等API要求ID匹配 ^[a-zA-Z0-9_-]+$（最多64字符）。
    
    Args:
        tool_call_id: 原始工具调用ID
        model: 目标模型
        source_msg: 源消息
        
    Returns:
        规范化的工具调用ID
    """
    # 如果ID已经是简单格式，直接返回
    import re
    if re.match(r'^[a-zA-Z0-9_-]{1,64}$', tool_call_id):
        return tool_call_id
    
    # 生成简化的ID
    # 使用原始ID的哈希或最后部分
    import hashlib
    
    # 方法1：使用hash截断
    hash_obj = hashlib.sha256(tool_call_id.encode())
    short_id = hash_obj.hexdigest()[:16]
    
    # 方法2：从原始ID提取有效字符
    # 提取字母数字和_-，取最后部分
    valid_chars = ''.join(c for c in tool_call_id if c.isalnum() or c in '_-')
    if valid_chars:
        # 取最后最多16个字符
        short_id = valid_chars[-16:]
    else:
        # 如果完全没有有效字符，使用时间戳
        short_id = f"call_{int(time.time())}"
    
    # 确保不超过64字符
    return short_id[:64]


def normalize_anthropic_tool_call_id(
    tool_call_id: str,
    model: Model,
    source_msg: AssistantMessage
) -> str:
    """
    Anthropic工具调用ID规范化函数
    
    Anthropic要求ID格式: ^[a-zA-Z0-9_-]+$，最多64字符
    
    Args:
        tool_call_id: 原始工具调用ID
        model: 目标模型
        source_msg: 源消息
        
    Returns:
        规范化的工具调用ID
    """
    import re
    
    # 移除所有不允许的字符
    normalized = re.sub(r'[^a-zA-Z0-9_-]', '', tool_call_id)
    
    # 如果结果为空，生成一个默认ID
    if not normalized:
        import hashlib
        import time
        normalized = f"tool_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    
    # 限制长度
    return normalized[:64]


def should_keep_thinking_block(
    thinking_block: ThinkingContent,
    is_same_model: bool
) -> bool:
    """
    判断是否应该保留思考块
    
    Args:
        thinking_block: 思考块
        is_same_model: 是否是同一模型
        
    Returns:
        是否保留
    """
    # 被屏蔽的思考仅对同一模型有效
    if thinking_block.redacted:
        return is_same_model
    
    # 同一模型：只要有签名就保留（即使是空的）
    if is_same_model and thinking_block.thinking_signature:
        return True
    
    # 不同模型：只有有内容的才保留（会转换为文本）
    if not is_same_model:
        return bool(thinking_block.thinking and thinking_block.thinking.strip())
    
    # 同一模型但没有签名：保留有内容的
    return bool(thinking_block.thinking and thinking_block.thinking.strip())
```

### 36. utils/stream_options.py

**路径**: `utils/stream_options.py`

**大小**: 6.3 KB

```python
"""
流选项工具函数
处理模型请求的选项配置
"""

from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass, field

from ..core.enums import ThinkingLevel, CacheRetention, Transport
from ..models import Model


@dataclass
class ThinkingBudgets:
    """各思考级别的token预算"""
    minimal: Optional[int] = None
    low: Optional[int] = None
    medium: Optional[int] = None
    high: Optional[int] = None


@dataclass
class StreamOptions:
    """流式选项"""
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    signal: Optional[Any] = None  # Python中可以使用asyncio.Event或自定义信号
    api_key: Optional[str] = None
    transport: Optional[Transport] = None  # 传输协议偏好
    cache_retention: Optional[CacheRetention] = None
    session_id: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    on_payload: Optional[Callable[[Any], None]] = None
    max_retry_delay_ms: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SimpleStreamOptions(StreamOptions):
    """简单流式选项（带推理配置）"""
    reasoning: Optional[ThinkingLevel] = None
    thinking_budgets: Optional[ThinkingBudgets] = None


def build_base_options(
    model: Model,
    options: Optional[SimpleStreamOptions] = None,
    api_key: Optional[str] = None
) -> StreamOptions:
    """
    构建基础流式选项
    
    Args:
        model: 模型对象
        options: 简单流式选项
        api_key: API密钥
        
    Returns:
        流式选项对象
    """
    return StreamOptions(
        temperature=options.temperature if options else None,
        max_tokens=options.max_tokens or min(model.max_tokens, 32000) if options else min(model.max_tokens, 32000),
        signal=options.signal if options else None,
        api_key=api_key or (options.api_key if options else None),
        transport=options.transport if options else None,
        cache_retention=options.cache_retention if options else None,
        session_id=options.session_id if options else None,
        headers=options.headers if options else None,
        on_payload=options.on_payload if options else None,
        max_retry_delay_ms=options.max_retry_delay_ms if options else None,
        metadata=options.metadata if options else None,
    )


def clamp_reasoning(effort: Optional[ThinkingLevel]) -> Optional[ThinkingLevel]:
    """
    将xhigh思考级别降级为high
    
    Args:
        effort: 思考级别
        
    Returns:
        降级后的思考级别，如果输入为None则返回None
    """
    if effort is None:
        return None
    return ThinkingLevel.HIGH if effort == ThinkingLevel.XHIGH else effort


def adjust_max_tokens_for_thinking(
    base_max_tokens: int,
    model_max_tokens: int,
    reasoning_level: ThinkingLevel,
    custom_budgets: Optional[ThinkingBudgets] = None
) -> Dict[str, int]:
    """
    为思考过程调整最大token数
    
    Args:
        base_max_tokens: 基础最大token数
        model_max_tokens: 模型最大token数
        reasoning_level: 思考级别
        custom_budgets: 自定义预算
        
    Returns:
        包含调整后的max_tokens和thinking_budget的字典
        
    Example:
        >>> result = adjust_max_tokens_for_thinking(4096, 8192, ThinkingLevel.MEDIUM)
        >>> print(result['max_tokens'], result['thinking_budget'])
    """
    # 默认预算
    default_budgets = ThinkingBudgets(
        minimal=1024,
        low=2048,
        medium=8192,
        high=16384
    )
    
    # 合并自定义预算
    budgets = ThinkingBudgets(
        minimal=custom_budgets.minimal if custom_budgets and custom_budgets.minimal is not None else default_budgets.minimal,
        low=custom_budgets.low if custom_budgets and custom_budgets.low is not None else default_budgets.low,
        medium=custom_budgets.medium if custom_budgets and custom_budgets.medium is not None else default_budgets.medium,
        high=custom_budgets.high if custom_budgets and custom_budgets.high is not None else default_budgets.high,
    )
    
    min_output_tokens = 1024
    level = clamp_reasoning(reasoning_level)
    
    if level is None:
        raise ValueError(f"Invalid reasoning level: {reasoning_level}")
    
    # 根据级别获取预算
    thinking_budget = getattr(budgets, level.value)
    if thinking_budget is None:
        raise ValueError(f"No budget defined for thinking level: {level}")
    
    max_tokens = min(base_max_tokens + thinking_budget, model_max_tokens)
    
    # 确保有足够的输出token
    if max_tokens <= thinking_budget:
        thinking_budget = max(0, max_tokens - min_output_tokens)
    
    return {
        'max_tokens': max_tokens,
        'thinking_budget': thinking_budget
    }


def build_thinking_params(
    reasoning_level: Optional[ThinkingLevel],
    custom_budgets: Optional[ThinkingBudgets] = None
) -> Optional[Dict[str, Any]]:
    """
    构建思考参数（用于不同提供商的API）
    
    Args:
        reasoning_level: 思考级别
        custom_budgets: 自定义预算
        
    Returns:
        思考参数字典，如果不需要思考则返回None
    """
    if reasoning_level is None:
        return None
    
    level = clamp_reasoning(reasoning_level)
    
    # 根据不同提供商格式返回
    return {
        'type': 'reasoning',
        'effort': level.value if level else None,
        'budget_tokens': get_thinking_budget(level, custom_budgets)
    }


def get_thinking_budget(
    level: Optional[ThinkingLevel],
    custom_budgets: Optional[ThinkingBudgets] = None
) -> Optional[int]:
    """
    获取指定思考级别的token预算
    
    Args:
        level: 思考级别
        custom_budgets: 自定义预算
        
    Returns:
        token预算，如果级别无效则返回None
    """
    if level is None:
        return None
    
    default_budgets = {
        ThinkingLevel.MINIMAL: 1024,
        ThinkingLevel.LOW: 2048,
        ThinkingLevel.MEDIUM: 8192,
        ThinkingLevel.HIGH: 16384,
        ThinkingLevel.XHIGH: 32768,
    }
    
    # 如果有自定义预算，优先使用
    if custom_budgets:
        budget = getattr(custom_budgets, level.value, None)
        if budget is not None:
            return budget
    
    return default_budgets.get(level)
```

### 37. utils/surrogate.py

**路径**: `utils/surrogate.py`

**大小**: 2.9 KB

```python
"""
代理项对处理工具
移除字符串中未配对的Unicode代理项字符
"""

import re


def sanitize_surrogates(text: str) -> str:
    """
    移除字符串中未配对的Unicode代理项字符。
    
    未配对的代理项（高代理项 0xD800-0xDBFF 没有匹配的低代理项 0xDC00-0xDFFF，
    或反之）会导致许多API提供商出现JSON序列化错误。
    
    基本多文种平面之外的有效的emoji和其他字符使用正确配对的代理项，
    不会受此函数影响。
    
    Args:
        text: 需要清理的文本
        
    Returns:
        移除未配对代理项后的清理文本
        
    Example:
        >>> # 有效的emoji（正确配对的代理项）会被保留
        >>> sanitize_surrogates("Hello 🙈 World")
        'Hello 🙈 World'
        
        >>> # 未配对的高代理项会被移除
        >>> unpaired = chr(0xD83D)  # 没有低代理项的高代理项
        >>> sanitize_surrogates(f"Text {unpaired} here")
        'Text  here'
    """
    if not text:
        return text
    
    # 方法1：使用正则表达式（类似TypeScript版本）
    # 匹配未配对的高代理项（后面没有低代理项）
    # 匹配未配对的低代理项（前面没有高代理项）
    pattern = re.compile(
        r'[\uD800-\uDBFF](?![\uDC00-\uDFFF])|'  # 高代理项后无低代理项
        r'(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]'    # 低代理项前无高代理项
    )
    
    return pattern.sub('', text)


def sanitize_surrogates_iterative(text: str) -> str:
    """
    使用迭代方式移除未配对的代理项（替代方法）
    
    Args:
        text: 需要清理的文本
        
    Returns:
        移除未配对代理项后的清理文本
    """
    if not text:
        return text
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        char = text[i]
        code = ord(char)
        
        # 检查是否为高代理项 (0xD800-0xDBFF)
        if 0xD800 <= code <= 0xDBFF:
            # 检查下一个字符是否存在且为低代理项
            if i + 1 < length and 0xDC00 <= ord(text[i + 1]) <= 0xDFFF:
                # 有效的代理项对，保留两个字符
                result.append(char)
                result.append(text[i + 1])
                i += 2
            else:
                # 未配对的高代理项，跳过
                i += 1
        # 检查是否为低代理项 (0xDC00-0xDFFF)
        elif 0xDC00 <= code <= 0xDFFF:
            # 未配对的低代理项，跳过
            i += 1
        else:
            # 普通字符，保留
            result.append(char)
            i += 1
    
    return ''.join(result)


# 默认使用正则表达式版本（性能更好）
# 如果需要更精确的控制或处理非常大的文本，可以使用迭代版本
__all__ = ['sanitize_surrogates', 'sanitize_surrogates_iterative']
```
