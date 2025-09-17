import os
import re
import secrets
import time
from urllib.parse import parse_qs, urlencode
from parser import VideoSource, parse_video_id, parse_video_share_url
from utils import verify_signature, get_query_string_from_url

import uvicorn
import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, status, Query
from fastapi.responses import HTMLResponse, StreamingResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi_mcp import FastApiMCP
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 配置：支持通过环境变量 PARSE_VIDEO_CORS_ORIGINS 设置，逗号分隔；默认允许所有
cors_origins = os.getenv("PARSE_VIDEO_CORS_ORIGINS", "*").strip()
if not cors_origins or cors_origins == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

mcp = FastApiMCP(app)

mcp.mount_http()

templates = Jinja2Templates(directory="templates")


def get_auth_dependency() -> list[Depends]:
    """
    根据环境变量动态返回 Basic Auth 依赖项
    - 如果设置了 USERNAME 和 PASSWORD，返回验证函数
    - 如果未设置，返回一个直接返回 None 的 Depends
    """
    basic_auth_username = os.getenv("PARSE_VIDEO_USERNAME")
    basic_auth_password = os.getenv("PARSE_VIDEO_PASSWORD")

    if not (basic_auth_username and basic_auth_password):
        return []  # 返回包含Depends实例的列表

    security = HTTPBasic()

    def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
        # 验证凭据
        correct_username = secrets.compare_digest(
            credentials.username, basic_auth_username
        )
        correct_password = secrets.compare_digest(
            credentials.password, basic_auth_password
        )
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials

    return [Depends(verify_credentials)]  # 返回封装好的 Depends


def verify_signature_dependency(request: Request):
    """
    签名验证依赖项
    """
    print(f"DEBUG: verify_signature_dependency called for {request.url}")
    
    # 获取签名参数
    signature = request.query_params.get("signature")
    if not signature:
        print("DEBUG: No signature parameter found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少签名参数"
        )
    
    # 获取query字符串（排除signature参数）
    query_params = dict(request.query_params)
    query_params.pop("signature", None)
    
    # 使用urlencode来构建query字符串，与前端URLSearchParams保持一致
    query_string = urlencode(query_params, doseq=True)
    print(f"DEBUG: Query string: {query_string}")
    print(f"DEBUG: Signature: {signature}")
    
    # 验证签名
    if not verify_signature(query_string, signature):
        print("DEBUG: Signature verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification failed"
        )
    
    print("DEBUG: Signature verification passed")
    return True


@app.get("/", response_class=HTMLResponse, dependencies=get_auth_dependency())
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "github.com/wujunwei928/parse-video-py Demo",
        },
    )


@app.get("/video/share/url/parse", dependencies=[Depends(verify_signature_dependency)] + get_auth_dependency())
async def share_url_parse(url: str):
    url_reg = re.compile(r"http[s]?:\/\/[\w.-]+[\w\/-]*[\w.-]*\??[\w=&:\-\+\%]*[/]*")
    video_share_url = url_reg.search(url).group()

    try:
        video_info = await parse_video_share_url(video_share_url)
        return {"code": 200, "msg": "解析成功", "data": video_info.__dict__}
    except Exception as err:
        return {
            "code": 500,
            "msg": str(err),
        }


@app.get("/video/id/parse", dependencies=[Depends(verify_signature_dependency)] + get_auth_dependency())
async def video_id_parse(source: VideoSource, video_id: str):
    try:
        video_info = await parse_video_id(source, video_id)
        return {"code": 200, "msg": "解析成功", "data": video_info.__dict__}
    except Exception as err:
        return {
            "code": 500,
            "msg": str(err),
        }


@app.get("/video/proxy", dependencies=[Depends(verify_signature_dependency)] + get_auth_dependency())
async def video_proxy(url: str):
    """
    视频代理接口，用于代理获取视频内容
    参数: url - 视频文件的URL地址
    """
    try:
        # 验证URL格式
        url_reg = re.compile(r"http[s]?:\/\/[\w.-]+[\w\/-]*[\w.-]*\??[\w=&:\-\+\%]*[/]*")
        if not url_reg.match(url):
            raise HTTPException(status_code=400, detail="无效的URL格式")
        
        # 设置请求头，模拟浏览器行为
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "video",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
        }
        
        # 使用httpx客户端获取视频内容
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            # 获取响应头信息
            content_type = response.headers.get("content-type", "video/mp4")
            content_length = response.headers.get("content-length")
            
            # 构建响应头
            response_headers = {
                "Content-Type": content_type,
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=3600",
            }
            
            if content_length:
                response_headers["Content-Length"] = content_length
            
            # 创建流式响应，逐块返回视频数据
            def generate():
                for chunk in response.iter_bytes(chunk_size=8192):
                    yield chunk
            
            return StreamingResponse(
                generate(),
                media_type=content_type,
                headers=response_headers
            )
            
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"上游服务器返回错误: {e.response.status_code}"
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="请求超时")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"网络请求错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代理视频失败: {str(e)}")


# 设置MCP服务器
mcp.setup_server()

# 为了兼容性，保留原有的启动方式
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
