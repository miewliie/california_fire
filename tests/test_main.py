import unittest
from unittest import mock

from california_fire.core.fire import Fire
from main import main


class TestMain(unittest.TestCase):
    def test_main_with_no_new_fire(self):
        old_path = 'outputs/old_fire.json'

        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=1,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')] * 2
        with mock.patch('main.network_manager.get_fire_data', return_value=fires) as mock_get_fire_data, \
                mock.patch('main.storage_manager.read_fire_data', return_value=fires) as mock_read_fire_data, \
                mock.patch('main.storage_manager.write_fire_data') as mock_write_fire_data, \
                mock.patch('main.social_manager') as mock_social_manager:
            main()
            mock_get_fire_data.assert_called_once()
            mock_read_fire_data.assert_called_once_with(old_fire_path=old_path)
            mock_write_fire_data.assert_called_once_with(new_fire_data=fires, old_path=old_path)
            mock_social_manager.assert_not_called()

    def test_main_with_no_fire_from_api(self):
        fires: list[Fire] = None
        with mock.patch('main.network_manager.get_fire_data', return_value=fires) as mock_get_fire_data, \
                mock.patch('main.storage_manager.read_fire_data') as mock_read_fire_data, \
                mock.patch('main.storage_manager.write_fire_data') as mock_write_fire_data, \
                mock.patch('main.social_manager') as mock_social_manager:
            main()
            mock_get_fire_data.assert_called_once()
            mock_read_fire_data.assert_not_called()
            mock_write_fire_data.assert_not_called()
            mock_social_manager.assert_not_called()

    def test_main_with_new_fire(self):
        old_path = 'outputs/old_fire.json'

        new_fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                      date_time='2023-04-26T10:16:00Z',
                                      acres_burned=1,
                                      latitude=34.293103,
                                      longitude=-117.565833,
                                      url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]

        old_fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                      date_time='2023-04-26T10:16:00Z',
                                      acres_burned=5,
                                      latitude=34.293103,
                                      longitude=-117.565833,
                                      url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]

        with mock.patch('main.network_manager.get_fire_data', return_value=new_fires) as mock_get_fire_data, \
                mock.patch('main.storage_manager.read_fire_data', return_value=old_fires) as mock_read_fire_data, \
                mock.patch('main.storage_manager.write_fire_data') as mock_write_fire_data, \
                mock.patch('main.social_manager') as mock_social_manager:
            main()
            mock_get_fire_data.assert_called_once()
            mock_read_fire_data.assert_called_once_with(old_fire_path=old_path)
            mock_write_fire_data.assert_called_once_with(new_fire_data=new_fires, old_path=old_path)
            mock_social_manager.assert_called_once_with(fires=new_fires)


if __name__ == '__main__':
    unittest.main()
