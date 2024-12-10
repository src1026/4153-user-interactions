class UserInteractionDataService:
    def __init__(self, db):
        self.db = db

    def create_comment(self, comment_data: dict) -> dict:
        return self.db.insert("comments", comment_data)

    def update_comment(self, comment_id: int, updated_data: dict) -> dict:
        return self.db.update("comments", key="comment_id", value=comment_id, data=updated_data)

    def delete_comment(self, comment_id: int) -> bool:
        return self.db.delete("comments", key="comment_id", value=comment_id)

    def create_like(self, like_data: dict) -> dict:
        return self.db.insert("likes", like_data)

    def delete_like(self, user_id: int, recipe_id: int) -> bool:
        return self.db.delete("likes", conditions={"user_id": user_id, "recipe_id": recipe_id})

    def create_follow(self, follow_data: dict) -> dict:
        return self.db.insert("follows", follow_data)

    def delete_follow(self, follower_id: int, following_id: int) -> bool:
        return self.db.delete("follows", conditions={"follower_id": follower_id, "following_id": following_id})
