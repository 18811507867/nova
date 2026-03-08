# Core 模块文档

## 概述

`core` 模块是 Nova AI 的核心基础模块，包含所有基础数据类型定义、枚举类型、消息结构和使用统计相关的类型定义。这些类型在整个 Nova AI 生态系统中被广泛使用，为不同的 AI 提供商提供统一的接口抽象。

## 目录结构

```
core/
├── __init__.py          # 核心模块导出文件
├── enums.py             # 枚举类型定义
├── content.py           # 内容类型定义
├── messages.py          # 消息类型定义
├── models.py            # 模型相关类型定义
├── usage.py             # 使用统计类型定义
```

## 模块详解

### 1. enums.py - 枚举类型定义

#### KnownApi 枚举

```python
class KnownApi(str, Enum):
    """已知的 API 类型枚举"""
    OPENAI_COMPLETIONS = "openai-completions"        # OpenAI Completions API
    OPENAI_RESPONSES = "openai-responses"            # OpenAI Responses API
    AZURE_OPENAI_RESPONSES = "azure-openai-responses" # Azure OpenAI Responses API
    OPENAI_CODEX_RESPONSES = "openai-codex-responses" # OpenAI Codex Responses API
    ANTHROPIC_MESSAGES = "anthropic-messages"        # Anthropic Messages API
    BEDROCK_CONVERSE_STREAM = "bedrock-converse-stream" # Bedrock Converse Stream API
    GOOGLE_GENERATIVE_AI = "google-generative-ai"    # Google Generative AI API
    GOOGLE_GEMINI_CLI = "google-gemini-cli"          # Google Gemini CLI API
    GOOGLE_VERTEX = "google-vertex"                  # Google Vertex AI API
```

#### KnownProvider 枚举

```python
class KnownProvider(str, Enum):
    """已知的服务提供商类型枚举"""
    AMAZON_BEDROCK = "amazon-bedrock"               # Amazon Bedrock
    ANTHROPIC = "anthropic"                        # Anthropic
    GOOGLE = "google"                              # Google
    GOOGLE_GEMINI_CLI = "google-gemini-cli"         # Google Gemini CLI
    GOOGLE_ANTIGRAVITY = "google-antigravity"       # Google Antigravity
    GOOGLE_VERTEX = "google-vertex"                # Google Vertex AI
    OPENAI = "openai"                              # OpenAI
    AZURE_OPENAI_RESPONSES = "azure-openai-responses" # Azure OpenAI Responses
    OPENAI_CODEX = "openai-codex"                  # OpenAI Codex
    GITHUB_COPILOT = "github-copilot"              # GitHub Copilot
    XAI = "xai"                                    # xAI
    GROQ = "groq"                                  # Groq
    CEREBRAS = "cerebras"                          # Cerebras
    OPENROUTER = "openrouter"                      # OpenRouter
    VERCEL_AI_GATEWAY = "vercel-ai-gateway"        # Vercel AI Gateway
    ZAI = "zai"                                    # ZAI
    MISTRAL = "mistral"                            # Mistral
    MINIMAX = "minimax"                            # Minimax
    MINIMAX_CN = "minimax-cn"                      # Minimax CN
    HUGGINGFACE = "huggingface"                    # HuggingFace
    OPENCODE = "opencode"                          # OpenCode
    KIMI_CODING = "kimi-coding"                    # Kimi Coding
```

#### StopReason 枚举

```python
class StopReason(str, Enum):
    """停止原因枚举"""
    STOP = "stop"       # 正常结束
    LENGTH = "length"   # 达到长度限制
    TOOL_USE = "toolUse"  # 触发工具调用
    ERROR = "error"     # 发生错误
    ABORTED = "aborted"  # 被中止
```

#### ThinkingLevel 枚举

```python
class ThinkingLevel(str, Enum):
    """思考级别枚举"""
    MINIMAL = "minimal"  # 最小思考
    LOW = "low"          # 低级别思考
    MEDIUM = "medium"    # 中级别思考
    HIGH = "high"        # 高级别思考
    XHIGH = "xhigh"      # 最高级别思考
```

#### CacheRetention 枚举

```python
class CacheRetention(str, Enum):
    """缓存保留策略枚举"""
    NONE = "none"    # 不缓存
    SHORT = "short"  # 短期缓存
    LONG = "long"    # 长期缓存
```

#### Transport 枚举

```python
class Transport(str, Enum):
    """传输协议枚举"""
    SSE = "sse"          # Server-Sent Events
    WEBSOCKET = "websocket" # WebSocket
    AUTO = "auto"        # 自动选择
```

#### ThinkingFormat 枚举

```python
class ThinkingFormat(str, Enum):
    """思考格式枚举（用于不同提供商）"""
    OPENAI = "openai"      # 使用 reasoning_effort (OpenAI格式)
    ZAI = "zai"            # 使用 thinking: { type: "enabled" } (ZAI格式)
    QWEN = "qwen"          # 使用 enable_thinking: boolean (QWEN格式)
```

### 2. content.py - 内容类型定义

#### TextContent 类

```python
@dataclass
class TextContent:
    """文本内容类型"""
    type: Literal["text"] = "text"           # 内容类型
    text: str = ""                           # 文本内容
    text_signature: Optional[str] = None     # 文本签名（如OpenAI响应中的消息ID）
```

#### ThinkingContent 类

```python
@dataclass
class ThinkingContent:
    """思考过程内容类型（推理过程）"""
    type: Literal["thinking"] = "thinking"   # 内容类型
    thinking: str = ""                       # 思考内容
    thinking_signature: Optional[str] = None  # 思考签名（如OpenAI响应中的推理项ID）
    redacted: bool = False                   # 是否被安全过滤器屏蔽
```

#### ToolCall 类

```python
@dataclass
class ToolCall:
    """工具调用类型"""
    type: Literal["toolCall"] = "toolCall"   # 内容类型
    id: str = ""                            # 工具调用ID
    name: str = ""                          # 工具名称
    arguments: Dict[str, Any] = field(default_factory=dict)  # 调用参数
    thought_signature: Optional[str] = None  # Google专用：重用思考上下文的签名
```

#### ImageContent 类

```python
@dataclass
class ImageContent:
    """图像内容类型（用于用户消息和工具结果）"""
    type: Literal["image"] = "image"         # 内容类型
    data: str = ""                           # base64编码的图像数据
    mime_type: str = ""                      # MIME类型
```

#### ContentUnion 类型别名

```python
ContentUnion = TextContent | ThinkingContent | ToolCall | ImageContent
```

### 3. messages.py - 消息类型定义

#### UserMessage 类

```python
@dataclass
class UserMessage:
    """用户消息类型（用于上下文理解）"""
    role: Literal["user"] = "user"           # 角色
    content: Union[str, List[Union[TextContent, ImageContent]]] = field(default_factory=list)  # 内容
    timestamp: int = 0                       # Unix时间戳（毫秒）
```

#### AssistantMessage 类

```python
@dataclass
class AssistantMessage:
    """助手消息类型"""
    role: Literal["assistant"] = "assistant" # 角色
    content: List[Union[TextContent, ThinkingContent, ToolCall]] = field(default_factory=list)  # 内容
    api: Api = ""                           # 使用的API类型
    provider: Provider = ""                 # 服务提供商
    model: str = ""                         # 模型名称
    usage: Usage = field(default_factory=Usage)  # 令牌使用统计
    stop_reason: StopReason = StopReason.STOP  # 停止原因
    error_message: Optional[str] = None      # 错误信息（如果有）
    timestamp: int = 0                       # Unix时间戳（毫秒）
```

#### ToolResultMessage 类

```python
@dataclass
class ToolResultMessage:
    """工具结果消息类型（用于上下文理解）"""
    role: Literal["toolResult"] = "toolResult"  # 角色
    tool_call_id: str = ""                     # 工具调用ID
    tool_name: str = ""                         # 工具名称
    content: List[Union[TextContent, ImageContent]] = field(default_factory=list)  # 内容
    details: Optional[Dict[str, Any]] = None    # 详细信息
    is_error: bool = False                      # 是否为错误结果
    timestamp: int = 0                          # Unix时间戳（毫秒）
```

#### Message 类型别名

```python
Message = Union[UserMessage, AssistantMessage, ToolResultMessage]
```

#### MessageUnion 类型别名

```python
MessageUnion = Message
```

#### Tool 类

```python
@dataclass
class Tool(Generic[T]):
    """工具定义"""
    name: str = ""                           # 工具名称
    description: str = ""                    # 工具描述
    parameters: Optional[T] = None           # 参数定义（应该是 TypeBox TSchema 的对应物）
```

#### Context 类

```python
@dataclass
class Context:
    """上下文类型"""
    system_prompt: Optional[str] = None      # 系统提示
    messages: List[Message] = field(default_factory=list)  # 消息列表
    tools: Optional[List[Tool]] = None       # 工具列表
```

### 4. models.py - 模型相关类型定义

#### ModelCost 类

```python
@dataclass
class ModelCost:
    """模型成本类型（$/百万tokens）"""
    input: float = 0.0          # 输入成本
    output: float = 0.0         # 输出成本
    cache_read: float = 0.0     # 缓存读取成本
    cache_write: float = 0.0    # 缓存写入成本
```

#### Model 类

```python
@dataclass
class Model:
    """模型定义类型"""
    id: str = ""                           # 模型ID
    name: str = ""                         # 模型名称
    api: Api = ""                          # API类型
    provider: Provider = ""                 # 服务提供商
    base_url: str = ""                     # 基础URL
    reasoning: bool = False                 # 是否支持推理
    input_types: List[Literal["text", "image"]] = field(default_factory=list)  # 支持的输入类型
    cost: ModelCost = field(default_factory=ModelCost)  # 成本信息
    context_window: int = 0                 # 上下文窗口大小
    max_tokens: int = 0                     # 最大token数
    headers: Optional[Dict[str, str]] = None  # 自定义请求头
    compat: Optional[Union[OpenAICompletionsCompat, OpenAIResponsesCompat]] = None  # 兼容性配置
```

### 5. usage.py - 使用统计类型定义

#### Cost 类

```python
@dataclass
class Cost:
    """成本明细类型"""
    input: float = 0.0          # 输入成本
    output: float = 0.0         # 输出成本
    cache_read: float = 0.0     # 缓存读取成本
    cache_write: float = 0.0    # 缓存写入成本
    total: float = 0.0          # 总成本
```

#### Usage 类

```python
@dataclass
class Usage:
    """令牌使用统计类型"""
    input: int = 0               # 输入令牌数
    output: int = 0              # 输出令牌数
    cache_read: int = 0          # 缓存读取令牌数
    cache_write: int = 0         # 缓存写入令牌数
    total_tokens: int = 0        # 总令牌数
    cost: Cost = field(default_factory=Cost)  # 成本明细
```

## 使用示例

### 创建用户消息

```python
from nova_ai.core import UserMessage, TextContent

# 创建简单的文本用户消息
user_message = UserMessage(
    role="user",
    content="你好，请帮我分析这个问题",
    timestamp=1640995200000
)

# 创建包含图像的用户消息
user_message_with_image = UserMessage(
    role="user",
    content=[
        TextContent(text="请分析这张图片"),
        ImageContent(
            data="base64_encoded_image_data",
            mime_type="image/jpeg"
        )
    ],
    timestamp=1640995200000
)
```

### 创建助手消息

```python
from nova_ai.core import AssistantMessage, TextContent, ThinkingContent, ToolCall
from nova_ai.core.enums import StopReason, KnownApi, KnownProvider

assistant_message = AssistantMessage(
    role="assistant",
    content=[
        ThinkingContent(thinking="让我先思考一下这个问题..."),
        TextContent(text="根据我的分析，答案是42"),
        ToolCall(
            id="tool_call_123",
            name="calculate",
            arguments={"a": 21, "b": 21}
        )
    ],
    api=KnownApi.OPENAI_RESPONSES,
    provider=KnownProvider.OPENAI,
    model="gpt-4",
    stop_reason=StopReason.STOP,
    timestamp=1640995200000
)
```

### 创建工具结果消息

```python
from nova_ai.core import ToolResultMessage, TextContent

tool_result = ToolResultMessage(
    role="toolResult",
    tool_call_id="tool_call_123",
    tool_name="calculate",
    content=[TextContent(text="计算结果：42")],
    details={"execution_time": "0.5s"},
    is_error=False,
    timestamp=1640995200000
)
```

## 类型关系图

```
                          +----------------+
                          |   Content      |
                          +----------------+
                          | - TextContent  |
                          | - ThinkingContent
                          | - ToolCall     |
                          | - ImageContent |
                          +----------------+
                                  |
                                  | contains
                                  v
+----------------+       +----------------+
|   Message      |<------|   UserMessage  |
+----------------+       +----------------+
| - role         |       | - content: str |
| - content      |       |   or list      |
| - timestamp    |       +----------------+
+----------------+               |
        |                       |
        | implements            | implements
        v                       v
+----------------+       +----------------+
| AssistantMessage|      | ToolResultMessage|
+----------------+       +----------------+
| - api          |       | - tool_call_id |
| - provider     |       | - tool_name    |
| - model        |       | - details      |
| - usage        |       | - is_error    |
| - stop_reason  |       +----------------+
| - error_message|
+----------------+
```

## 注意事项

1. **时间戳**：所有消息类型都使用毫秒级Unix时间戳
2. **内容签名**：`text_signature` 和 `thinking_signature` 用于API响应中的特定标识符
3. **内容类型**：`ContentUnion` 提供了类型安全的联合类型
4. **错误处理**：`AssistantMessage` 包含 `error_message` 用于错误追踪
5. **使用统计**：`Usage` 类提供了完整的token使用和成本统计

## 扩展性

Core 模块设计为可扩展的，可以通过以下方式添加新的类型：

1. 在 `enums.py` 中添加新的枚举值
2. 在 `content.py` 中添加新的内容类型
3. 在 `messages.py` 中添加新的消息类型
4. 更新相应的联合类型定义

所有类型都使用 `dataclass` 装饰器，确保良好的序列化和反序列化支持。