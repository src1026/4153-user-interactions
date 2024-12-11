from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService

class UserInteractionDataService:
    def __init__(self, db):
        self.db = db

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
    
    def delete_user(self, user_id: int):
        return self.db.delete("users", conditions={"user_id": user_id})