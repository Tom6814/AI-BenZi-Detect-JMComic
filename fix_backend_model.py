import re

file_path = 'backend/app/routers/identify.py'
content = open(file_path, 'r', encoding='utf-8').read()

old_model = """class IdentifyResponse(BaseModel):
    score: int
    avoid: List[TagResult]
    like: List[TagResult]
    reasoning: str"""

new_model = """class IdentifyResponse(BaseModel):
    score: int
    avoid: List[TagResult]
    like: List[TagResult]
    reasoning: str
    title: Optional[str] = ""
    cover_url: Optional[str] = ""
    author: Optional[str] = ""
    album_id: Optional[str] = "" """

content = content.replace(old_model, new_model)

old_mock = """        "like": like_results,
        "reasoning": "> **这是一份基于Mock数据的测试鉴定报告。**\\n\\n由于未配置AI API，系统返回了模拟数据。作品整体氛围偏向暗黑奇幻，含有明显触手要素，请纯爱读者谨慎阅读。"
    }"""

new_mock = """        "like": like_results,
        "reasoning": "> **这是一份基于Mock数据的测试鉴定报告。**\\n\\n由于未配置AI API，系统返回了模拟数据。作品整体氛围偏向暗黑奇幻，含有明显触手要素，请纯爱读者谨慎阅读。",
        "title": "Mock Title",
        "cover_url": "",
        "author": "Mock Author",
        "album_id": "12345"
    }"""

content = content.replace(old_mock, new_mock)

old_return = """                result = json.loads(content)
                return result"""

new_return = """                result = json.loads(content)
                result["title"] = req.title
                result["cover_url"] = req.cover_url
                result["author"] = req.author
                result["album_id"] = req.query
                return result"""

content = content.replace(old_return, new_return)

open(file_path, 'w', encoding='utf-8').write(content)
print("Updated backend identify model.")
