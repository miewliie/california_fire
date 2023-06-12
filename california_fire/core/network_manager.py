from california_fire.core.fire_api import fetch_fires
from california_fire.storage.data_handler import fire_encoder


def get_fire_data():
    """Get fire data from an API"""
    data = fetch_fires()
    return fire_encoder(fire_data=data)
