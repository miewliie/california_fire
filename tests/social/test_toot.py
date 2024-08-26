import unittest
from unittest import mock
from unittest.mock import MagicMock

from california_fire.social.toot import send_new_toot, Mastodon


class TestToot(unittest.TestCase):
    def test_toot(self):
        status: str = '📍East Blue Ridge and Paiute, south of Wrightwood\n' \
                       '⏰2023-04-26 10:16🔥1 acres\n' \
                       '#california #californiawildfire #californiafire'
        image_path: str = 'output/map.png'
        expected_response: str = 'https://mastodon.social/@california_fire/106079404732732845'
        reply = []
        mastodon_mock = MagicMock(spec=Mastodon)
        mastodon_mock.media_post.return_value = {'id': '1234'}
        with mock.patch('california_fire.social.toot.send_new_toot',
                        return_value=expected_response), \
                mock.patch('california_fire.social.toot.Mastodon',
                           return_value=mastodon_mock) as mock_mastodon:
            send_new_toot(message=status, replies=reply, image_path=image_path)
            mock_mastodon.assert_called_once()
            mastodon_mock.media_post.assert_called_once_with(media_file=image_path)
            mastodon_mock.status_post.assert_called_once_with(status=status,
                                                              in_reply_to_id=None,
                                                              media_ids={'id': '1234'}
                                                              )
            
    def test_toot_reply(self):
        status: str = '📍East Blue Ridge and Paiute, south of Wrightwood\n' \
                       '⏰2023-04-26 10:16🔥1 acres\n' \
                       '#california #californiawildfire #californiafire'
        image_path: str = 'output/map.png'
        expected_response: str = 'https://mastodon.social/@california_fire/106079404732732845'
        reply: list = ['📍1This is reply, south of Wrightwood\n' \
                       '⏰2023-04-26 10:16🔥1 acres\n']
        mastodon_mock = MagicMock(spec=Mastodon)
        mastodon_mock.media_post.return_value = {'id': '1234'}
        with mock.patch('california_fire.social.toot.send_new_toot',
                        return_value=expected_response), \
                mock.patch('california_fire.social.toot.Mastodon',
                           return_value=mastodon_mock) as mock_mastodon:
            send_new_toot(message=status, replies=reply, image_path=image_path)
            mock_mastodon.assert_called_once()
            mastodon_mock.media_post.assert_called_once_with(media_file=image_path)
            first_post_response = mastodon_mock.status_post(status=status, in_reply_to_id=None, media_ids={'id': '1234'})
            mastodon_mock.status_post.assert_has_calls([
                mock.call(status=reply[0], in_reply_to_id=first_post_response.id),
            ])


if __name__ == '__main__':
    unittest.main()