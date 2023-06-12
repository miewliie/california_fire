import unittest
from unittest import mock

from california_fire.core.fire_api import fetch_fires


class TestAPI(unittest.TestCase):
    def test_api(self):
        expected_result = {'key': 'value'}
        with mock.patch('california_fire.core.fire_api.requests.get') as mock_get:
            mock_get.return_value.json.return_value = expected_result
            result = fetch_fires()
            mock_get.assert_called_once()
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()