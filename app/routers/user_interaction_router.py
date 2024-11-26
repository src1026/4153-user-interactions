from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user_interaction_service import UserInteractionService
from app.services.database import get_db
from app.models.user_interaction import Like, Comment, Follow

router = APIRouter()
service = UserInteractionService()

@router.post("/like/", status_code=status.HTTP_201_CREATED)
async def like_recipe(like_data: Like, db: Session = Depends(get_db)):
    like = service.like_recipe(db, like_data.user_id, like_data.recipe_id)
    return {
        "message": "Recipe liked successfully",
        "data": like,
        "Location": f"/likes/{like.user_id}/{like.recipe_id}"
    }

@router.delete("/like/{user_id}/{recipe_id}")
async def unlike_recipe(user_id: int, recipe_id: int, db: Session = Depends(get_db)):
    success = service.unlike_recipe(db, user_id, recipe_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    return {"message": "Recipe unliked successfully"}

@router.post("/comment/", status_code=status.HTTP_201_CREATED)
async def add_comment(comment_data: Comment, db: Session = Depends(get_db)):
    comment = service.add_comment(db, comment_data.dict())
    # Include Location header for the new resource
    return {
        "message": "Comment created successfully",
        "data": comment,
        "Location": f"/comments/{comment.comment_id}"
    }

@router.put("/comment/{comment_id}")
async def update_comment(comment_id: int, updated_data: Comment, db: Session = Depends(get_db)):
    updated_comment = service.update_comment(db, comment_id, updated_data.dict())
    if not updated_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return {"message": "Comment updated successfully", "data": updated_comment}

@router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    success = service.delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
    
@router.post("/follow/", status_code=status.HTTP_201_CREATED)
async def follow_user(follow_data: Follow, db: Session = Depends(get_db)):
    follow = service.follow_user(db, follow_data.follower_id, follow_data.following_id)
    return {
        "message": "User followed successfully",
        "data": follow,
        "Location": f"/follows/{follow.following_id}/{follow.follower_id}"
    }

@router.delete("/follow/{follower_id}/{following_id}")
async def unfollow_user(follower_id: int, following_id: int, db: Session = Depends(get_db)):
    success = service.unfollow_user(db, follower_id, following_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follow relationship not found")
    return {"message": "User unfollowed successfully"}

