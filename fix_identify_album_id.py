import re

file_path = 'backend/app/routers/identify.py'
content = open(file_path, 'r', encoding='utf-8').read()

# 1. Update IdentifyResponse
content = re.sub(
    r'class IdentifyResponse\(BaseModel\):\n.*?reasoning: str\n.*?title: Optional\[str\] = ""\n.*?cover_url: Optional\[str\] = ""\n.*?author: Optional\[str\] = ""',
    r'class IdentifyResponse(BaseModel):\n    score: int\n    avoid: List[TagResult]\n    like: List[TagResult]\n    reasoning: str\n    title: Optional[str] = ""\n    cover_url: Optional[str] = ""\n    author: Optional[str] = ""\n    album_id: Optional[str] = ""',
    content, flags=re.DOTALL
)

# 2. Update get_mock_response
content = re.sub(
    r'"author": "Mock Author"\n    }',
    r'"author": "Mock Author",\n        "album_id": "12345"\n    }',
    content
)

# 3. Update return result (in two places for openai and gemini)
content = re.sub(
    r'result\["author"\] = req\.author\n                return result',
    r'result["author"] = req.author\n                result["album_id"] = req.query\n                return result',
    content
)

open(file_path, 'w', encoding='utf-8').write(content)
print("Regex replace completed for album_id")
