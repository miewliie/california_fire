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


def write_json(data:  list[dict[str, Any]], file_path: str):
    """ Write data to json file."""
    with open(file_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file)
        print("Done write data into json file")


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


def to_dict(fire_data: Fire) -> dict[str, Any]:
    """Convert Fire object to dictionary."""
    return {
        'Location': fire_data.location,
        'Started': fire_data.date_time,
        'AcresBurned': fire_data.acres_burned,
        'Latitude': fire_data.latitude,
        'Longitude': fire_data.longitude,
        'Url': fire_data.url
    }


def fire_encoder(fire_data: list[dict[str, Any]]) -> list[Fire]:
    """Convert list of dictionary to list of Fire object."""
    fires: list[Fire] = []
    for fire in fire_data:
        fires.append(from_dict_to_fire(dict_data=fire))
    return fires


def fire_decoder(fires_data: list[Fire]) -> list[dict[str, Any]]:
    """Convert list of Fire object to list of dictionary."""
    fires: list[dict[str, Any]] = []
    for fire in fires_data:
        fires.append(to_dict(fire_data=fire))
    return fires
