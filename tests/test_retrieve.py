import unittest
from osmpoi import retrieve
from unittest.mock import ANY, patch, mock_open
import json


class TestRetrieve(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_bbox(self, mock_file):
        expected_output = {"Area": "-3.491100,50.822500,-3.465700,50.812900", "Timestamp": ANY, "Sustenance": 62,
                           "Education": 214, "Transportation": 39, "Financial": 19, "Healthcare": 57,
                           "Entertainment": 9, "Public Services": 28, "Facilities": 18, "Waste Management": 1,
                           "Other": 121, "Total": 568}
        result = retrieve.pois_bbox(-3.4911, 50.8225, -3.4657, 50.8129)
        self.assertEqual(expected_output, result)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_percent(self, mock_file):
        expected_output = {'Area': '-3.539900,50.734200,-3.489000,50.715000', 'Timestamp': ANY, 'Sustenance': '3.42%',
                           'Education': '46.43%', 'Transportation': '4.81%', 'Financial': '2.02%',
                           'Healthcare': '9.63%', 'Entertainment': '2.33%', 'Public Services': '4.19%',
                           'Facilities': '2.48%', 'Waste Management': '0.0%', 'Other': '24.69%', 'Total': 644}
        result = retrieve.pois_percent(-3.5399, 50.7342, -3.4890, 50.7150)
        self.assertEqual(expected_output, result)


if __name__ == '__main__':
    unittest.main()
