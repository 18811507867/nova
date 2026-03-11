# 代码文件汇总

- **项目根目录**: `/root/nova/packages/nova_agent/src/pi_agent`
- **文件总数**: 6
- **生成时间**: 2026-03-09 15:48:32

## 目录结构

```
pi_agent/
```

## 文件内容

### 1. __init__.py

**路径**: `__init__.py`

**大小**: 1.8 KB

```python
"""
Nova Agent - 智能代理框架
提供状态管理、事件订阅、消息队列和生命周期控制的Agent类
"""

from .agent import Agent
from .events import (
    # 事件类型
    AgentEvent,
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
    
    # 核心类型
    AgentMessage,
    AgentContext,
    AgentState,
    AgentLoopConfig,
    AgentTool,
    AgentToolResult,
    CustomAgentMessage,
    
    # 类型别名
    ThinkingLevel,
    StreamFn,
    AgentToolUpdateCallback,
)

from .agent_loop import agent_loop, agent_loop_continue, AgentEventStream
from .utils import validate_tool_call, validate_tool_arguments, set_validation_enabled, clear_validator_cache

# 版本信息
__version__ = "0.1.0"

# 导出公共接口
__all__ = [
    # 主要类
    "Agent",
    "AgentEventStream",
    
    # 核心函数
    "agent_loop",
    "agent_loop_continue",
    
    # 事件类型
    "AgentEvent",
    "AgentStartEvent",
    "AgentEndEvent",
    "TurnStartEvent",
    "TurnEndEvent",
    "MessageStartEvent",
    "MessageUpdateEvent",
    "MessageEndEvent",
    "ToolExecutionStartEvent",
    "ToolExecutionUpdateEvent",
    "ToolExecutionEndEvent",
    
    # 核心类型
    "AgentMessage",
    "AgentContext",
    "AgentState",
    "AgentLoopConfig",
    "AgentTool",
    "AgentToolResult",
    "CustomAgentMessage",
    
    # 类型别名
    "ThinkingLevel",
    "StreamFn",
    "AgentToolUpdateCallback",
    
    # 工具函数
    "validate_tool_call",
    "validate_tool_arguments",
    "set_validation_enabled",
    "clear_validator_cache",
]

# 方便导入的快捷方式
from typing import Union, List, Optional, Any, Dict, Callable, Awaitable
```

### 2. agent.py

**路径**: `agent.py`

**大小**: 18.1 KB

```python
"""
Agent class that encapsulates the agent loop.
Provides state management, event subscription, message queuing, and lifecycle control.
"""

import asyncio
from typing import (
    Any, Callable, List, Literal, Optional, Set, Union, Awaitable, cast
)
from dataclasses import dataclass, field

# Import from nova_ai (replaces pi-ai)
from nova_ai import (
    get_model,
    TextContent,
    ImageContent,
    Message,
    UserMessage,
    AssistantMessage,
    Model,
    stream_simple,
    TextContent,
    ThinkingBudgets,
    Transport,
    Usage,
    Cost
)

# Import our custom agent types and loop functions
from .events import (
    AgentMessage,
    AgentContext,
    AgentEvent,
    AgentLoopConfig,
    AgentState,
    AgentTool,
    StreamFn,
    ThinkingLevel,
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
)
from .agent_loop import agent_loop, agent_loop_continue


async def _default_convert_to_llm(messages: List[AgentMessage]) -> List[Message]:
    """Default converter: keep only LLM‑compatible messages."""
    return [m for m in messages if m.role in ("user", "assistant", "toolResult")]


class Agent:
    """
    Agent that manages conversation state, tools, and message queues.
    Uses the agent loop internally and emits events for UI updates.
    """

    def __init__(
        self,
        *,
        initial_state: Optional[AgentState] = None,
        convert_to_llm: Optional[Callable[[List[AgentMessage]], Union[List[Message], Awaitable[List[Message]]]]] = None,
        transform_context: Optional[Callable[[List[AgentMessage], Optional[asyncio.Event]], Awaitable[List[AgentMessage]]]] = None,
        steering_mode: Literal["all", "one-at-a-time"] = "one-at-a-time",
        follow_up_mode: Literal["all", "one-at-a-time"] = "one-at-a-time",
        stream_fn: Optional[StreamFn] = None,
        session_id: Optional[str] = None,
        get_api_key: Optional[Callable[[str], Union[Optional[str], Awaitable[Optional[str]]]]] = None,
        thinking_budgets: Optional[ThinkingBudgets] = None,
        transport: Transport = "sse",
        max_retry_delay_ms: Optional[int] = None,
    ):
        # Default model (matching the TypeScript example)
        default_model = get_model("google", "gemini-2.5-flash-lite-preview-06-17")

        # Initialise state
        self._state = AgentState(
            system_prompt=initial_state.get("system_prompt", "") if initial_state else "",
            model=initial_state.get("model", default_model) if initial_state else default_model,
            thinking_level=initial_state.get("thinking_level", "off") if initial_state else "off",
            tools=initial_state.get("tools", []) if initial_state else [],
            messages=initial_state.get("messages", []) if initial_state else [],
            is_streaming=False,
            stream_message=None,
            pending_tool_calls=set(),
            error=None,
        )

        self._listeners: Set[Callable[[AgentEvent], None]] = set()
        self._abort_event: Optional[asyncio.Event] = None
        self._running_task: Optional[asyncio.Task] = None

        self.convert_to_llm = convert_to_llm or _default_convert_to_llm
        self.transform_context = transform_context
        self.steering_mode = steering_mode
        self.follow_up_mode = follow_up_mode
        self.stream_fn = stream_fn or stream_simple
        self._session_id = session_id
        self.get_api_key = get_api_key
        self._thinking_budgets = thinking_budgets
        self._transport = transport
        self._max_retry_delay_ms = max_retry_delay_ms

        # Message queues
        self._steering_queue: List[AgentMessage] = []
        self._follow_up_queue: List[AgentMessage] = []

    # ----------------------------------------------------------------------
    # Properties (mirroring TypeScript get/set)
    # ----------------------------------------------------------------------

    @property
    def session_id(self) -> Optional[str]:
        return self._session_id

    @session_id.setter
    def session_id(self, value: Optional[str]) -> None:
        self._session_id = value

    @property
    def thinking_budgets(self) -> Optional[ThinkingBudgets]:
        return self._thinking_budgets

    @thinking_budgets.setter
    def thinking_budgets(self, value: Optional[ThinkingBudgets]) -> None:
        self._thinking_budgets = value

    @property
    def transport(self) -> Transport:
        return self._transport

    @transport.setter
    def transport(self, value: Transport) -> None:
        self._transport = value

    @property
    def max_retry_delay_ms(self) -> Optional[int]:
        return self._max_retry_delay_ms

    @max_retry_delay_ms.setter
    def max_retry_delay_ms(self, value: Optional[int]) -> None:
        self._max_retry_delay_ms = value

    @property
    def state(self) -> AgentState:
        return self._state

    # ----------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------

    def subscribe(self, fn: Callable[[AgentEvent], None]) -> Callable[[], None]:
        """Register an event listener. Returns an unsubscribe function."""
        self._listeners.add(fn)
        return lambda: self._listeners.discard(fn)

    # State mutators
    def set_system_prompt(self, value: str) -> None:
        self._state.system_prompt = value

    def set_model(self, model: Model) -> None:
        self._state.model = model

    def set_thinking_level(self, level: ThinkingLevel) -> None:
        self._state.thinking_level = level

    def set_steering_mode(self, mode: Literal["all", "one-at-a-time"]) -> None:
        self.steering_mode = mode

    def get_steering_mode(self) -> Literal["all", "one-at-a-time"]:
        return self.steering_mode

    def set_follow_up_mode(self, mode: Literal["all", "one-at-a-time"]) -> None:
        self.follow_up_mode = mode

    def get_follow_up_mode(self) -> Literal["all", "one-at-a-time"]:
        return self.follow_up_mode

    def set_tools(self, tools: List[AgentTool[Any, Any]]) -> None:
        self._state.tools = tools

    def replace_messages(self, messages: List[AgentMessage]) -> None:
        self._state.messages = messages[:]

    def append_message(self, message: AgentMessage) -> None:
        self._state.messages.append(message)

    def steer(self, message: AgentMessage) -> None:
        """Queue a steering message to interrupt the agent mid‑run."""
        self._steering_queue.append(message)

    def follow_up(self, message: AgentMessage) -> None:
        """Queue a follow‑up message to be processed after the agent finishes."""
        self._follow_up_queue.append(message)

    def clear_steering_queue(self) -> None:
        self._steering_queue.clear()

    def clear_follow_up_queue(self) -> None:
        self._follow_up_queue.clear()

    def clear_all_queues(self) -> None:
        self._steering_queue.clear()
        self._follow_up_queue.clear()

    def has_queued_messages(self) -> bool:
        return bool(self._steering_queue or self._follow_up_queue)

    def clear_messages(self) -> None:
        self._state.messages.clear()

    def abort(self) -> None:
        """Abort the currently running prompt."""
        if self._abort_event:
            self._abort_event.set()

    async def wait_for_idle(self) -> None:
        """Wait until the agent finishes processing the current prompt."""
        if self._running_task:
            await self._running_task

    def reset(self) -> None:
        """Reset the agent state (clears messages, queues, and errors)."""
        self._state.messages.clear()
        self._state.is_streaming = False
        self._state.stream_message = None
        self._state.pending_tool_calls.clear()
        self._state.error = None
        self._steering_queue.clear()
        self._follow_up_queue.clear()

    async def prompt(
        self,
        input: Union[str, AgentMessage, List[AgentMessage]],
        images: Optional[List[ImageContent]] = None,
    ) -> None:
        """
        Send a prompt to the agent.
        - If input is a string, it is treated as user text (optional images).
        - If input is an AgentMessage or a list of AgentMessages, they are used directly.
        """
        if self._state.is_streaming:
            raise RuntimeError(
                "Agent is already processing a prompt. Use steer() or follow_up() to queue messages, "
                "or wait for completion."
            )

        if not self._state.model:
            raise RuntimeError("No model configured")

        # Convert input to a list of AgentMessages
        messages: List[AgentMessage]
        if isinstance(input, str):
            content: List[Union[TextContent, ImageContent]] = [TextContent(**{"type": "text", "text": input})]
            if images:
                content.extend(images)
            messages = [UserMessage(**{
                "role": "user",
                "content": content,
                "timestamp": asyncio.get_event_loop().time(),  # approximate; use int if needed
            })]
        elif isinstance(input, list):
            messages = input
        else:
            messages = [input]

        await self._run_loop(messages)

    async def continue_(self) -> None:
        """
        Continue from the current context (used for retries and resuming queued messages).
        In TypeScript this method is named 'continue' (a keyword in Python, hence the trailing underscore).
        """
        if self._state.is_streaming:
            raise RuntimeError("Agent is already processing. Wait for completion before continuing.")

        if not self._state.messages:
            raise RuntimeError("No messages to continue from")

        last_msg = self._state.messages[-1]
        if last_msg.role == "assistant":
            # If the last message is assistant, first try steering messages
            queued_steering = self._dequeue_steering_messages()
            if queued_steering:
                await self._run_loop(queued_steering, skip_initial_steering_poll=True)
                return

            queued_follow_up = self._dequeue_follow_up_messages()
            if queued_follow_up:
                await self._run_loop(queued_follow_up)
                return

            raise RuntimeError("Cannot continue from message role: assistant")

        await self._run_loop(None)

    # ----------------------------------------------------------------------
    # Private helpers
    # ----------------------------------------------------------------------

    def _dequeue_steering_messages(self) -> List[AgentMessage]:
        """Retrieve messages from the steering queue according to the current mode."""
        if self.steering_mode == "one-at-a-time":
            if self._steering_queue:
                return [self._steering_queue.pop(0)]
            return []
        else:  # "all"
            messages = self._steering_queue[:]
            self._steering_queue.clear()
            return messages

    def _dequeue_follow_up_messages(self) -> List[AgentMessage]:
        """Retrieve messages from the follow‑up queue according to the current mode."""
        if self.follow_up_mode == "one-at-a-time":
            if self._follow_up_queue:
                return [self._follow_up_queue.pop(0)]
            return []
        else:  # "all"
            messages = self._follow_up_queue[:]
            self._follow_up_queue.clear()
            return messages

    async def _run_loop(
        self,
        messages: Optional[List[AgentMessage]] = None,
        *,
        skip_initial_steering_poll: bool = False,
    ) -> None:
        """
        Run the agent loop.
        If messages is None, continue from existing context (agent_loop_continue).
        Otherwise, start a new turn with the given messages.
        """
        model = self._state.model
        if not model:
            raise RuntimeError("No model configured")

        # Mark as streaming and set up cancellation
        self._state.is_streaming = True
        self._state.stream_message = None
        self._state.error = None
        self._abort_event = asyncio.Event()

        # Prepare context
        context = AgentContext(
            system_prompt=self._state.system_prompt,
            messages=self._state.messages[:],
            tools=self._state.tools,
        )

        # Steering and follow‑up closures for the config
        skip_initial = skip_initial_steering_poll

        async def get_steering() -> List[AgentMessage]:
            nonlocal skip_initial
            if skip_initial:
                skip_initial = False
                return []
            return self._dequeue_steering_messages()

        async def get_follow_up() -> List[AgentMessage]:
            return self._dequeue_follow_up_messages()

        # Build the loop configuration
        config = AgentLoopConfig(
            model=model,
            reasoning=None if self._state.thinking_level == "off" else self._state.thinking_level,
            session_id=self._session_id,
            transport=self._transport,
            thinking_budgets=self._thinking_budgets,
            max_retry_delay_ms=self._max_retry_delay_ms,
            convert_to_llm=self.convert_to_llm,
            transform_context=self.transform_context,
            get_api_key=self.get_api_key,
            get_steering_messages=get_steering,
            get_follow_up_messages=get_follow_up,
        )

        # Choose the appropriate loop starter
        if messages is not None:
            stream = agent_loop(messages, context, config, self._abort_event, self.stream_fn)
        else:
            stream = agent_loop_continue(context, config, self._abort_event, self.stream_fn)

        # Create a task that runs the loop and updates state
        async def _run() -> None:
            partial: Optional[AgentMessage] = None
            try:
                async for event in stream:
                    # Update internal state based on event type
                    if isinstance(event, MessageStartEvent):
                        partial = event.message
                        self._state.stream_message = event.message
                    elif isinstance(event, MessageUpdateEvent):
                        partial = event.message
                        self._state.stream_message = event.message
                    elif isinstance(event, MessageEndEvent):
                        partial = None
                        self._state.stream_message = None
                        self.append_message(event.message)
                    elif isinstance(event, ToolExecutionStartEvent):
                        self._state.pending_tool_calls.add(event.tool_call_id)
                    elif isinstance(event, ToolExecutionEndEvent):
                        self._state.pending_tool_calls.discard(event.tool_call_id)
                    elif isinstance(event, TurnEndEvent):
                        # Check for error message (assistant message may carry error info)
                        if event.message.role == "assistant" and hasattr(event.message, "error_message"):
                            self._state.error = event.message.error_message  # type: ignore
                    elif isinstance(event, AgentEndEvent):
                        self._state.is_streaming = False
                        self._state.stream_message = None

                    # Emit to listeners
                    self._emit(event)

                # Handle any remaining partial message (non‑empty)
                if partial and partial.role == "assistant" and partial.content:
                    # Check if it contains any non‑empty thinking/text/toolCall
                    non_empty = any(
                        (c.type == "thinking" and c.thinking.strip()) or
                        (c.type == "text" and c.text.strip()) or
                        (c.type == "toolCall" and c.name.strip())
                        for c in partial.content
                    )
                    if non_empty:
                        self.append_message(partial)
                    elif self._abort_event and self._abort_event.is_set():
                        raise asyncio.CancelledError("Request was aborted")
            except asyncio.CancelledError:
                # Abort handled
                raise
            except Exception as e:
                # Build an error assistant message
                error_msg: AgentMessage = AssistantMessage(**{
                    "role": "assistant",
                    "content": [TextContent(**{"type": "text", "text": ""})],
                    "api": model.api,
                    "provider": model.provider,
                    "model": model.id,
                    "usage": Usage(**{
                        "input": 0,
                        "output": 0,
                        "cache_read": 0,
                        "cache_write": 0,
                        "total_tokens": 0,
                        "cost": Cost(**{"input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "total": 0}),
                    }),
                    "stop_reason": "aborted" if (self._abort_event and self._abort_event.is_set()) else "error",
                    "error_message": str(e),
                    "timestamp": asyncio.get_event_loop().time(),
                })
                self.append_message(error_msg)
                self._state.error = str(e)
                self._emit(AgentEndEvent(messages=[error_msg]))
            finally:
                self._state.is_streaming = False
                self._state.stream_message = None
                self._state.pending_tool_calls.clear()
                self._abort_event = None

        # Run the task and store it
        self._running_task = asyncio.create_task(_run())
        try:
            await self._running_task
        finally:
            self._running_task = None

    def _emit(self, event: AgentEvent) -> None:
        """Synchronously notify all listeners."""
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                # Log or ignore listener errors
                pass
```

### 3. agent_loop.py

**路径**: `agent_loop.py`

**大小**: 16.1 KB

```python
"""
Agent loop implementation in Python.
Converts AgentMessage to LLM messages only at the call boundary.
"""

import asyncio
from typing import (
    AsyncIterator, Optional, List, Callable, Awaitable, Union, Any, cast
)
from dataclasses import dataclass, field
from copy import deepcopy
# Import from nova_ai (replacing pi-ai)
from nova_ai import (
    AssistantMessage,
    Context,
    stream_simple,
    ToolResultMessage,
    AssistantMessageEvent,  # for type hints
    SimpleStreamOptions,
    TextContent
)

from .utils import validate_tool_arguments

# Import custom agent types (from the previous conversion)
from .events import (
    AgentMessage,
    AgentContext,
    AgentEvent,
    AgentLoopConfig,
    AgentTool,
    AgentToolResult,
    StreamFn,
    MessageStartEvent,
    MessageEndEvent,
    MessageUpdateEvent,
    TurnStartEvent,
    TurnEndEvent,
    ToolExecutionStartEvent,
    ToolExecutionUpdateEvent,
    ToolExecutionEndEvent,
    AgentStartEvent,
    AgentEndEvent,
)


# ----------------------------------------------------------------------
# Custom async event stream (replacement for EventStream from pi-ai)
# ----------------------------------------------------------------------

class AgentEventStream(AsyncIterator[AgentEvent]):
    """
    An asynchronous stream of AgentEvents. Usage:
        stream = AgentEventStream()
        asyncio.create_task(run_loop(..., stream))
        async for event in stream:
            process(event)
    """

    def __init__(self):
        self._queue: asyncio.Queue[Union[AgentEvent, _EndMarker]] = asyncio.Queue()
        self._final_result: Optional[List[AgentMessage]] = None
        self._ended = False

    def push(self, event: AgentEvent) -> None:
        """Push an event into the stream."""
        if self._ended:
            raise RuntimeError("Stream already ended")
        self._queue.put_nowait(event)

    def end(self, result: List[AgentMessage]) -> None:
        """Mark the stream as finished and provide the final result."""
        if self._ended:
            return
        self._ended = True
        self._final_result = result
        self._queue.put_nowait(_EndMarker())

    def get_result(self) -> List[AgentMessage]:
        """Return the final result after the stream ends."""
        if self._final_result is None:
            raise RuntimeError("Stream not ended yet")
        return self._final_result

    async def __anext__(self) -> AgentEvent:
        item = await self._queue.get()
        if isinstance(item, _EndMarker):
            raise StopAsyncIteration
        return item


class _EndMarker:
    """Internal marker to signal stream end."""
    pass


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------

def agent_loop(
    prompts: List[AgentMessage],
    context: AgentContext,
    config: AgentLoopConfig,
    signal: Optional[asyncio.Event] = None,
    stream_fn: Optional[StreamFn] = None,
) -> AgentEventStream:
    """
    Start an agent loop with a new prompt message.
    The prompt is added to the context and events are emitted for it.
    """
    stream = AgentEventStream()
    current_context = AgentContext(
        system_prompt=context.system_prompt,
        messages=context.messages + prompts,
        tools=context.tools,
    )
    new_messages: List[AgentMessage] = list(prompts)

    async def _run():
        stream.push(AgentStartEvent())
        stream.push(TurnStartEvent())
        for prompt in prompts:
            stream.push(MessageStartEvent(message=prompt))
            stream.push(MessageEndEvent(message=prompt))

        await _run_loop(current_context, new_messages, config, signal, stream, stream_fn)

    asyncio.create_task(_run())
    return stream


def agent_loop_continue(
    context: AgentContext,
    config: AgentLoopConfig,
    signal: Optional[asyncio.Event] = None,
    stream_fn: Optional[StreamFn] = None,
) -> AgentEventStream:
    """
    Continue an agent loop from the current context without adding a new message.
    Used for retries – context already has user message or tool results.
    """
    if not context.messages:
        raise ValueError("Cannot continue: no messages in context")

    if context.messages[-1].role == "assistant":
        raise ValueError("Cannot continue from message role: assistant")

    stream = AgentEventStream()
    current_context = context  # copy? assume caller doesn't modify
    new_messages: List[AgentMessage] = []

    async def _run():
        stream.push(AgentStartEvent())
        stream.push(TurnStartEvent())
        await _run_loop(current_context, new_messages, config, signal, stream, stream_fn)

    asyncio.create_task(_run())
    return stream


# ----------------------------------------------------------------------
# Core loop logic
# ----------------------------------------------------------------------

async def _run_loop(
    current_context: AgentContext,
    new_messages: List[AgentMessage],
    config: AgentLoopConfig,
    signal: Optional[asyncio.Event],
    stream: AgentEventStream,
    stream_fn: Optional[StreamFn],
) -> None:
    """Main loop logic shared by agent_loop and agent_loop_continue."""
    first_turn = True
    # Check for steering messages at start (user may have typed while waiting)
    pending_messages: List[AgentMessage] = []
    if config.get_steering_messages:
        pending_messages = await config.get_steering_messages() or []

    while True:
        has_more_tool_calls = True
        steering_after_tools: Optional[List[AgentMessage]] = None

        while has_more_tool_calls or pending_messages:
            if not first_turn:
                stream.push(TurnStartEvent())
            else:
                first_turn = False

            # Process pending messages (inject before next assistant response)
            if pending_messages:
                for msg in pending_messages:
                    stream.push(MessageStartEvent(message=msg))
                    stream.push(MessageEndEvent(message=msg))
                    current_context.messages.append(msg)
                    new_messages.append(msg)
                pending_messages = []

            # Stream assistant response
            assistant_msg = await _stream_assistant_response(
                current_context, config, signal, stream, stream_fn
            )
            new_messages.append(assistant_msg)

            if assistant_msg.stop_reason in ("error", "aborted"):
                stream.push(TurnEndEvent(message=assistant_msg, tool_results=[]))
                stream.push(AgentEndEvent(messages=new_messages))
                stream.end(new_messages)
                return

            # Check for tool calls
            tool_calls = [c for c in assistant_msg.content if c.type == "toolCall"]
            has_more_tool_calls = len(tool_calls) > 0

            tool_results: List[ToolResultMessage] = []
            if has_more_tool_calls:
                tool_exec = await _execute_tool_calls(
                    current_context.tools,
                    assistant_msg,
                    signal,
                    stream,
                    config.get_steering_messages,
                )
                tool_results = tool_exec.tool_results
                steering_after_tools = tool_exec.steering_messages

                for result in tool_results:
                    current_context.messages.append(result)
                    new_messages.append(result)

            stream.push(TurnEndEvent(message=assistant_msg, tool_results=tool_results))

            # Get steering messages after turn completes
            if steering_after_tools:
                pending_messages = steering_after_tools
                steering_after_tools = None
            elif config.get_steering_messages:
                pending_messages = await config.get_steering_messages() or []

        # Agent would stop here. Check for follow-up messages.
        if config.get_follow_up_messages:
            follow_up = await config.get_follow_up_messages() or []
            if follow_up:
                pending_messages = follow_up
                continue

        # No more messages, exit
        break

    stream.push(AgentEndEvent(messages=new_messages))
    stream.end(new_messages)


# ----------------------------------------------------------------------
# Assistant response streaming
# ----------------------------------------------------------------------

async def _stream_assistant_response(
    context: AgentContext,
    config: AgentLoopConfig,
    signal: Optional[asyncio.Event],
    stream: AgentEventStream,
    stream_fn: Optional[StreamFn],
) -> AssistantMessage:
    """
    Stream an assistant response from the LLM.
    This is where AgentMessage[] gets transformed to Message[] for the LLM.
    """
    # Apply context transform if configured (AgentMessage[] → AgentMessage[])
    messages = context.messages
    if config.transform_context:
        messages = await config.transform_context(messages, signal)

    # Convert to LLM-compatible messages (AgentMessage[] → Message[])
    llm_messages = await config.convert_to_llm(messages)

    # Build LLM context
    llm_context = Context(
        system_prompt=context.system_prompt,
        messages=llm_messages,
        tools=context.tools,  # type: ignore (tools are AgentTool, but Context expects Tool)
    )

    stream_func = stream_fn or stream_simple

    # Resolve API key (important for expiring tokens)
    api_key = config.api_key
    if config.get_api_key:
        resolved = await config.get_api_key(config.model.provider)
        if resolved:
            api_key = resolved

    # Create a copy of config with resolved api_key
    stream_config = {**config.__dict__, "api_key": api_key}
    # Remove custom fields not needed by stream_simple
    stream_config.pop("convert_to_llm", None)
    stream_config.pop("transform_context", None)
    stream_config.pop("get_api_key", None)
    stream_config.pop("get_steering_messages", None)
    stream_config.pop("get_follow_up_messages", None)
    stream_config.pop("signal", None)
    stream_config.pop("model",None)

    # Call the underlying streaming function (returns async iterator of events)
    response = await stream_func(
        config.model,
        llm_context,
        SimpleStreamOptions(
            **stream_config,
            signal=signal
        ),
    )

    partial_message: Optional[AssistantMessage] = None
    added_partial = False

    async for event in response:
        # event is of type AssistantMessageEvent (from nova_ai)
        if event.type == "start":
            partial_message = event.partial
            context.messages.append(partial_message)
            added_partial = True
            stream.push(MessageStartEvent(message=deepcopy(partial_message)))
        elif event.type in ("text_start", "text_delta", "text_end",
                            "thinking_start", "thinking_delta", "thinking_end",
                            "toolcall_start", "toolcall_delta", "toolcall_end"):
            if partial_message:
                partial_message = event.partial
                context.messages[-1] = partial_message
                stream.push(MessageUpdateEvent(
                    assistant_message_event=event,
                    message=deepcopy(partial_message),
                ))
        elif event.type in ("done", "error"):
            final_message = await response.result()
            if added_partial:
                context.messages[-1] = final_message
            else:
                context.messages.append(final_message)
            if not added_partial:
                stream.push(MessageStartEvent(message=(final_message)))
            stream.push(MessageEndEvent(message=final_message))
            return final_message

    # Fallback (should not happen)
    return await response.result()


# ----------------------------------------------------------------------
# Tool execution
# ----------------------------------------------------------------------

@dataclass
class ToolExecutionResult:
    tool_results: List[ToolResultMessage]
    steering_messages: Optional[List[AgentMessage]] = None


async def _execute_tool_calls(
    tools: Optional[List[AgentTool]],
    assistant_message: AssistantMessage,
    signal: Optional[asyncio.Event],
    stream: AgentEventStream,
    get_steering_messages: Optional[Callable[[], Awaitable[List[AgentMessage]]]],
) -> ToolExecutionResult:
    """Execute tool calls from an assistant message."""
    tool_calls = [c for c in assistant_message.content if c.type == "toolCall"]
    results: List[ToolResultMessage] = []
    steering_messages: Optional[List[AgentMessage]] = None

    for idx, tool_call in enumerate(tool_calls):
        tool = next((t for t in (tools or []) if t.name == tool_call.name), None)

        stream.push(ToolExecutionStartEvent(
            tool_call_id=tool_call.id,
            tool_name=tool_call.name,
            args=tool_call.arguments,
        ))

        result: AgentToolResult[Any]
        is_error = False

        try:
            if not tool:
                raise ValueError(f"Tool {tool_call.name} not found")

            # Validate arguments using nova_ai helper
            validated_args = validate_tool_arguments(tool, tool_call)

            # Execute tool (must be async)
            def on_update(partial: AgentToolResult[Any]):
                stream.push(ToolExecutionUpdateEvent(
                    tool_call_id=tool_call.id,
                    tool_name=tool_call.name,
                    args=tool_call.arguments,
                    partial_result=partial,
                ))

            result = await tool.execute(
                tool_call.id,
                validated_args,
                signal,
                on_update,
            )
        except Exception as e:
            result = AgentToolResult(
                content=[TextContent(**{"type": "text", "text": str(e)})],
                details={},
            )
            is_error = True

        stream.push(ToolExecutionEndEvent(
            tool_call_id=tool_call.id,
            tool_name=tool_call.name,
            result=result,
            is_error=is_error,
        ))

        tool_result_message = ToolResultMessage(
            role="toolResult",
            tool_call_id=tool_call.id,
            tool_name=tool_call.name,
            content=result.content,
            details=result.details,
            is_error=is_error,
            timestamp=asyncio.get_event_loop().time(),  # approximate; use int if needed
        )

        results.append(tool_result_message)
        stream.push(MessageStartEvent(message=tool_result_message))
        stream.push(MessageEndEvent(message=tool_result_message))

        # Check for steering messages – skip remaining tools if user interrupted
        if get_steering_messages:
            steering = await get_steering_messages()
            if steering:
                steering_messages = steering
                remaining = tool_calls[idx + 1:]
                for skipped in remaining:
                    results.append(_skip_tool_call(skipped, stream))
                break

    return ToolExecutionResult(tool_results=results, steering_messages=steering_messages)


def _skip_tool_call(
    tool_call: Any,  # tool call object from AssistantMessage content
    stream: AgentEventStream,
) -> ToolResultMessage:
    """Create a 'skipped' tool result for remaining tool calls when interrupted."""
    result = AgentToolResult(
        content=[TextContent(**{"type": "text", "text": "Skipped due to queued user message."})],
        details={},
    )

    stream.push(ToolExecutionStartEvent(
        tool_call_id=tool_call.id,
        tool_name=tool_call.name,
        args=tool_call.arguments,
    ))
    stream.push(ToolExecutionEndEvent(
        tool_call_id=tool_call.id,
        tool_name=tool_call.name,
        result=result,
        is_error=True,
    ))

    tool_result_message = ToolResultMessage(
        role="toolResult",
        tool_call_id=tool_call.id,
        tool_name=tool_call.name,
        content=result.content,
        details={},
        is_error=True,
        timestamp=asyncio.get_event_loop().time(),
    )

    stream.push(MessageStartEvent(message=tool_result_message))
    stream.push(MessageEndEvent(message=tool_result_message))

    return tool_result_message
```

### 4. events.py

**路径**: `events.py`

**大小**: 8.2 KB

```python
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
    system_prompt: str
    messages: List[AgentMessage]
    tools: Optional[List[AgentTool[Any, Any]]] = None

@dataclass
class AgentLoopConfig(SimpleStreamOptions):
    """
    Configuration for the agent loop.
    Inherits all fields from SimpleStreamOptions and adds agent‑specific ones.
    """

    model: Model = None
    """The LLM model to use."""

    convert_to_llm: Callable[[List[AgentMessage]], Union[List[Message], Awaitable[List[Message]]]] = NotImplemented
    """
    Converts AgentMessage[] to LLM‑compatible Message[] before each LLM call.
    Each AgentMessage must be converted to a UserMessage, AssistantMessage,
    or ToolResultMessage that the LLM can understand. Messages that cannot be
    converted (e.g., UI‑only notifications) should be filtered out.
    """

    transform_context: Optional[Callable[[List[AgentMessage], Optional[Any]], Awaitable[List[AgentMessage]]]] = None
    """
    Optional transform applied to the context before `convert_to_llm`.
    Use this for operations that work at the AgentMessage level:
    - Context window management (pruning old messages)
    - Injecting context from external sources
    """

    get_api_key: Optional[Callable[[str], Union[Optional[str], Awaitable[Optional[str]]]]] = None
    """
    Resolves an API key dynamically for each LLM call.
    Useful for short‑lived OAuth tokens that may expire during long‑running tool execution.
    """

    get_steering_messages: Optional[Callable[[], Awaitable[List[AgentMessage]]]] = None
    """
    Returns steering messages to inject into the conversation mid‑run.
    Called after each tool execution to check for user interruptions.
    If messages are returned, remaining tool calls are skipped and these messages
    are added to the context before the next LLM call.
    """

    get_follow_up_messages: Optional[Callable[[], Awaitable[List[AgentMessage]]]] = None
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
    system_prompt: str
    model: Model
    thinking_level: ThinkingLevel
    tools: List[AgentTool[Any, Any]]
    messages: List[AgentMessage]
    is_streaming: bool
    stream_message: Optional[AgentMessage] = None
    pending_tool_calls: Set[str] = field(default_factory=set)
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
    messages: List[AgentMessage] = None

@dataclass
class TurnStartEvent:
    type: Literal["turn_start"] = "turn_start"

@dataclass
class TurnEndEvent:
    type: Literal["turn_end"] = "turn_end"
    message: AgentMessage = None
    tool_results: List[ToolResultMessage] = None

@dataclass
class MessageStartEvent:
    type: Literal["message_start"] = "message_start"
    message: AgentMessage = None

@dataclass
class MessageUpdateEvent:
    type: Literal["message_update"] = "message_update"
    message: AgentMessage = None
    assistant_message_event: AssistantMessageEvent = None

@dataclass
class MessageEndEvent:
    type: Literal["message_end"] = "message_end"
    message: AgentMessage = None

@dataclass
class ToolExecutionStartEvent:
    type: Literal["tool_execution_start"] = "tool_execution_start"
    tool_call_id: str = None
    tool_name: str = None
    args: Any = None

@dataclass
class ToolExecutionUpdateEvent:
    type: Literal["tool_execution_update"] = "tool_execution_update"
    tool_call_id: str = None
    tool_name: str = None
    args: Any = None
    partial_result: Any = None

@dataclass
class ToolExecutionEndEvent:
    type: Literal["tool_execution_end"] = "tool_execution_end"
    tool_call_id: str = None
    tool_name: str = None
    result: Any = None
    is_error: bool = None

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
```

### 5. proxy.py

**路径**: `proxy.py`

**大小**: 0.0 B

*[文件内容为空]*

### 6. utils.py

**路径**: `utils.py`

**大小**: 3.8 KB

```python
"""
工具调用验证器
使用JSON Schema验证工具调用的参数
"""

import copy
import json
from typing import List, Optional, Any, Dict
import jsonschema
from jsonschema import ValidationError

from nova_ai import Tool, ToolCall

# 全局配置：是否启用验证（可以设置为False以禁用，模拟浏览器环境）
ENABLE_VALIDATION = True

# 缓存编译后的schema验证器，提高性能
_validator_cache: Dict[str, Any] = {}


def validate_tool_call(tools: List[Tool], tool_call: ToolCall) -> Any:
    """
    通过名称查找工具，并验证工具调用参数

    Args:
        tools: 工具定义列表
        tool_call: 来自LLM的工具调用

    Returns:
        验证后的参数字典（可能经过类型转换）

    Raises:
        ValueError: 如果工具未找到或验证失败
    """
    # 查找工具
    tool = None
    for t in tools:
        if t.name == tool_call.name:
            tool = t
            break

    if tool is None:
        raise ValueError(f'Tool "{tool_call.name}" not found')

    return validate_tool_arguments(tool, tool_call)


def validate_tool_arguments(tool: Tool, tool_call: ToolCall) -> Any:
    """
    根据工具的JSON Schema验证工具调用参数

    Args:
        tool: 工具定义（包含parameters JSON Schema）
        tool_call: 工具调用对象

    Returns:
        验证后的参数字典（可能经过类型转换）

    Raises:
        ValueError: 如果验证失败，包含格式化的错误信息
    """
    # 如果全局禁用验证，直接返回原始参数
    if not ENABLE_VALIDATION:
        return tool_call.arguments

    # 获取schema
    schema = tool.parameters
    if schema is None:
        # 没有schema，无需验证
        return tool_call.arguments

    # 克隆参数以避免修改原始数据
    args = copy.deepcopy(tool_call.arguments)

    # 编译或获取缓存的验证器
    # 使用工具名称和schema的字符串表示作为缓存键
    cache_key = f"{tool.name}_{json.dumps(schema, sort_keys=True)}"
    if cache_key not in _validator_cache:
        # 创建验证器（jsonschema.Draft7Validator 或根据schema版本选择）
        try:
            # 尝试使用默认的Draft7Validator
            validator = jsonschema.Draft7Validator(schema)
            _validator_cache[cache_key] = validator
        except Exception as e:
            # 如果schema版本不兼容，回退到基础验证
            _validator_cache[cache_key] = None
            # 如果没有验证器，直接返回参数
            return args
    else:
        validator = _validator_cache.get(cache_key)

    if validator is None:
        return args

    # 执行验证
    errors = list(validator.iter_errors(args))
    if not errors:
        return args

    # 格式化错误信息
    error_lines = []
    for err in errors:
        # 获取错误路径
        path = ".".join(str(p) for p in err.path) if err.path else "root"
        # 如果是缺少属性，从validator的上下文获取
        if err.validator == "required":
            missing = err.message.split("'")[1] if "'" in err.message else "unknown"
            path = missing
            message = f"is required"
        else:
            message = err.message
        error_lines.append(f"  - {path}: {message}")

    error_msg = "\n".join(error_lines)
    args_str = json.dumps(tool_call.arguments, indent=2, ensure_ascii=False)

    raise ValueError(
        f'Validation failed for tool "{tool_call.name}":\n{error_msg}\n\nReceived arguments:\n{args_str}'
    )


def set_validation_enabled(enabled: bool) -> None:
    """
    设置是否启用验证（用于测试或特殊环境）
    """
    global ENABLE_VALIDATION
    ENABLE_VALIDATION = enabled


def clear_validator_cache() -> None:
    """清空验证器缓存"""
    _validator_cache.clear()
```
