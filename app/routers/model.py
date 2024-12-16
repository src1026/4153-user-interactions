from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    profile_pic = Column(String) 
    ranking = Column(Integer) 
    created_at = Column(String)
    updated_at = Column(String)


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer)
    recipe_id = Column(Integer, primary_key=True)

class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    recipe_id = Column(Integer)
    content = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(Integer)
    following_id = Column(Integer, primary_key=True)