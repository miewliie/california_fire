import unittest
import json
from typing import Any
from unittest import mock

from california_fire.storage.data_handler import Fire, from_dict_to_fire, fire_encoder, write_json, to_dict, \
    fire_decoder
from california_fire.storage.data_handler import read_json


class TestDataHandler(unittest.TestCase):
    def test_read_json_output_json_if_content_exist(self):
        input_value: str = repr([{'key': 'value'}])
        expected_value: str = repr([{'key': 'value'}])
        file_path: str = 'tests/storage/test_data/read_json.json'

        mock_file = mock.mock_open(read_data=json.dumps(input_value))
        with mock.patch('california_fire.storage.data_handler.open', mock_file) as mock_open:
            actual_value = read_json(file_path=file_path)
            mock_open.assert_called_once_with(file_path, 'r', encoding='utf-8')
            self.assertEqual(expected_value, actual_value)

    def test_read_json_output_none_if_no_content(self):
        input_value = 'Any content'
        expected_value = None
        file_path: str = 'tests/storage/test_data/read_json.json'

        mock_file = mock.mock_open(read_data=json.dumps(input_value))
        with mock.patch('california_fire.storage.data_handler.open', mock_file) as mock_open, \
                mock.patch('california_fire.storage.data_handler.os.path.getsize', return_value=0) as mock_getsize:
            actual_value = read_json(file_path=file_path)
            mock_getsize.assert_called_once_with(file_path)
            mock_open.assert_called_once_with(file_path, 'r', encoding='utf-8')
            self.assertEqual(expected_value, actual_value)

    def test_write_json(self):
        fires = [{'key': 'value'}]
        file_path = 'tests/storage/test_data/write_json.json'
        mock_file = mock.mock_open(read_data=json.dumps(fires))
        with mock.patch('california_fire.storage.data_handler.open', mock_file) as mock_open, \
                mock.patch('california_fire.storage.data_handler.json.dump') as mock_dump:
            write_json(data=fires, file_path=file_path)
            mock_open.assert_called_once_with(file_path, 'w', encoding='utf-8')
            mock_dump.assert_called_once_with(fires, mock_open.return_value)

    def test_fire_encoder(self):
        input_value: list[dict[str, Any]] = [{
            'Location': 'Location',
            'Started': '2023-04-26T10:16:00Z',
            'AcresBurned': 120,
            'Latitude': 34.293103,
            'Longitude': -117.565833,
            'Url': 'Url'
        }]
        expected_value = [Fire(
            location='Location',
            date_time='2023-04-26T10:16:00Z',
            acres_burned=120,
            latitude=34.293103,
            longitude=-117.565833,
            url='Url'
        )]
        with mock.patch('california_fire.storage.data_handler.from_dict_to_fire') as mock_from_dict_to_fire:
            mock_from_dict_to_fire.return_value = expected_value[0]
            actual_value = fire_encoder(input_value)
            self.assertEqual(expected_value, actual_value)

    def test_from_dict_to_fire(self):
        input_value: list[dict[str, Any]] = [{
            'Location': 'Location',
            'Started': '2023-04-26T10:16:00Z',
            'AcresBurned': 120,
            'Latitude': 34.293103,
            'Longitude': -117.565833,
            'Url': 'Url'
        }]
        expected_value = Fire(
            location='Location',
            date_time='2023-04-26T10:16:00Z',
            acres_burned=120,
            latitude=34.293103,
            longitude=-117.565833,
            url='Url'
        )
        with mock.patch('california_fire.storage.data_handler.Fire') as mock_fire:
            mock_fire.return_value = expected_value
            actual_value = from_dict_to_fire(dict_data=input_value[0])
            self.assertEqual(expected_value, actual_value)

    def test_fire_to_dict(self):
        new_fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                      date_time='2023-04-26T10:16:00Z',
                                      acres_burned=10,
                                      latitude=34.293103,
                                      longitude=-117.565833,
                                      url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]
        expected_value: dict[str, Any] = {'Location': 'East Blue Ridge and Paiute, south of Wrightwood',
                                          'Started': '2023-04-26T10:16:00Z',
                                          'AcresBurned': 10,
                                          'Latitude': 34.293103,
                                          'Longitude': -117.565833,
                                          'Url': 'https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'}
        with mock.patch('california_fire.storage.data_handler.to_dict') as mock_to_dict:
            mock_to_dict.return_value = expected_value
            actual_value = to_dict(new_fires[0])
            self.assertEqual(expected_value, actual_value)

    def test_fire_decoder(self):
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=1,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'),
                             Fire(location='San Vicente Road, north of Soledad',
                                  date_time='2023-06-04T17:38:50Z',
                                  acres_burned=72.0,
                                  latitude=36.4647,
                                  longitude=-121.3319,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]
        fires_dict: list[dict[str, Any]] = [{'Location': 'East Blue Ridge and Paiute, south of Wrightwood',
                                             'Started': '2023-04-26T10:16:00Z',
                                             'AcresBurned': 1,
                                             'Latitude': 34.293103,
                                             'Longitude': -117.565833,
                                             'Url': 'https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'},
                                            {
                                                'Location': 'San Vicente Road, north of Soledad',
                                                'Started': '2023-06-04T17:38:50Z',
                                                'AcresBurned': 72.0,
                                                'Latitude': 36.4647,
                                                'Longitude': -121.3319,
                                                'Url': 'https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/'
                                            }]
        actual_value = fire_decoder(fires)
        self.assertEqual(fires_dict, actual_value)


if __name__ == '__main__':
    unittest.main()
