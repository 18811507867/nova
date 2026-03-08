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