"""
代理项对处理工具
移除字符串中未配对的Unicode代理项字符
"""

import re


def sanitize_surrogates(text: str) -> str:
    """
    移除字符串中未配对的Unicode代理项字符。
    
    未配对的代理项（高代理项 0xD800-0xDBFF 没有匹配的低代理项 0xDC00-0xDFFF，
    或反之）会导致许多API提供商出现JSON序列化错误。
    
    基本多文种平面之外的有效的emoji和其他字符使用正确配对的代理项，
    不会受此函数影响。
    
    Args:
        text: 需要清理的文本
        
    Returns:
        移除未配对代理项后的清理文本
        
    Example:
        >>> # 有效的emoji（正确配对的代理项）会被保留
        >>> sanitize_surrogates("Hello 🙈 World")
        'Hello 🙈 World'
        
        >>> # 未配对的高代理项会被移除
        >>> unpaired = chr(0xD83D)  # 没有低代理项的高代理项
        >>> sanitize_surrogates(f"Text {unpaired} here")
        'Text  here'
    """
    if not text:
        return text
    
    # 方法1：使用正则表达式（类似TypeScript版本）
    # 匹配未配对的高代理项（后面没有低代理项）
    # 匹配未配对的低代理项（前面没有高代理项）
    pattern = re.compile(
        r'[\uD800-\uDBFF](?![\uDC00-\uDFFF])|'  # 高代理项后无低代理项
        r'(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]'    # 低代理项前无高代理项
    )
    
    return pattern.sub('', text)


def sanitize_surrogates_iterative(text: str) -> str:
    """
    使用迭代方式移除未配对的代理项（替代方法）
    
    Args:
        text: 需要清理的文本
        
    Returns:
        移除未配对代理项后的清理文本
    """
    if not text:
        return text
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        char = text[i]
        code = ord(char)
        
        # 检查是否为高代理项 (0xD800-0xDBFF)
        if 0xD800 <= code <= 0xDBFF:
            # 检查下一个字符是否存在且为低代理项
            if i + 1 < length and 0xDC00 <= ord(text[i + 1]) <= 0xDFFF:
                # 有效的代理项对，保留两个字符
                result.append(char)
                result.append(text[i + 1])
                i += 2
            else:
                # 未配对的高代理项，跳过
                i += 1
        # 检查是否为低代理项 (0xDC00-0xDFFF)
        elif 0xDC00 <= code <= 0xDFFF:
            # 未配对的低代理项，跳过
            i += 1
        else:
            # 普通字符，保留
            result.append(char)
            i += 1
    
    return ''.join(result)


# 默认使用正则表达式版本（性能更好）
# 如果需要更精确的控制或处理非常大的文本，可以使用迭代版本
__all__ = ['sanitize_surrogates', 'sanitize_surrogates_iterative']