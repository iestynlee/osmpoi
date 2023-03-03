import unittest
from unittest.mock import patch, ANY
from osmpoi import pois
import requests
import json


class TestPOIs(unittest.TestCase):

    @patch('requests.get')
    def test_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError
        result = pois.collect("-3.5399,50.7342,-3.4890,50.7150")
        self.assertIsNone(result)

    @patch('requests.get')
    @patch('json.loads')
    def test_json_decode_error(self, mock_get, mock_loads):
        mock_loads.side_effect = json.decoder.JSONDecodeError('Expecting value: ', '{}', 0)
        result = pois.collect("-3.5399,50.7342,-3.4890,50.7150")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
