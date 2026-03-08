# Nova AI - 认证模块文档

## 概述

`auth` 模块负责处理不同AI服务提供商的认证凭据检查和配置管理。该模块提供统一的接口来验证和获取各种AI服务的认证信息。

## 目录结构

```
nova_ai/
├── auth/
    ├── __init__.py          # 模块入口文件
    ├── bedrock.py          # Amazon Bedrock 认证处理
    ├── vertex.py           # Google Vertex AI 认证处理
    └── ...                # 其他提供商认证文件（预留）
```

## 模块导入

```python
from nova_ai.auth import (
    has_vertex_adc_credentials,
    has_bedrock_credentials,
    is_vertex_fully_configured,
    get_vertex_adc_path,
    get_bedrock_credentials_type,
    get_bedrock_region
)
```

## API 参考

### Vertex AI 认证函数

#### `has_vertex_adc_credentials()`

检查是否存在有效的 Google Vertex AI Application Default Credentials (ADC)。

**检查顺序**:
1. `GOOGLE_APPLICATION_CREDENTIALS` 环境变量指向的文件
2. 默认ADC路径: `~/.config/gcloud/application_default_credentials.json`

**返回值**:
- `bool`: 是否存在有效凭据

**示例**:
```python
if has_vertex_adc_credentials():
    print("Vertex AI credentials found")
else:
    print("No Vertex AI credentials found")
```

#### `get_vertex_project()`

获取配置的 Google Cloud 项目ID。

**检查的环境变量**:
- `GOOGLE_CLOUD_PROJECT`
- `GCLOUD_PROJECT`

**返回值**:
- `Optional[str]`: 项目ID，如果未配置则返回 `None`

#### `get_vertex_location()`

获取配置的 Google Cloud 位置/区域。

**检查的环境变量**:
- `GOOGLE_CLOUD_LOCATION`

**返回值**:
- `Optional[str]`: 位置/区域，如果未配置则返回 `None`

#### `is_vertex_fully_configured()`

检查 Vertex AI 是否完全配置。

**要求**:
- 有效的 ADC 凭据
- 项目ID
- 位置信息

**返回值**:
- `bool`: 是否完全配置

**示例**:
```python
if is_vertex_fully_configured():
    print("Vertex AI is fully configured")
else:
    print("Vertex AI configuration is incomplete")
```

#### `get_vertex_adc_path()`

获取 ADC 凭据文件的实际路径。

**检查顺序**:
1. `GOOGLE_APPLICATION_CREDENTIALS` 环境变量指定的路径
2. 默认ADC路径

**返回值**:
- `Optional[Path]`: 凭据文件路径，如果不存在则返回 `None`

### Amazon Bedrock 认证函数

#### `has_bedrock_credentials()`

检查是否存在有效的 Amazon Bedrock 凭据。

**支持的凭据源**:
1. `AWS_PROFILE` - `~/.aws/credentials` 中的命名配置
2. `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` - 标准IAM密钥对
3. `AWS_BEARER_TOKEN_BEDROCK` - Bedrock API密钥（bearer token）
4. `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` - ECS任务角色
5. `AWS_CONTAINER_CREDENTIALS_FULL_URI` - ECS任务角色（完整URI）
6. `AWS_WEB_IDENTITY_TOKEN_FILE` - IRSA (IAM Roles for Service Accounts)
7. 默认AWS配置文件 (`~/.aws/credentials`)

**返回值**:
- `bool`: 是否存在有效凭据

**示例**:
```python
if has_bedrock_credentials():
    print("Bedrock credentials found")
else:
    print("No Bedrock credentials found")
```

#### `get_bedrock_credentials_type()`

获取当前使用的 Bedrock 凭据类型。

**返回值**:
- `Optional[str]`: 凭据类型字符串，包括:
  - `"profile"` - 命名配置
  - `"iam_keys"` - IAM访问密钥
  - `"bearer_token"` - Bearer令牌
  - `"ecs_relative_uri"` - ECS相对URI
  - `"ecs_full_uri"` - ECS完整URI
  - `"irsa"` - IRSA (IAM Roles for Service Accounts)
  - `"aws_config_file"` - AWS配置文件
  - `None` - 无有效凭据

#### `get_bedrock_region()`

获取配置的 AWS 区域。

**检查的环境变量**:
- `AWS_REGION`
- `AWS_DEFAULT_REGION`

**返回值**:
- `Optional[str]`: AWS区域，如果未配置则返回 `None`

## 使用示例

### 基本认证检查

```python
from nova_ai.auth import has_vertex_adc_credentials, has_bedrock_credentials

# 检查Vertex AI凭据
if has_vertex_adc_credentials():
    print("Vertex AI: Credentials available")
else:
    print("Vertex AI: No credentials found")

# 检查Bedrock凭据
if has_bedrock_credentials():
    print("Bedrock: Credentials available")
else:
    print("Bedrock: No credentials found")
```

### 详细配置检查

```python
from nova_ai.auth import (
    has_vertex_adc_credentials,
    get_vertex_project,
    get_vertex_location,
    is_vertex_fully_configured,
    get_bedrock_credentials_type,
    get_bedrock_region
)

# Vertex AI 详细配置
print("Vertex AI Configuration:")
print(f"Has ADC: {has_vertex_adc_credentials()}")
print(f"Project: {get_vertex_project()}")
print(f"Location: {get_vertex_location()}")
print(f"Fully Configured: {is_vertex_fully_configured()}")

# Bedrock 详细配置
print("\nBedrock Configuration:")
print(f"Credentials Type: {get_bedrock_credentials_type()}")
print(f"Region: {get_bedrock_region()}")
```

### 条件性服务启用

```python
from nova_ai.auth import has_vertex_adc_credentials, has_bedrock_credentials

def get_available_services():
    services = []
    
    if has_vertex_adc_credentials():
        services.append({
            'name': 'Vertex AI',
            'type': 'google'
        })
    
    if has_bedrock_credentials():
        services.append({
            'name': 'Amazon Bedrock',
            'type': 'aws'
        })
    
    return services

available_services = get_available_services()
print(f"Available AI services: {available_services}")
```

## 环境变量要求

### Vertex AI 环境变量
- `GOOGLE_APPLICATION_CREDENTIALS`: 服务账户密钥文件路径
- `GOOGLE_CLOUD_PROJECT` 或 `GCLOUD_PROJECT`: Google Cloud 项目ID
- `GOOGLE_CLOUD_LOCATION`: Google Cloud 位置/区域

### Bedrock 环境变量
- `AWS_PROFILE`: AWS配置文件名
- `AWS_ACCESS_KEY_ID`: AWS访问密钥ID
- `AWS_SECRET_ACCESS_KEY`: AWS秘密访问密钥
- `AWS_BEARER_TOKEN_BEDROCK`: Bedrock Bearer令牌
- `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI`: ECS任务角色相对URI
- `AWS_CONTAINER_CREDENTIALS_FULL_URI`: ECS任务角色完整URI
- `AWS_WEB_IDENTITY_TOKEN_FILE`: IRSA令牌文件路径
- `AWS_REGION` 或 `AWS_DEFAULT_REGION`: AWS区域

## 最佳实践

1. **凭据缓存**: 模块内部实现了凭据存在性检查的缓存机制，避免重复的文件系统检查

2. **错误处理**: 所有函数都设计为优雅地处理缺失的凭据，返回 `None` 或 `False` 而不是抛出异常

3. **多环境支持**: 支持多种认证方式，适应不同的部署环境（本地开发、容器、云环境）

4. **安全性**: 不直接暴露凭据内容，只进行存在性检查和类型判断

## 扩展性

模块设计为可扩展的，可以轻松添加新的认证提供商。每个提供商应该有独立的Python文件，并通过 `__init__.py` 暴露相应的函数。

## 故障排除

### 常见问题

1. **Vertex AI 凭据未找到**
   - 运行 `gcloud auth application-default login`
   - 设置 `GOOGLE_APPLICATION_CREDENTIALS` 环境变量

2. **Bedrock 凭据未找到**
   - 配置 AWS CLI: `aws configure`
   - 设置必要的环境变量

3. **区域未配置**
   - 设置 `AWS_REGION` 或 `GOOGLE_CLOUD_LOCATION` 环境变量

### 调试信息

```python
import os
from pathlib import Path

# 检查环境变量
print("Environment variables:")
for key in ['GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_CLOUD_PROJECT', 'AWS_REGION']:
    print(f"{key}: {os.environ.get(key)}")

# 检查默认凭据文件
adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
print(f"Default ADC path exists: {adc_path.exists()}")

aws_config = Path.home() / ".aws" / "credentials"
print(f"AWS config exists: {aws_config.exists()}")
```