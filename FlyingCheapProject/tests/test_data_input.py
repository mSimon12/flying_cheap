from unittest import main, TestCase
from data_input.generic_flight_api import FlightAPI


class TestFlightApi(TestCase):

    def setUp(self):
        self.test_auth_file = "api_auth_test.json"
        api_count = 3

        self.flight_api = []
        for api in range(0, api_count):
            self.flight_api.append(FlightAPI(f"api_name{api}", self.test_auth_file))

    def test_get_api_credentials(self):
        for api_idx in range(0, len(self.flight_api)):
            credentials = self.flight_api[api_idx].get_api_credentials(self.test_auth_file)
            self.assertEqual(credentials['base_url'], f"url{api_idx}")
            self.assertEqual(credentials['key'], f"key{api_idx}")
            self.assertEqual(credentials['host'], f"host{api_idx}")

    def test_build_header(self):
        header_model = {"X-RapidAPI-Key": "example_key123",
                        "X-RapidAPI-Host": "test_host.com"}

        self.assertEqual(header_model, self.flight_api[0].build_header("example_key123", "test_host.com"))


if __name__ == "__main__":
    main()
