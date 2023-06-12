from typing import NamedTuple

"""Provides a Fire class"""


class Fire(NamedTuple):
    """Fire data"""

    location: str
    """Location of the fire"""

    date_time: str
    """Date and time the fire started"""

    acres_burned: float
    """Acres burned by the fire"""

    latitude: float
    """Latitude of the fire"""

    longitude: float
    """Longitude of the fire"""

    url: str
    """Url for more information about the fire"""
