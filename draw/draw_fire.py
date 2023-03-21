from PIL import Image, ImageDraw

TOP = 43.009518
BOTTOM = 31.534156
LEFT = -130.409591
RIGHT = -108.131211


def convert_lon_to_x_pixel(image_width: float, longitude: float):
    range_of_x = RIGHT - LEFT
    norm_value = longitude - LEFT
    pct_of_x = norm_value / range_of_x
    xp = pct_of_x * image_width
    return xp


def convert_lat_to_y_pixel(image_height: float, latitude: float):
    range_of_y = TOP - BOTTOM
    norm_value = latitude - BOTTOM
    pct_of_y = norm_value / range_of_y
    yp = image_height - (pct_of_y * image_height)
    return yp


def draw_fire_points(image_path, output_path, fire_data):
    image = Image.open(image_path).convert('RGBA')
    im_width = image.size[0]
    im_height = image.size[1]
    draw = ImageDraw.Draw(image)

    for obj in fire_data:
        x_longitude = obj['Longitude']
        y_latitude = obj['Latitude']
        acres_burned = obj['AcresBurned']

        lon_x_pixel = convert_lon_to_x_pixel(im_width, x_longitude)
        lat_y_pixel = convert_lat_to_y_pixel(im_height, y_latitude)

        if not acres_burned:
            radius = 10
            outline_color = 'orange'
            outline_width = 5
        elif acres_burned <= 1000:
            radius = 20
            outline_color = 'orange'
            outline_width = 10
        elif acres_burned <= 10000:
            radius = 30
            outline_color = 'orange'
            outline_width = 15
        else:
            radius = 40
            outline_color = 'orange'
            outline_width = 20

        draw.ellipse((lon_x_pixel - radius, lat_y_pixel - radius, lon_x_pixel + radius, lat_y_pixel + radius),
                     fill='red', outline=outline_color, width=outline_width)

    image.save(output_path)
