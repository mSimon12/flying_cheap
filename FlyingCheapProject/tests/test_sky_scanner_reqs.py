from unittest import main, TestCase
from data_requests.sky_scanner_api import SkyScanner


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
        self.assertNotEqual(filtered_info, '', f"'{info_level_1}' should be a valid info!")
        self.assertEqual(filtered_info, 'eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9',
                         'Info does not match with info in raw data!')

        info_level_2 = 'entityType'
        filtered_info = self.sky_scanner_flight_api.extract_info(self.raw_info, info_level_2)
        self.assertNotEqual(filtered_info, '', f"'{info_level_2}' should be a valid info!")
        self.assertEqual(filtered_info, 'CITY', 'Info does not match with info in raw data!')

        info_level_3 = 'skyId'
        filtered_info = self.sky_scanner_flight_api.extract_info(self.raw_info, info_level_3)
        self.assertNotEqual(filtered_info, '', f"'{info_level_3}' should be a valid info!")
        self.assertEqual(filtered_info, 'RIOA', 'Info does not match with info in raw data!')

    def test_extract_invalid_info(self):
        invalid_info = 'myId'
        filtered_info = self.sky_scanner_flight_api.extract_info(self.raw_info, invalid_info)
        self.assertEqual(filtered_info, '', f"'{invalid_info}' should not be a valid info!")

    def test_search_info_at_ids_backup(self):
        # input: search name

        #
        # search value
        pass

    def test_save_id_info_to_empty_backup(self):
        # input: dict or Series
        # save it to file
        # check if info is on file
        # delete file
        pass

    def test_save_id_info_to_existing_backup(self):
        # create file
        # input: dict or Series
        # save it to file
        # check if info is on file
        # delete file
        pass

    def test_filter_id_request_info(self):
        # input: result from id_request
        # return: filtered info

        # Check if data is correctly extracted from fake id_response with multiple options
        pass


if __name__ == "__main__":
    main()
