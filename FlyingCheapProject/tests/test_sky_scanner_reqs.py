from unittest import main, TestCase
from data_requests.sky_scanner_api import SkyScanner, RELEVANT_ID_INFO
import pandas as pd
import os


class TestSkyScannerApi(TestCase):

    def setUp(self):
        self.sky_scanner_flight_api = SkyScanner()
        self.sky_scanner_flight_api.set_credentials_from_file("api_auth_test.json")

        self.raw_location_id_response = {'id': 'eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9',
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

        test_info_dict = {'skyId': ['BRL'], 'id': ["ad51ads64das6asd654a"], 'title': ["Berlin"]}
        self.test_info = pd.DataFrame(test_info_dict)


    def test_search_existing_info_at_ids_backup(self):
        # input: search name
        filtered_data = self.sky_scanner_flight_api.filter_id_info_from_location_request(
            [self.raw_location_id_response])
        self.sky_scanner_flight_api.save_id_info_to_backup(filtered_data)
        city = 'Rio de Janeiro'
        country = 'Brasil'

        found, options = self.sky_scanner_flight_api.search_info_at_ids_backup(city, country)
        # option = {skyID:{'id': xxx, 'title': sss}}
        self.assertTrue(found, f"{city} ({country}) should be found on backup file!")
        self.assertTrue('RIOA' in options, f"RIOA should be a skyID present on backup file!")
        self.assertEqual('eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9', options['RIOA']['id'],
                         f"Wrong ID for {city} ({country})!")
        self.assertEqual('Rio de Janeiro',  options['RIOA']['title'], f"Wrong Title for {city} ({country})!")

    def test_extract_valid_info_from_id_request_response(self):
        """
            Test if VALID data is correctly extracted from raw data retrieved from http response.
            *Info on 3 different levels must be correctly extracted
        """
        info_level_1 = 'id'
        filtered_info = self.sky_scanner_flight_api.extract_info_from_id_request_response(self.raw_location_id_response, info_level_1)
        self.assertNotEqual(filtered_info, '', f"'{info_level_1}' should be a valid info!")
        self.assertEqual(filtered_info, 'eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9',
                         'Info does not match with info in raw data!')

        info_level_2 = 'entityType'
        filtered_info = self.sky_scanner_flight_api.extract_info_from_id_request_response(self.raw_location_id_response, info_level_2)
        self.assertNotEqual(filtered_info, '', f"'{info_level_2}' should be a valid info!")
        self.assertEqual(filtered_info, 'CITY', 'Info does not match with info in raw data!')

        info_level_3 = 'skyId'
        filtered_info = self.sky_scanner_flight_api.extract_info_from_id_request_response(self.raw_location_id_response, info_level_3)
        self.assertNotEqual(filtered_info, '', f"'{info_level_3}' should be a valid info!")
        self.assertEqual(filtered_info, 'RIOA', 'Info does not match with info in raw data!')

    def test_extract_invalid_info_from_id_request_response(self):
        """ Test if INVALID data is avoided at extraction """
        invalid_info = 'myId'
        filtered_info = self.sky_scanner_flight_api.extract_info_from_id_request_response(self.raw_location_id_response, invalid_info)
        self.assertEqual(filtered_info, '', f"'{invalid_info}' should not be a valid info!")

    def test_filter_id_request_info(self):
        # input: result from id_request
        # return: filtered info

        filtered_data = self.sky_scanner_flight_api.filter_id_info_from_location_request([self.raw_location_id_response])
        # print(filtered_data.loc['RIOA'])
        self.assertTrue('RIOA' in filtered_data.index, "SkyId=RIOA should be present in Indexes from result!")
        self.assertEqual('Rio de Janeiro', filtered_data.loc['RIOA', 'title'],
                         "title=Rio de Janeiro should be present on result!")
        self.assertEqual('Brasil', filtered_data.loc['RIOA', 'subtitle'],
                         "subtitle=Brasil should be present on result!")
        self.assertEqual('CITY', filtered_data.loc['RIOA', 'entityType'],
                         "entityType=CITY should be present on result!")
        self.assertEqual('eyJzIjoiUklPQSIsImUiOiIyNzU0MTgzNyIsImgiOiIyNzU0MTgzNyJ9', filtered_data.loc['RIOA', 'id'],
                         "id=eyJzIjoiUklP... should be present on result!")
        self.assertEqual('27541837', filtered_data.loc['RIOA', 'entityId'],
                         "entityId=27541837 should be present on result!")

    def test_saving_id_info_to_empty_backup(self):
        save_status = self.sky_scanner_flight_api.save_id_info_to_backup(self.test_info)

        file_exist = os.path.isfile(self.test_filename)
        self.assertTrue(file_exist, "Backup file should have been created!")

        saved_file = pd.read_csv(self.test_filename)

        for col in self.test_info.columns:
            value = self.test_info[col].values[0]
            self.assertTrue(col in saved_file.columns, f"Key {col} should be present in Columns!")
            self.assertTrue(value in saved_file.loc[:, col].values, f"Value {value} should be present in column {col}!")

        self.assertTrue(save_status, "Function should return true for saving the file!")

    def test_saving_id_info_to_existing_backup(self):
        info_df = pd.DataFrame(columns=RELEVANT_ID_INFO)
        info_df.to_csv(self.test_filename, index_label="skyId")

        save_status = self.sky_scanner_flight_api.save_id_info_to_backup(self.test_info)

        saved_file = pd.read_csv(self.test_filename)
        for col in self.test_info.columns:
            value = self.test_info[col].values[0]
            self.assertTrue(col in saved_file.columns, f"Key {col} should be present in Columns!")
            self.assertTrue(value in saved_file.loc[:, col].values, f"Value {value} should be present in column {col}!")

        self.assertTrue(save_status, "Function should return true for updating backup file!")

    def test_saving_duplicated_info_backup(self):
        # Duplicate info should not be saved, it should be filtered by the function and avoided

        for attempt in range(5):
            save_status = self.sky_scanner_flight_api.save_id_info_to_backup(self.test_info)
            saved_file = pd.read_csv(self.test_filename)
            if attempt > 0:
                self.assertEqual(1, len(saved_file), "Only One row should be added. All duplicates must be ignored!")
                self.assertFalse(save_status, "Function should return false if skyId info is duplicated!")

    def test_saving_multiple_duplicated_info_backup(self):
        # Duplicate info should not be saved, it should be filtered by the function and avoided

        self.test_info.loc[len(self.test_info)] = ['USA', "ad51ads64dsadsa", "United States"]

        for attempt in range(5):
            save_status = self.sky_scanner_flight_api.save_id_info_to_backup(self.test_info)
            saved_file = pd.read_csv(self.test_filename)
            if attempt > 0:
                self.assertEqual(len(self.test_info), len(saved_file), "All duplicates must be ignored!")
                self.assertFalse(save_status, "Function should return false if skyId info is duplicated!")

    def tearDown(self):
        # Clean file created
        if os.path.isfile(self.test_filename):
            os.remove(self.test_filename)

if __name__ == "__main__":
    main()
