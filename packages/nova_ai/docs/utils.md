# Nova AI Utils 模块文档

## 目录

- [概述](#概述)
- [模块结构](#模块结构)
- [Copilot 工具函数](#copilot-工具函数)
  - [infer_copilot_initiator](#infer_copilot_initiator)
  - [has_copilot_vision_input](#has_copilot_vision_input)
  - [build_copilot_dynamic_headers](#build_copilot_dynamic_headers)
  - [build_copilot_headers_from_messages](#build_copilot_headers_from_messages)
- [环境变量工具](#环境变量工具)
  - [get_env_api_key](#get_env_api_key)
  - [get_env_api_key_typed](#get_env_api_key_typed)
  - [get_all_env_api_keys](#get_all_env_api_keys)
- [JSON 解析工具](#json-解析工具)
  - [parse_streaming_json](#parse_streaming_json)
- [字符串处理工具](#字符串处理工具)
  - [sanitize_surrogates](#sanitize_surrogates)
  - [sanitize_surrogates_iterative](#sanitize_surrogates_iterative)
- [流选项工具](#流选项工具)
  - [ThinkingBudgets](#thinkingbudgets)
  - [StreamOptions](#streamoptions)
  - [SimpleStreamOptions](#simplestreamoptions)
  - [build_base_options](#build_base_options)
  - [clamp_reasoning](#clamp_reasoning)
  - [adjust_max_tokens_for_thinking](#adjust_max_tokens_for_thinking)
  - [build_thinking_params](#build_thinking_params)
  - [get_thinking_budget](#get_thinking_budget)
- [消息转换工具](#消息转换工具)
  - [transform_messages](#transform_messages)
  - [normalize_openai_tool_call_id](#normalize_openai_tool_call_id)
  - [normalize_anthropic_tool_call_id](#normalize_anthropic_tool_call_id)
  - [should_keep_thinking_block](#should_keep_thinking_block)

## 概述

`utils` 模块包含 Nova AI 框架的核心工具函数，用于处理各种跨提供商兼容性、认证、消息转换和流式处理相关的功能。这些工具函数被设计为可重用、类型安全的辅助函数，支持整个 AI 代理系统的运行。

## 模块结构

```
nova_ai/
├── utils/
    ├── __init__.py          # 模块导出
    ├── copilot.py           # Copilot 特定工具
    ├── env.py              # 环境变量处理
    ├── json_parser.py      # JSON 流式解析
    ├── message_transformer.py  # 消息转换
    ├── stream_options.py   # 流选项配置
    └── surrogate.py        # 字符串代理项处理
```

## Copilot 工具函数

### infer_copilot_initiator

推断 Copilot 请求的发起者类型。

**函数签名:**
```python
def infer_copilot_initiator(messages: List[Message]) -> Literal["user", "agent"]
```

**参数:**
- `messages`: 消息列表

**返回值:**
- `"user"` 或 `"agent"`，表示请求是由用户还是代理发起的

**说明:**
Copilot 期望 `X-Initiator` 头部指示请求是用户发起还是代理发起（例如：在助手/工具消息后的后续请求）。

### has_copilot_vision_input

检查消息中是否包含图像输入。

**函数签名:**
```python
def has_copilot_vision_input(messages: List[Message]) -> bool
```

**参数:**
- `messages`: 消息列表

**返回值:**
- `bool`: 是否包含图像输入

**说明:**
Copilot 在发送图像时需要 `Copilot-Vision-Request` 头部。

### build_copilot_dynamic_headers

构建 Copilot 动态请求头部。

**函数签名:**
```python
def build_copilot_dynamic_headers(
    messages: List[Message],
    has_images: bool
) -> Dict[str, str]
```

**参数:**
- `messages`: 消息列表
- `has_images`: 是否包含图像

**返回值:**
- `Dict[str, str]`: Copilot 请求头部字典

### build_copilot_headers_from_messages

直接从消息构建 Copilot 请求头部。

**函数签名:**
```python
def build_copilot_headers_from_messages(messages: List[Message]) -> Dict[str, str]
```

**参数:**
- `messages`: 消息列表

**返回值:**
- `Dict[str, str]`: Copilot 请求头部字典

## 环境变量工具

### get_env_api_key

从环境变量获取提供商的 API 密钥。

**函数签名:**
```python
def get_env_api_key(provider: str) -> Optional[str]
```

**参数:**
- `provider`: 提供商名称

**返回值:**
- `Optional[str]`: API 密钥或 None

**说明:**
对于需要 OAuth 令牌的提供商不会返回 API 密钥。支持以下提供商：
- GitHub Copilot: `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`
- Anthropic: `ANTHROPIC_OAUTH_TOKEN` (优先), `ANTHROPIC_API_KEY`
- Vertex AI: 使用 Application Default Credentials
- Amazon Bedrock: 支持多种认证源
- 其他标准 API 密钥映射

### get_env_api_key_typed

类型化的 `get_env_api_key` 版本。

**函数签名:**
```python
def get_env_api_key_typed(provider: KnownProvider) -> Optional[str]
```

**参数:**
- `provider`: KnownProvider 枚举

**返回值:**
- `Optional[str]`: API 密钥或 None

### get_all_env_api_keys

获取所有已知提供商的环境变量值。

**函数签名:**
```python
def get_all_env_api_keys() -> Dict[str, Optional[str]]
```

**返回值:**
- `Dict[str, Optional[str]]`: 提供商到 API 密钥的映射字典

**说明:**
隐藏实际密钥值，只显示是否存在。

## JSON 解析工具

### parse_streaming_json

解析流式响应中的部分 JSON。

**函数签名:**
```python
def parse_streaming_json(json_str: str | None) -> Union[Dict[str, Any], List[Any]]
```

**参数:**
- `json_str`: 流式响应中的部分 JSON 字符串

**返回值:**
- `Union[Dict[str, Any], List[Any]]`: 解析后的对象，如果解析失败则返回空对象

**说明:**
始终返回一个有效的对象，即使 JSON 不完整。使用 `json_repair` 库修复损坏的 JSON。

## 字符串处理工具

### sanitize_surrogates

移除字符串中未配对的 Unicode 代理项字符。

**函数签名:**
```python
def sanitize_surrogates(text: str) -> str
```

**参数:**
- `text`: 需要清理的文本

**返回值:**
- `str`: 移除未配对代理项后的清理文本

**说明:**
未配对的代理项（高代理项 0xD800-0xDBFF 没有匹配的低代理项 0xDC00-0xDFFF，或反之）会导致许多 API 提供商出现 JSON 序列化错误。基本多文种平面之外的有效 emoji 和其他字符使用正确配对的代理项，不会受此函数影响。

### sanitize_surrogates_iterative

使用迭代方式移除未配对的代理项（替代方法）。

**函数签名:**
```python
def sanitize_surrogates_iterative(text: str) -> str
```

**参数:**
- `text`: 需要清理的文本

**返回值:**
- `str`: 移除未配对代理项后的清理文本

## 流选项工具

### ThinkingBudgets

**类定义:**
```python
@dataclass
class ThinkingBudgets:
    """各思考级别的token预算"""
    minimal: Optional[int] = None
    low: Optional[int] = None
    medium: Optional[int] = None
    high: Optional[int] = None
```

### StreamOptions

**类定义:**
```python
@dataclass
class StreamOptions:
    """流式选项"""
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    signal: Any = None
    api_key: Optional[str] = None
    transport: Optional[Transport] = None
    cache_retention: Optional[CacheRetention] = None
    session_id: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    on_payload: Optional[Callable[[Any], None]] = None
    max_retry_delay_ms: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
```

### SimpleStreamOptions

**类定义:**
```python
@dataclass
class SimpleStreamOptions(StreamOptions):
    """简单流式选项（带推理配置）"""
    reasoning: Optional[ThinkingLevel] = None
    thinking_budgets: Optional[ThinkingBudgets] = None
```

### build_base_options

构建基础流式选项。

**函数签名:**
```python
def build_base_options(
    model: Model,
    options: Optional[SimpleStreamOptions] = None,
    api_key: Optional[str] = None
) -> StreamOptions
```

**参数:**
- `model`: 模型对象
- `options`: 简单流式选项
- `api_key`: API 密钥

**返回值:**
- `StreamOptions`: 流式选项对象

### clamp_reasoning

将 xhigh 思考级别降级为 high。

**函数签名:**
```python
def clamp_reasoning(effort: Optional[ThinkingLevel]) -> Optional[ThinkingLevel]
```

**参数:**
- `effort`: 思考级别

**返回值:**
- `Optional[ThinkingLevel]`: 降级后的思考级别，如果输入为 None 则返回 None

### adjust_max_tokens_for_thinking

为思考过程调整最大 token 数。

**函数签名:**
```python
def adjust_max_tokens_for_thinking(
    base_max_tokens: int,
    model_max_tokens: int,
    reasoning_level: ThinkingLevel,
    custom_budgets: Optional[ThinkingBudgets] = None
) -> Dict[str, int]
```

**参数:**
- `base_max_tokens`: 基础最大 token 数
- `model_max_tokens`: 模型最大 token 数
- `reasoning_level`: 思考级别
- `custom_budgets`: 自定义预算

**返回值:**
- `Dict[str, int]`: 包含调整后的 max_tokens 和 thinking_budget 的字典

### build_thinking_params

构建思考参数（用于不同提供商的 API）。

**函数签名:**
```python
def build_thinking_params(
    reasoning_level: Optional[ThinkingLevel],
    custom_budgets: Optional[ThinkingBudgets] = None
) -> Optional[Dict[str, Any]]
```

**参数:**
- `reasoning_level`: 思考级别
- `custom_budgets`: 自定义预算

**返回值:**
- `Optional[Dict[str, Any]]`: 思考参数字典，如果不需要思考则返回 None

### get_thinking_budget

获取指定思考级别的 token 预算。

**函数签名:**
```python
def get_thinking_budget(
    level: Optional[ThinkingLevel],
    custom_budgets: Optional[ThinkingBudgets] = None
) -> Optional[int]
```

**参数:**
- `level`: 思考级别
- `custom_budgets`: 自定义预算

**返回值:**
- `Optional[int]`: token 预算，如果级别无效则返回 None

## 消息转换工具

### transform_messages

转换消息以实现跨提供商兼容性。

**函数签名:**
```python
def transform_messages(
    messages: List[Message],
    model: Model,
    normalize_tool_call_id: Optional[Callable[[str, Model, AssistantMessage], str]] = None
) -> List[Message]
```

**参数:**
- `messages`: 原始消息列表
- `model`: 目标模型
- `normalize_tool_call_id`: 可选的工具调用 ID 规范化函数

**返回值:**
- `List[Message]`: 转换后的消息列表

### normalize_openai_tool_call_id

OpenAI 工具调用 ID 规范化函数。

**函数签名:**
```python
def normalize_openai_tool_call_id(
    tool_call_id: str,
    model: Model,
    source_msg: AssistantMessage
) -> str
```

**参数:**
- `tool_call_id`: 原始工具调用 ID
- `model`: 目标模型
- `source_msg`: 源消息

**返回值:**
- `str`: 规范化的工具调用 ID

**说明:**
OpenAI Responses API 生成的 ID 长达 450+ 字符，包含 `|` 等特殊字符。Anthropic 等 API 要求 ID 匹配 `^[a-zA-Z0-9_-]+$`（最多 64 字符）。

### normalize_anthropic_tool_call_id

Anthropic 工具调用 ID 规范化函数。

**函数签名:**
```python
def normalize_anthropic_tool_call_id(
    tool_call_id: str,
    model: Model,
    source_msg: AssistantMessage
) -> str
```

**参数:**
- `tool_call_id`: 原始工具调用 ID
- `model`: 目标模型
- `source_msg`: 源消息

**返回值:**
- `str`: 规范化的工具调用 ID

**说明:**
Anthropic 要求 ID 格式: `^[a-zA-Z0-9_-]+$`，最多 64 字符。

### should_keep_thinking_block

判断是否应该保留思考块。

**函数签名:**
```python
def should_keep_thinking_block(
    thinking_block: ThinkingContent,
    is_same_model: bool
) -> bool
```

**参数:**
- `thinking_block`: 思考块
- `is_same_model`: 是否是同一模型

**返回值:**
- `bool`: 是否保留

**说明:**
被屏蔽的思考仅对同一模型有效。同一模型：只要有签名就保留（即使是空的）。不同模型：只有有内容的才保留（会转换为文本）。