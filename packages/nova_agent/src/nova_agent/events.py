"""
Agent loop types for AI agents, converted from TypeScript definitions.
Uses nova_ai as the underlying AI library.
"""

from typing import (
    Any, Union, Optional, List, Dict, Set, Callable, Awaitable, TypeVar, Generic,
    Protocol, runtime_checkable, Literal
)
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import asyncio

# Import types from nova_ai (replacement for pi-ai)
from nova_ai import (
    AssistantMessageEvent,
    ImageContent,
    Message,
    Model,
    SimpleStreamOptions,
    stream_simple,
    TextContent,
    Tool,
    ToolResultMessage,
)

# ----------------------------------------------------------------------
# Custom message support
# ----------------------------------------------------------------------

class CustomAgentMessage(ABC):
    """Base class for custom agent messages. Extend this to add your own message types."""
    pass

# AgentMessage can be either a standard Message or any custom message
AgentMessage = Union[Message, CustomAgentMessage]

# ----------------------------------------------------------------------
# Type aliases
# ----------------------------------------------------------------------

ThinkingLevel = Literal["off", "minimal", "low", "medium", "high", "xhigh"]
"""Thinking/reasoning level for models that support it."""

# Stream function signature – can be sync or async (returns a Promise in TS)
class StreamFn(Protocol):
    def __call__(self, *args: Any) -> Union[Any, Awaitable[Any]]:
        """Matches the signature of streamSimple from nova_ai."""
        ...

# ----------------------------------------------------------------------
# Tool-related types
# ----------------------------------------------------------------------

TDetails = TypeVar("TDetails")
"""Type variable for tool execution details."""

@dataclass
class AgentToolResult(Generic[TDetails]):
    """Result of a tool execution."""
    content: List[Union[TextContent, ImageContent]]
    """Content blocks supporting text and images."""
    details: TDetails
    """Details to be displayed in a UI or logged."""

AgentToolUpdateCallback = Callable[[AgentToolResult[TDetails]], None]
"""Callback for streaming tool execution updates."""

TParameters = TypeVar("TParameters")
"""Type variable for tool parameters (schema)."""

class AgentTool(Tool[TParameters], Generic[TParameters, TDetails], ABC):
    """
    Extends Tool with an execute method and a human‑readable label.
    TParameters: schema type (should match Tool's parameter schema)
    TDetails: type of the details returned in AgentToolResult
    """

    label: str
    """A human-readable label for the tool to be displayed in UI."""

    @abstractmethod
    async def execute(
        self,
        tool_call_id: str,
        params: Any,  # In TypeScript this would be Static<TParameters>
        signal: Optional[Any] = None,  # AbortSignal equivalent (e.g., asyncio.CancelledError)
        on_update: Optional[AgentToolUpdateCallback[TDetails]] = None,
    ) -> AgentToolResult[TDetails]:
        """
        Execute the tool with given parameters.
        - tool_call_id: unique identifier for this tool call
        - params: validated parameters matching TParameters
        - signal: optional cancellation signal (can be an asyncio.Event or similar)
        - on_update: optional callback for streaming partial results
        """
        pass

# ----------------------------------------------------------------------
# Context and configuration
# ----------------------------------------------------------------------

@dataclass
class AgentContext:
    """Agent context similar to SimpleStreamOptions but using AgentMessage."""
    systemPrompt: str
    messages: List[AgentMessage]
    tools: Optional[List[AgentTool[Any, Any]]] = None

@dataclass
class AgentLoopConfig(SimpleStreamOptions):
    """
    Configuration for the agent loop.
    Inherits all fields from SimpleStreamOptions and adds agent‑specific ones.
    """

    model: Model[Any]
    """The LLM model to use."""

    convertToLlm: Callable[[List[AgentMessage]], Union[List[Message], Awaitable[List[Message]]]]
    """
    Converts AgentMessage[] to LLM‑compatible Message[] before each LLM call.
    Each AgentMessage must be converted to a UserMessage, AssistantMessage,
    or ToolResultMessage that the LLM can understand. Messages that cannot be
    converted (e.g., UI‑only notifications) should be filtered out.
    """

    transformContext: Optional[Callable[[List[AgentMessage], Optional[Any]], Awaitable[List[AgentMessage]]]] = None
    """
    Optional transform applied to the context before `convertToLlm`.
    Use this for operations that work at the AgentMessage level:
    - Context window management (pruning old messages)
    - Injecting context from external sources
    """

    getApiKey: Optional[Callable[[str], Union[Optional[str], Awaitable[Optional[str]]]]] = None
    """
    Resolves an API key dynamically for each LLM call.
    Useful for short‑lived OAuth tokens that may expire during long‑running tool execution.
    """

    getSteeringMessages: Optional[Callable[[], Awaitable[List[AgentMessage]]]] = None
    """
    Returns steering messages to inject into the conversation mid‑run.
    Called after each tool execution to check for user interruptions.
    If messages are returned, remaining tool calls are skipped and these messages
    are added to the context before the next LLM call.
    """

    getFollowUpMessages: Optional[Callable[[], Awaitable[List[AgentMessage]]]] = None
    """
    Returns follow‑up messages to process after the agent would otherwise stop.
    Called when the agent has no more tool calls and no steering messages.
    If messages are returned, they're added to the context and the agent continues.
    """

# ----------------------------------------------------------------------
# Agent state
# ----------------------------------------------------------------------

@dataclass
class AgentState:
    """Agent state containing all configuration and conversation data."""
    systemPrompt: str
    model: Model[Any]
    thinkingLevel: ThinkingLevel
    tools: List[AgentTool[Any, Any]]
    messages: List[AgentMessage]
    isStreaming: bool
    streamMessage: Optional[AgentMessage] = None
    pendingToolCalls: Set[str] = field(default_factory=set)
    error: Optional[str] = None

# ----------------------------------------------------------------------
# Agent events (for UI updates)
# ----------------------------------------------------------------------

@dataclass
class AgentStartEvent:
    type: Literal["agent_start"] = "agent_start"

@dataclass
class AgentEndEvent:
    type: Literal["agent_end"] = "agent_end"
    messages: List[AgentMessage]

@dataclass
class TurnStartEvent:
    type: Literal["turn_start"] = "turn_start"

@dataclass
class TurnEndEvent:
    type: Literal["turn_end"] = "turn_end"
    message: AgentMessage
    toolResults: List[ToolResultMessage]

@dataclass
class MessageStartEvent:
    type: Literal["message_start"] = "message_start"
    message: AgentMessage

@dataclass
class MessageUpdateEvent:
    type: Literal["message_update"] = "message_update"
    message: AgentMessage
    assistantMessageEvent: AssistantMessageEvent

@dataclass
class MessageEndEvent:
    type: Literal["message_end"] = "message_end"
    message: AgentMessage

@dataclass
class ToolExecutionStartEvent:
    type: Literal["tool_execution_start"] = "tool_execution_start"
    toolCallId: str
    toolName: str
    args: Any

@dataclass
class ToolExecutionUpdateEvent:
    type: Literal["tool_execution_update"] = "tool_execution_update"
    toolCallId: str
    toolName: str
    args: Any
    partialResult: Any

@dataclass
class ToolExecutionEndEvent:
    type: Literal["tool_execution_end"] = "tool_execution_end"
    toolCallId: str
    toolName: str
    result: Any
    isError: bool

# Union of all possible agent events
AgentEvent = Union[
    AgentStartEvent,
    AgentEndEvent,
    TurnStartEvent,
    TurnEndEvent,
    MessageStartEvent,
    MessageUpdateEvent,
    MessageEndEvent,
    ToolExecutionStartEvent,
    ToolExecutionUpdateEvent,
    ToolExecutionEndEvent,
]