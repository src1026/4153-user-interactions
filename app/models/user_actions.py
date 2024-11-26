from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Like(BaseModel):
    user_id: int
    recipe_id: int

class Comment(BaseModel):
    comment_id: int
    user_id: int
    recipe_id: int
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Follow(BaseModel):
    follower_id: int
    following_id: int
