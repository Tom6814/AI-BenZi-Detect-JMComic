import httpx
import asyncio

async def test():
    base = "https://grsaiapi.com"
    if "grsai" in base.lower() or "openai" in base.lower() or base.endswith("/v1") or "/v1/" in base:
        if "grsai" in base.lower() and not base.endswith("/v1") and "/v1/" not in base:
            test_url = f"{base}/v1/chat/completions"
        else:
            test_url = f"{base}/chat/completions"
        print("test_url:", test_url)
        headers = {
            "Authorization": f"Bearer sk-test",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gemini-1.5-pro",
            "stream": False,
            "messages": [{"role": "user", "content": "Hello"}]
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(test_url, headers=headers, json=payload)
            print(resp.status_code, resp.text)
            
asyncio.run(test())
