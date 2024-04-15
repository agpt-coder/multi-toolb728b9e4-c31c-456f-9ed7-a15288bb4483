from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GeolocationResponse(BaseModel):
    """
    Detailed geolocation information for a given IP address.
    """

    country: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    error: Optional[str] = None


async def get_geolocation(ip: str) -> GeolocationResponse:
    """
    Retrieves geolocation data for a given IP address by querying the database.

    Args:
        ip (str): The IP address for which to fetch geolocation information.

    Returns:
        GeolocationResponse: Detailed geolocation information for a given IP address.
    """
    geolocation_data = await prisma.models.GeolocationData.prisma().find_unique(
        where={"ipAddress": ip}
    )
    if geolocation_data:
        response = GeolocationResponse(
            country=geolocation_data.country,
            city=geolocation_data.city,
            latitude=geolocation_data.latitude,
            longitude=geolocation_data.longitude,
        )
    else:
        response = GeolocationResponse(error=f"No geolocation data found for IP: {ip}")
    return response
