import unittest
import json
from typing import Any
from unittest import mock

from california_fire.storage.data_handler import Fire, from_dict_to_fire, fire_encoder
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


if __name__ == '__main__':
    unittest.main()
