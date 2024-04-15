from datetime import datetime, timedelta

import bcrypt
import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    A model representing basic user information that can be safely shared in the authentication response.
    """

    user_id: str
    email: str


class AuthenticateUserResponse(BaseModel):
    """
    This model represents the response data after a successful authentication, including the JWT token for session management.
    """

    jwt_token: str
    user_info: UserInfo


SECRET_KEY = "your_secret_key"

ALGORITHM = "HS256"


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticates user credentials and returns a JWT for session management.

    Args:
    email (str): The email address of the user attempting to authenticate.
    password (str): The password of the user attempting to authenticate.

    Returns:
    AuthenticateUserResponse: This model represents the response data after a successful authentication,
    including the JWT token for session management.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user is None:
        raise Exception("User not found")
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise Exception("Incorrect password")
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    user_info = UserInfo(user_id=user.id, email=user.email)
    authenticate_user_response = AuthenticateUserResponse(
        jwt_token=token, user_info=user_info
    )
    return authenticate_user_response
