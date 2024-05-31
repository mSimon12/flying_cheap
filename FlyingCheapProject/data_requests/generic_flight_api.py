import requests
import json

AUTH_FILE = 'api-auth.json'


class FlightAPI(object):

    def __init__(self, api_name: str):
        self.api_name = api_name
        self.header = None
        self.api_url = None

    @staticmethod
    def load_credentials(api_name: str, filename: str) -> dict:
        with open(filename, 'r') as file:
            auth_data = json.load(file)
        credentials = auth_data[api_name]
        return credentials

    @staticmethod
    def build_header(key: str, host: str) -> dict:
        if isinstance(key, str) and isinstance(host, str):
            head = {
                "X-RapidAPI-Key": key,
                "X-RapidAPI-Host": host
            }
            return head
        return None

    def set_credentials(self, credentials: dict) -> bool:
        required_info = ['base_url', 'key', 'host']
        required_info.sort()
        credentials_keys = list(credentials.keys())
        credentials_keys.sort()

        # Check for all info present
        if required_info != credentials_keys:
            return False

        # Check values types
        for info in credentials:
            if not isinstance(credentials[info], str):
                return False

        self.api_url = credentials["base_url"]
        self.header = self.build_header(credentials["key"], credentials["host"])
        return True

    def set_credentials_from_file(self, filename: str = AUTH_FILE) -> bool:
        credentials = self.load_credentials(self.api_name, filename)
        return self.set_credentials(credentials)
