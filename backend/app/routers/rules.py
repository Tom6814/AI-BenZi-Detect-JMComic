from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json
import os

router = APIRouter(
    prefix="/api/rules",
    tags=["rules"]
)

from typing import Optional
class RulesConfig(BaseModel):
    avoid: List[str]
    like: List[str]
    additional_prompt: Optional[str] = ""

import os
DATA_DIR = os.environ.get("DATA_DIR", "data")
DATA_FILE = os.path.join(DATA_DIR, "rules.json")

def get_default_rules() -> RulesConfig:
    return RulesConfig(avoid=[], like=[], additional_prompt="")

def read_rules() -> RulesConfig:
    if not os.path.exists(DATA_FILE):
        return get_default_rules()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return RulesConfig(**data)
    except Exception:
        return get_default_rules()

def save_rules(rules: RulesConfig):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(rules.model_dump_json(indent=2))

@router.get("", response_model=RulesConfig)
async def get_rules():
    return read_rules()

@router.post("", response_model=RulesConfig)
async def update_rules(rules: RulesConfig):
    save_rules(rules)
    return rules
