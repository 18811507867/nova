# Streaming 模块文档

## 概述

Streaming 模块是 Nova AI 框架的核心组件，负责处理 AI 助手的流式消息事件。该模块提供了类型安全的异步事件流处理机制，支持实时处理文本、思考过程和工具调用等不同类型的 AI 响应内容。

## 目录结构

```
streaming/
├── __init__.py          # 模块导出文件
├── events.py            # 事件类型定义
└── event_stream.py      # 事件流处理实现
```

## 核心概念

### 事件类型 (Events)

Streaming 模块定义了多种事件类型，用于表示 AI 响应过程中的不同阶段：

1. **开始事件** (`StartEvent`): 流式处理开始的信号
2. **内容事件**: 包括文本、思考、工具调用的开始、增量、结束事件
3. **完成事件** (`DoneEvent`): 正常处理完成的信号
4. **错误事件** (`ErrorEvent`): 处理过程中发生错误的信号

### 事件流 (Event Stream)

事件流提供了异步迭代器接口，允许客户端按顺序消费事件，同时支持结果等待机制。

## API 参考

### events.py

#### 事件基类

所有事件都继承自基础事件结构，包含以下通用属性：

- `type`: 事件类型标识符
- `partial`: 当前部分完成的助手消息对象

#### 具体事件类型

##### StartEvent
```python
class StartEvent:
    """流开始事件"""
    type: Literal["start"] = "start"
    partial: AssistantMessage
```

##### 文本内容事件

- `TextStartEvent`: 文本内容开始
- `TextDeltaEvent`: 文本内容增量更新
- `TextEndEvent`: 文本内容结束

##### 思考内容事件

- `ThinkingStartEvent`: 思考过程开始
- `ThinkingDeltaEvent`: 思考过程增量更新
- `ThinkingEndEvent`: 思考过程结束

##### 工具调用事件

- `ToolCallStartEvent`: 工具调用开始
- `ToolCallDeltaEvent`: 工具调用参数增量更新
- `ToolCallEndEvent`: 工具调用结束

##### 完成事件

```python
class DoneEvent:
    """完成事件"""
    type: Literal["done"] = "done"
    reason: Literal["stop", "length", "toolUse"] = "stop"
    message: AssistantMessage
```

##### 错误事件

```python
class ErrorEvent:
    """错误事件"""
    type: Literal["error"] = "error"
    reason: Literal["aborted", "error"] = "error"
    error: AssistantMessage
```

#### 事件联合类型

```python
AssistantMessageEvent = Union[
    StartEvent,
    TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallDeltaEvent, ToolCallEndEvent,
    DoneEvent,
    ErrorEvent
]
```

### event_stream.py

#### EventStream 类

通用事件流基类，支持异步迭代和结果等待。

##### 构造函数
```python
def __init__(self, is_complete_func, extract_result_func):
    """
    初始化事件流
    
    Args:
        is_complete_func: 判断事件是否为完成事件的函数
        extract_result_func: 从完成事件中提取结果的函数
    """
```

##### 主要方法

###### push
```python
def push(self, event: T) -> None:
    """
    推送事件到流中
    
    Args:
        event: 要推送的事件对象
    """
```

###### end
```python
def end(self, result: Optional[R] = None) -> None:
    """
    结束事件流
    
    Args:
        result: 可选的最终结果
    """
```

###### __aiter__
```python
async def __aiter__(self) -> AsyncIterator[T]:
    """异步迭代器接口"""
```

###### result
```python
async def result(self) -> R:
    """等待并获取最终结果"""
```

#### AssistantMessageEventStream 类

专门用于处理助手消息的事件流实现。

##### 构造函数
```python
def __init__(self):
    """初始化助手消息事件流"""
```

#### 工厂函数

##### create_assistant_message_event_stream
```python
def create_assistant_message_event_stream() -> AssistantMessageEventStream:
    """
    创建助手消息事件流
    
    Returns:
        新创建的助手消息事件流实例
    """
```

## 使用示例

### 基本用法

```python
from nova_ai.streaming import (
    create_assistant_message_event_stream,
    AssistantMessageEvent
)

async def process_stream(stream):
    """处理事件流"""
    async for event in stream:
        if event.type == "text_delta":
            print(f"文本更新: {event.delta}")
        elif event.type == "thinking_delta":
            print(f"思考过程: {event.delta}")
        elif event.type == "done":
            print(f"处理完成: {event.message}")
            break
    
    # 等待最终结果
    result = await stream.result()
    return result

# 创建事件流
stream = create_assistant_message_event_stream()

# 处理流（通常在另一个任务中）
result = await process_stream(stream)
```

### 事件生产者示例

```python
async def generate_events(stream):
    """模拟事件生成"""
    # 开始事件
    stream.push(StartEvent(partial=AssistantMessage()))
    
    # 文本内容事件
    stream.push(TextStartEvent(content_index=0, partial=AssistantMessage()))
    stream.push(TextDeltaEvent(content_index=0, delta="Hello", partial=AssistantMessage()))
    stream.push(TextDeltaEvent(content_index=0, delta=" World!", partial=AssistantMessage()))
    stream.push(TextEndEvent(content_index=0, content="Hello World!", partial=AssistantMessage()))
    
    # 完成事件
    final_message = AssistantMessage(content=[TextContent(text="Hello World!")])
    stream.push(DoneEvent(reason="stop", message=final_message))
    stream.end()
```

## 事件处理流程

1. **初始化**: 创建 `AssistantMessageEventStream` 实例
2. **事件推送**: 生产者调用 `push()` 方法推送事件
3. **事件消费**: 消费者使用 `async for` 循环迭代事件
4. **结果等待**: 消费者调用 `await stream.result()` 等待最终结果
5. **流结束**: 生产者调用 `end()` 方法结束流

## 错误处理

事件流支持完善的错误处理机制：

- **正常结束**: 通过 `DoneEvent` 表示成功完成
- **错误结束**: 通过 `ErrorEvent` 表示处理失败
- **超时处理**: 内置超时机制防止无限等待
- **异常传播**: 异常信息通过错误事件传递

## 性能特点

- **异步非阻塞**: 基于 asyncio 实现，支持高并发
- **内存高效**: 使用队列缓冲，避免内存溢出
- **类型安全**: 完整的类型注解支持
- **线程安全**: 支持多线程环境下的安全访问

## 集成指南

### 与 AI 提供商集成

Streaming 模块设计为与各种 AI 提供商兼容：

```python
async def stream_from_provider(provider, context, options):
    """从AI提供商获取流式响应"""
    stream = create_assistant_message_event_stream()
    
    async def process_provider_stream():
        # 连接到提供商API
        async for chunk in provider.stream(context, options):
            # 转换提供商特定格式为标准事件
            event = convert_to_standard_event(chunk)
            stream.push(event)
        
        # 完成处理
        stream.push(DoneEvent(reason="stop", message=final_message))
        stream.end()
    
    # 启动处理任务
    asyncio.create_task(process_provider_stream())
    
    return stream
```

### 自定义事件处理

```python
class CustomEventHandler:
    def __init__(self):
        self.stream = create_assistant_message_event_stream()
    
    async def handle_events(self):
        async for event in self.stream:
            if event.type == "text_delta":
                await self.on_text_delta(event)
            elif event.type == "thinking_delta":
                await self.on_thinking_delta(event)
            elif event.type == "toolcall_start":
                await self.on_toolcall_start(event)
    
    async def on_text_delta(self, event):
        """处理文本增量事件"""
        pass
    
    async def on_thinking_delta(self, event):
        """处理思考增量事件"""
        pass
    
    async def on_toolcall_start(self, event):
        """处理工具调用开始事件"""
        pass
```

## 最佳实践

1. **及时消费**: 尽快消费事件以避免队列积压
2. **错误处理**: 始终处理错误事件并适当恢复
3. **资源清理**: 确保在不再需要时结束事件流
4. **超时设置**: 为长时间运行的操作设置合理的超时
5. **并发控制**: 在高并发场景下适当限制并发流数量

## 限制和注意事项

- 事件流是单向的，一旦结束就不能重新开始
- 大量事件可能导致内存使用增加，需要适当控制
- 异步操作需要正确的 asyncio 事件循环管理
- 在多线程环境中使用时需要注意线程安全性

## 版本兼容性

- Python 3.8+
- 依赖 asyncio 和标准库
- 与所有主流 AI 提供商 API 兼容

## 故障排除

### 常见问题

1. **事件不触发**: 检查是否正确调用了 `push()` 和 `end()`
2. **内存泄漏**: 确保不再使用的流被正确结束
3. **性能问题**: 检查事件生产速度是否超过消费速度

### 调试技巧

```python
# 启用调试日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 跟踪事件流状态
print(f"Stream done: {stream._done}")
print(f"Queue size: {stream._queue.qsize()}")
```

---

本文档最后更新: 2026-03-05