# Nova AI - 统一AI模型接口框架

## 概述

Nova AI 是一个现代化的统一AI模型接口框架，为开发者提供一致的API来访问各种AI提供商（OpenAI、Anthropic、Google、GitHub Copilot等）的模型服务。框架抽象了不同提供商的API差异，提供类型安全的流式处理和统一的错误处理机制。

## 主要特性

- **多提供商支持**: 支持 OpenAI、Anthropic、Google、GitHub Copilot、Amazon Bedrock 等主流AI服务
- **统一接口**: 一致的API设计，无需关心不同提供商的API差异
- **类型安全**: 完整的类型注解和数据结构定义
- **流式处理**: 支持实时流式响应处理
- **工具调用**: 统一的工具调用和结果处理机制
- **成本计算**: 自动计算API调用成本和token使用量
- **兼容性层**: 处理不同提供商的API兼容性问题

## 目录结构

```
nova_ai/
├── __init__.py              # 主模块导出
├── auth/                   # 认证模块
│   ├── __init__.py
│   ├── bedrock.py         # Amazon Bedrock 认证
│   ├── vertex.py          # Google Vertex AI 认证
├── compat/                 # 兼容性配置模块
│   ├── __init__.py
│   ├── openai.py          # OpenAI 兼容性配置
│   ├── routing.py         # 路由配置
├── core/                   # 核心类型定义
│   ├── __init__.py
│   ├── content.py         # 内容类型定义
│   ├── enums.py          # 枚举类型定义
│   ├── messages.py       # 消息类型定义
│   ├── models.py         # 模型相关类型
│   ├── usage.py          # 使用统计类型
├── models/                 # 模型定义和注册表
│   ├── __init__.py
│   ├── anthropic.py      # Anthropic 模型定义
│   ├── base.py          # 基础模型类型
│   ├── google.py         # Google 模型定义
│   ├── openai.py         # OpenAI 模型定义
│   ├── registry.py       # 模型注册表
├── provider/               # 提供商实现
│   ├── openai_completions.py  # OpenAI Completions 实现
├── streaming/             # 流式处理模块
│   ├── __init__.py
│   ├── event_stream.py   # 事件流处理
│   ├── events.py        # 事件类型定义
├── utils/                 # 工具函数模块
    ├── __init__.py
    ├── copilot.py         # Copilot 工具函数
    ├── env.py            # 环境变量工具
    ├── json_parser.py    # JSON 解析工具
    ├── message_transformer.py  # 消息转换工具
    ├── stream_options.py # 流选项工具
    ├── surrogate.py      # 代理项对处理工具
```

## 快速开始

### 安装

```bash
pip install nova-ai
```

### 基本用法

```python
from nova_ai import AssistantMessageEventStream
from nova_ai.core.messages import UserMessage, Context
from nova_ai.models.registry import get_model

# 获取模型
model = get_model("openai", "gpt-4.1")

# 创建上下文
context = Context(
    system_prompt="你是一个有帮助的助手",
    messages=[UserMessage(content="你好，请介绍一下你自己")]
)

# 创建流式处理
stream = AssistantMessageEventStream()

# 处理流事件
async for event in stream:
    if event.type == "text_delta":
        print(event.delta, end="", flush=True)
    elif event.type == "done":
        print("\n--- 完成 ---")
        print(f"总token使用: {event.message.usage.total_tokens}")
```

## 核心概念

### 消息系统

Nova AI 使用统一的消息格式来处理与AI模型的交互：

- **UserMessage**: 用户输入消息
- **AssistantMessage**: AI助手回复消息
- **ToolResultMessage**: 工具调用结果消息

### 内容类型

支持多种内容类型：
- **TextContent**: 文本内容
- **ThinkingContent**: 思考过程内容（推理）
- **ToolCall**: 工具调用
- **ImageContent**: 图像内容

### 模型注册表

框架维护一个模型注册表，可以：
- 按提供商查询模型
- 根据能力过滤模型
- 自动计算使用成本
- 管理自定义模型注册

## 模块详细说明

- [**认证模块 (auth)**](./auth.md) - 处理各提供商的认证逻辑
- [**兼容性模块 (compat)**](./compat.md) - 处理不同API提供商的兼容性配置
- [**核心类型模块 (core)**](./core.md) - 基础数据类型和枚举定义
- [**模型模块 (models)**](./models.md) - 模型定义和注册表管理
- [**提供商模块 (provider)**](./provider.md) - 具体提供商的API实现
- [**流式处理模块 (streaming)**](./streaming.md) - 事件流处理和类型定义
- [**工具函数模块 (utils)**](./utils.md) - 辅助工具函数

## 支持的提供商

| 提供商 | 支持状态 | 主要模型 |
|--------|----------|----------|
| OpenAI | ✅ 完全支持 | GPT-4.1, GPT-4, GPT-3.5, o1系列 |
| Anthropic | ✅ 完全支持 | Claude 3.5系列, Claude 3系列 |
| Google | ✅ 完全支持 | Gemini 2.0, Gemini 1.5系列 |
| GitHub Copilot | ✅ 完全支持 | Copilot模型 |
| Amazon Bedrock | ✅ 完全支持 | 通过Bedrock访问的模型 |
| Azure OpenAI | ✅ 完全支持 | Azure托管的OpenAI模型 |

## 环境变量配置

框架支持通过环境变量配置API密钥：

```bash
export OPENAI_API_KEY=your_openai_key
export ANTHROPIC_API_KEY=your_anthropic_key
export GEMINI_API_KEY=your_google_key
# 其他提供商...
```

## 错误处理

框架提供统一的错误处理机制：
- **StopReason**: 停止原因枚举（正常停止、长度限制、工具调用、错误等）
- **ErrorEvent**: 错误事件，包含详细的错误信息
- **重试机制**: 支持配置重试延迟和策略

## 性能特性

- **流式处理**: 支持实时响应，减少等待时间
- **类型安全**: 完整的类型注解，减少运行时错误
- **内存效率**: 优化的内存使用，支持大上下文窗口
- **并发支持**: 基于asyncio的异步处理

## 扩展性

框架设计为高度可扩展：
- **自定义模型**: 可以注册自定义模型和提供商
- **兼容性层**: 可以扩展支持新的API格式
- **工具系统**: 支持自定义工具定义和调用

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进Nova AI框架。

## 支持

如有问题请查看详细模块文档或提交GitHub Issue。