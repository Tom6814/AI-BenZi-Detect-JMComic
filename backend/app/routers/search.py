from fastapi import APIRouter, Query
from typing import Optional
from app.services.jm_service import fetch_jm_album, search_jm_albums

router = APIRouter(
    prefix="/api/search",
    tags=["search"]
)

@router.get("")
async def search(query: str = Query(..., description="Search query string")):
    if query.isdigit():
        # fetch directly by id to confirm existence
        album = fetch_jm_album(query)
        if album:
            return {
                "type": "exact",
                "id": int(query),
                "title": album["title"],
                "cover": album.get("cover_url", "")
            }
        else:
            return {
                "type": "exact",
                "id": int(query),
                "title": f"未找到该本子: {query}"
            }
    else:
        results = search_jm_albums(query)
        # Limit to top 10 to keep it clean
        items = results[:10] if results else []
        return {
            "type": "list",
            "items": items
        }
