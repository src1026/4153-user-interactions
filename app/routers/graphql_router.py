from fastapi import APIRouter, Depends, HTTPException, Query, Body
from starlette_graphene3 import GraphQLApp
from graphql import build_schema, graphql_sync
from app.models.user_actions import Like, Comment, Follow, User
from graphene import ObjectType, Field, ID, List
from typing import Optional
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

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

current_dir = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(current_dir, "schema.graphql")
with open(schema_path, "r") as file:
    schema_definition = file.read()

# Build the schema
schema = build_schema(schema_definition)

graphql_app = GraphQLApp(schema=schema)
graphql_router = APIRouter()

class Query(ObjectType):
    like_by_id = Field(Like, id=ID(required=True))
    comment_by_id = Field(Comment, id=ID(required=True))
    user_likes = Field(List(Like), user_id=ID(required=True))
    user_comments = Field(List(Comment), user_id=ID(required=True))
    user_follows = Field(List(Follow), user_id=ID(required=True))

    def resolve_like_by_id(self, info, id):
        session: Session = info.context['session']  # Use the session provided by the context
        return session.query(Like).filter(Like.id == id).first()

    def resolve_comment_by_id(self, info, id):
        session: Session = info.context['session']
        return session.query(Comment).filter(Comment.id == id).first()

    def resolve_user_likes(self, info, user_id):
        session: Session = info.context['session']
        return session.query(Like).filter(Like.user_id == user_id).all()

    def resolve_user_comments(self, info, user_id):
        session: Session = info.context['session']
        return session.query(Comment).filter(Comment.user_id == user_id).all()

    def resolve_user_follows(self, info, user_id):
        session: Session = info.context['session']
        return session.query(Follow).filter(Follow.follower_id == user_id).all()

    # def resolve_like_by_id(self, id):
    #     return SessionLocal.query.filter(Like.id == id).all()

    # def resolve_comment_by_id(self, id):
    #     return SessionLocal.query.filter(Comment.id == id).all()

    # def resolve_user_likes(self, user_id):
    #     return SessionLocal.query.filter(Like.user_id == user_id).all()

    # def resolve_user_comments(self, user_id):
    #     return SessionLocal.query.filter(Comment.user_id == user_id).all()

    # def resolve_user_follows(self, user_id):
    #     return SessionLocal.query.filter(Follow.follower_id == user_id).all()


@graphql_router.post("/graphql")
async def graphql_query(
    query: Optional[str] = Query(None)
):
    print(query)
    print(json.loads(query))
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    result = graphql_sync(
        schema=schema,    
        source=json.loads(query), 
        context_value={"session": SessionLocal}
    )
    return result

graphql_router.add_route("/graphql", graphql_app)