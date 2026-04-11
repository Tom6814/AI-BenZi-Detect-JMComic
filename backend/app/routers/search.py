from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(
    prefix="/api/search",
    tags=["search"]
)

@router.get("")
async def search(query: str = Query(..., description="Search query string")):
    if query.isdigit():
        return {
            "type": "exact",
            "id": int(query),
            "title": f"Mock Exact Match for {query}"
        }
    else:
        return {
            "type": "list",
            "items": [
                {
                    "id": 1,
                    "title": f"Mock Result 1 for {query}",
                    "cover": "https://example.com/cover1.jpg"
                },
                {
                    "id": 2,
                    "title": f"Mock Result 2 for {query}",
                    "cover": "https://example.com/cover2.jpg"
                },
                {
                    "id": 3,
                    "title": f"Mock Result 3 for {query}",
                    "cover": "https://example.com/cover3.jpg"
                }
            ]
        }
