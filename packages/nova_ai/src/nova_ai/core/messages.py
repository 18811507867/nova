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