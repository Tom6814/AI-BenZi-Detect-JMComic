import sys
content = open('backend/app/routers/identify.py', 'r').read()

old_logic = """            if provider == "openai":
                url = base_url or "https://api.openai.com/v1"
                url = f"{url.rstrip('/')}/chat/completions\""""

new_logic = """            if provider == "openai":
                base = base_url.rstrip('/') if base_url else "https://api.openai.com/v1"
                if base != "https://api.openai.com/v1" and not base.endswith("/v1") and "/v1/" not in base:
                    if "grsai" in base.lower() or "openai" in base.lower():
                        base = f"{base}/v1"
                url = f"{base}/chat/completions\""""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    open('backend/app/routers/identify.py', 'w').write(content)
    print("Fixed identify.py openai logic")
else:
    print("Could not find old_logic in identify.py")
