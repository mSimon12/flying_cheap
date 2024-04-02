import requests
from generic_flight_api import FlightAPI
from pandas import DataFrame, read_json


class SkyScanner(FlightAPI):
    def __init__(self):
        super().__init__("skyscanner")

    @staticmethod
    def get_config(country: str):
        df = read_json("sky_scanner_config.json", orient="index")
        return df.loc[country].to_dict()

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
    # ss.get_location_id("Rio de Janeiro", "Brazil")
