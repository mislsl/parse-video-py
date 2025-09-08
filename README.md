   * [支持平台](#支持平台)
   * [安装](#安装)
   * [Docker](#docker)
   * [依赖模块](#依赖模块)

Python短视频去水印, 视频目前支持20个平台, 图集目前支持4个平台, 欢迎各位Star。
> 💡tips
> 1. 出现解析失败可在 issue 中提问，请提供可用于复现的平台信息、分享链接.
> 2. 使用时, 请尽量使用app分享链接, 电脑网页版未做充分测试.

# 其他语言版本
- [Golang版本](https://github.com/wujunwei928/parse-video)

# MCP 支持
本项目现已支持 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)，提供StreamableHttp方式接入， 接入URL： http://localhost:8000/mcp

# 支持平台
## 图集
| 平台 | 状态 |
|----|----|
| 抖音 | ✔  |
| 快手 | ✔  |
| 小红书 | ✔  |
| 皮皮虾 | ✔  |

## 图集 LivePhoto
| 平台 | 状态 |
|----|----|
| 小红书 | ✔  |

## 视频
| 平台       | 状态 |
|----------|----|
| 小红书      | ✔  |
| 皮皮虾      | ✔  |
| 抖音短视频    | ✔  |
| 火山短视频    | ✔  |
| 皮皮搞笑     | ✔  |
| 快手短视频    | ✔  |
| 微视短视频    | ✔  |
| 西瓜视频     | ✔  |
| 最右       | ✔  |
| 梨视频      | ✔  |
| 度小视(原全民) | ✔  |
| 逗拍       | ✔  |
| 微博       | ✔  |
| 绿洲       | ✔  |
| 全民K歌     | ✔  |
| 6间房      | ✔  |
| 美拍       | ✔  |
| 新片场      | ✔  |
| 好看视频     | ✔  |
| 虎牙       | ✔  |
| AcFun    | ✔  |

# 运行

## 本地运行

### 创建并激活 python 虚拟环境
```shell
# 进入项目根目录
cd parse-video-py

# 创建虚拟环境
# 注意python 版本需要 >= 3.10
python -m venv venv

# macos & linux 激活虚拟环境
source venv/bin/activate

# windows 激活虚拟环境
venv\Scripts\activate
```

### 安装依赖库
```shell
pip install -r requirements.txt
```

### 如需开启basic auth认证，请自行设置环境变量，不设置不开启，默认不开启
```shell
export PARSE_VIDEO_USERNAME=username
export PARSE_VIDEO_PASSWORD=password
```

### 运行app
```shell
uvicorn main:app --reload
```

## Docker运行
### 获取 docker image
```bash
docker pull wujunwei928/parse-video-py
```

### 运行 docker 容器, 端口 8000
```bash
docker run -d -p 8000:8000 wujunwei928/parse-video-py
```

### 运行docker容器，开启basic auth认证
```bash
docker run -d -p 8000:8000 -e PARSE_VIDEO_USERNAME=username -e PARSE_VIDEO_PASSWORD=password wujunwei928/parse-video-py
```

# 查看前端页面
访问: http://127.0.0.1:8000/

请求接口, 查看json返回
```bash
curl 'http://127.0.0.1:8000/video/share/url/parse?url=视频分享链接' | jq
```
返回格式
```json
{
  "author": {
    "uid": "uid",
    "name": "name",
    "avatar": "https://xxx"
  },
  "title": "记录美好生活#峡谷天花板",
  "video_url": "https://xxx",
  "music_url": "https://yyy",
  "cover_url": "https://zzz"
}
```
| 字段名 | 说明 |
| ---- | ---- |
| author.uid | 视频作者id |
| author.name | 视频作者名称 |
| author.avatar | 视频作者头像 |
| title | 视频标题 |
| video_url | 视频无水印链接 |
| music_url | 视频音乐链接 |
| cover_url | 视频封面 |
| images | 图集图片列表 |
| images.[index].url | 图集图片地址 |
| images.[index].live_photo_url | 图集图片 livephoto 视频地址 |
> 字段除了视频地址, 其他字段可能为空

# 自己写方法调用
```python
import json
import asyncio

from parser import parse_video_share_url, parse_video_id, VideoSource

# 根据分享链接解析
video_info = asyncio.run(parse_video_share_url("分享链接"))
print(
    "解析分享链接：\n",
    json.dumps(video_info, ensure_ascii=False, indent=4, default=lambda x: x.__dict__),
    "\n",
)

# 根据视频id解析
video_info = asyncio.run(
    parse_video_id(VideoSource.DouYin, "视频ID")
)
print(
    "解析视频ID：\n",
    json.dumps(video_info, ensure_ascii=False, indent=4, default=lambda x: x.__dict__),
    "\n",
)
```


# 依赖模块
| 模块        | 作用                                   |
|-------------|--------------------------------------|
| fastapi     | web框架                                |
| fastapi-mcp | 支持MCP                                |
| httpx       | HTTP 和 REST 客户端                      |
| parsel      | 解析html页面                             |
| pre-commit  | 对git代码提交前进行检查，结合flake8，isort，black使用 |
| flake8      | 工程化：代码风格一致性                          |
| isort       | 工程化：格式化导入package                     |
| black       | 工程化：代码格式化                            |

# Vercel 一键部署

## 快速部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/你的用户名/parse-video-py)

## 部署步骤

1. **Fork 此仓库到你的 GitHub 账户**

2. **点击上方按钮或访问 [Vercel](https://vercel.com/new) 进行部署**

3. **导入你的 GitHub 仓库**

4. **Vercel 会自动检测到 `vercel.json` 配置文件并开始部署**

5. **部署完成后，你可以通过 Vercel 提供的域名访问服务**

## 环境变量配置（可选）

如果需要开启 Basic Auth 认证，在 Vercel 项目设置中添加以下环境变量：

- `PARSE_VIDEO_USERNAME`: 用户名
- `PARSE_VIDEO_PASSWORD`: 密码

## 注意事项

- Vercel 免费版函数执行时间限制为 10 秒，复杂解析可能需要升级
- 项目已优化依赖，使用 `requirements-vercel.txt` 进行部署
- 支持所有原有功能，包括 MCP 协议

