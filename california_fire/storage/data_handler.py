import json
import os
from typing import Any

from california_fire.core.fire import Fire

"""Provide functions handle fire data."""


def read_json(file_path: str):
    """ Read data from json file."""
    with open(file_path, 'r', encoding='utf-8') as output_file:
        size = os.path.getsize(file_path)
        return json.loads(output_file.read()) if size > 0 else None


def from_dict_to_fire(dict_data: dict[str, Any]) -> Fire:
    """Convert dictionary to Fire object."""
    return Fire(
        location=dict_data['Location'],
        date_time=dict_data['Started'],
        acres_burned=dict_data['AcresBurned'],
        latitude=dict_data['Latitude'],
        longitude=dict_data['Longitude'],
        url=dict_data['Url']
    )


def fire_encoder(fire_data: list[dict[str, Any]]) -> list[Fire]:
    """Convert dictionary to list of Fire object."""
    fires: list[Fire] = []
    for fire in fire_data:
        fires.append(from_dict_to_fire(dict_data=fire))
    return fires
