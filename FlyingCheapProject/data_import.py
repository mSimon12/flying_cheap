import requests
import json

AUTH_FILE = 'api-auth.json'


class FlightAPI(object):

    def __init__(self, api_name: str, auth_file: str = AUTH_FILE):
        self.api_name = api_name

        credentials = self.get_api_credentials(auth_file)
        self.api_url = credentials["base_url"]
        self.header = self.build_header(credentials["key"], credentials["host"])

    def get_api_credentials(self, filename) -> dict:
        with open(filename, 'r') as f:
            auth_data = json.load(f)
        credentials = auth_data[self.api_name]
        return credentials

    @staticmethod
    def build_header(key: str, host: str) -> dict:
        head = {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": host
        }
        return head


class SkyScanner(FlightAPI):
    def __init__(self):
        super().__init__("skyscanner")

    def search_one_way(self):
        querystring = {"fromId": "eyJzIjoiTEFYQSIsImUiOiIyNzUzNjIxMSIsImgiOiIyNzUzNjIxMSJ9=",
                       "toId": "eyJzIjoiTE9ORCIsImUiOiIyNzU0NDAwOCIsImgiOiIyNzU0NDAwOCJ9", "departDate": "2024-05-23",
                       "adults": "1", "currency": "USD", "market": "US", "locale": "en-US"}

        complete_url = self.api_url + '/search-one-way'

        try:
            search_res = requests.get(complete_url, headers=self.header, params=querystring)
            search_res.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            return

        print(search_res.status_code)
        print(search_res.headers)
        print(search_res.json())


def main():
    ss = SkyScanner()
    # ss.search_one_way()


if __name__ == '__main__':
    main()