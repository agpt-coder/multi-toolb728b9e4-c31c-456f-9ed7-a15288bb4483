import prisma
import prisma.models
from pydantic import BaseModel


class RevokeAccessResponse(BaseModel):
    """
    Confirms the successful revocation of access credentials.
    """

    success: bool
    message: str


async def revoke_access(
    user_id: str, token_type: str, token: str
) -> RevokeAccessResponse:
    """
    Revokes access by invalidating the current JWT or API key.

    Args:
        user_id (str): The ID of the user performing the revoke operation. This ensures that only authorized users can invalidate tokens or keys.
        token_type (str): Specifies the type of token being revoked, either a JWT or an API key.
        token (str): The actual JWT or API key to be revoked.

    Returns:
        RevokeAccessResponse: Confirms the successful revocation of access credentials.

    Example:
        user_id = 'some-user-id'
        token_type = 'API_KEY'
        token = 'some-api-key'
        revoke_access(user_id, token_type, token)
        > RevokeAccessResponse(success=True, message="API Key revoked successfully.")
    """
    if token_type.lower() == "api_key":
        api_key = await prisma.models.ApiKey.prisma().find_unique(where={"key": token})
        if api_key and api_key.userId == user_id:
            await prisma.models.ApiKey.prisma().delete(where={"key": token})
            return RevokeAccessResponse(
                success=True, message="API Key revoked successfully."
            )
        else:
            return RevokeAccessResponse(
                success=False,
                message="API Key not found or you are not authorized to revoke this key.",
            )
    else:
        return RevokeAccessResponse(
            success=False,
            message="Currently, JWT revocation is not supported directly in this function.",
        )
