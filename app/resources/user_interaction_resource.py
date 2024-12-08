from app.models.user_actions import Like, Comment, Follow
from app.services.service_factory import ServiceFactory

class UserInteractionResource:
    def __init__(self):
        self.data_service = ServiceFactory.get_service("UserInteractionDataService")

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
        return Follow(**follow)

    def unfollow_user(self, follower_id: int, following_id: int) -> bool:
        return self.data_service.delete_follow(follower_id, following_id)
