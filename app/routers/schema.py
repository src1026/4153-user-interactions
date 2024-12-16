from graphene import ObjectType, String, Int, Field, Schema, List
from sqlalchemy import create_engine, text
from app.routers.model import User
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

schema=Schema(query=Query)

graphql_app = GraphQLApp(schema=schema)
graphql_router = APIRouter()

graphql_router.add_route("/graphql", graphql_app, methods=["POST"])