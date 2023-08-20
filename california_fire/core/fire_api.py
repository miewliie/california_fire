import logging
import requests
import datetime

URL = "https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?"
STATUS = 'false'
YEAR = datetime.datetime.now().year
TIMEOUT = 10 # seconds


def fetch_fires():
    logging.info(f'Fetching fires for year: {YEAR}')
    fire_url = f"{URL}inactive={STATUS}&year={YEAR}"
    
    try:
        response = requests.get(fire_url, timeout=TIMEOUT)
        return response.json()
    except requests.exceptions.Timeout:
        logging.critical("Fetch fires request timed out after {TIMEOUT} seconds (URL: {fire_url})")
        return []
