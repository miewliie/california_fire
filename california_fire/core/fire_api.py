import requests
import datetime

URL = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?"
STATUS = 'false'
YEAR = datetime.datetime.now().year


def fetch_fires():
    print('Year: ', YEAR)
    response = requests.get(URL + 'inactive=' + STATUS + '&year=' + str(YEAR))
    json_data = response.json()
    return json_data



