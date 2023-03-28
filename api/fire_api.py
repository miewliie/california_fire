import requests
import os
import datetime
import json

URL = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?"
STATUS = 'false'
YEAR = datetime.datetime.now().year


def request_fire():
    print('Year: ', YEAR)
    response = requests.get(URL + 'inactive=' + STATUS + '&year=' + str(YEAR))
    json_data = response.json()
    return json_data


def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file)
        print("Done write response into json file")


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as output_file:
        size = os.path.getsize(file_path)
        if size > 0:
            data = json.loads(output_file.read())
        else:
            data = None
        return data


def get_dup_fire_data(new_fire_data, prev):
    prev_data = read_json(prev)
    new_data = new_fire_data

    dup_index_list = []
    if prev_data:
        for i in range(len(new_data)):
            item = new_data[i]
            for j in prev_data:
                if item['UniqueId'] == j['UniqueId']:
                    dup_index_list.insert(0, i)
                    break
        return dup_index_list
    else:
        return dup_index_list


def save_latest_fire_data(new_json_data, prev):
    write_json(new_json_data, prev)


def prepare_ready_to_use_data(dup_index_list, new_fire_data, fire_json_output):
    new_data = new_fire_data

    if not dup_index_list == []:
        for i in range(len(dup_index_list)):
            del new_data[dup_index_list[i]]
        write_json(new_data, fire_json_output)
    else:
        write_json(new_data, fire_json_output)


if __name__ == '__main__':
    prev_json_path = '../outputs/previous_fire_data.json'
    fire_json_path = '../outputs/fire.json'

    fire_data = request_fire()
    if fire_data:
        dup_list = get_dup_fire_data(fire_data, prev_json_path)
        save_latest_fire_data(fire_data, prev_json_path)
        prepare_ready_to_use_data(dup_list, fire_data, fire_json_path)
