import re

content = open('backend/app/routers/identify.py', 'r').read()

new_logic = """            if provider == "openai":
                base = base_url.rstrip('/') if base_url else "https://api.openai.com/v1"
                if base != "https://api.openai.com/v1" and not base.endswith("/v1") and "/v1/" not in base:
                    if "grsai" in base.lower() or "openai" in base.lower():
                        base = f"{base}/v1"
                url = f"{base}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
                resp = await client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                # Check GRSAI errors
                if isinstance(data, dict) and data.get("code") == -1:
                    raise Exception(data.get("msg", "Unknown API error from proxy"))
                content = data["choices"][0]["message"]["content"]

            elif provider == "gemini":
                base = base_url.rstrip('/') if base_url else "https://generativelanguage.googleapis.com/v1beta"

                if "grsai" in base.lower() or "openai" in base.lower() or base.endswith("/v1") or "/v1/" in base:
                    if base != "https://api.openai.com/v1" and not base.endswith("/v1") and "/v1/" not in base:
                        if "grsai" in base.lower() or "openai" in base.lower():
                            base = f"{base}/v1"
                    url = f"{base}/chat/completions"

                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": model,
                        "stream": False,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                    resp = await client.post(url, headers=headers, json=payload)
                    resp.raise_for_status()
                    data = resp.json()
                    # Check GRSAI errors
                    if isinstance(data, dict) and data.get("code") == -1:
                        raise Exception(data.get("msg", "Unknown API error from proxy"))
                    content = data["choices"][0]["message"]["content"]
                else:
                    url = f"{base}/models/{model}:generateContent?key={api_key}"
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "systemInstruction": {
                            "parts": [{"text": SYSTEM_PROMPT}]
                        },
                        "contents": [
                            {"role": "user", "parts": [{"text": user_prompt}]}
                        ],
                        "generationConfig": {
                            "responseMimeType": "application/json"
                        }
                    }
                    resp = await client.post(url, headers=headers, json=payload)
                    resp.raise_for_status()
                    data = resp.json()
                    content = data["candidates"][0]["content"]["parts"][0]["text"]"""

# Find the block inside identify.py to replace
start_str = '            if provider == "openai":'
end_str = '            else:\n                return get_mock_response(rules)'
start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_logic + "\n" + content[end_idx:]
    open('backend/app/routers/identify.py', 'w').write(content)
    print("Rewrote identify.py successfully.")
else:
    print("Failed to find boundaries in identify.py")
