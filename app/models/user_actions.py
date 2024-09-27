from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

class Like(BaseModel):
    user_id: int
    recipe_id: int

class Comment(BaseModel):
    comment_id: int
    user_id: int
    recipe_id: int
    content: str

class Follow(BaseModel):
    follower_id: int
    following_id: int


    class Config:
        json_schema_extra = {
            "example": {
                "course_id": 204283,
                "course_name": "COMSW4153_001_2024_3 - Cloud Computing",
                "uuid": "3jHCxUV0ck9Z8TF1sZeI8WTx47olDGkX1YPL3USM",
                "created_at": "2024-04-05T00:58:50Z",
                "course_code": "COMSW4153_001_2024_3 - Cloud Computing",
                "sis_course_id": "COMSW4153_001_2024_3",
                "course_no": "COMSW4153",
                "section": "001",
                "course_year": "2024",
                "semester": "3"
            }
        }
