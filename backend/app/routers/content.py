from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.blocking_words import blocking_word_lib
from typing import List

router = APIRouter(
    prefix="/content",
    tags=["content"]
)

class ContentRequest(BaseModel):
    text: str

class ContentResponse(BaseModel):
    is_clean: bool
    blocked_words: List[str]

@router.post("/check", response_model=ContentResponse)
def check_content(request: ContentRequest):
    """
    Check if the submitted text contains any blocking words.
    """
    text = request.text
    has_blocked = blocking_word_lib.contains_blocking_word(text)
    blocked_words = blocking_word_lib.get_blocking_words(text)
    
    return ContentResponse(
        is_clean=not has_blocked,
        blocked_words=blocked_words
    )
