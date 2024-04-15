import logging
from contextlib import asynccontextmanager

import project.authenticate_user_service
import project.get_geolocation_service
import project.refresh_token_service
import project.revoke_access_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="multi tool",
    lifespan=lifespan,
    description="The Multi-Purpose API Toolkit project was designed to offer a wide array of functionalities via a comprehensive suite of single-endpoint APIs, targeting developers who wish to streamline common tasks without integrating multiple third-party services. This all-encompassing toolkit delivers a rich set of tools, ranging from QR code generation to advanced features like text-to-speech conversion and IP geolocation, addressing the need for a versatile and efficient toolset in software development projects.\n\nKey functionalities discussed include the QR Code Generator for creating custom QR codes, Currency Exchange Rate for fetching real-time currency values, IP Geolocation for obtaining detailed location data from IP addresses, Image Resizing for on-the-fly image optimization, and the Password Strength Checker to evaluate and improve password security. It also offers unique features like Text-to-Speech conversion, Barcode Generation, Email Validation, Time Zone Conversion, URL Preview, PDF Watermarking, and an RSS Feed to JSON converter, catering to a broad spectrum of developer needs. The emphasis throughout this project has been on ensuring scalability, security, and developer efficiency by aligning with best practices for API kit construction, such as clear API design, robust documentation, and flexible data format support.\n\nThe user feedback highlighted the significance of authentication and authorization endpoints for optimal project security, anticipating moderate to high traffic volumes and identifying crucial scalability and security considerations. Additionally, there was interest in AI-driven analytics enhancements for real-time performance optimization and security vulnerability identification. Technical preferences include Python, Node.js, and Docker in the tech stack, emphasizing RESTful principles and possibly GraphQL for complex querying, signaling a clear direction towards a scalable, secure, and developer-centric API toolkit.",
)


@app.get(
    "/geolocation/{ip}",
    response_model=project.get_geolocation_service.GeolocationResponse,
)
async def api_get_get_geolocation(
    ip: str,
) -> project.get_geolocation_service.GeolocationResponse | Response:
    """
    Retrieves geolocation data for a given IP address.
    """
    try:
        res = await project.get_geolocation_service.get_geolocation(ip)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/auth/revoke", response_model=project.revoke_access_service.RevokeAccessResponse
)
async def api_delete_revoke_access(
    user_id: str, token_type: str, token: str
) -> project.revoke_access_service.RevokeAccessResponse | Response:
    """
    Revokes access by invalidating the current JWT or API key.
    """
    try:
        res = await project.revoke_access_service.revoke_access(
            user_id, token_type, token
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticates user credentials and returns a JWT for session management.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/refresh", response_model=project.refresh_token_service.RefreshTokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.RefreshTokenResponse | Response:
    """
    Refresh the JWT for the user session upon expiration.
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
