import requests
import datetime

URL = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?"
STATUS = 'false'
YEAR = datetime.datetime.now().year
TIMEOUT = 10 # seconds


def fetch_fires():
    print('Year: ', YEAR)
    try:
        response = requests.get(URL + 'inactive=' + STATUS + '&year=' + str(YEAR))
    except requests.exceptions.Timeout:
        print(f"Requests timed out after {TIMEOUT} seconds")
        
    json_data = response.json()
    return json_data



