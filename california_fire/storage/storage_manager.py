from california_fire.core.fire import Fire
from california_fire.storage import data_handler


def read_fire_data(old_fire_path) -> list[Fire]:
    """Reads the fire data from the file path and returns a list of Fire objects."""
    previous_fires = data_handler.read_json(file_path=old_fire_path)
    return data_handler.fire_encoder(fire_data=previous_fires)


def write_fire_data(new_fire_data, old_path):
    """Writes the new fire data to the file path."""
    fire_json = data_handler.fire_decoder(fires_data=new_fire_data)
    data_handler.write_json(data=fire_json, file_path=old_path)
