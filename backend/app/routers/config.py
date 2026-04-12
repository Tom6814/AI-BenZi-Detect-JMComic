from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.core.utils import strip_think_tags

router = APIRouter(
    prefix="/api/config",
    tags=["config"]
)

class ConnectionTestRequest(BaseModel):
    provider: str  # "openai" or "gemini"
    api_key: str
    base_url: str = None
    model: str = None

@router.post("/test")
async def test_connection(req: ConnectionTestRequest):
    if req.provider.lower() == "openai":
        # 对于 OpenAI，同样使用真实的 chat/completions 接口测试连通性，防止部分代理不支持 /models
        base = req.base_url.rstrip('/') if req.base_url else "https://api.openai.com/v1"
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
        # 如果 base_url 中包含 'openai' 或者 'v1'，或者用户明确意图使用 OpenAI 格式的 Gemini
        if "openai" in base.lower() or base.endswith("/v1") or "/v1/" in base:
            test_url = f"{base}/chat/completions"
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
                        return {"status": "success", "message": "Gemini (OpenAI Format) connection successful"}
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
