"""
Vertex AI 认证处理
"""

import os
from pathlib import Path
from typing import Optional
import sys
import importlib.util


# 懒加载Node.js模块的替代：使用Python的os.path
def _get_home_dir() -> Path:
    """获取用户主目录"""
    return Path.home()


def _get_default_adc_path() -> Path:
    """获取默认的Application Default Credentials路径"""
    return _get_home_dir() / ".config" / "gcloud" / "application_default_credentials.json"


# 缓存ADC凭据存在性检查结果
_cached_vertex_adc_credentials_exists: Optional[bool] = None


def has_vertex_adc_credentials() -> bool:
    """
    检查是否存在Vertex AI Application Default Credentials
    
    检查顺序:
    1. GOOGLE_APPLICATION_CREDENTIALS 环境变量指向的文件
    2. 默认的ADC路径: ~/.config/gcloud/application_default_credentials.json
    
    Returns:
        是否存在有效凭据
    """
    global _cached_vertex_adc_credentials_exists
    
    if _cached_vertex_adc_credentials_exists is not None:
        return _cached_vertex_adc_credentials_exists
    
    # 检查 GOOGLE_APPLICATION_CREDENTIALS 环境变量
    gac_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if gac_path:
        _cached_vertex_adc_credentials_exists = Path(gac_path).exists()
        return _cached_vertex_adc_credentials_exists
    
    # 检查默认ADC路径
    default_path = _get_default_adc_path()
    _cached_vertex_adc_credentials_exists = default_path.exists()
    
    return _cached_vertex_adc_credentials_exists


def get_vertex_project() -> Optional[str]:
    """获取Vertex AI项目ID"""
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")


def get_vertex_location() -> Optional[str]:
    """获取Vertex AI位置"""
    return os.environ.get("GOOGLE_CLOUD_LOCATION")


def is_vertex_fully_configured() -> bool:
    """
    检查Vertex AI是否完全配置
    
    需要:
    - 有效的ADC凭据
    - 项目ID
    - 位置
    """
    return (has_vertex_adc_credentials() and 
            get_vertex_project() is not None and 
            get_vertex_location() is not None)


def get_vertex_adc_path() -> Optional[Path]:
    """获取ADC凭据文件路径（如果存在）"""
    gac_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if gac_path and Path(gac_path).exists():
        return Path(gac_path)
    
    default_path = _get_default_adc_path()
    if default_path.exists():
        return default_path
    
    return None