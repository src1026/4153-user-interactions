from fastapi import APIRouter, HTTPException, Depends, status, Query
from app.resources.user_interaction_resource import UserInteractionResource
from app.models.user_actions import Like, Comment, Follow, User
from app.services.service_factory import ServiceFactory
#from app.models.user_actions import User
from app.services.email_service import send_email
from app.services.user_interaction_service import UserInteractionDataService

def data_service_factory():
    return ServiceFactory.get_service("UserInteractionDataService")
resource = UserInteractionResource(data_service_factory=data_service_factory)
router = APIRouter()

@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             summary="Register a new user", 
             description="Register a user with their information and send a confirmation email.",
             responses={
                 201: {"description": "User registered successfully", 
                       "content": {"application/json": {"example": {"message": "User registered successfully", "user": {"user_id": 1, "email": "user@example.com"}}}}}
             })
async def register_user(user_data: dict):
    service = ServiceFactory.get_service("UserInteractionDataService")
    user = service.register_user(user_data)

    # send welcome email to the registered user
    try:
        send_email(
            to_email=user["email"],  # Dynamically use the user's email
            subject="Welcome to the Recipe App",
            message=f"Hi {user.get('name', 'User')},\n\nYour registration was successful! Thank you for joining our Recipe App."
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error sending email: {e}")

    return {"message": "User registered successfully", "user": user}

@router.post("/like/", 
             tags=["likes"], 
             response_model=Like, 
             status_code=status.HTTP_201_CREATED,
             summary="Like a recipe",
             description="Allows a user to like a recipe with unique recipe and user ID",
             responses={ 
                 201: {"description": "Successfully liked the recipe", 
                       "content": {"application/json": {"example": {"user_id": 1, "recipe_id": 123}}}},
                 400: {"description": "Invalid input data"},
                 404: {"description": "Recipe not found"}
             })
async def like_recipe(like_data: Like):
    like = resource.add_like(like_data.dict())

    # Send email notification to the user who received the like
    try:
        user_email = resource.get_user_email(like_data.user_id)
        send_email(
            to_email=user_email,
            subject="New like on your recipe",
            message=f"Someone liked your recipe! Check it out: https://your-app.com/recipes/{like_data.recipe_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error sending email: {e}")

    return {
        "message": "Recipe liked successfully",
        "data": like,
        "Location": f"/likes/{like.user_id}/{like.recipe_id}"
    }

@router.delete("/like/{user_id}/{recipe_id}",
               tags=["likes"], 
               status_code=status.HTTP_200_OK, 
               summary="Unlike a recipe", 
               description="Allows a user to remove their like from a recipe by providing the user ID and recipe ID",
               responses={ 
                   200: {"description": "Successfully unliked the recipe", 
                         "content": {"application/json": {"example": {"message": "Recipe unliked successfully"}}}},
                   404: {"description": "Like not found"}
               })
async def unlike_recipe(user_id: int, recipe_id: int):
    success = resource.delete_like(user_id, recipe_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    return {"message": "Recipe unliked successfully"}

@router.get("/comment/{comment_id}", 
            tags=["comments"],
            response_model=Comment,
            summary="Get a comment",
            description="Get comment based on unique comment ID",
            responses={
                200: {
                    "description": "List of comments returned successfully",
                    "content": {"application/json": {"example": [{"comment_id": 1, "user_id": 2, "recipe_id": 101, "content": "Great recipe!"}]}}},
                404: {"description": "Recipe not found"}
            })
async def get_comment(comment_id: int):
    result = resource.get_comment(comment_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if isinstance(result, dict):
        result = Comment(**result)
        
    # # HATEOAS
    # result.links = [
    #     {"rel": "self", "href": f"/comment/{comment_id}", "method": "GET"},
    #     {"rel": "update", "href": f"/comment/{comment_id}", "method": "PUT"},
    #     {"rel": "delete", "href": f"/comment/{comment_id}", "method": "DELETE"},
    #     {"rel": "comments", "href": f"/comment/{comment_id}/comments", "method": "GET"},
    # ]
    return result

@router.post("/comment/", 
             tags=["comments"], 
             response_model=Comment,
             status_code=status.HTTP_201_CREATED,
             summary="Add a new comment",
             description="Allows a user to comment on a recipe", 
             responses={ 
                 201: {"description": "Comment added successfully", 
                       "content": {"application/json": {"example": {"message": "Comment added successfully", "data": {"comment_id": 1, "user_id": 2, "recipe_id": 101, "content": "This recipe is amazing!", "created_at": "2024-01-01T12:00:00", "updated_at": "2024-01-01T12:00:00"}}}}},
                 400: {"description": "Invalid comment data"}
             })
async def add_comment(comment_data: Comment):
    comment = resource.add_comment(comment_data.dict())
    return {
        "message": "Comment added successfully",
        "data": comment,
        "Location": f"/comment/{comment.comment_id}"
    }

@router.put("/comment/{comment_id}",
            tags=["comments"], 
            response_model=Comment,
            summary="Update an existing comment", 
            description="Allows a user to update a comment by providing the comment ID and the updated data", 
            responses={ 
                200: {"description": "Comment updated successfully", 
                      "content": {"application/json": {"example": {"message": "Comment updated successfully", "data": {"comment_id": 1, "user_id": 2, "recipe_id": 101, "content": "Updated comment", "created_at": "2024-01-01T12:00:00", "updated_at": "2024-01-02T15:30:00"}}}}},
                404: {"description": "Comment not found"},
                400: {"description": "Invalid comment data"}
            })
async def update_comment(comment_id: int, updated_data: Comment):
    updated_comment = resource.update_comment(comment_id, updated_data.dict())
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment updated successfully", "data": updated_comment}

@router.delete("/comment/{comment_id}",
               tags=["comments"], 
               status_code=status.HTTP_200_OK, 
               summary="Delete a comment", 
               description="Allows a user to delete a comment by using the unique comment ID", 
               responses={ 
                   200: {"description": "Comment deleted successfully", 
                         "content": {"application/json": {"example": {"message": "Comment deleted successfully"}}}},
                   404: {"description": "Comment not found"}
               })
async def delete_comment(comment_id: int):
    success = resource.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}

@router.post("/follow/", 
             tags=["follow"],
             response_model=Follow,
             status_code=status.HTTP_201_CREATED,
             summary="Follow a user", 
             description="Allows a user to follow another user", 
             responses={ 
                 201: {"description": "User followed successfully", 
                       "content": {"application/json": {"example": {"message": "User followed successfully", "data": {"follower_id": 1, "following_id": 2}, "Location": "/follows/2/1"}}}},
                 400: {"description": "Invalid follow data"}
             })
async def follow_user(follow_data: Follow):
    follow = resource.follow_user(follow_data.dict())
    if not follow:
        return {
            "message": f"User {follow_data.follower_id} already follows {follow_data.following_id}"
        }
    return {
        "message": "User followed successfully",
        "data": follow,
        "Location": f"/follows/{follow.following_id}/{follow.follower_id}"
    }

@router.delete("/follow/{follower_id}/{following_id}",
               tags=["follow"], 
               status_code=status.HTTP_200_OK, 
               summary="Unfollow a user", 
               description="Allows a user to unfollow another user", 
               responses={ 
                   200: {"description": "User unfollowed successfully", 
                         "content": {"application/json": {"example": {"message": "User unfollowed successfully"}}}},
                   404: {"description": "Follow relationship not found"}
               })
async def unfollow_user(follower_id: int, following_id: int):
    success = resource.unfollow_user(follower_id, following_id)
    if not success:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    return {"message": "User unfollowed successfully"}

@router.post("/users/", 
             status_code=status.HTTP_201_CREATED,
             response_model=User,
             summary="Create a user",
             description="Create a user with unique user ID",
             responses={ 
                   201: {"description": "User created successfully", 
                         "content": {"application/json": {"example": {"message": "User created successfully"}}}},
                   400: {"description": "Follow relationship not found"}
               })
async def create_user(user_data: User):
    try:
        user = resource.create_user(user_data.dict())
        return {
            "message": "User created successfully",
            "data": user,
            "Location": f"/users/{user.user_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/users/{user_id}", 
            response_model=User,
            status_code=status.HTTP_200_OK,
            summary="Get/find a user",
            description="Get a user and their account details by the unique user ID",
            responses={ 
                200: {
                    "description": "User found successfully",
                    "content": {
                        "application/json": {
                            "example": {
                                "user_id": 1,
                                "email": "jigglypuff@example.com",
                                "profile_pic": "https://example.com/avatar.jpg",
                                "ranking": 5,
                                "created_at": "2024-01-01T12:00:00",
                                "updated_at": "2024-01-02T15:30:00"
                            }
                        }
                    }
                },
                404: {
                    "description": "User not found",
                    "content": {
                        "application/json": {
                            "example": {"detail": "User with ID {user_id} not found."}
                        }
                    }
                }
            })
async def get_user(user_id: int):
    try:
        return resource.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
# @router.delete("/users/{user_id}")
# async def delete_user(user_id: int):
#     result = resource.delete_user(user_id)
#     if not result:
#         return {
#             "message": f"User {user_id} doesn't exist."
#         }
#     return {
#         "message": f"User {user_id} is deleted successfully."
#     }