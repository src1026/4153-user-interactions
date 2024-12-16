from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create the base class for declarative models
Base = declarative_base()

# Define the Person table as a SQLAlchemy model
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    profile_pic = Column(String) 
    ranking = Column(Integer) 
    created_at = Column(String)
    updated_at = Column(String)
    