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
    replies: list[str] = []
    reply_list: list[str] = []
    i = 0
    for fire in fires:
        dt = datetime.strptime(fire.date_time, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M')
        if fire.acres_burned:
            message = f"📍{fire.location}\n⏰{dt}🔥{fire.acres_burned} acres"
        else:
            message = f"📍{fire.location}\n⏰{dt}🔥0 acre"
        if i < 3:
            messages.append(message)
            i+=1
        else:
            replies.append(message)

    if replies: 
        messages.append("👉 More fire on reply...") 
        reply_list: list = compose_reply_message(replies=replies)
    messages.append("#california #californiawildfire #californiafire")
    post: list[str] = '\n'.join(messages)

    return post, reply_list

def compose_reply_message(replies: list[str]) -> list[str]:
    """Compose reply(s) for the new fire"""
    reply_list = []
    compose_replies = []
    for reply in replies:
        if len(compose_replies) == 3: 
            reply_set = '\n'.join(compose_replies)
            reply_list.append(reply_set)
            compose_replies = []
        
        compose_replies.append(reply)

    if compose_replies:
        reply_set = '\n'.join(compose_replies)
        reply_list.append(reply_set)

    return reply_list
