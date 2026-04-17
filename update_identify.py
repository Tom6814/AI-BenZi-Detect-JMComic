import re
import os

file_path = 'backend/app/routers/identify.py'
content = open(file_path, 'r', encoding='utf-8').read()

# 1. Update SYSTEM_PROMPT
new_system_prompt = """SYSTEM_PROMPT = \"\"\"你是一个极其严谨、经验丰富且懂ACG次文化的“专业同人志及漫画成分鉴定师”。
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
\"\"\""""
content = re.sub(r'SYSTEM_PROMPT = """.*?"""', new_system_prompt, content, flags=re.DOTALL)

# 2. Import reddit service
import_stmt = "from app.services.reddit_service import search_reddit_posts"
if import_stmt not in content:
    content = content.replace("from app.services.jm_service import fetch_jm_album", "from app.services.jm_service import fetch_jm_album\n" + import_stmt)

# 3. Rewrite user prompt section
user_prompt_logic = """
    # Fetch Reddit Context
    reddit_context = ""
    try:
        reddit_posts = await search_reddit_posts(req.title)
        if reddit_posts:
            reddit_context = "以下是在 Reddit 上找到的相关讨论（供参考）：\\n"
            for p in reddit_posts:
                reddit_context += f"- 【{p['title']}】: {p['content']}\\n"
    except Exception as e:
        print("Reddit fetch error:", e)

    # 组合用户 Prompt
    user_prompt = f\"\"\"
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
\"\"\""""

start_str = '# 组合用户 Prompt'
end_str = 'if not config or not config.get("api_key"):'
start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + user_prompt_logic + "\n    " + content[end_idx:]

open(file_path, 'w', encoding='utf-8').write(content)
print("Identify endpoint fully updated.")
