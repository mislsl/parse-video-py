# Vercel 部署指南

## 一键部署到 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/你的用户名/parse-video-py)

## 手动部署步骤

1. **Fork 或克隆此仓库**
   ```bash
   git clone https://github.com/你的用户名/parse-video-py.git
   cd parse-video-py
   ```

2. **安装 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

3. **登录 Vercel**
   ```bash
   vercel login
   ```

4. **部署到 Vercel**
   ```bash
   vercel
   ```

5. **设置环境变量（可选）**
   如果需要开启 Basic Auth 认证，在 Vercel 控制台设置以下环境变量：
   - `PARSE_VIDEO_USERNAME`: 用户名
   - `PARSE_VIDEO_PASSWORD`: 密码

## 项目结构

- `vercel.json`: Vercel 配置文件
- `requirements-vercel.txt`: 精简的依赖文件，专为 Vercel 优化
- `main.py`: 主应用文件，已适配 Vercel 无服务器环境
- `templates/`: HTML 模板文件
- `parser/`: 视频解析器模块

## 功能特性

- 支持 20+ 个视频平台去水印解析
- 支持图集解析（4个平台）
- 支持 LivePhoto 解析
- 可选的 Basic Auth 认证
- 响应式 Web 界面
- MCP (Model Context Protocol) 支持

## API 接口

- `GET /`: 主页面
- `GET /video/share/url/parse?url=分享链接`: 解析分享链接
- `GET /video/id/parse?source=平台&video_id=视频ID`: 解析视频ID
- `GET /mcp`: MCP 协议接口

## 注意事项

1. Vercel 免费版有函数执行时间限制（10秒），对于复杂的视频解析可能需要升级到付费版
2. 某些视频平台可能有反爬虫机制，解析成功率可能因平台而异
3. 建议设置 Basic Auth 认证以防止滥用

## 故障排除

如果部署后遇到问题：

1. 检查 Vercel 函数日志
2. 确认所有依赖都已正确安装
3. 验证环境变量设置
4. 检查网络连接和平台访问限制
