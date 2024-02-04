import requests
import pandas as pd 
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(Path("/my/path/.env"))

EIA_API_KEY = os.getenv("EIA_API_KEY")

api_url = "https://api.eia.gov/v2/densified-biomass/wood-pellet-plants/data/?frequency=annual&data[0]=capacity&facets[stateId][]=AL&facets[stateId][]=AR&facets[stateId][]=AZ&facets[stateId][]=CA&facets[stateId][]=GA&facets[stateId][]=IA&facets[stateId][]=ID&facets[stateId][]=IN&facets[stateId][]=LA&facets[stateId][]=MI&facets[stateId][]=MO&facets[stateId][]=NC&facets[stateId][]=OR&facets[stateId][]=PA&facets[stateId][]=SC&facets[stateId][]=TN&facets[stateId][]=VA&facets[stateId][]=VT&facets[stateId][]=WI&start=2016&end=2023&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key=6tNRsQQ0cL9HRwdFjKD0nbFV34c2QyzJkwjI5krD"

headers = {
    "X-Params":
    '{"frequency": "annual", "data": ["capacity"], "facets": {"stateId": ["AL","AR","AZ","CA","GA","IA","ID","IN","LA","MI","MO","NC","OR","PA","SC","TN","VA","VT","WI"]}, "start": "2016", "end": "2023", "sort": [{"column": "period", "direction": "desc"}], "offset": 0, "length": 5000}',
    "Authorization": f"Bearer {EIA_API_KEY}"
}

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    print(response.json())
    biomass_data = response.json()
    df = pd.json_normalize(biomass_data, sep='')
    df.to_csv('biomass_data.csv', index=False)

    # data = response.json()
    # df = pd.DataFrame(data)
    # df.to_csv('biomass_data.csv', index=False)
    # # print(df)
    # print(df.head())

    # biomass_data = response.json()

    # biomass_csv_file = "biomass_data.csv"

    # with open(biomass_csv_file, mode='w', newline='') as biomas_data:
    #     writer = csv.writer(biomas_data)

    #     writer.writerow(biomass_data['series'][0]['data'][0].keys())

    #     for entry in biomass_data['series'][0]['data']:
    #         writer.writerow(entry.values())
