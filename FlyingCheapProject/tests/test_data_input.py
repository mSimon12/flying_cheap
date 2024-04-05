from unittest import main, TestCase
from data_input.generic_flight_api import FlightAPI


class TestFlightApi(TestCase):

    def setUp(self):
        self.test_auth_file = "api_auth_test.json"
        self.flight_api = FlightAPI("api", self.test_auth_file)

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

        flight_api = FlightAPI("api", self.test_auth_file)
        self.assertIsNone(flight_api.api_url, "URL should be initialized as None!")
        self.assertIsNone(flight_api.header, "Header should be initialized as None!")

        for case in use_cases:
            credentials = flight_api.load_credentials(case, self.test_auth_file)
            res = self.flight_api.set_credentials(credentials)
            self.assertFalse(res, "Should return False for missing credentials!")

        self.assertIsNone(flight_api.api_url, "URL should be still be None if not all info is given!")
        self.assertIsNone(flight_api.header, "Header should be still be None if not all info is given!")


if __name__ == "__main__":
    main()
