#!/usr/bin/env python3
"""
签名工具使用示例
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.signature import custom_signature, verify_signature, generate_signed_url

def main():
    # 设置密钥
    secret = "my_secret_key"
    
    # 示例1: 生成签名
    query_string = "source=douyin&video_id=123456"
    signature = custom_signature(query_string, secret)
    print(f"Query String: {query_string}")
    print(f"Signature: {signature}")
    
    # 示例2: 验证签名
    is_valid = verify_signature(query_string, signature, secret)
    print(f"Signature Valid: {is_valid}")
    
    # 示例3: 生成带签名的URL
    base_url = "http://localhost:8000/video/id/parse"
    params = {
        "source": "douyin",
        "video_id": "123456"
    }
    signed_url = generate_signed_url(base_url, params, secret)
    print(f"Signed URL: {signed_url}")
    
    # 示例4: 验证错误的签名
    wrong_signature = "wrong_signature_here"
    is_valid_wrong = verify_signature(query_string, wrong_signature, secret)
    print(f"Wrong Signature Valid: {is_valid_wrong}")

if __name__ == "__main__":
    main()
