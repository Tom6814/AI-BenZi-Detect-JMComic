import re

file_path = 'backend/app/routers/identify.py'
content = open(file_path, 'r', encoding='utf-8').read()

old_response_model = """class IdentifyResponse(BaseModel):
    score: int
    avoid: List[TagResult]
    like: List[TagResult]
    reasoning: str
    title: Optional[str] = ""
    cover_url: Optional[str] = ""
    author: Optional[str] = "" """
new_response_model = """class IdentifyResponse(BaseModel):
    score: int
    avoid: List[TagResult]
    like: List[TagResult]
    reasoning: str
    title: Optional[str] = ""
    cover_url: Optional[str] = ""
    author: Optional[str] = ""
    album_id: Optional[str] = "" """

content = content.replace(old_response_model, new_response_model)

old_return_mock = """        "title": "Mock Title",
        "cover_url": "",
        "author": "Mock Author"
    }"""
new_return_mock = """        "title": "Mock Title",
        "cover_url": "",
        "author": "Mock Author",
        "album_id": "12345"
    }"""
content = content.replace(old_return_mock, new_return_mock)

old_return_result = """                result["title"] = req.title
                result["cover_url"] = req.cover_url
                result["author"] = req.author
                return result"""
new_return_result = """                result["title"] = req.title
                result["cover_url"] = req.cover_url
                result["author"] = req.author
                result["album_id"] = req.query
                return result"""
content = content.replace(old_return_result, new_return_result)

open(file_path, 'w', encoding='utf-8').write(content)
print("Updated IdentifyResponse with album_id.")

