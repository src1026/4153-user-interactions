from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from passlib.hash import bcrypt
from fastapi import HTTPException
import logging

class UserInteractionDataService:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def register_user(self, user_data: dict) -> dict:
        required_fields = ["email"]
        for field in required_fields:
            if field not in user_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        existing_user = self.db.get_data_object("users", {"email": user_data["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        insert_data = {
            "email": user_data["email"],
            "profile_pic": user_data.get("profile_pic", ""),
            "ranking": user_data.get("ranking", 0),
            "created_at": user_data.get("created_at"),
            "updated_at": user_data.get("updated_at"),
        }

        new_user = self.db.insert("users", insert_data)
        if not new_user:
            raise HTTPException(status_code=500, detail="Failed to register user")

        return new_user

    def get_comment(self, comment_id: int) -> dict:
        return self.db.get_data_object("comments", conditions={"comment_id": comment_id})

    def create_comment(self, comment_data: dict) -> dict:
        return self.db.insert("comments", comment_data)

    def update_comment(self, comment_id: int, updated_data: dict) -> dict:
        return self.db.update("comments", conditions={"comment_id": comment_id}, data=updated_data)

    def delete_comment(self, comment_id: int) -> bool:
        return self.db.delete("comments", conditions={"comment_id": comment_id})

    def create_like(self, like_data: dict) -> dict:
        return self.db.insert("likes", like_data)

    def delete_like(self, user_id: int, recipe_id: int) -> bool:
        return self.db.delete("likes", conditions={"user_id": user_id, "recipe_id": recipe_id})
    
    def create_follow(self, follow_data: dict) -> dict:
        return self.db.insert("follows", follow_data)

    def delete_follow(self, follower_id: int, following_id: int) -> bool:
        return self.db.delete("follows", conditions={"follower_id": follower_id, "following_id": following_id})

    def create_user(self, user_data: dict) -> dict:
        """
        Insert a new user into the users table.

        :param user_data: Dictionary containing user details (e.g., username, email, etc.)
        :return: The inserted user data including its generated primary key (id).
        """
        return self.db.insert("users", user_data)
    
    def get_user(self, user_id: int):
        return self.db.get_data_object("users", conditions={"user_id": user_id})
    
    # def delete_user(self, user_id: int):
    #     return self.db.delete("users", conditions={"user_id": user_id})