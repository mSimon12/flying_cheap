from unittest import main, TestCase
from data_requests.sky_scanner_api import SkyScanner, RELEVANT_ID_INFO
import pandas as pd
import os


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
        self.test_filename = "test_backup_file.csv"
        self.sky_scanner_flight_api.backup_file = self.test_filename

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
        # All the values that accepted info should be correctly saved in the backup file
        test_info_dict = {'skyId': ['BRL'],
                                 'id': ["ad51ads64das6asd654a"],
                                 'title': ["Berlin"]}
        test_info = pd.DataFrame(test_info_dict)
        save_status = self.sky_scanner_flight_api.save_id_info_to_backup(test_info)

        file_exist = os.path.isfile(self.test_filename)
        self.assertTrue(file_exist, "Backup file should have been created!")

        saved_file = pd.read_csv(self.test_filename)
        for col, value in test_info_dict.items():
            self.assertTrue(col in saved_file.columns, f"Key {col} should be present in Columns!")
            self.assertTrue(value in saved_file.loc[:, col].values, f"Value {value} should be present in column {col}!")

        self.assertTrue(save_status, "Function should return true for saving the file!")

    def test_save_id_info_to_existing_backup(self):
        info_df = pd.DataFrame(columns=RELEVANT_ID_INFO)
        info_df.to_csv(self.test_filename, index_label="skyId")

        test_info_dict = {'skyId': ['BRL'],
                          'id': ["ad51ads64das6asd654a"],
                          'title': ["Berlin"]}
        test_info = pd.DataFrame(test_info_dict)
        save_status = self.sky_scanner_flight_api.save_id_info_to_backup(test_info)

        saved_file = pd.read_csv(self.test_filename)
        for col, value in test_info_dict.items():
            self.assertTrue(col in saved_file.columns, f"Key {col} should be present in Columns!")
            self.assertTrue(value in saved_file.loc[:, col].values, f"Value {value} should be present in column {col}!")

        self.assertTrue(save_status, "Function should return true for updating backup file!")

    def test_save_duplicated_info_backup(self):
        # Duplicate info should not be saved, it should be filtered by the function and avoided
        test_info_dict = {'skyId': ['BRL'],
                          'id': ["ad51ads64das6asd654a"],
                          'title': ["Berlin"]}
        test_info = pd.DataFrame(test_info_dict)

        for attempt in range(5):
            save_status = self.sky_scanner_flight_api.save_id_info_to_backup(test_info)
            saved_file = pd.read_csv(self.test_filename)
            if attempt > 0:
                self.assertEqual(1, len(saved_file), "Only One row should be added. All duplicates must be ignored!")
                self.assertFalse(save_status, "Function should return false if skyId info is duplicated!")

    def test_save_multiple_duplicated_info_backup(self):
        # Duplicate info should not be saved, it should be filtered by the function and avoided
        test_info_dict = {'skyId': ['BRL', 'USA'],
                          'id': ["ad51ads64das6asd654a", "ad51ads64dsadsa"],
                          'title': ["Berlin", "United States"]}
        test_info = pd.DataFrame(test_info_dict)

        for attempt in range(5):
            save_status = self.sky_scanner_flight_api.save_id_info_to_backup(test_info)
            saved_file = pd.read_csv(self.test_filename)
            if attempt > 0:
                self.assertEqual(len(test_info_dict["skyId"]), len(saved_file), "All duplicates must be ignored!")
                self.assertFalse(save_status, "Function should return false if skyId info is duplicated!")


    def test_filter_id_request_info(self):
        # input: result from id_request
        # return: filtered info

        # Check if data is correctly extracted from fake id_response with multiple options
        pass

    def tearDown(self):
        # Clean file created
        if os.path.isfile(self.test_filename):
            os.remove(self.test_filename)

if __name__ == "__main__":
    main()
