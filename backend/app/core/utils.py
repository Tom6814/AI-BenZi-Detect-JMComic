import re

def strip_think_tags(text: str) -> str:
    """
    Remove <think>...</think> tags and their contents from the response text.
    """
    if not text:
        return text
    # re.DOTALL is needed to match newlines inside the tags
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
