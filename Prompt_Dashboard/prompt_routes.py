from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import os
import json

router = APIRouter(prefix="/prompts", tags=["Prompt Dashboard"])

PROMPT_FILE_PATH = os.path.join("data", "prompt_library.json")

class PromptItem(BaseModel):
    id: str
    title: str
    category: Optional[str] = None
    tags: Optional[List[str]] = []

@router.get("/", response_model=List[PromptItem])
def list_prompts(category: Optional[str] = Query(None), tag: Optional[str] = Query(None)):
    try:
        with open(PROMPT_FILE_PATH, "r") as file:
            prompts = json.load(file)

        if category:
            prompts = [p for p in prompts if p.get("category") == category]
        if tag:
            prompts = [p for p in prompts if tag in p.get("tags", [])]

        return prompts
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Prompt data file missing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading prompts: {str(e)}")