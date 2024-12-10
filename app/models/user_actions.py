from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
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
    user_id: Optional[int] = Field(None, description="The unique identifier for the user")  # Auto-incremented
    email: EmailStr = Field(..., description="The unique email address of the user")  # Ensures a valid email format
    profile_pic: Optional[str] = Field(None, description="The URL of the user's profile picture")
    ranking: Optional[int] = Field(None, description="The ranking of the user, used for leaderboard purposes")
    created_at: Optional[datetime] = Field(None, description="The timestamp when the user was created")
    updated_at: Optional[datetime] = Field(None, description="The timestamp when the user was last updated")

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "email": "jigglypuff@example.com",
                "profile_pic": "https://example.com/avatar.jpg",
                "ranking": 5,
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-02T15:30:00"
            }
        }
