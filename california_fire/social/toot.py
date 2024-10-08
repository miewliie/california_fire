import os
import logging
from mastodon import Mastodon


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
    mastodon.log_in(USER, PASSWORD)
    return mastodon


def send_new_toot(message: str, replies: list, image_path: str):
    """ Post fire status and fire recent map. """

    mastodon = connect_to_mastodon()

    image_id = mastodon.media_post(media_file=image_path)
    post_dict = mastodon.status_post(
        status=message, in_reply_to_id=None, media_ids=image_id)
    logging.info(f"Post ID: {post_dict.id}")
    if replies:
        for reply in replies:
            reply_dict = mastodon.status_post( status=reply, in_reply_to_id=post_dict.id)
            logging.info(f"Replies ID: {reply_dict.id}")