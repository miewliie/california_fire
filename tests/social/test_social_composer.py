import unittest
from unittest import mock

from california_fire.core.fire import Fire
from california_fire.social.social_composer import create_map, compose_message


class TestSocialComposer(unittest.TestCase):
    def test_create_map(self):
        base_img_path = 'assets/california_base_map.png'
        output_path = 'outputs/california_fire_map.png'
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=1,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'),
                             Fire(location='Ave 66 and Hwy 86',
                                  date_time='2023-05-15T12:10:00Z',
                                  acres_burned=127.0,
                                  latitude=33.569342,
                                  longitude=-116.092746,
                                  url='https://incidents.fire.ca.gov/incidents/2023/5/15/66-fire/')]

        with mock.patch('california_fire.social.social_composer.draw_fire_map') as mock_draw_map:
            mock_draw_map.return_value = output_path
            image_path = create_map(fires=fires, base_image_path=base_img_path, output_path=output_path)
            mock_draw_map.assert_called_once_with(fire_data=fires, base_image_path=base_img_path,
                                                  output_path=output_path)
            self.assertEqual(image_path, output_path)

    def test_compose_message_with_one_fire(self):
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=1,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]
        expected_msg = '📍East Blue Ridge and Paiute, south of Wrightwood\n' \
                       '⏰2023-04-26 10:16🔥1 acres\n' \
                       '#california #californiawildfire #californiafire'

        with mock.patch('california_fire.social.social_composer.compose_message',
                        return_value=expected_msg):
            message = compose_message(fires=fires)
            self.assertEqual(message, expected_msg)

    def test_compose_message_with_multiple_fires(self):
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=1,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'),
                             Fire(location='Ave 66 and Hwy 86',
                                  date_time='2023-05-15T12:10:00Z',
                                  acres_burned=127.0,
                                  latitude=33.569342,
                                  longitude=-116.092746,
                                  url='https://incidents.fire.ca.gov/incidents/2023/5/15/66-fire/')]
        expected_msg = '📍East Blue Ridge and Paiute, south of Wrightwood\n' \
                       '⏰2023-04-26 10:16🔥1 acres\n' \
                       '📍Ave 66 and Hwy 86\n' \
                       '⏰2023-05-15 12:10🔥127.0 acres\n' \
                       '#california #californiawildfire #californiafire'
        with mock.patch('california_fire.social.social_composer.compose_message',
                        return_value=expected_msg):
            message = compose_message(fires=fires)
            self.assertEqual(message, expected_msg)

    def test_compose_message_with_zero_acres_burned(self):
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=None,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]
        expected_msg = '📍East Blue Ridge and Paiute, south of Wrightwood\n' \
                       '⏰2023-04-26 10:16🔥0 acre\n' \
                       '#california #californiawildfire #californiafire'

        with mock.patch('california_fire.social.social_composer.compose_message',
                        return_value=expected_msg):
            message = compose_message(fires=fires)
            self.assertEqual(message, expected_msg)


if __name__ == '__main__':
    unittest.main()
