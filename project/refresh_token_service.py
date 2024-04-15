from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    The response model for the refresh_token endpoint. It provides the new JWT for the user.
    """

    jwt_token: str
    refresh_token: str


async def fetch_user_from_refresh_token(
    refresh_token: str,
) -> Optional[prisma.models.User]:
    """
    Retrieves the user associated with the given refresh token if it exists.

    Args:
        refresh_token (str): The refresh token purported to belong to a user.

    Returns:
        Optional[prisma.models.User]: The user associated with the refresh token or None.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"ApiKeys_some": {"key": refresh_token}}, include={"ApiKeys": True}
    )
    return user


async def refresh_token(refresh_token: str) -> RefreshTokenResponse:
    """
    Refreshes the JWT for the user session upon expiration.

    Args:
        refresh_token (str): The refresh token provided by the user to obtain a new JWT.

    Returns:
        RefreshTokenResponse: The response model for the refresh_token endpoint.
                              It provides the new JWT for the user.

    This method is a high-level simulation and does not actually generate JWTs. In a real implementation,
    after validating the refresh token and identifying the user, new JWT and refresh tokens would be generated
    using a secure method and returned to the user.
    """
    user = await fetch_user_from_refresh_token(refresh_token)
    if user is None:
        raise Exception("No user found with the given refresh token")
    new_jwt_token = "newly_generated_jwt_token_for_" + user.id
    new_refresh_token = "newly_generated_refresh_token_for_" + user.id
    return RefreshTokenResponse(
        jwt_token=new_jwt_token, refresh_token=new_refresh_token
    )
