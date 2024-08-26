import unittest
from unittest import mock

from california_fire.core.fire import Fire
from california_fire.social.social_composer import create_map, compose_message, compose_reply_message


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
        expected_msg: str = '📍East Blue Ridge and Paiute, south of Wrightwood\n' \
                            '⏰2023-04-26 10:16🔥1 acres\n' \
                            '#california #californiawildfire #californiafire'
        expected_reply = []
        with mock.patch('california_fire.social.social_composer.compose_message',
                        return_value=expected_msg):
            message, replies = compose_message(fires=fires)
            self.assertEqual(message, expected_msg)
            self.assertEqual(replies, expected_reply)

    def test_compose_message_with_multiple_fires(self):
        fires: list[Fire] = [Fire(location='1East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=1,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'),
                            Fire(location='2East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=2,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'),
                            Fire(location='3East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=3,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'),
                             Fire(location='Ave 66 and Hwy 86',
                                  date_time='2023-05-15T12:10:00Z',
                                  acres_burned=127.0,
                                  latitude=33.569342,
                                  longitude=-116.092746,
                                  url='https://incidents.fire.ca.gov/incidents/2023/5/15/66-fire/')]
        expected_msg: str = '📍1East Blue Ridge and Paiute, south of Wrightwood\n' \
                            '⏰2023-04-26 10:16🔥1 acres\n' \
                            '📍2East Blue Ridge and Paiute, south of Wrightwood\n' \
                            '⏰2023-04-26 10:16🔥2 acres\n' \
                            '📍3East Blue Ridge and Paiute, south of Wrightwood\n' \
                            '⏰2023-04-26 10:16🔥3 acres\n' \
                            '👉 More fire on reply...\n' \
                            '#california #californiawildfire #californiafire'
                            
        expected_reply: list = ['📍Ave 66 and Hwy 86\n' \
                            '⏰2023-05-15 12:10🔥127.0 acres'] 

        with mock.patch('california_fire.social.social_composer.compose_message',
                        return_value=expected_msg):
            message, replies = compose_message(fires=fires)
            self.assertEqual(message, expected_msg)
            self.assertEqual(replies, expected_reply)

    def test_compose_message_with_zero_acres_burned(self):
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=None,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]
        expected_msg: str = '📍East Blue Ridge and Paiute, south of Wrightwood\n' \
                            '⏰2023-04-26 10:16🔥0 acre\n' \
                            '#california #californiawildfire #californiafire'
        expected_reply = []

        with mock.patch('california_fire.social.social_composer.compose_message',
                        return_value=expected_msg):
            message, replies = compose_message(fires=fires)
            self.assertEqual(message, expected_msg)
            self.assertEqual(replies, expected_reply)

    def test_compose_reply_message(self):
        replies: list[str] = ['📍South of Orleans\n' \
                            '⏰2024-08-09 11:25🔥12893.0 acres', \
                            '📍West of Homers Nose Grove, Sequoia National Park\n' \
                            '⏰2024-08-03 08:05🔥3123.0 acres', \
                            '📍Highway 101/Old Coast Highway, Las Cruces\n' \
                            '⏰2024-08-20 16:31🔥25.0 acres', \
                            '📍Big Tujunga Canyon Road, Tujunga\n' \
                            '⏰2024-08-21 17:25🔥15.1 acres'] \
                            
        expected_reply_list: list[str] = ['📍South of Orleans\n' \
                            '⏰2024-08-09 11:25🔥12893.0 acres\n' \
                            '📍West of Homers Nose Grove, Sequoia National Park\n' \
                            '⏰2024-08-03 08:05🔥3123.0 acres\n' \
                            '📍Highway 101/Old Coast Highway, Las Cruces\n' \
                            '⏰2024-08-20 16:31🔥25.0 acres', \
                            '📍Big Tujunga Canyon Road, Tujunga\n' \
                            '⏰2024-08-21 17:25🔥15.1 acres']
        
        with mock.patch('california_fire.social.social_composer.compose_reply_message',
                return_value=expected_reply_list):
            reply_list: list[str] = compose_reply_message(replies=replies)
            self.assertEqual(reply_list, expected_reply_list)


if __name__ == '__main__':

    unittest.main()
