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
