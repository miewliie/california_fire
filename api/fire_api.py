import requests
import datetime
from utilities.json_util import read_json, write_json

URL = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?"
STATUS = 'false'
YEAR = datetime.datetime.now().year


def request_fire():
    print('Year: ', YEAR)
    response = requests.get(URL + 'inactive=' + STATUS + '&year=' + str(YEAR))
    json_data = response.json()
    return json_data


def get_dup_fire_data(new_fire_data, prev):
    """ This function will return the index of the duplicate data.
    By comparing the UniqueId of the previous and latest response. """

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
    """ Save the all latest response into previous json file. """
    write_json(new_json_data, prev)


def prepare_ready_to_use_data(dup_index_list, new_fire_data, fire_json_output):
    """ Use duplication index list to remove the duplicate data out from latest response. """

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
