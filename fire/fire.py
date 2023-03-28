import os
import json
import datetime


def read_json_output():
    file_path = './outputs/fire.json'
    with open(file_path, "r", encoding="utf-8") as output_file:
        size = os.path.getsize(file_path)
        if size > 0:
            data = json.loads(output_file.read())
        else:
            data = None
        return data


def get_fire_title():
    fire_data = read_json_output()
    titles = []

    for obj in fire_data:
        temp_obj = []
        temp_loc = []
        started_dt = obj['Started']
        old_dt_format = datetime.datetime.strptime(started_dt, "%Y-%m-%dT%H:%M:%SZ")
        date_time = old_dt_format.strftime('%Y-%m-%d %H:%M')
        location = obj['Location']
        acres_burned = obj['AcresBurned']

        if acres_burned:
            temp_loc.append("📍")
            temp_loc.append(location)
            temp_obj.append("⏰")
            temp_obj.append(str(date_time))
            temp_obj.append("🔥")
            temp_obj.append(str(acres_burned))
            temp_obj.append("Acres")
        else:
            temp_loc.append("📍")
            temp_loc.append(location)
            temp_obj.append("⏰")
            temp_obj.append(str(date_time))
            temp_obj.append("🔥")
            temp_obj.append('0')
            temp_obj.append("Acre")
        str_loc = ' '.join(temp_loc)
        str_title = ' '.join(temp_obj)
        titles.append(str_loc)
        titles.append(str_title)

    if len(titles) > 0:
        titles.append("#california #californiawildfire #californiafire")
        title = '\n'.join(titles)
        print(title)
        return title
    else:
        title = titles
    return title
