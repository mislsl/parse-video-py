# 短视频去水印解析 API 文档

## 概述

这是一个基于 FastAPI 的短视频去水印解析服务，支持 20+ 个主流视频平台，提供 RESTful API 接口和 Web 界面。

## 基础信息

- **API 版本**: v1.0
- **基础 URL**: `https://your-domain.vercel.app` (部署后)
- **本地开发**: `http://localhost:3000` (使用 `vercel dev`)
- **内容类型**: `application/json`
- **字符编码**: UTF-8

## 认证方式

### Basic Auth (可选)

如果设置了环境变量 `PARSE_VIDEO_USERNAME` 和 `PARSE_VIDEO_PASSWORD`，所有接口都需要 Basic Auth 认证。

**请求头示例:**
```
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

## 支持的平台

### 视频平台 (20个)
| 平台 | 状态 | 域名示例 |
|------|------|----------|
| 抖音 | ✅ | v.douyin.com, www.iesdouyin.com |
| 快手 | ✅ | v.kuaishou.com |
| 皮皮虾 | ✅ | h5.pipix.com |
| 微博 | ✅ | weibo.com |
| 微视 | ✅ | isee.weishi.qq.com |
| 绿洲 | ✅ | weibo.cn |
| 最右 | ✅ | share.xiaochuankeji.cn |
| 度小视(原全民) | ✅ | xspshare.baidu.com |
| 西瓜视频 | ✅ | v.ixigua.com, www.ixigua.com |
| 梨视频 | ✅ | www.pearvideo.com |
| 皮皮搞笑 | ✅ | h5.pipigx.com |
| 虎牙 | ✅ | v.huya.com |
| AcFun | ✅ | www.acfun.cn |
| 逗拍 | ✅ | doupai.cc |
| 美拍 | ✅ | meipai.com |
| 全民K歌 | ✅ | kg.qq.com |
| 六间房 | ✅ | 6.cn |
| 新片场 | ✅ | xinpianchang.com |
| 好看视频 | ✅ | haokan.baidu.com |
| 小红书 | ✅ | www.xiaohongshu.com, xhslink.com |

### 图集平台 (4个)
| 平台 | 状态 | 支持功能 |
|------|------|----------|
| 抖音 | ✅ | 图片 + LivePhoto |
| 快手 | ✅ | 图片 |
| 小红书 | ✅ | 图片 + LivePhoto |
| 皮皮虾 | ✅ | 图片 |

## API 接口

### 1. 获取主页

**接口地址:** `GET /`

**描述:** 返回 Web 界面主页

**请求参数:** 无

**响应示例:**
```html
<!DOCTYPE html>
<html lang="zh-cmn-Hans">
<head>
    <title>github.com/wujunwei928/parse-video-py Demo</title>
    <!-- ... -->
</head>
<body>
    <!-- 解析界面 -->
</body>
</html>
```

---

### 2. 解析分享链接

**接口地址:** `GET /video/share/url/parse`

**描述:** 根据视频分享链接解析视频信息

**请求参数:**
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| url | string | 是 | 视频分享链接 | https://v.douyin.com/ieFbH3DP/ |

**请求示例:**
```bash
curl "https://your-domain.vercel.app/video/share/url/parse?url=https://v.douyin.com/ieFbH3DP/"
```

**响应格式:**
```json
{
  "code": 200,
  "msg": "解析成功",
  "data": {
    "author": {
      "uid": "用户ID",
      "name": "用户昵称",
      "avatar": "https://头像链接"
    },
    "title": "视频标题",
    "video_url": "https://无水印视频链接",
    "music_url": "https://背景音乐链接",
    "cover_url": "https://视频封面链接",
    "images": [
      {
        "url": "https://图片链接",
        "live_photo_url": "https://LivePhoto链接"
      }
    ]
  }
}
```

**错误响应:**
```json
{
  "code": 500,
  "msg": "错误信息描述"
}
```

---

### 3. 解析视频ID

**接口地址:** `GET /video/id/parse`

**描述:** 根据平台和视频ID解析视频信息

**请求参数:**
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| source | string | 是 | 视频平台 | douyin |
| video_id | string | 是 | 视频ID | 7123456789012345678 |

**支持的 source 值:**
- `douyin` - 抖音
- `kuaishou` - 快手
- `pipixia` - 皮皮虾
- `weibo` - 微博
- `weishi` - 微视
- `lvzhou` - 绿洲
- `zuiyou` - 最右
- `quanmin` - 度小视
- `xigua` - 西瓜视频
- `lishipin` - 梨视频
- `pipigaoxiao` - 皮皮搞笑
- `huya` - 虎牙
- `acfun` - AcFun
- `doupai` - 逗拍
- `meipai` - 美拍
- `quanminkge` - 全民K歌
- `sixroom` - 六间房
- `xinpianchang` - 新片场
- `haokan` - 好看视频
- `redbook` - 小红书

**请求示例:**
```bash
curl "https://your-domain.vercel.app/video/id/parse?source=douyin&video_id=7123456789012345678"
```

**响应格式:** 与分享链接解析相同

---

### 4. MCP 协议接口

**接口地址:** `GET /mcp`

**描述:** Model Context Protocol 协议接口，用于 AI 模型集成

**请求参数:** 无

**响应:** MCP 协议格式的响应

## 数据模型

### VideoInfo 对象
```json
{
  "author": {
    "uid": "string",      // 作者ID
    "name": "string",     // 作者昵称
    "avatar": "string"    // 作者头像URL
  },
  "title": "string",      // 视频标题
  "video_url": "string",  // 无水印视频URL
  "music_url": "string",  // 背景音乐URL
  "cover_url": "string",  // 视频封面URL
  "images": [             // 图集图片列表
    {
      "url": "string",           // 图片URL
      "live_photo_url": "string" // LivePhoto URL (可选)
    }
  ]
}
```

### 响应状态码
| 状态码 | 描述 |
|--------|------|
| 200 | 请求成功 |
| 401 | 未授权 (需要 Basic Auth) |
| 422 | 参数验证失败 |
| 500 | 服务器内部错误 |

## 使用示例

### Python 示例
```python
import requests
import asyncio
from parser import parse_video_share_url, parse_video_id, VideoSource

# 方法1: 使用 API 接口
def parse_video_by_api(share_url):
    response = requests.get(
        "https://your-domain.vercel.app/video/share/url/parse",
        params={"url": share_url}
    )
    return response.json()

# 方法2: 直接调用解析函数
async def parse_video_direct(share_url):
    video_info = await parse_video_share_url(share_url)
    return video_info.__dict__

# 使用示例
result = parse_video_by_api("https://v.douyin.com/ieFbH3DP/")
print(result)
```

### JavaScript 示例
```javascript
// 解析分享链接
async function parseVideo(shareUrl) {
    try {
        const response = await fetch(
            `https://your-domain.vercel.app/video/share/url/parse?url=${encodeURIComponent(shareUrl)}`
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('解析失败:', error);
    }
}

// 使用示例
parseVideo("https://v.douyin.com/ieFbH3DP/")
    .then(result => console.log(result));
```

### cURL 示例
```bash
# 解析分享链接
curl "https://your-domain.vercel.app/video/share/url/parse?url=https://v.douyin.com/ieFbH3DP/"

# 解析视频ID
curl "https://your-domain.vercel.app/video/id/parse?source=douyin&video_id=7123456789012345678"

# 带认证的请求
curl -u "username:password" "https://your-domain.vercel.app/video/share/url/parse?url=https://v.douyin.com/ieFbH3DP/"
```

## 错误处理

### 常见错误码
| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| 500 | 解析失败 | 检查链接是否正确，平台是否支持 |
| 401 | 未授权 | 检查 Basic Auth 凭据 |
| 422 | 参数错误 | 检查请求参数格式 |

### 错误响应示例
```json
{
  "code": 500,
  "msg": "share url [https://example.com] does not have source config"
}
```

## 部署说明

### Vercel 部署
1. Fork 项目到你的 GitHub
2. 访问 [Vercel](https://vercel.com/new)
3. 导入 GitHub 仓库
4. 自动部署完成

### 环境变量配置
| 变量名 | 描述 | 是否必填 |
|--------|------|----------|
| PARSE_VIDEO_USERNAME | Basic Auth 用户名 | 否 |
| PARSE_VIDEO_PASSWORD | Basic Auth 密码 | 否 |

### 本地开发
```bash
# 安装依赖
pip install -r requirements-vercel.txt

# 启动开发服务器
vercel dev
```

## 注意事项

1. **使用限制**: Vercel 免费版有函数执行时间限制 (10秒)
2. **平台限制**: 某些平台可能有反爬虫机制，解析成功率可能因平台而异
3. **链接格式**: 建议使用 APP 分享链接，网页版链接可能解析失败
4. **频率限制**: 建议控制请求频率，避免被平台限制
5. **认证设置**: 生产环境建议设置 Basic Auth 防止滥用

## 更新日志

### v1.0.0 (2025-01-08)
- ✅ 支持 20+ 个视频平台解析
- ✅ 支持 4 个图集平台解析
- ✅ 支持 LivePhoto 解析
- ✅ 提供 Web 界面
- ✅ 支持 MCP 协议
- ✅ 适配 Vercel 部署
- ✅ 可选的 Basic Auth 认证

## 技术支持

- **GitHub**: https://github.com/mislsl/parse-video-py
- **问题反馈**: 请在 GitHub Issues 中提交
- **功能建议**: 欢迎提交 Pull Request

---

*最后更新: 2025-01-08*
