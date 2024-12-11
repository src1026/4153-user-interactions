from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.resources.user_interaction_resource import UserInteractionResource
from app.models.user_actions import Like, Comment, Follow
from app.utils.pagination import PaginationParams, paginate_results

router = APIRouter(
    prefix="/user-interactions",
    tags=["User Interactions"],
    responses={404: {"description": "Not found"}}
)
resource = UserInteractionResource()

class HATEOSLink(BaseModel):
    href: str
    rel: str
    method: str

class LikeResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    created_at: str
    _links: List[HATEOSLink] = []

class CommentResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    content: str
    created_at: str
    _links: List[HATEOSLink] = []

class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: str
    _links: List[HATEOSLink] = []

def generate_hateos_links(resource_type: str, resource_id: int, additional_links: List[dict] = None) -> List[HATEOSLink]:
    """Generate HATEOAS links for a resource."""
    base_links = [
        HATEOSLink(href=f"/user-interactions/{resource_type}/{resource_id}", rel="self", method="GET"),
        HATEOSLink(href=f"/user-interactions/{resource_type}/{resource_id}", rel="update", method="PUT"),
        HATEOSLink(href=f"/user-interactions/{resource_type}/{resource_id}", rel="delete", method="DELETE")
    ]
    
    if additional_links:
        base_links.extend([HATEOSLink(**link) for link in additional_links])
    
    return base_links

@router.post("/like/", 
             status_code=201, 
             response_model=LikeResponse, 
             summary="Create a new like",
             description="Add a like to a recipe")
async def like_recipe(like_data: Like, request: Request):
    """
    Create a new like with 201 Created response and Location header.
    
    - Implements HATEOAS principles
    - Returns created resource with self-referential links
    """
    like = resource.add_like(like_data.dict())
    response_data = LikeResponse(
        **like.dict(), 
        _links=generate_hateos_links("like", like.id)
    )
    
    return JSONResponse(
        status_code=201, 
        content=response_data.dict(),
        headers={"Location": f"{request.base_url}user-interactions/like/{like.id}"}
    )

@router.get("/likes/", response_model=List[LikeResponse])
async def list_likes(
    pagination: PaginationParams = Depends(),
    user_id: Optional[int] = None
):
    """
    Retrieve paginated list of likes with optional filtering.
    
    - Implements pagination
    - Supports optional user_id filtering
    """
    likes = resource.get_likes(user_id=user_id)
    paginated_likes = paginate_results(likes, pagination.page, pagination.page_size)
    
    return [
        LikeResponse(
            **like.dict(), 
            _links=generate_hateos_links("like", like.id)
        ) for like in paginated_likes
    ]

@router.post("/comment/", 
             status_code=202,  # Asynchronous processing example
             response_model=CommentResponse,
             summary="Create a new comment")
async def add_comment(comment_data: Comment):
    """
    Create a new comment with 202 Accepted response for asynchronous processing.
    
    - Demonstrates asynchronous execution pattern
    - Provides resource links
    """
    # Simulating async processing
    comment = resource.add_comment(comment_data.dict())
    response_data = CommentResponse(
        **comment.dict(), 
        _links=generate_hateos_links("comment", comment.id)
    )
    
    return JSONResponse(
        status_code=202, 
        content={
            "message": "Comment processing started", 
            "data": response_data.dict(),
            "status_url": f"/user-interactions/comment/{comment.id}/status"
        }
    )

@router.post("/follow/", 
             status_code=201, 
             response_model=FollowResponse,
             summary="Follow a user")
async def follow_user(follow_data: Follow, request: Request):
    """
    Create a new follow relationship with 201 Created response.
    
    - Implements HATEOAS with self and related links
    - Returns created resource location
    """
    follow = resource.follow_user(follow_data.dict())
    response_data = FollowResponse(
        **follow.dict(), 
        _links=generate_hateos_links("follow", follow.id)
    )
    
    return JSONResponse(
        status_code=201, 
        content=response_data.dict(),
        headers={"Location": f"{request.base_url}user-interactions/follow/{follow.id}"}
    )

@router.delete("/like/{user_id}/{recipe_id}", 
               response_model=dict, 
               summary="Remove a like",
               description="Delete a specific like for a user and recipe")
async def unlike_recipe(user_id: int, recipe_id: int):
    """
    Delete a like with comprehensive error handling and HATEOAS principles.
    
    - Checks for existence before deletion
    - Provides informative error responses
    """
    success = resource.delete_like(user_id, recipe_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Like not found",
            headers={
                "Link": '</user-interactions/likes>; rel="collection"'
            }
        )
    
    return {
        "message": "Recipe unliked successfully",
        "links": [
            {"href": "/user-interactions/likes", "rel": "collection", "method": "GET"}
        ]
    }

@router.put("/comment/{comment_id}", 
            response_model=CommentResponse,
            summary="Update a comment",
            description="Modify an existing comment")
async def update_comment(comment_id: int, updated_data: Comment):
    """
    Update a comment with comprehensive error handling and HATEOAS support.
    
    - Validates comment existence
    - Returns updated resource with links
    - Provides navigation links
    """
    updated_comment = resource.update_comment(comment_id, updated_data.dict())
    if not updated_comment:
        raise HTTPException(
            status_code=404, 
            detail="Comment not found",
            headers={
                "Link": '</user-interactions/comments>; rel="collection"'
            }
        )
    
    response_data = CommentResponse(
        **updated_comment.dict(), 
        _links=generate_hateos_links("comment", comment_id)
    )
    
    return response_data

@router.delete("/comment/{comment_id}", 
               response_model=dict, 
               summary="Delete a comment",
               description="Remove a specific comment")
async def delete_comment(comment_id: int):
    """
    Delete a comment with comprehensive error handling.
    
    - Checks for comment existence
    - Provides informative error responses and navigation links
    """
    success = resource.delete_comment(comment_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Comment not found",
            headers={
                "Link": '</user-interactions/comments>; rel="collection"'
            }
        )
    
    return {
        "message": "Comment deleted successfully",
        "links": [
            {"href": "/user-interactions/comments", "rel": "collection", "method": "GET"}
        ]
    }

@router.delete("/follow/{follower_id}/{following_id}", 
               response_model=dict, 
               summary="Unfollow a user",
               description="Remove a follow relationship between two users")
async def unfollow_user(follower_id: int, following_id: int):
    """
    Delete a follow relationship with comprehensive error handling.
    
    - Verifies existence of follow relationship
    - Returns informative response with navigation links
    """
    success = resource.unfollow_user(follower_id, following_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Follow relationship not found",
            headers={
                "Link": '</user-interactions/follows>; rel="collection"'
            }
        )
    
    return {
        "message": "User unfollowed successfully",
        "links": [
            {"href": "/user-interactions/follows", "rel": "collection", "method": "GET"}
        ]
    }
