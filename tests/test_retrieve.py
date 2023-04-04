import unittest
from osmpoi import retrieve
from unittest.mock import ANY, patch, mock_open
import json


# These tests can break if OSM update their database with new POIs
class TestRetrieve(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_bbox(self, mock_file):
        expected_output = {"Area": "-3.491100,50.822500,-3.465700,50.812900", "Timestamp": ANY, "Sustenance": 102,
                           "Education": 325, "Transportation": 64, "Financial": 25, "Healthcare": 95,
                           "Entertainment": 23, "Public Services": 55, "Facilities": 23, "Waste Management": 1,
                           "Other": 255, "Total": 968}
        result = retrieve.pois_bbox(-3.4911, 50.8225, -3.4657, 50.8129)
        self.assertEqual(expected_output, result)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_percent(self, mock_file):
        expected_output = {'Area': '-3.539900,50.734200,-3.489000,50.715000', 'Timestamp': ANY, 'Sustenance': '3.24%',
                           'Education': '42.12%', 'Transportation': '4.59%', 'Financial': '1.26%',
                           'Healthcare': '11.43%', 'Entertainment': '1.53%', 'Public Services': '3.6%',
                           'Facilities': '1.71%', 'Waste Management': '0.0%', 'Other': '30.51%', 'Total': 1111}
        result = retrieve.pois_percent(-3.5399, 50.7342, -3.4890, 50.7150)
        self.assertEqual(expected_output, result)


if __name__ == '__main__':
    unittest.main()
