import sys
content = open('backend/app/routers/config.py', 'r').read()

old_logic = """    if req.provider.lower() == "openai":
        # 对于 OpenAI，同样使用真实的 chat/completions 接口测试连通性，防止部分代理不支持 /models
        base = req.base_url.rstrip('/') if req.base_url else "https://api.openai.com/v1"
        test_url = f"{base}/chat/completions\""""

new_logic = """    if req.provider.lower() == "openai":
        # 对于 OpenAI，同样使用真实的 chat/completions 接口测试连通性，防止部分代理不支持 /models
        base = req.base_url.rstrip('/') if req.base_url else "https://api.openai.com/v1"
        # 如果是第三方兼容 API 且没有携带 /v1，自动补全（防止 404）
        if base != "https://api.openai.com/v1" and not base.endswith("/v1") and "/v1/" not in base:
            # 某些特定的代理（如 grsai）必须带 /v1
            if "grsai" in base.lower() or "openai" in base.lower():
                base = f"{base}/v1"
        test_url = f"{base}/chat/completions\""""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    open('backend/app/routers/config.py', 'w').write(content)
    print("Fixed config.py openai logic")
else:
    print("Could not find old_logic in config.py")
