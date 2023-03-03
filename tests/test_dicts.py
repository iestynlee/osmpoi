from osmpoi import dicts
from unittest.mock import ANY
import unittest


class TestDicts(unittest.TestCase):
    def test_process(self):
        # Test Area with the same region as the overpass api
        test_area = '-3.4911,50.8225,-3.4657,50.8129'

        # The output request from overpass api when inputted as url
        test_api_output = {'version': 0.6, 'generator': 'Overpass API 0.7.59.2 0994154d', 'osm3s': {'timestamp_osm_base': '2023-02-20T16:49:38Z', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.'}, 'elements': [{'type': 'count', 'id': 0, 'tags': {'nodes': '62', 'ways': '0', 'relations': '0', 'total': '62'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '214', 'ways': '0', 'relations': '0', 'total': '214'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '39', 'ways': '0', 'relations': '0', 'total': '39'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '19', 'ways': '0', 'relations': '0', 'total': '19'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '57', 'ways': '0', 'relations': '0', 'total': '57'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '9', 'ways': '0', 'relations': '0', 'total': '9'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '28', 'ways': '0', 'relations': '0', 'total': '28'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '18', 'ways': '0', 'relations': '0', 'total': '18'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '1', 'ways': '0', 'relations': '0', 'total': '1'}}, {'type': 'count', 'id': 0, 'tags': {'nodes': '121', 'ways': '0', 'relations': '0', 'total': '121'}}]}

        # Expected output when processed
        expected_processed_output = {'Area': '-3.4911,50.8225,-3.4657,50.8129', 'Timestamp': ANY, 'Sustenance': 62, 'Education': 214, 'Transportation': 39, 'Financial': 19, 'Healthcare': 57, 'Entertainment': 9, 'Public Services': 28, 'Facilities': 18, 'Waste Management': 1, 'Other': 121, 'Total': 568}

        # Checking if it is correct when using the process function
        assert dicts.process(test_area, test_api_output) == expected_processed_output


if __name__ == '__main__':
    unittest.main()
