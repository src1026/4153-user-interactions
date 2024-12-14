from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.services.auth_service import verify_google_token, generate_jwt
from pydantic import BaseModel
import os
from datetime import datetime, timedelta

# Router setup
router = APIRouter()

# JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: str
    grants: list[str]

class GoogleLoginRequest(BaseModel):
    token: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with optional expiration
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token: str):
    """
    Verify and decode a JWT token
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        grants: list[str] = payload.get("grants")
        
        if not username or not grants:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Could not validate credentials"
            )
        
        return TokenData(username=username, grants=grants)
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token has expired"
        )
    
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials"
        )

def verify_google_token(token: str):
    try:
        # Verify the token using Google APIs
        credentials, project = jwt.decode(
            token, 
            audience=os.getenv("GOOGLE_CLIENT_ID"),  # Use your Google OAuth client ID
            issuer="accounts.google.com",
        )
        return credentials
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Google token"
        )

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Token generation endpoint with simple username/password check
    """
    # TODO: Replace with actual user authentication against database
    if form_data.username != "jigglypuff" or form_data.password != "test":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "grants": ["read", "write"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """
    Protected endpoint to get current user's information
    """
    token_data = verify_token(token)
    return {"username": token_data.username, "grants": token_data.grants}

@router.post("/login/google")
async def google_login(data: GoogleLoginRequest):
    """
    Google OAuth login endpoint
    """
    user_info = verify_google_token(data.token)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = create_access_token(
        data={
            "sub": user_info.get("email", ""),
            "grants": ["read", "write"]
        },
        expires_delta=access_token_expires
    )
    
    return {"access_token": jwt_token, "token_type": "bearer"}

@router.get("/validate-token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    """
    Token validation endpoint
    """
    payload = verify_token(token)
    return {"valid": True, "user": payload.dict()}
