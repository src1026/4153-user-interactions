from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Like(BaseModel):
    user_id: int
    recipe_id: int

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "recipe_id": 101
            }
        }

class Comment(BaseModel):
    comment_id: Optional[int]
    user_id: int
    recipe_id: int
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "comment_id": 1,
                "user_id": 2,
                "recipe_id": 101,
                "content": "This recipe is amazing!",
                "rating": 4.5,
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T15:30:00"
            }
        }

class Follow(BaseModel):
    follower_id: int
    following_id: int

    class Config:
        schema_extra = {
            "example": {
                "follower_id": 1,
                "following_id": 2
            }
        }

class User(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "username": "jigglypuff",
                "email": "jigglypuff@example.com",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T15:30:00",
                "bio": "I love sharing my cooking experiments!",
                "avatar_url": "https://example.com/avatar.jpg"
            }
        }
