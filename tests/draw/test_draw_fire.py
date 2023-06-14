import unittest
from unittest import mock

from california_fire.core.fire import Fire
from california_fire.draw.draw_fire import convert_lon_to_x_pixel, convert_lat_to_y_pixel, \
    draw_fire_map, Image, ImageDraw


class TestDrawFire(unittest.TestCase):
    def test_convert_lon_to_x_pixel(self):
        im_width = 1312
        longitude = -117.565833
        expected_result = 756.3840142775193

        x_pixel = convert_lon_to_x_pixel(image_width=im_width, longitude=longitude)
        self.assertEqual(expected_result, x_pixel)

    def test_convert_lat_to_y_pixel(self):
        im_height = 2022
        latitude = 34.293103
        expected_result = 1535.8636294001003

        y_pixel = convert_lat_to_y_pixel(image_height=im_height, latitude=latitude)
        self.assertEqual(expected_result, y_pixel)

    def test_draw_fire_map(self):
        output_path: str = "tests/draw/test_data/fire_map.png"
        base_image_path: str = "tests/draw/test_data/california_base_map.png"
        fires: list[Fire] = [Fire(location='East Blue Ridge and Paiute, south of Wrightwood',
                                  date_time='2023-04-26T10:16:00Z',
                                  acres_burned=150,
                                  latitude=34.293103,
                                  longitude=-117.565833,
                                  url='https://incidents.fire.ca.gov/incidents/2023/4/26/nob-fire/')]
        x: float = 756.3840142775193
        y: float = 1535.8636294001003

        with mock.patch('california_fire.draw.draw_fire.Image.open') as mock_open:
            mock_open.Image.convert.return_value = mock.MagicMock(spec=Image, size=(1672, 1280), mode='RGBA')
            with mock.patch('california_fire.draw.draw_fire.ImageDraw.Draw') as mock_draw:
                mock_draw.ellipse.return_value = mock.MagicMock(spec=ImageDraw)
                actual_result = draw_fire_map(base_image_path=base_image_path,
                                              output_path=output_path, fire_data=fires)

                mock_open.assert_called_once_with(base_image_path)
                mock_draw.assert_called_once()
                self.assertEqual(actual_result, output_path)


if __name__ == '__main__':
    unittest.main()
