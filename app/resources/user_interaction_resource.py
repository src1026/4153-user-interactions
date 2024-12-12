from app.models.user_actions import Like, Comment, Follow, User
from typing import List


class UserInteractionResource:
    def __init__(self, data_service_factory):
        self._data_service_factory = data_service_factory
        self._data_service = None  # Lazy initialization

    @property
    def data_service(self):
        # Initialize the data service only when accessed
        if self._data_service is None:
            self._data_service = self._data_service_factory()
            print(f"Initialized data_service: {self._data_service}")
        return self._data_service
    
    def get_comment(self, comment_id: int) -> Comment:
        comment = self.data_service.get_comment(comment_id)
        return Comment(**comment)

    def add_comment(self, comment_data: dict) -> Comment:
        comment = self.data_service.create_comment(comment_data)
        return Comment(**comment)

    def update_comment(self, comment_id: int, updated_data: dict) -> Comment:
        comment = self.data_service.update_comment(comment_id, updated_data)
        return Comment(**comment)

    def delete_comment(self, comment_id: int) -> bool:
        return self.data_service.delete_comment(comment_id)

    def add_like(self, like_data: dict) -> Like:
        like = self.data_service.create_like(like_data)
        return Like(**like)

    def delete_like(self, user_id: int, recipe_id: int) -> bool:
        return self.data_service.delete_like(user_id, recipe_id)

    def follow_user(self, follow_data: dict) -> Follow:
        follow = self.data_service.create_follow(follow_data)
        if not follow:
            return None
        return Follow(**follow)

    def unfollow_user(self, follower_id: int, following_id: int) -> bool:
        return self.data_service.delete_follow(follower_id, following_id)

    def create_user(self, user_data: dict) -> User:
        user = self.data_service.create_user(user_data)
        return User(**user)

    def get_user(self, user_id: int) -> User:
        user = self.data_service.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        return User(**user)

    def validate_user(self, user_id: int) -> bool:
        user = self.data_service.get_user(user_id)
        return bool(user)
    
    # def delete_user(self, user_id: int) -> bool:
    #     user = self.data_service.delete_user(user_id)
    #     return (user is not None)

    def get_created_recipes(self, user_id: int) -> List[dict]:
        return self.data_service.get_recipes_created_by_user(user_id)

    def get_liked_recipes(self, user_id: int) -> List[dict]:
        return self.data_service.get_recipes_liked_by_user(user_id)

