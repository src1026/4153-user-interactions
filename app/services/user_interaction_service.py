from sqlalchemy.orm import Session
from app.models.user_interaction import Like, Comment, Follow
from app.services.database import get_db

class UserInteractionService:

    def like_recipe(self, db: Session, user_id: int, recipe_id: int):
        like = Like(user_id=user_id, recipe_id=recipe_id)
        db.add(like)
        db.commit()
        return like

    def comment_on_recipe(self, db: Session, comment_data: dict):
        comment = Comment(**comment_data)
        db.add(comment)
        db.commit()
        return comment

    def follow_user(self, db: Session, follower_id: int, following_id: int):
        follow = Follow(follower_id=follower_id, following_id=following_id)
        db.add(follow)
        db.commit()
        return follow
