from california_fire.core.fire import Fire
from california_fire.social.social_composer import create_map, compose_message
from california_fire.social.toot import send_new_toot


def social_manager(fires: list[Fire], base_image_path: str, output_path: str):
    map_path: str = create_map(fires=fires, base_image_path=base_image_path, output_path=output_path)
    status_message: str = compose_message(fires=fires)
    send_new_toot(message=status_message, image_path=map_path)