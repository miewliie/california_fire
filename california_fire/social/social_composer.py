from datetime import datetime

from california_fire.core.fire import Fire
from california_fire.draw.draw_fire import draw_fire_map


def create_map(fires: list[Fire], base_image_path: str, output_path: str) -> str:
    """Create a map with markers for each fire. """
    map_path = draw_fire_map(fire_data=fires, base_image_path=base_image_path, output_path=output_path)
    return map_path


def compose_message(fires: list[Fire]) -> str:
    """Compose a message for the new fire. """
    messages: list[str] = []
    for fire in fires:
        dt = datetime.strptime(fire.date_time, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M')
        if fire.acres_burned:
            message = f"📍{fire.location}\n⏰{dt}🔥{fire.acres_burned} acres"
        else:
            message = f"📍{fire.location}\n⏰{dt}🔥0 acre"

        messages.append(message)

    messages.append("#california #californiawildfire #californiafire")
    return '\n'.join(messages)
