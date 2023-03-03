import unittest
from osmpoi import downloader
from unittest.mock import patch, mock_open
from datetime import datetime
import numpy as np
import os
import json


class TestDownloader(unittest.TestCase):
    def test_has_expired(self):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M")

        test_data_today = {'Area': '-3.4911,50.8225,-3.4657,50.8129', 'Timestamp': today, 'Sustenance': 62,
                           'Education': 214, 'Transportation': 39, 'Financial': 19, 'Healthcare': 57,
                           'Entertainment': 9, 'Public Services': 28, 'Facilities': 18, 'Waste Management': 1,
                           'Other': 121, 'Total': 568}

        # Checks if it works for the current day and checking if it is not more than month old
        assert downloader.has_expired(test_data_today) is False

    def test_has_expired_difference(self):
        now = datetime.now()

        today_month = now.strftime("%Y-%m")
        today_split = now.strftime("-%d %H:%M")

        new_date = np.datetime64(today_month) + np.timedelta64(-2, 'M')
        new_date = str(new_date) + today_split

        test_month_difference = {'Area': '-3.4911,50.8225,-3.4657,50.8129', 'Timestamp': new_date,
                                 'Sustenance': 62,
                                 'Education': 214, 'Transportation': 39, 'Financial': 19, 'Healthcare': 57,
                                 'Entertainment': 9, 'Public Services': 28, 'Facilities': 18, 'Waste Management': 1,
                                 'Other': 121, 'Total': 568}

        # Month old check - This one is 2 month old data
        assert downloader.has_expired(test_month_difference) is True

    def test_concat(self):
        min_long, min_lat, max_long, max_lat = -3.5399, 50.7342, -3.4890, 50.7150

        expected_output = "-3.539900,50.734200,-3.489000,50.715000"

        assert downloader.concat(min_long, min_lat, max_long, max_lat) == expected_output

    @patch('os.path.exists')
    def test_exists_true(self, mock_exists):
        # Testing if a file exists, this uses same system in the downloader
        mock_exists.return_value = True
        filename = "data.json"
        self.assertTrue(os.path.exists(filename), f"File '{filename}' does not exist")

    @patch('builtins.open', new_callable=mock_open,
           read_data=json.dumps([{"Area": "-3.539900,50.734200,-3.489000,50.715000", "Timestamp": "2023-02-15 20:40",
                                  "Sustenance": 23, "Education": 300, "Transportation": 31, "Financial": 13,
                                  "Healthcare": 62, "Entertainment": 15, "Public Services": 27, "Facilities": 15,
                                  "Waste Management": 0, "Other": 160, "Total": 646}]))
    def test_loader(self, mock_open):
        area = "-3.539900,50.734200,-3.489000,50.715000"
        expected_output = {"Area": "-3.539900,50.734200,-3.489000,50.715000", "Timestamp": "2023-02-15 20:40",
                           "Sustenance": 23, "Education": 300, "Transportation": 31, "Financial": 13, "Healthcare": 62,
                           "Entertainment": 15, "Public Services": 27, "Facilities": 15, "Waste Management": 0,
                           "Other": 160, "Total": 646}
        result = downloader.loader(area)

        self.assertEqual(expected_output, result)


if __name__ == '__main__':
    unittest.main()
