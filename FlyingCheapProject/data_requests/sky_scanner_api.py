import requests
from data_requests.generic_flight_api import FlightAPI
import pandas as pd

RELEVANT_ID_INFO = ["title", "subtitle", "entityType", "id", "entityId"]


class SkyScanner(FlightAPI):
    def __init__(self):
        super().__init__("skyscanner")
        self.backup_file = "backup_ids.csv"

    @staticmethod
    def get_config(country: str):
        df = pd.read_json("sky_scanner_config.json", orient="index")
        return df.loc[country].to_dict()

    def request_new_location_id(self, city: str, country_name: str):
        cfg = self.get_config(country_name)
        locale = cfg['locale']
        market = cfg['market']

        querystring = {"query": city, "market": market, "locale": locale}
        complete_url = self.api_url + '/flights/auto-complete'

        try:
            search_res = requests.get(complete_url, headers=self.header, params=querystring)
            search_res.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return

        return search_res.json()['data']

    def search_info_at_ids_backup(self, info: str):
        pass

    def save_id_info_to_backup(self, info) -> bool:
        try:
            backup_df = pd.read_csv(self.backup_file, index_col="skyId", dtype='str')
        except FileNotFoundError or pd.errors.EmptyDataError:
            backup_df = pd.DataFrame(columns=RELEVANT_ID_INFO)
            backup_df.index.name = "skyId"

        # Avoid saving duplicated info
        if "skyId" in info.columns:
            info.set_index("skyId", inplace=True)
        status = True
        for info_row in info.index:
            if info_row in backup_df.index.values:
                status = False
                continue

            backup_df = pd.concat([backup_df, info.loc[info_row, :].to_frame().T])
            try:
                backup_df.to_csv(self.backup_file, index_label="skyId")
            except Exception:
                status = False

        return status

    def extract_info_from_id_request_response(self, info_source: dict, desired_info: str) -> str:
        if desired_info in info_source:
            return info_source[desired_info]
        else:
            for info in info_source:
                if isinstance(info_source[info], dict):
                    extract_res = self.extract_info_from_id_request_response(info_source[info], desired_info)
                    if extract_res:
                        return extract_res
        return ''

    def filter_id_info_from_location_request(self, id_request_result):
        id_info = pd.DataFrame(columns=RELEVANT_ID_INFO)
        id_info.index.name = "skyId"

        for option in id_request_result:
            sky_id = self.extract_info_from_id_request_response(option, id_info.index.name)
            for info in RELEVANT_ID_INFO:
                id_info.loc[sky_id, info] = self.extract_info_from_id_request_response(option, info)

        return id_info

    def get_example_id_request_result(self):
        example_id = [{'id': 'eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9',
                       'presentation': {'title': 'Rio de Janeiro', 'suggestionTitle': 'Rio de Janeiro (qualquer)',
                                        'subtitle': 'Brasil'},
                       'navigation': {'entityId': '27541837', 'entityType': 'CITY', 'localizedName': 'Rio de Janeiro',
                                      'relevantFlightParams': {'skyId': 'RIOA', 'entityId': '27541837',
                                                               'flightPlaceType': 'CITY',
                                                               'localizedName': 'Rio de Janeiro'},
                                      'relevantHotelParams': {'entityId': '27541837', 'entityType': 'CITY',
                                                              'localizedName': 'Rio de Janeiro'}}},
                      {'id': 'eyJzIjoiR0lHIiwiZSI6Ijk1NjczMzQ3IiwiaCI6IjI3NTQxODM3In0=',
                       'presentation': {'title': 'Internacional do Rio de Janeiro/Galeão - Antonio C',
                                        'suggestionTitle': 'Internacional do Rio de Janeiro/Galeão - Antonio C (GIG)',
                                        'subtitle': 'Brasil'},
                       'navigation': {'entityId': '95673347', 'entityType': 'AIRPORT',
                                      'localizedName': 'Internacional do Rio de Janeiro/Galeão - Antonio C',
                                      'relevantFlightParams': {'skyId': 'GIG', 'entityId': '95673347',
                                                               'flightPlaceType': 'AIRPORT',
                                                               'localizedName': 'Internacional do Rio de Janeiro/Galeão - Antonio C'},
                                      'relevantHotelParams': {'entityId': '27541837', 'entityType': 'CITY',
                                                              'localizedName': 'Rio de Janeiro'}}},
                      {'id': 'eyJzIjoiU0RVIiwiZSI6Ijk1NjczMzQ2IiwiaCI6IjI3NTQxODM3In0=',
                       'presentation': {'title': 'Rio de Janeiro Santos Dumont',
                                        'suggestionTitle': 'Rio de Janeiro Santos Dumont (SDU)', 'subtitle': 'Brasil'},
                       'navigation': {'entityId': '95673346', 'entityType': 'AIRPORT',
                                      'localizedName': 'Rio de Janeiro Santos Dumont',
                                      'relevantFlightParams': {'skyId': 'SDU', 'entityId': '95673346',
                                                               'flightPlaceType': 'AIRPORT',
                                                               'localizedName': 'Rio de Janeiro Santos Dumont'},
                                      'relevantHotelParams': {'entityId': '27541837', 'entityType': 'CITY',
                                                              'localizedName': 'Rio de Janeiro'}}},
                      {'id': 'eyJzIjoiUlJKIiwiZSI6IjIxNjc2NjE2OSIsImgiOiIyNzU0MTgzNyJ9',
                       'presentation': {'title': 'Jacarepaguá', 'suggestionTitle': 'Jacarepaguá (RRJ)',
                                        'subtitle': 'Brasil'},
                       'navigation': {'entityId': '216766169', 'entityType': 'AIRPORT', 'localizedName': 'Jacarepaguá',
                                      'relevantFlightParams': {'skyId': 'RRJ', 'entityId': '216766169',
                                                               'flightPlaceType': 'AIRPORT',
                                                               'localizedName': 'Jacarepaguá'},
                                      'relevantHotelParams': {'entityId': '27541837', 'entityType': 'CITY',
                                                              'localizedName': 'Rio de Janeiro'}}}]

        return example_id

    def get_location_id(self, city: str, country_name: str):
        # TODO: create a cache with successful results
        #  and check cache before requesting id via API

        # Check if ID from city is on backup
        # if yes - get from it
        # else - request it and save result to bkp

        pass

    def search_one_way(self):
        querystring = {"fromId": "eyJzIjoiTEFYQSIsImUiOiIyNzUzNjIxMSIsImgiOiIyNzUzNjIxMSJ9=",
                       "toId": "eyJzIjoiTE9ORCIsImUiOiIyNzU0NDAwOCIsImgiOiIyNzU0NDAwOCJ9", "departDate": "2024-05-23",
                       "adults": "1", "currency": "USD", "market": "US", "locale": "en-US"}

        complete_url = self.api_url + '/flights/search-one-way'

        try:
            search_res = requests.get(complete_url, headers=self.header, params=querystring)
            search_res.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return

        print(search_res.status_code)
        print(search_res.headers)
        print(search_res.json())

    def search(self):
        # Step 1: get search info (from, to, date, type of search [one_way, ...])
        # Step 2: check if already have ids
        # Step 3: get ids if not available
        # Step 4: save new ids
        # Step 5: do the search call
        pass


if __name__ == "__main__":
    ss = SkyScanner()
    ss.set_credentials_from_file()
    id_res = ss.get_example_id_request_result()
    res = ss.filter_id_info_from_location_request(id_res)
    print(res)

    for option in id_res:
        # print(f"ID: {option['id']})
        for info in option:
            print(f"{info} => {option[info]}")
        print()
