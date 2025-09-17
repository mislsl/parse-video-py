# 签名工具使用说明

本目录包含了用于API签名验证的工具，包括Python和JavaScript两个版本。

## 文件说明

- `signature.py`: Python版本的签名工具
- `signature.js`: JavaScript版本的签名工具
- `examples/signature_example.py`: Python使用示例

## 签名算法

签名算法采用以下步骤：

1. 将query字符串与密钥拼接
2. 每隔5个字符取1个字符进行步长抽样
3. 将抽样结果反转，并对每个字符的ASCII码加2
4. 对结果进行Base64编码
5. 截取前32个字符作为最终签名

## Python版本使用

```python
from utils.signature import custom_signature, verify_signature, generate_signed_url

# 生成签名
query_string = "source=douyin&video_id=123456"
secret = "my_secret_key"
signature = custom_signature(query_string, secret)

# 验证签名
is_valid = verify_signature(query_string, signature, secret)

# 生成带签名的URL
base_url = "http://localhost:8000/video/id/parse"
params = {"source": "douyin", "video_id": "123456"}
signed_url = generate_signed_url(base_url, params, secret)
```

## JavaScript版本使用

```javascript
// 在浏览器中直接使用
const queryString = "source=douyin&video_id=123456";
const secret = "my_secret_key";
const signature = customSignature(queryString, secret);

// 验证签名
const isValid = verifySignature(queryString, signature, secret);

// 生成带签名的URL
const baseUrl = "http://localhost:8000/video/id/parse";
const params = {source: "douyin", video_id: "123456"};
const signedUrl = generateSignedUrl(baseUrl, params, secret);
```

## 环境变量配置

可以通过环境变量 `PARSE_VIDEO_SECRET` 设置默认密钥，如果不设置则使用 `default_secret`。

## 安全注意事项

1. 密钥应该保密，不要在前端代码中硬编码
2. 建议定期更换密钥
3. 签名验证失败时应该记录日志以便监控异常访问
