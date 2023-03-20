import requests
import json

# URL = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?inactive=true&year=2022"
URL = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?"
STATUS = 'true'
YEAR = '2022'


def request_fire():
    response = requests.get(URL + 'inactive=' + STATUS + '&year=' + YEAR)
    json_data = response.json()
    return json_data


def write_response(data):
    with open('../outputs/fire.json', 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file)
        print("Done write response into json file")


if __name__ == '__main__':
    fire_data = request_fire()
    write_response(fire_data)
