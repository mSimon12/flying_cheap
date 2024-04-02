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


if __name__ == '__main__':
    pass