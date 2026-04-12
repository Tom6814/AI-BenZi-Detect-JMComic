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
        base = req.base_url.rstrip('/') if req.base_url else "https://api.openai.com/v1"
        if base != "https://api.openai.com/v1" and not base.endswith("/v1") and "/v1/" not in base:
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
                    data = resp.json()
                    if isinstance(data, dict) and data.get("code") == -1:
                        raise HTTPException(status_code=400, detail=f"OpenAI API Key Error: {data.get('msg')}")
                    return {"status": "success", "message": "OpenAI connection successful"}
                else:
                    raise HTTPException(status_code=400, detail=f"OpenAI connection failed: HTTP {resp.status_code} - {resp.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"OpenAI connection error: {str(e)}")

    elif req.provider.lower() == "gemini":
        base = req.base_url.rstrip('/') if req.base_url else "https://generativelanguage.googleapis.com/v1beta"
        model_name = req.model or "gemini-1.5-pro"

        if "grsai" in base.lower() or "openai" in base.lower() or base.endswith("/v1") or "/v1/" in base:
            if base != "https://api.openai.com/v1" and not base.endswith("/v1") and "/v1/" not in base:
                if "grsai" in base.lower() or "openai" in base.lower():
                    base = f"{base}/v1"
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
                        data = resp.json()
                        if isinstance(data, dict) and data.get("code") == -1:
                            raise HTTPException(status_code=400, detail=f"Gemini API Key Error: {data.get('msg')}")
                        return {"status": "success", "message": "Gemini (GRSAI/OpenAI Format) connection successful"}
                    else:
                        raise HTTPException(status_code=400, detail=f"Gemini (OpenAI Format) connection failed: HTTP {resp.status_code} - {resp.text}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=400, detail=f"Gemini (OpenAI Format) connection error: {str(e)}")
        else:
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
                        raise HTTPException(status_code=400, detail=f"Gemini connection failed: HTTP {resp.status_code} - {resp.text}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=400, detail=f"Gemini connection error: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")
