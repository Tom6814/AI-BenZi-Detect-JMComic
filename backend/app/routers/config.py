import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.core.utils import strip_think_tags

router = APIRouter(
    prefix="/api/config",
    tags=["config"]
)

import os
DATA_DIR = os.environ.get("DATA_DIR", "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

class ConnectionTestRequest(BaseModel):
    provider: str  # "openai" or "gemini"
    api_key: str
    base_url: str = None
    model: str = None

@router.get("/get")
def get_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

@router.post("/save")
def save_config(req: ConnectionTestRequest):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(req.model_dump(), f, ensure_ascii=False, indent=2)
    return {"status": "success"}

@router.post("/test")
async def test_connection(req: ConnectionTestRequest):
    if req.provider.lower() == "openai":
        # 对于 OpenAI，同样使用真实的 chat/completions 接口测试连通性，防止部分代理不支持 /models
        base = req.base_url.rstrip('/') if req.base_url else "https://api.openai.com/v1"
        # 如果是第三方兼容 API 且没有携带 /v1，自动补全（防止 404）
        if base != "https://api.openai.com/v1" and not base.endswith("/v1") and "/v1/" not in base:
            # 某些特定的代理（如 grsai）必须带 /v1
            if "grsai" in base.lower() or "openai" in base.lower():
                base = f"{base}/v1"
        test_url = f"{base}/chat/completions"
        model_name = req.model or "gpt-4o"
        
        headers = {
            "Authorization": f"Bearer {req.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 5
        }
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(test_url, headers=headers, json=payload)
                if resp.status_code == 200:
                    return {"status": "success", "message": "OpenAI connection successful"}
                else:
                    raise HTTPException(status_code=400, detail=f"OpenAI connection failed: {resp.text}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"OpenAI connection error: {str(e)}")

    elif req.provider.lower() == "gemini":
        # 对于 Gemini，使用真实的 generateContent 请求测试连通性
        base = req.base_url.rstrip('/') if req.base_url else "https://generativelanguage.googleapis.com/v1beta"
        model_name = req.model or "gemini-1.5-pro"

        # 兼容 GRSAI 等第三方 OpenAI 格式的 Gemini API (如：使用 chat/completions 调用 gemini)
        # 如果 base_url 包含 'grsai', 'openai', 'v1'，则使用 OpenAI 的接口格式
        if "grsai" in base.lower() or "openai" in base.lower() or base.endswith("/v1") or "/v1/" in base:
            # GRSAI 的地址通常以 /v1 结尾，如果是纯域名(如 grsaiapi.com)，这里我们确保补全 /v1
            if "grsai" in base.lower() and not base.endswith("/v1") and "/v1/" not in base:
                test_url = f"{base}/v1/chat/completions"
            else:
                test_url = f"{base}/chat/completions"
                
            headers = {
                "Authorization": f"Bearer {req.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "stream": False,
                "messages": [{"role": "user", "content": "Hello"}]
            }
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(test_url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        return {"status": "success", "message": "Gemini (GRSAI/OpenAI Format) connection successful"}
                    else:
                        raise HTTPException(status_code=400, detail=f"Gemini (OpenAI Format) connection failed: {resp.text}")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Gemini (OpenAI Format) connection error: {str(e)}")
        else:
            # 标准的 Google 原生 Gemini 格式
            test_url = f"{base}/models/{model_name}:generateContent?key={req.api_key}"
            payload = {
                "contents": [{"parts": [{"text": "Hello"}]}]
            }
    
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(test_url, json=payload)
                    if resp.status_code == 200:
                        return {"status": "success", "message": "Gemini connection successful"}
                    else:
                        raise HTTPException(status_code=400, detail=f"Gemini connection failed: {resp.text}")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Gemini connection error: {str(e)}")
            
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")
