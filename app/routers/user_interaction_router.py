from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user_interaction_service import UserInteractionService
from app.services.database import get_db
from app.models.user_interaction import Like, Comment

router = APIRouter()
service = UserInteractionService()

@router.post("/like/")
async def like_recipe(user_id: int, recipe_id: int, db: Session = Depends(get_db)):
    return service.like_recipe(db, user_id, recipe_id)

@router.post("/comment/")
async def comment_on_recipe(comment_data: Comment, db: Session = Depends(get_db)):
    return service.comment_on_recipe(db, comment_data.dict())

@router.post("/follow/")
async def follow_user(follower_id: int, following_id: int, db: Session = Depends(get_db)):
    return service.follow_user(db, follower_id, following_id)

