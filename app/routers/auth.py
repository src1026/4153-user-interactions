from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from jose import JWTError, jwt
from app.services.auth_service import verify_google_token, generate_jwt, verify_jwt
from pydantic import BaseModel
import os


router = APIRouter()

# JWT config
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

class TokenData(BaseModel):
    username: str
    grants: list[str]

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        grants: list[str] = payload.get("grants")
        if username is None or grants is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return TokenData(username=username, grants=grants)
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate token")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "test" or form_data.password != "test":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    grants = ["read", "write"]
    access_token = jwt.encode({"sub": form_data.username, "grants": grants}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str):
    token_data = verify_token(token)
    return {"username": token_data.username, "grants": token_data.grants}



class GoogleLoginRequest(BaseModel):
    token: str

@router.post("/login/google")
async def google_login(data: GoogleLoginRequest):
    user_info = verify_google_token(data.token)
    jwt_token = generate_jwt(user_info)
    return {"access_token": jwt_token, "token_type": "bearer"}

@router.get("/validate-token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    payload = verify_jwt(token)
    return {"valid": True, "user": payload}

