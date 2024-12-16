from graphene import ObjectType, String, Int, Field, Schema, List
from sqlalchemy import create_engine, text
from app.routers.model import User, Like, Comment, Follow
from sqlalchemy.orm import sessionmaker
from starlette_graphene3 import GraphQLApp
from fastapi import APIRouter
# DB
context = dict(
                user="jigglypuff7",
                password="Jigglypuff7!",
                host="jigglypuff7.c7s86kaawl6v.us-east-2.rds.amazonaws.com",
                port=3306,
                database="user_interactions"
            )

DATABASE_URL = f"mysql+pymysql://{context['user']}:{context['password']}@{context['host']}:{context['port']}/{context['database']}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_db_connection():
    session = None
    try:
        print("Creating a new session...")
        session = SessionLocal()
        
        # Test the connection with a simple query
        result = session.execute(text("SELECT 1"))
        print("Database connection successful:", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)
    finally:
        if session:
            print("Closing session...")
            session.close()
test_db_connection()

class LikeType(ObjectType):
    user_id=Int()
    recipe_id=Int()

    def resolve_user_id(like, info):
        return like.user_id
    
    def resolve_recipe_id(like, info):
        return like.recipe_id
    
class CommentType(ObjectType):
    comment_id=Int()
    user_id=Int()
    recupe_id=Int()
    content=String()
    created_at=String()
    updated_at=String()

    def resolve_comment_id(comment, info):
        return comment.comment_id
    
    def resolve_user_id(comment, info):
        return comment.user_id
    
    def resolve_recipe_id(comment, info):
        return comment.recupe_id
    
    def resolve_content(comment, info):
        return comment.content
    
    def resolve_created_at(comment, info):
        return comment.created_at
    
    def resolve_updated_at(comment, info):
        return comment.updated_at
    
class FollowType(ObjectType):
    follower_id=Int()
    following_id=Int()

    def resolve_follower_id(follow, info):
        return follow.follower_id
    
    def resolve_following_id(follow, info):
        return follow.following_id

class UserType(ObjectType):
    user_id=Int()
    email=String()
    profile_pic=String()
    ranking=Int()
    created_at=String()
    updated_at=String()

    #resolvers
    def resolve_user_id(person,info):
        return person.user_id

    def resolve_email(person,info):
        return person.email

    def resolve_profile_pic(person,info):
        return person.profile_pic

    def resolve_ranking(person,info):
        return person.ranking
    
    def resolve_created_at(person,info):
        return person.created_at
    
    def resolve_updated_at(person,info):
        return person.updated_at
    

class Query(ObjectType):
    allUser=List(UserType)
    user=Field(UserType,userId=Int())

    def resolve_allUser(root, info):
        session = SessionLocal()
        try:
            return session.query(User).all()
        finally:
            session.close()

    def resolve_user(root, info, userId):
        session = SessionLocal()
        try:
            return session.query(User).filter(User.user_id == userId).first()
        finally:
            session.close()

    allLike=List(LikeType)
    like=Field(LikeType,recipeId=Int())

    def resolve_allLike(root, info):
        session = SessionLocal()
        try:
            return session.query(Like).all()
        finally:
            session.close()
    
    def resolve_like(root, info, recipeId):
        session = SessionLocal()
        try:
            return session.query(Like).filter(Like.recipe_id == recipeId).all()
        finally:
            session.close()

    allComment=List(CommentType)
    comment=Field(CommentType,recipeId=Int())

    def resolve_allComment(root, info):
        session = SessionLocal()
        try:
            return session.query(Comment).all()
        finally:
            session.close()

    def resolve_comment(root, info, recipeId):
        session = SessionLocal()
        try:
            return session.query(Comment).filter(Comment.recipe_id == recipeId).all()
        finally:
            session.close()

    allFollow=List(FollowType)
    follow=Field(FollowType,followingId=Int())

    def resolve_allFollow(root, info):
        session = SessionLocal()
        try:
            return session.query(Follow).all()
        finally:
            session.close()

    def resolve_follow(root, info, followingId):
        session = SessionLocal()
        try:
            return session.query(Follow).filter(Follow.following_id == followingId).all()
        finally:
            session.close()

schema=Schema(query=Query)

graphql_app = GraphQLApp(schema=schema)
graphql_router = APIRouter()

graphql_router.add_route("/graphql", graphql_app, methods=["POST"])