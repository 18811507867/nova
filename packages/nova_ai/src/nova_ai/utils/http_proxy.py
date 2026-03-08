"""
HTTP代理配置
根据环境变量为基于`fetch`的SDK设置HTTP代理
"""

import os
import sys
import platform


def is_node_environment() -> bool:
    """
    检查是否在Node.js环境中
    
    Python中我们检查是否在支持undici的环境中
    """
    # 检查是否在Node.js（通过进程名）
    if platform.system() == "Windows":
        return False
    
    # 检查是否在Bun环境
    if "bun" in sys.executable or os.environ.get("BUN_INSTALL"):
        return True
    
    # 检查是否在Node环境（通过环境变量）
    if os.environ.get("NODE_ENV") or os.environ.get("npm_config_user_agent"):
        return True
    
    return False


def setup_http_proxy() -> None:
    """
    根据环境变量设置HTTP代理
    
    在Node.js环境中，这应该被任何需要为fetch()提供代理支持的代码早期导入。
    ES模块会被缓存，所以多次导入是安全的 - 设置只运行一次。
    """
    if not is_node_environment():
        return
    
    try:
        # 在Python中，我们可以配置urllib3或requests的代理
        # 这里我们只是读取代理环境变量，供其他模块使用
        http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
        https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        
        if http_proxy or https_proxy:
            # 设置环境变量供其他库使用
            if http_proxy and not os.environ.get("HTTP_PROXY"):
                os.environ["HTTP_PROXY"] = http_proxy
            if https_proxy and not os.environ.get("HTTPS_PROXY"):
                os.environ["HTTPS_PROXY"] = https_proxy
            
            # 这里可以导入并配置urllib3或aiohttp的代理
            # 但为了保持简单，我们只设置环境变量
            pass
            
    except Exception:
        # 静默失败，不影响主要功能
        pass


def get_http_proxy() -> str | None:
    """获取HTTP代理配置"""
    return os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")


def get_https_proxy() -> str | None:
    """获取HTTPS代理配置"""
    return os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")


def configure_http_client_proxy(client_kwargs: dict) -> None:
    """
    配置HTTP客户端代理
    
    Args:
        client_kwargs: 客户端参数字典
    """
    http_proxy = get_http_proxy()
    https_proxy = get_https_proxy()
    
    if http_proxy or https_proxy:
        proxies = {}
        if http_proxy:
            proxies["http://"] = http_proxy
        if https_proxy:
            proxies["https://"] = https_proxy
        
        client_kwargs["proxies"] = proxies


__all__ = [
    "setup_http_proxy",
    "get_http_proxy",
    "get_https_proxy",
    "configure_http_client_proxy",
    "is_node_environment",
]