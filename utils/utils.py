import re
import requests

def check_date(pub2agents_file):
    '''Function to check the date of the pub2agents file'''
    log_file = open(pub2agents_file, 'r', encoding="utf8")
    textfile = log_file.read()
    log_file.close()
    date = re.findall("--month (\d+)-(\d+)", textfile)

    return date[0]


def search_europe_pmc(query):
    """Search Europe PMC and return the JSON response."""
    api_endpoint = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        'query': query,
        'format': 'json',
        'resultType': 'core'
    }
    response = requests.get(api_endpoint, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None