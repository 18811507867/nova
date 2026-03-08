# Models 模块详细说明文档

## 目录结构

```
nova_ai/
├── models/
    ├── __init__.py          # 模块导入文件
    ├── base.py              # 基础模型类型定义
    ├── openai.py            # OpenAI 模型定义
    ├── anthropic.py         # Anthropic 模型定义
    ├── google.py            # Google/Gemini 模型定义
    ├── registry.py          # 模型注册表管理
```

## 模块概述

Models 模块是 Nova AI SDK 的核心组件之一，负责管理所有 AI 模型的定义、注册和查询。该模块提供了统一的接口来操作不同供应商的模型，包括 OpenAI、Anthropic 和 Google 等。

## 核心类型

### ModelCost

模型成本结构体，用于存储按千万 token 计算的成本信息。

**属性：**
- `input` (float): 输入 token 成本（$/M tokens）
- `output` (float): 输出 token 成本（$/M tokens）
- `cache_read` (float): 缓存读取成本（$/M tokens）
- `cache_write` (float): 缓存写入成本（$/M tokens）

### Model

模型定义结构体，描述一个 AI 模型的完整属性。

**属性：**
- `id` (str): 模型唯一标识符
- `name` (str): 模型显示名称
- `api` (Api): API 类型（如 `openai-completions`）
- `provider` (Provider): 供应商（如 `openai`）
- `base_url` (str): API 基础 URL
- `reasoning` (bool): 是否支持推理功能
- `input_types` (List[Literal["text", "image"]]): 支持的输入类型
- `cost` (ModelCost): 成本信息
- `context_window` (int): 上下文窗口大小（token数）
- `max_tokens` (int): 最大输出 token 数
- `headers` (Optional[Dict[str, str]]): 自定义请求头部
- `compat` (Optional[Union[OpenAICompletionsCompat, OpenAIResponsesCompat]]): 兼容性配置

## 模型定义文件

### base.py

基础模型类型定义，包含 `Model` 和 `ModelCost` 类。

### openai.py

OpenAI 模型定义，包含以下模型：

- **GPT-4.1 系列**: `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`
- **GPT-4 系列**: `gpt-4`, `gpt-4-turbo`
- **GPT-3.5 系列**: `gpt-3.5-turbo`
- **o1 推理模型**: `o1`, `o1-mini`, `o3-mini`

**API 函数：**
- `get_openai_model(model_id: str) -> Model`: 通过 ID 获取 OpenAI 模型
- `list_openai_models() -> Dict[str, Model]`: 列出所有 OpenAI 模型

### anthropic.py

Anthropic 模型定义，包含以下模型：

- **Claude 3.5 系列**: `claude-3-5-sonnet-latest`, `claude-3-5-haiku-latest`
- **Claude 3 系列**: `claude-3-opus-latest`, `claude-3-sonnet-latest`, `claude-3-haiku-latest`

**API 函数：**
- `get_anthropic_model(model_id: str) -> Model`: 通过 ID 获取 Anthropic 模型
- `list_anthropic_models() -> Dict[str, Model]`: 列出所有 Anthropic 模型

### google.py

Google/Gemini 模型定义，包含以下模型：

- **Gemini 2.0 系列**: `gemini-2.0-flash`, `gemini-2.0-flash-lite`
- **Gemini 1.5 系列**: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-1.5-flash-8b`
- **Gemini 1.0 系列**: `gemini-1.0-pro`

**API 函数：**
- `get_google_model(model_id: str) -> Model`: 通过 ID 获取 Google 模型
- `list_google_models() -> Dict[str, Model]`: 列出所有 Google 模型

## 注册表管理 (registry.py)

注册表管理模块提供了一系列函数来管理和查询注册的模型。

### 初始化

模块加载时自动从 `MODELS_BY_PROVIDER` 字典初始化注册表。

### 核心 API 函数

#### 模型查询

- `get_model(provider: Union[str, KnownProvider], model_id: str) -> Model`
  - 获取指定供应商的模型
  - 抛出 KeyError 异常如果供应商或模型不存在

- `get_providers() -> List[KnownProvider]`
  - 获取所有已注册的供应商列表（返回枚举）

- `get_provider_strings() -> List[str]`
  - 获取所有已注册的供应商字符串列表

- `get_models(provider: Union[str, KnownProvider]) -> List[Model]`
  - 获取指定供应商的所有模型

- `find_model_by_id(model_id: str) -> Optional[Model]`
  - 在所有供应商中通过 ID 查找模型

#### 模型管理

- `register_model(provider: Union[str, KnownProvider], model: Model) -> None`
  - 注册新模型到注册表

- `unregister_model(provider: Union[str, KnownProvider], model_id: str) -> Optional[Model]`
  - 从注册表移除模型
  - 返回被移除的模型，如果不存在则返回 None

- `refresh_registry() -> None`
  - 刷新注册表（重新从 `MODELS_BY_PROVIDER` 加载）

#### 模型过滤和排序

- `get_models_by_capability(**filters) -> List[Model]`
  - 根据能力过滤模型
  - 支持的过滤条件：
    - `supports_reasoning`: 是否支持推理
    - `supports_images`: 是否支持图像
    - `min_context_window`/​`max_context_window`: 上下文窗口范围
    - `provider`: 供应商过滤
    - `min_cost_input`/​`max_cost_input`: 输入成本范围
    - `min_cost_output`/​`max_cost_output`: 输出成本范围
    - `api_type`: API 类型过滤

- `get_cheapest_model(**filters) -> Optional[Model]`
  - 获取最便宜的模型（按输出价格排序）

- `get_fastest_model(**filters) -> Optional[Model]`
  - 获取最快的模型（通过模型ID中的关键词启发式判断）

#### 应用功能

- `calculate_cost(model: Model, usage: Usage) -> Usage.Cost`
  - 根据模型和用量计算成本

- `supports_xhigh_thinking(model: Model) -> bool`
  - 检查模型是否支持 xhigh 思考级别
  - 当前支持的模型：
    - GPT-5.2 / GPT-5.3 模型家族
    - Anthropic Messages API Opus 4.6 模型

- `models_are_equal(model_a: Optional[Model], model_b: Optional[Model]) -> bool`
  - 检查两个模型是否相等（通过比较 id 和 provider）

- `get_model_stats() -> Dict[str, int]`
  - 获取注册表统计信息
  - 返回各供应商模型数量的字典

- `get_provider_enum(provider_str: str) -> Optional[KnownProvider]`
  - 将供应商字符串转换为枚举

- `is_known_provider(provider: Union[str, KnownProvider]) -> bool`
  - 检查是否为已知供应商

## 使用示例

### 基本用法

```python
from nova_ai.models import get_model, get_models, calculate_cost
from nova_ai.core.usage import Usage

# 通过供应商和模型ID获取模型
model = get_model("openai", "gpt-4.1")
print(f"Model: {model.name}, Cost: ${model.cost.input}/M input tokens")

# 获取指定供应商的所有模型
openai_models = get_models("openai")
for model in openai_models:
    print(f"{model.id}: {model.name}")

# 计算成本
usage = Usage(input=1000, output=500)
cost = calculate_cost(model, usage)
print(f"Total cost: ${cost.total:.4f}")
```

### 高级过滤

```python
from nova_ai.models import get_models_by_capability, get_cheapest_model

# 查找支持图像输入的模型
image_models = get_models_by_capability(supports_images=True)
for model in image_models:
    print(f"{model.provider}/{model.id}: {model.name}")

# 找到最便宜的支持图像的模型
cheapest_image_model = get_cheapest_model(supports_images=True)
if cheapest_image_model:
    print(f"Cheapest image model: {cheapest_image_model.name}")
```

### 注册自定义模型

```python
from nova_ai.models import register_model, Model, ModelCost
from nova_ai.core.enums import KnownApi, KnownProvider

# 创建自定义模型
custom_model = Model(
    id="my-custom-model",
    name="My Custom Model",
    api=KnownApi.OPENAI_COMPLETIONS,
    provider="custom-provider",
    base_url="https://api.example.com/v1",
    reasoning=False,
    input_types=["text"],
    cost=ModelCost(input=1.0, output=2.0),
    context_window=8192,
    max_tokens=4096
)

# 注册自定义模型
register_model("custom-provider", custom_model)

# 使用注册的模型
model = get_model("custom-provider", "my-custom-model")
print(f"Custom model: {model.name}")
```

## 性能考虑

- 注册表在模块加载时初始化，但可以通过 `refresh_registry()` 重新加载
- 模型查询操作都是内存操作，性能高效
- 对大型模型集合的过滤操作可能需要考虑性能优化

## 扩展性

模型注册表设计为可扩展的，支持：

1. **添加新供应商**: 通过 `register_model()` 函数
2. **动态更新**: 通过 `refresh_registry()` 重新加载
3. **自定义兼容性**: 通过 Model 对象的 `compat` 属性
4. **自定义认证**: 通过 Model 对象的 `headers` 属性

## 常见问题

### Q: 如何添加新的模型供应商？
A: 使用 `register_model()` 函数注册新的模型，或者在相应的模型定义文件中添加新的模型定义。

### Q: 如何获取所有支持图像输入的模型？
A: 使用 `get_models_by_capability(supports_images=True)` 或者通过模型的 `input_types` 属性进行过滤。

### Q: 如何计算请求成本？
A: 使用 `calculate_cost(model, usage)` 函数，其中 usage 包含输入和输出的 token 数量。

### Q: 如何检查模型是否支持高级推理功能？
A: 检查模型的 `reasoning` 属性为 True，或者使用 `supports_xhigh_thinking(model)` 检查是否支持 xhigh 级别。