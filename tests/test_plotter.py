import unittest
from unittest.mock import patch, MagicMock
from osmpoi import plotter
import matplotlib.pyplot as plt


class TestPlotter(unittest.TestCase):
    @patch('matplotlib.pyplot.show')
    def test_plot(self, mock_show):
        # Data being used
        data = {"Area": "-3.539900,50.734200,-3.489000,50.715000", "Timestamp": "2023-02-28 15:39", "Sustenance": 22,
                "Education": 299, "Transportation": 31, "Financial": 13, "Healthcare": 62, "Entertainment": 15,
                "Public Services": 27, "Facilities": 16, "Waste Management": 0, "Other": 159, "Total": 644}

        # Expect xtick labels
        x = ['Sustenance', 'Education', 'Transportation', 'Financial', 'Healthcare', 'Entertainment', 'Public Services',
             'Facilities', 'Waste Management', 'Other']

        # Expect Labels
        title = 'Region Co-ordinates: ' + data['Area']
        xlabel = 'Points of Interest'
        ylabel = 'Quantity'

        # Plotting the data
        plotter.plot(data, percent=False)

        # Mock show of the data
        mock_show.assert_called_once()

        # Check x and y labels
        x_label = plt.gca().get_xlabel()
        y_label = plt.gca().get_ylabel()
        self.assertEqual(x_label, xlabel)
        self.assertEqual(y_label, ylabel)

        # Checks title are correct
        title_text = plt.gca().get_title()
        self.assertEqual(title_text, title)

        # Check xticks are right
        xticks = plt.gca().get_xticklabels()
        self.assertListEqual([label.get_text() for label in xticks], x)

    @patch('matplotlib.pyplot.show')
    def test_compare(self, mock_show):
        # Data being used for the test
        data = {"Area": "-3.539900,50.734200,-3.489000,50.715000", "Timestamp": "2023-02-28 15:39", "Sustenance": 22,
                "Education": 299, "Transportation": 31, "Financial": 13, "Healthcare": 62, "Entertainment": 15,
                "Public Services": 27, "Facilities": 16, "Waste Management": 0, "Other": 159, "Total": 644}

        data2 = {'Area': '-3.491100,50.822500,-3.465700,50.812900', 'Timestamp': "2023-02-28 15:39", 'Sustenance': 62,
                 'Education': 214,
                 'Transportation': 39, 'Financial': 19, 'Healthcare': 57, 'Entertainment': 9, 'Public Services': 28,
                 'Facilities': 18, 'Waste Management': 1, 'Other': 121, 'Total': 568}

        # Expected xtick labels
        x = ['Sustenance', 'Education', 'Transportation', 'Financial', 'Healthcare', 'Entertainment', 'Public Services',
             'Facilities', 'Waste Management', 'Other']

        # Expected Labels
        title = 'Comparison'
        xlabel = 'Points of Interest'
        ylabel = 'Quantity'
        legend_labels = ['-3.539900,50.734200,-3.489000,50.715000', '-3.491100,50.822500,-3.465700,50.812900']

        # Plotting the data
        plotter.compare(data, data2, percent=False)

        # Mock show of the data
        mock_show.assert_called_once()

        # Check x and y labels
        x_label = plt.gca().get_xlabel()
        y_label = plt.gca().get_ylabel()
        self.assertEqual(x_label, xlabel)
        self.assertEqual(y_label, ylabel)

        # Checks title are correct
        title_text = plt.gca().get_title()
        self.assertEqual(title_text, title)

        # Check xticks are right
        xticks = plt.gca().get_xticklabels()
        self.assertListEqual([label.get_text() for label in xticks], x)

        # Check the legends are right
        legends = plt.gca().get_legend()
        legend_result = [t.get_text() for t in legends.get_texts()]
        self.assertListEqual(legend_result, legend_labels)


if __name__ == '__main__':
    unittest.main()
