from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from the .env file
load_dotenv()

# Secret key and algorithm
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def generate_jwt_token(username: str, grants: list[str]):
    """
    Generate a JWT token.

    :param username: The username or subject of the token
    :param grants: A list of grants/permissions for the token
    :return: Encoded JWT token
    """
    expiration_time = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    payload = {
        "sub": username,             # Subject of the token
        "grants": grants,            # Permissions or roles
        "exp": expiration_time,      # Expiration time
        "iat": datetime.utcnow(),    # Issued at
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

# Example usage
username = "example_user"
grants = ["read", "write"]

jwt_token = generate_jwt_token(username, grants)
print("Generated JWT:", jwt_token)
