import json
import os
from mastodon import Mastodon
from draw.draw_fire import draw_fire_points
from fire.fire import get_fire_title, read_json_output


USER = os.getenv('MASTODON_EMAIL')
PASSWORD = os.getenv('MASTODON_PASSWORD')
MASTODON_SERVER = os.getenv('MASTODON_SERVER')


def connect_to_mastodon():
    """ Create a connection to your server. And provide account credential. """

    Mastodon.create_app(
        'pytooterapp',
        api_base_url=MASTODON_SERVER,
        to_file='pytooter_clientcred.secret'
    )

    mastodon = Mastodon(client_id='pytooter_clientcred.secret',)
    mastodon.log_in(
        USER,
        PASSWORD)
    return mastodon


def send_new_status_for(earthquake_title: str, earthquake_map_path: str):
    """ Post fire status and fire recent map. """

    mastodon = connect_to_mastodon()

    image_id = mastodon.media_post(earthquake_map_path)
    post_dict = mastodon.status_post(
        earthquake_title, in_reply_to_id=None, media_ids=image_id)
    print("post id: ", post_dict.id)


if __name__ == '__main__':

    image_path = "./assets/california_base_map.png"
    output_path = "./outputs/california_fire_map.png"

    fire_data = read_json_output()
    draw_fire_points(image_path, output_path, fire_data)
    fire_info = get_fire_title()
    send_new_status_for(fire_info, output_path)
