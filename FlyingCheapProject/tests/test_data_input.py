from unittest import main, TestCase
from data_input.generic_flight_api import FlightAPI
from data_input.sky_scanner_api import SkyScanner


class TestFlightApi(TestCase):

    def setUp(self):
        self.test_auth_file = "api_auth_test.json"
        self.flight_api = FlightAPI("api")

    # Load credentials test
    def test_load_credentials(self):
        credentials = self.flight_api.load_credentials("api_valid_credentials", self.test_auth_file)
        self.assertEqual(credentials['base_url'], "https://valid.url.com/test")
        self.assertEqual(credentials['key'], "val1dk3y")
        self.assertEqual(credentials['host'], "apihost.valid.com")

    # Build Header tests
    def test_build_header_valid_parameters(self):
        header_model = {"X-RapidAPI-Key": "examplekey123",
                        "X-RapidAPI-Host": "test_host.com"}
        new_header = self.flight_api.build_header("examplekey123", "test_host.com")
        self.assertEqual(header_model, new_header, "Fail building Header!")

    def test_build_header_invalid_parameters(self):
        header = self.flight_api.build_header(111, "test_host.com")
        self.assertIsNone(header, "Header with invalid key params should return None!")
        header = self.flight_api.build_header(True, "test_host.com")
        self.assertIsNone(header, "Header with invalid key params should return None!")
        header = self.flight_api.build_header("example_key123", 15.6)
        self.assertIsNone(header, "Header with invalid host param should return None!")
        header = self.flight_api.build_header("example_key123", False)
        self.assertIsNone(header, "Header with invalid host param should return None!")

    # Set Credentials test
    def test_set_credentials_valid_info(self):
        header_model = {"X-RapidAPI-Key": "val1dk3y",
                        "X-RapidAPI-Host": "apihost.valid.com"}

        credentials = self.flight_api.load_credentials("api_valid_credentials", self.test_auth_file)
        res = self.flight_api.set_credentials(credentials)

        self.assertTrue(res, "Should return True for valid credentials!")
        self.assertEqual("https://valid.url.com/test", self.flight_api.api_url, "Fail parsing URL!")
        self.assertEqual(header_model, self.flight_api.header, "Fail parsing Header!")

    def test_set_credentials_invalid_info(self):
        self.flight_api.api_url = None
        self.flight_api.header = None

        credentials = self.flight_api.load_credentials("api_invalid_credentials", self.test_auth_file)
        res = self.flight_api.set_credentials(credentials)

        self.assertFalse(res, "Should return False for invalid credentials!")
        self.assertIsNone(self.flight_api.api_url, "URL should not be changed if some info is invalid!")
        self.assertIsNone(self.flight_api.header, "Header should not be changed if some info is invalid!")

    def test_set_credentials_missing_info(self):
        use_cases = ["api_missing_url", "api_missing_key", "api_missing_host"]

        flight_api = FlightAPI("api")
        self.assertIsNone(flight_api.api_url, "URL should be initialized as None!")
        self.assertIsNone(flight_api.header, "Header should be initialized as None!")

        for case in use_cases:
            credentials = flight_api.load_credentials(case, self.test_auth_file)
            res = self.flight_api.set_credentials(credentials)
            self.assertFalse(res, "Should return False for missing credentials!")

        self.assertIsNone(flight_api.api_url, "URL should be still be None if not all info is given!")
        self.assertIsNone(flight_api.header, "Header should be still be None if not all info is given!")


class TestSkyScannerApi(TestCase):

    def setUp(self):
        self.sky_scanner_flight_api = SkyScanner()
        self.sky_scanner_flight_api.set_credentials_from_file("api_auth_test.json")

        self.raw_info = {'id': 'eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9',
                       'presentation': {'title': 'Rio de Janeiro', 'suggestionTitle': 'Rio de Janeiro (qualquer)',
                                        'subtitle': 'Brasil'},
                       'navigation': {'entityId': '27541837', 'entityType': 'CITY', 'localizedName': 'Rio de Janeiro',
                                      'relevantFlightParams': {'skyId': 'RIOA', 'entityId': '27541837',
                                                               'flightPlaceType': 'CITY',
                                                               'localizedName': 'Rio de Janeiro'},
                                      'relevantHotelParams': {'entityId': '27541837', 'entityType': 'CITY',
                                                              'localizedName': 'Rio de Janeiro'}}}

    def test_extract_valid_info(self):
        info_level_1 = 'id'
        filtered_info = self.sky_scanner_flight_api.extract_info(self.raw_info, info_level_1)
        self.assertIsNotNone(filtered_info, f"'{info_level_1}' should be a valid info!")
        self.assertEqual(filtered_info, 'eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9',
                         'Info does not match with info in raw data!')

        info_level_2 = 'entityType'
        filtered_info = self.sky_scanner_flight_api.extract_info(self.raw_info, info_level_2)
        self.assertIsNotNone(filtered_info, f"'{info_level_2}' should be a valid info!")
        self.assertEqual(filtered_info, 'CITY', 'Info does not match with info in raw data!')

        info_level_3 = 'skyId'
        filtered_info = self.sky_scanner_flight_api.extract_info(self.raw_info, info_level_3)
        self.assertIsNotNone(filtered_info, f"'{info_level_3}' should be a valid info!")
        self.assertEqual(filtered_info, 'RIOA', 'Info does not match with info in raw data!')

    def test_extract_invalid_info(self):
        invalid_info = 'myId'
        filtered_info = self.sky_scanner_flight_api.extract_info(self.raw_info, invalid_info)
        self.assertIsNone(filtered_info, f"'{invalid_info}' should not be a valid info!")


if __name__ == "__main__":
    main()
