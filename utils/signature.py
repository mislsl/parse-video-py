import base64
import os
from typing import Optional


def custom_signature(query_string: str, secret: str) -> str:
    """
    生成自定义签名
    :param query_string: URL的query字符串
    :param secret: 密钥
    :return: 签名结果
    """
    # 拼接query和secret
    s = query_string + secret
    
    # 步长抽样（每隔5个字符取1个）
    sampled = ""
    for i in range(0, len(s), 5):
        sampled += s[i]
    
    # 反转+charCode偏移
    arr = []
    for i in range(len(sampled) - 1, -1, -1):
        arr.append(chr(ord(sampled[i]) + 2))
    
    result = "".join(arr)
    
    # Base64编码
    b64 = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    
    # 截取前32字符
    return b64[:32]


def verify_signature(query_string: str, signature: str, secret: str = None) -> bool:
    """
    验证签名
    :param query_string: URL的query字符串
    :param signature: 要验证的签名
    :param secret: 密钥，如果为None则从环境变量获取
    :return: 验证结果
    """
    if secret is None:
        secret = os.getenv("PARSE_VIDEO_SECRET", "default_secret")
    
    expected_signature = custom_signature(query_string, secret)
    return signature == expected_signature


def get_query_string_from_url(url: str) -> str:
    """
    从URL中提取query字符串
    :param url: 完整的URL
    :return: query字符串
    """
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return parsed_url.query


def generate_signed_url(base_url: str, params: dict, secret: str = None) -> str:
    """
    生成带签名的URL
    :param base_url: 基础URL
    :param params: 参数字典
    :param secret: 密钥
    :return: 带签名的完整URL
    """
    if secret is None:
        secret = os.getenv("PARSE_VIDEO_SECRET", "default_secret")
    
    # 构建query字符串（排除signature参数）
    query_params = []
    for key, value in sorted(params.items()):
        if key != 'signature':
            query_params.append(f"{key}={value}")
    
    query_string = "&".join(query_params)
    signature = custom_signature(query_string, secret)
    
    # 添加签名参数
    query_params.append(f"signature={signature}")
    
    return f"{base_url}?{'&'.join(query_params)}"
