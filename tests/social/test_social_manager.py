import unittest
from unittest import mock

from california_fire.core.fire import Fire
from california_fire.social.social_manager import social_manager


class TestSocialManager(unittest.TestCase):
    def test_social_manager(self):
        image_path = 'test_data/test_map.png'
        base_image_path = 'test_data/test_map.png'
        output_path = 'test_data/test_map.png'
        message = 'test message'
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=1,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]

        with mock.patch('california_fire.social.social_manager.create_map',
                        return_value=image_path) as mock_create_map, \
                mock.patch('california_fire.social.social_manager.compose_message',
                           return_value=message) as mock_compose_message, \
                mock.patch('california_fire.social.social_manager.send_new_toot') as mock_send_new_toot:

            social_manager(fires=fires, base_image_path=base_image_path, output_path=output_path)
            mock_create_map.assert_called_once_with(fires=fires, base_image_path=base_image_path,
                                                    output_path=output_path)
            mock_compose_message.assert_called_once_with(fires=fires)
            mock_send_new_toot.assert_called_once_with(message=message, image_path=image_path)


if __name__ == '__main__':
    unittest.main()
