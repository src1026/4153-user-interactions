from fastapi import APIRouter, HTTPException, Depends
from app.resources.user_interaction_resource import UserInteractionResource
from app.models.user_actions import Like, Comment, Follow
from app.services.service_factory import ServiceFactory
from app.models.user_actions import User

def data_service_factory():
    return ServiceFactory.get_service("UserInteractionDataService")
resource = UserInteractionResource(data_service_factory=data_service_factory)
router = APIRouter()

@router.post("/like/", status_code=201)
async def like_recipe(like_data: Like):
    like = resource.add_like(like_data.dict())
    return {
        "message": "Recipe liked successfully",
        "data": like,
        "Location": f"/likes/{like.user_id}/{like.recipe_id}"
    }

@router.delete("/like/{user_id}/{recipe_id}")
async def unlike_recipe(user_id: int, recipe_id: int):
    success = resource.delete_like(user_id, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"message": "Recipe unliked successfully"}

@router.post("/comment/", status_code=201)
async def add_comment(comment_data: Comment):
    comment = resource.add_comment(comment_data.dict())
    return {
        "message": "Comment added successfully",
        "data": comment,
        "Location": f"/comment/{comment.comment_id}"
    }

@router.put("/comment/{comment_id}")
async def update_comment(comment_id: int, updated_data: Comment):
    updated_comment = resource.update_comment(comment_id, updated_data.dict())
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment updated successfully", "data": updated_comment}

@router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int):
    success = resource.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
    
@router.post("/follow/", status_code=201)
async def follow_user(follow_data: Follow):
    follow = resource.follow_user(follow_data.dict())
    return {
        "message": "User followed successfully",
        "data": follow,
        "Location": f"/follows/{follow.following_id}/{follow.follower_id}"
    }

@router.delete("/follow/{follower_id}/{following_id}")
async def unfollow_user(follower_id: int, following_id: int):
    success = resource.unfollow_user(follower_id, following_id)
    if not success:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    return {"message": "User unfollowed successfully"}

@router.post("/users/", status_code=201)
async def create_user(user_data: User):
    try:
        user = resource.create_user(user_data.dict())
        return {
            "message": "User created successfully",
            "data": user,
            "Location": f"/users/{user.user_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    try:
        return resource.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))