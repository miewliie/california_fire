import unittest
from unittest import mock

from california_fire.core.fire import Fire
from california_fire.storage.storage_manager import read_fire_data, write_fire_data


class TestStorageManager(unittest.TestCase):
    def test_read_fire_data(self):
        test_path: str = 'test_path'
        test_json: str = 'test_json'
        test_fire: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                      date_time='2023-04-26T10:16:00Z',
                                      acres_burned=1,
                                      latitude=34.293103,
                                      longitude=-117.565833,
                                      url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')] * 2

        with mock.patch('california_fire.storage.storage_manager.data_handler.read_json',
                        return_value=test_json) as mock_read_json, \
                mock.patch('california_fire.storage.storage_manager.data_handler.fire_encoder',
                           return_value=test_fire) as mock_fire_decoder:
            result = read_fire_data(old_fire_path=test_path)
            mock_read_json.assert_called_once_with(file_path=test_path)
            mock_fire_decoder.assert_called_once_with(fire_data=test_json)
            self.assertEqual(result, test_fire)

    def test_write_fire_data(self):
        test_path: str = 'test_path'
        test_json: str = 'test_json'
        test_fire: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                      date_time='2023-04-26T10:16:00Z',
                                      acres_burned=1,
                                      latitude=34.293103,
                                      longitude=-117.565833,
                                      url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')] * 2

        with mock.patch('california_fire.storage.storage_manager.data_handler.fire_decoder',
                        return_value=test_json) as mock_fire_decoder, \
                mock.patch('california_fire.storage.storage_manager.data_handler.write_json') as mock_write_json:
            write_fire_data(new_fire_data=test_fire, old_path=test_path)
            mock_fire_decoder.assert_called_once_with(fires_data=test_fire)
            mock_write_json.assert_called_once_with(data=test_json, file_path=test_path)


if __name__ == '__main__':
    unittest.main()
