import requests
from generic_flight_api import FlightAPI
from pandas import read_json


class SkyScanner(FlightAPI):
    def __init__(self):
        super().__init__("skyscanner")
        credentials = self.load_credentials("skyscanner")
        self.set_credentials(credentials)

    @staticmethod
    def get_config(country: str):
        df = read_json("sky_scanner_config.json", orient="index")
        return df.loc[country].to_dict()

    def get_exemple_id_request_result(self):
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
                                      'relevantHotelParams': {'entityId': '27541837', 'entityType': 'CITY', 'localizedName': 'Rio de Janeiro'}}},
                      {'id': 'eyJzIjoiU0RVIiwiZSI6Ijk1NjczMzQ2IiwiaCI6IjI3NTQxODM3In0=',
                       'presentation': {'title': 'Rio de Janeiro Santos Dumont', 'suggestionTitle': 'Rio de Janeiro Santos Dumont (SDU)', 'subtitle': 'Brasil'},
                       'navigation': {'entityId': '95673346', 'entityType': 'AIRPORT',
                                      'localizedName': 'Rio de Janeiro Santos Dumont',
                                      'relevantFlightParams': {'skyId': 'SDU', 'entityId': '95673346', 'flightPlaceType': 'AIRPORT',
                                                               'localizedName': 'Rio de Janeiro Santos Dumont'},
                                      'relevantHotelParams': {'entityId': '27541837', 'entityType': 'CITY',
                                                              'localizedName': 'Rio de Janeiro'}}},
                      {'id': 'eyJzIjoiUlJKIiwiZSI6IjIxNjc2NjE2OSIsImgiOiIyNzU0MTgzNyJ9',
                       'presentation': {'title': 'Jacarepaguá', 'suggestionTitle': 'Jacarepaguá (RRJ)', 'subtitle': 'Brasil'},
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
        cfg = self.get_config(country_name)
        print(cfg)
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


if __name__ == "__main__":
    ss = SkyScanner()
    id_res = ss.get_exemple_id_request_result()

    for option in id_res:
        # print(f"ID: {option['id']})
        for info in option:
            print(f"{info} => {option[info]}")
        print()
