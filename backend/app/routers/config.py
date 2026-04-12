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
        url = req.base_url or "https://api.openai.com/v1"
        url = f"{url.rstrip('/')}/models"
        headers = {
            "Authorization": f"Bearer {req.api_key}"
        }
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    return {"status": "success", "message": "OpenAI connection successful"}
                else:
                    raise HTTPException(status_code=400, detail=f"OpenAI connection failed: {resp.text}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"OpenAI connection error: {str(e)}")
            
    elif req.provider.lower() == "gemini":
        url = req.base_url or "https://generativelanguage.googleapis.com/v1beta"
        # 修正 Gemini API 验证地址格式
        url = f"{url.rstrip('/')}/models?key={req.api_key}"
        
        # 很多代理中转站并不支持 /models 端点，我们使用最基础的模型生成请求来做连通性测试
        # 构造简单的 generateContent 请求
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
