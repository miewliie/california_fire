from PIL import Image, ImageDraw

from california_fire.core.fire import Fire

TOP = 43.009518
BOTTOM = 31.534156
LEFT = -130.409591
RIGHT = -108.131211


def convert_lon_to_x_pixel(image_width: float, longitude: float) -> float:
    """Convert longitude to x pixel."""
    range_of_x: float = RIGHT - LEFT
    norm_value: float = longitude - LEFT
    pct_of_x: float = norm_value / range_of_x
    xp: float = pct_of_x * image_width
    return xp


def convert_lat_to_y_pixel(image_height: float, latitude: float) -> float:
    """Convert latitude to y pixel."""
    range_of_y: float = TOP - BOTTOM
    norm_value: float = latitude - BOTTOM
    pct_of_y: float = norm_value / range_of_y
    yp: float = image_height - (pct_of_y * image_height)
    return yp


def draw_fire_map(base_image_path: str, output_path: str, fire_data: list[Fire]) -> str:
    image: Image = Image.open(base_image_path).convert('RGBA')
    im_width: int = image.size[0]
    im_height: int = image.size[1]
    draw: ImageDraw = ImageDraw.Draw(image)

    for fire in fire_data:
        x_longitude: float = fire.longitude
        y_latitude: float = fire.latitude
        acres_burned: float | None = fire.acres_burned

        lon_x_pixel: float = convert_lon_to_x_pixel(im_width, x_longitude)
        lat_y_pixel: float = convert_lat_to_y_pixel(im_height, y_latitude)

        outline_color: str = 'orange'
        if not acres_burned:
            radius: int = 10
            outline_width: int = 5
        elif acres_burned <= 1000:
            radius: int = 20
            outline_width: int = 10
        elif acres_burned <= 10000:
            radius: int = 30
            outline_width: int = 15
        else:
            radius: int = 40
            outline_width: int = 20

        draw.ellipse((lon_x_pixel - radius, lat_y_pixel - radius,
                      lon_x_pixel + radius, lat_y_pixel + radius),
                     fill='red', outline=outline_color, width=outline_width)

    image.save(output_path)
    return output_path
