import sys
import re

content = open('backend/app/routers/config.py', 'r').read()

# Fix the exception catching logic so we don't double wrap HTTPException
# And fix the /v1 auto-completion for gemini to be exactly like openai
old_gemini_block = """    elif req.provider.lower() == "gemini":
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
                raise HTTPException(status_code=400, detail=f"Gemini (OpenAI Format) connection error: {str(e)}")"""

new_gemini_block = """    elif req.provider.lower() == "gemini":
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
                            return {"status": "error", "detail": f"Gemini API Key Error: {data.get('msg')}"}
                        return {"status": "success", "message": "Gemini (GRSAI/OpenAI Format) connection successful"}
                    else:
                        return {"status": "error", "detail": f"Gemini (OpenAI Format) connection failed: HTTP {resp.status_code} - {resp.text}"}
            except Exception as e:
                return {"status": "error", "detail": f"Gemini (OpenAI Format) connection error: {str(e)}"}"""

if old_gemini_block in content:
    content = content.replace(old_gemini_block, new_gemini_block)
    open('backend/app/routers/config.py', 'w').write(content)
    print("Fixed config.py gemini logic")
else:
    print("Could not find old_gemini_block in config.py")

