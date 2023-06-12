import unittest
from unittest import mock

from california_fire.core.fire import Fire
from california_fire.core.network_manager import get_fire_data
from california_fire.storage.data_handler import read_json


class TestNetworkManager(unittest.TestCase):
    def test_network_manager(self):
        fires = read_json('test_data/get_fire_data.json')
        expected_fire = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
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
                              url='https://incidents.fire.ca.gov/incidents/2023/6/4/range-fire/')]

        with mock.patch('california_fire.core.network_manager.fetch_fires', return_value=fires) as mock_fetch_fires, \
                mock.patch('california_fire.core.network_manager.fire_encoder',
                           return_value=expected_fire) as mock_fire_encoder:
            result = get_fire_data()
            mock_fetch_fires.assert_called_once()
            mock_fire_encoder.assert_called_once_with(fire_data=fires)
            self.assertEqual(result, expected_fire)

    def test_empty_fire_data(self):
        fire = read_json('test_data/empty_fire_data.json')
        expected_fire = []
        with mock.patch('california_fire.core.network_manager.fetch_fires', return_value=fire) as mock_fetch_fires, \
                mock.patch('california_fire.core.network_manager.fire_encoder',
                           return_value=expected_fire) as mock_fire_encoder:
            result = get_fire_data()
            mock_fetch_fires.assert_called_once()
            mock_fire_encoder.assert_called_once_with(fire_data=fire)
            self.assertEqual(result, expected_fire)


if __name__ == '__main__':
    unittest.main()
