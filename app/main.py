from fastapi import Depends, FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_interaction_router
from app.routers import auth
from app.services.auth_service import verify_jwt
from fastapi.responses import JSONResponse
from app.routers.graphql_router import graphql_router

app = FastAPI()
app.include_router(auth.router)
app.include_router(graphql_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)
app.include_router(user_interaction_router.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.middleware("http")
async def validate_and_propagate_token(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
    if token:
        try:
            # Validate token
            verify_jwt(token)
        except Exception as e:
            return JSONResponse(status_code=401, content={"message": "Invalid or expired token"})
    response = await call_next(request)
    return response

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



