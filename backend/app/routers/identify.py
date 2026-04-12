from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import httpx
from app.routers.rules import read_rules
from app.core.utils import strip_think_tags
from app.services.jm_service import fetch_jm_album

router = APIRouter(
    prefix="/api/identify",
    tags=["identify"]
)

class IdentifyRequest(BaseModel):
    query: str  # Can be JM ID or something else. We'll prioritize JM ID here.
    title: Optional[str] = "Mock Title"
    description: Optional[str] = "Mock Description"
    author: Optional[str] = "Mock Author"
    tags: Optional[List[str]] = []
    cover_url: Optional[str] = ""
    comments: Optional[List[str]] = []

class TagResult(BaseModel):
    tag: str
    contains: bool
    probability: float
    reasoning: str

class IdentifyResponse(BaseModel):
    avoid: List[TagResult]
    like: List[TagResult]
    reasoning: str

CONFIG_FILE = "data/config.json"

def read_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

SYSTEM_PROMPT = """你是一个专业的同人志/漫画成分鉴定专家。
你的任务是根据提供的作品信息（标题、简介、作者、标签、封面URL和评论），分析作品中是否包含用户指定的【避雷清单】（avoid）和【喜欢清单】（like）中的成分。
请进行多维信息审视和推理，并强制返回 JSON 格式的鉴定报告。

返回的 JSON 必须严格符合以下结构：
{
  "avoid": [
    {
      "tag": "避雷标签名称",
      "contains": true或false,
      "probability": 0.0到1.0之间的浮点数（表示该成分存在的概率）,
      "reasoning": "针对该标签的详细分析理由"
    }
  ],
  "like": [
    {
      "tag": "喜欢标签名称",
      "contains": true或false,
      "probability": 0.0到1.0之间的浮点数（表示该成分存在的概率）,
      "reasoning": "针对该标签的详细分析理由"
    }
  ],
  "reasoning": "整体分析和总结。首句必须是核心结论（以加粗引语形式展示的总结）。"
}
"""

def get_mock_response(rules) -> dict:
    avoid_results = []
    for tag in rules.avoid:
        avoid_results.append({
            "tag": tag,
            "contains": True if tag in ["NTR", "触手", "胃疼"] else False,
            "probability": 0.95 if tag in ["NTR", "触手", "胃疼"] else 0.1,
            "reasoning": f"根据Mock数据，系统检测到可能存在{tag}成分..."
        })
        
    like_results = []
    for tag in rules.like:
        like_results.append({
            "tag": tag,
            "contains": True if tag in ["纯爱", "魔法少女"] else False,
            "probability": 0.88 if tag in ["纯爱", "魔法少女"] else 0.05,
            "reasoning": f"根据Mock数据，系统分析了{tag}成分的可能性..."
        })
        
    return {
        "avoid": avoid_results,
        "like": like_results,
        "reasoning": "> **这是一份基于Mock数据的测试鉴定报告。**\n\n由于未配置AI API，系统返回了模拟数据。作品整体氛围偏向暗黑奇幻，含有明显触手要素，请纯爱读者谨慎阅读。"
    }

@router.post("", response_model=IdentifyResponse)
async def identify_content(req: IdentifyRequest):
    rules = read_rules()
    config = read_config()
    
    # Try fetching real data from JM if query is an ID
    if req.query.isdigit():
        jm_album = fetch_jm_album(req.query)
        if jm_album:
            req.title = jm_album.get("title", req.title)
            req.author = jm_album.get("author", req.author)
            req.description = jm_album.get("description", req.description)
            req.tags = jm_album.get("tags", req.tags)
            req.cover_url = jm_album.get("cover_url", req.cover_url)
            # Use the fetched top 10 comments
            req.comments = jm_album.get("comments", [])

    # 组合用户 Prompt
    user_prompt = f"""
请基于以下通过 JM API 爬取到的真实本子数据进行专业鉴定。

作品信息：
- 标题：{req.title}（可能是生肉或汉化名，请综合推测）
- 作者：{req.author}（如为多作者请综合考虑，如有需要，可利用你的知识库检索该作者其他作品风格）
- 标签：{', '.join(req.tags)}
- 简介：{req.description}
- 封面URL：{req.cover_url}（如能分析图片请分析，如不能请依据标题标签推理）
- 评论区精选（点赞数最高的前10条）：
{chr(10).join(f"- {c}" for c in req.comments) if req.comments else '无评论'}

注意：评论中可能包含推销广告或抖机灵等无用信息，请自动过滤，只提取其中关于剧情走向、角色命运的真实反馈（即使是黑话或隐喻）。

需要鉴定的规则清单：
- 避雷清单 (avoid)：{', '.join(rules.avoid) if rules.avoid else '无'}
- 喜欢清单 (like)：{', '.join(rules.like) if rules.like else '无'}

请严格按照 System Prompt 的 JSON 格式输出鉴定结果。
"""

    if not config or not config.get("api_key"):
        return get_mock_response(rules)

    provider = config.get("provider", "openai").lower()
    api_key = config.get("api_key")
    model = config.get("model", "gpt-4o")
    base_url = config.get("base_url")

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            if provider == "openai":
                url = base_url or "https://api.openai.com/v1"
                url = f"{url.rstrip('/')}/chat/completions"
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
                content = data["choices"][0]["message"]["content"]
                
            elif provider == "gemini":
                base = base_url.rstrip('/') if base_url else "https://generativelanguage.googleapis.com/v1beta"

                # 兼容 GRSAI 等第三方 OpenAI 格式的 Gemini API (如：使用 chat/completions 调用 gemini)
                if "grsai" in base.lower() or "openai" in base.lower() or base.endswith("/v1") or "/v1/" in base:
                    if "grsai" in base.lower() and not base.endswith("/v1") and "/v1/" not in base:
                        url = f"{base}/v1/chat/completions"
                    else:
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
                    content = data["choices"][0]["message"]["content"]
                else:
                    # 标准的 Google 原生 Gemini 格式
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
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                
            else:
                return get_mock_response(rules)
                
            # 清洗可能存在的 <think> 标签
            content = strip_think_tags(content)

            # 尝试解析 JSON
            try:
                # Some models might return markdown code blocks, e.g. ```json\n{...}\n```
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

                result = json.loads(content)
                return result
            except json.JSONDecodeError as je:
                print(f"JSON 解析失败，AI原始返回内容为: {content}")
                raise HTTPException(status_code=500, detail=f"AI 返回的格式不是有效的 JSON。请检查 AI 输出内容。")

    except httpx.HTTPStatusError as e:
        print(f"API HTTP 调用失败: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"API Error: {e.response.text}")
    except httpx.RequestError as e:
        print(f"API 网络请求失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Network Error: {str(e)}")
    except HTTPException:
        # Re-raise FastApi HTTPExceptions
        raise
    except Exception as e:
        print(f"AI 调用内部错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"内部错误: {str(e)}")
