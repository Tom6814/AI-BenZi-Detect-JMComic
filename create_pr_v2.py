import urllib.request
import json
import os

token = os.environ.get("TOKEN")
url = "https://api.github.com/repos/Tom6814/AI-BenZi-Detect-JMComic/pulls"
data = {
    "title": "fix: 修复 Gemini 模式及代理接口连接的连通性异常与路径错误",
    "head": "fix/gemini-api-connection-v2",
    "base": "main",
    "body": "此 PR 包含了对于 GRSAI 等第三方接口兼容性的深度修复：\n1. 修复 config.py 和 identify.py 中 Gemini 模式下丢失 /v1 导致的 404 Not Found 错误。\n2. 增加了针对 {\"code\": -1} 假 200 响应的拦截，确保错误的 API Key 不会通过连通性测试。\n3. 重写了异常抛出逻辑，确保真实的错误原因可以正确透传到前端界面。"
}

req = urllib.request.Request(url, json.dumps(data).encode("utf-8"))
req.add_header("Accept", "application/vnd.github+json")
req.add_header("Authorization", f"token {token}")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print(result.get("html_url"))
except Exception as e:
    print(f"Error: {e}")
