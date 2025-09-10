# API 快速参考

## 基础信息
- **Base URL**: `https://your-domain.vercel.app`
- **Content-Type**: `application/json`
- **Auth**: Basic Auth (可选)

## 接口列表

### 1. 主页
```
GET /
```
返回 Web 界面

### 2. 解析分享链接
```
GET /video/share/url/parse?url={分享链接}
```

**参数:**
- `url` (string, 必填): 视频分享链接

**响应:**
```json
{
  "code": 200,
  "msg": "解析成功",
  "data": {
    "author": {"uid": "", "name": "", "avatar": ""},
    "title": "",
    "video_url": "",
    "music_url": "",
    "cover_url": "",
    "images": [{"url": "", "live_photo_url": ""}]
  }
}
```

### 3. 解析视频ID
```
GET /video/id/parse?source={平台}&video_id={视频ID}
```

**参数:**
- `source` (string, 必填): 平台名称 (douyin, kuaishou, pipixia, 等)
- `video_id` (string, 必填): 视频ID

### 4. MCP接口
```
GET /mcp
```
Model Context Protocol 接口

## 支持的平台

**视频平台:** 抖音, 快手, 皮皮虾, 微博, 微视, 绿洲, 最右, 度小视, 西瓜, 梨视频, 皮皮搞笑, 虎牙, AcFun, 逗拍, 美拍, 全民K歌, 六间房, 新片场, 好看视频, 小红书

**图集平台:** 抖音, 快手, 小红书, 皮皮虾

## 使用示例

```bash
# 解析抖音视频
curl "https://your-domain.vercel.app/video/share/url/parse?url=https://v.douyin.com/ieFbH3DP/"

# 解析快手视频
curl "https://your-domain.vercel.app/video/id/parse?source=kuaishou&video_id=3x1234567890"
```

```python
import requests

# Python 示例
response = requests.get(
    "https://your-domain.vercel.app/video/share/url/parse",
    params={"url": "https://v.douyin.com/ieFbH3DP/"}
)
print(response.json())
```

```javascript
// JavaScript 示例
fetch("https://your-domain.vercel.app/video/share/url/parse?url=" + 
      encodeURIComponent("https://v.douyin.com/ieFbH3DP/"))
  .then(response => response.json())
  .then(data => console.log(data));
```
