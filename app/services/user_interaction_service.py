from sqlalchemy.orm import Session
from app.models.user_actions import Like, Comment, Follow
from app.services.database import get_db

class UserInteractionService:

    def like_recipe(self, db: Session, user_id: int, recipe_id: int):
        try:
            like = Like(user_id=user_id, recipe_id=recipe_id)
            db.add(like)
            db.commit()
            logger.info(f"Recipe liked successfully: User {user_id}, Recipe {recipe_id}")
            return like
        except Exception as e:
            logger.error(f"Failed to like recipe: {e}")
            raise
            
    def unlike_recipe(self, db: Session, user_id: int, recipe_id: int):
        like = db.query(Like).filter(Like.user_id == user_id, Like.recipe_id == recipe_id).first()
        if not like:
            logger.warning(f"Like not found: User {user_id}, Recipe {recipe_id}")
            return False
        try:
            db.delete(like)
            db.commit()
            logger.info(f"Recipe unliked successfully: User {user_id}, Recipe {recipe_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to unlike recipe: {e}")
            raise

    def add_comment(self, db: Session, comment_data: dict):
        try:
            comment = Comment(**comment_data)
            db.add(comment)
            db.commit()
            db.refresh(comment)
            logger.info(f"Comment created successfully: {comment.comment_id}")
            return comment
        except Exception as e:
            logger.error(f"Failed to create comment: {e}")
            raise

    def update_comment(self, db: Session, comment_id: int, updated_data: dict):
        comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
        if not comment:
            logger.warning(f"Comment not found: {comment_id}")
            return None
        try:
            for key, value in updated_data.items():
                setattr(comment, key, value)
            comment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(comment)
            logger.info(f"Comment updated successfully: {comment.comment_id}")
            return comment
        except Exception as e:
            logger.error(f"Failed to update comment: {e}")
            raise

    def delete_comment(self, db: Session, comment_id: int):
        comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
        if not comment:
            logger.warning(f"Comment not found: {comment_id}")
            return False
        try:
            db.delete(comment)
            db.commit()
            logger.info(f"Comment deleted successfully: {comment_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete comment: {e}")
            raise

    def follow_user(self, db: Session, follower_id: int, following_id: int):
        try:
            follow = Follow(follower_id=follower_id, following_id=following_id)
            db.add(follow)
            db.commit()
            logger.info(f"User followed successfully: Follower {follower_id}, Following {following_id}")
            return follow
        except Exception as e:
            logger.error(f"Failed to follow user: {e}")
            raise

    def unfollow_user(self, db: Session, follower_id: int, following_id: int):
        follow = db.query(Follow).filter(Follow.follower_id == follower_id, Follow.following_id == following_id).first()
        if not follow:
            logger.warning(f"Follow relationship not found: Follower {follower_id}, Following {following_id}")
            return False
        try:
            db.delete(follow)
            db.commit()
            logger.info(f"User unfollowed successfully: Follower {follower_id}, Following {following_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to unfollow user: {e}")
            raise
