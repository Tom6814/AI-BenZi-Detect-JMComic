from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import httpx
from app.routers.rules import read_rules
from app.core.utils import strip_think_tags
from app.services.jm_service import fetch_jm_album
from app.services.reddit_service import search_reddit_posts

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

import os
DATA_DIR = os.environ.get("DATA_DIR", "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

def read_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

SYSTEM_PROMPT = """你是一个极其严谨、经验丰富且懂ACG次文化的“专业同人志及漫画成分鉴定师”。
你的任务是根据提供的作品信息（包括Reddit相关讨论），分析作品中是否包含用户指定的【避雷清单】（avoid）和【喜欢清单】（like）中的成分。
特别注意判定逻辑：
1. 关于【纯女】的定义，是指“女角色除了男主以外，绝对没有被其他任何人碰过或操过”。如果有任何暗示被其他人碰过，即不属于纯女。
2. 判定逻辑提示参考：如果没有明确说明或暗示，那么女主就是处女。

请进行多维信息审视和推理，并强制返回 JSON 格式的鉴定报告。

返回的 JSON 必须严格符合以下结构：
{
  "avoid": [
    {
      "tag": "避雷标签名称",
      "contains": true或false,
      "probability": 0.0到1.0之间的浮点数（表示该成分存在的概率）,
      "reasoning": "针对该标签的详细分析理由（请尽量详细，不少于50字）"
    }
  ],
  "like": [
    {
      "tag": "喜欢标签名称",
      "contains": true或false,
      "probability": 0.0到1.0之间的浮点数（表示该成分存在的概率）,
      "reasoning": "针对该标签的详细分析理由（请尽量详细，不少于50字）"
    }
  ],
  "reasoning": "整体分析和总结，必须为 Markdown 格式。开头的第一句话必须带有强烈的情感、口语化且激进（例如：“是纯爱，猛冲！”、“核弹级雷区，快跑！”或“成分复杂，谨慎驾驶”），随后分点详细列出你的推理依据（如画风与作者、剧情推测、评论反馈等）。请确保这份总结报告足够长、内容丰富，且不少于300字，能够给读者提供极具参考价值的排雷指南。"
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
        else:
            raise HTTPException(status_code=404, detail="JM 图集未找到，可能是 ID 错误或被隐藏。")

    
    # Fetch Reddit Context
    reddit_context = ""
    try:
        reddit_posts = await search_reddit_posts(req.title)
        if reddit_posts:
            reddit_context = "以下是在 Reddit 上找到的相关讨论（供参考）：\n"
            for p in reddit_posts:
                reddit_context += f"- 【{p['title']}】: {p['content']}\n"
    except Exception as e:
        print("Reddit fetch error:", e)

    # 组合用户 Prompt
    user_prompt = f"""
# Role
你是一位极其严谨且经验丰富的“专业漫画及同人志成分鉴定师”。你的核心任务是保护读者的阅读体验，精准分析并预测作品中是否含有读者无法接受的“避雷”内容，同时标记出读者期待的“喜好”内容。

# Task Workflow
1. **信息审视**：仔细分析提供的漫画标题、简介、标签、评论以及 Reddit 上的相关讨论。
2. **深度挖掘（联网/知识库）**：结合作者（{req.author}）的其他作品风格，获取更详尽的剧情走向、同人设定或读者排雷反馈。
3. **精准匹配**：将漫画的实际内容与用户提供的【避雷清单】和【喜欢清单】进行逐一、严格的比对。注意“纯女”等特殊定义的严格约束，且默认女主为处女。
4. **格式化输出**：严格按照 System Prompt 的 JSON 格式输出最终结论，保证输出内容丰富详细。

# Input Data
- 标题：{req.title}（可能是生肉或汉化名，请综合推测）
- 作者：{req.author}
- 标签：{', '.join(req.tags)}
- 简介：{req.description}
- 封面URL：{req.cover_url}
- 评论区精选（最新15条，已自动过滤无关信息）：
{chr(10).join(f"- {c}" for c in req.comments) if req.comments else '无评论'}

{reddit_context}

# User Preferences
- 避雷清单 (avoid)：{', '.join(rules.avoid) if rules.avoid else '无'}
- 喜欢清单 (like)：{', '.join(rules.like) if rules.like else '无'}
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
