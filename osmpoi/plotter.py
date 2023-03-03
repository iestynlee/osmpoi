import matplotlib.pyplot as plt
import copy
import numpy as np


def plot(poi):
    """Plots a bar graph of POIs in a region.

    :param poi: Dictionary of POIs
    :type poi: dict
    :return: A bar graph
    """
    # Setting up variables for the graph
    poi_values = copy.copy(poi)
    poi_title = list(poi.values())[0]

    # Ensure the data doesn't have useless data for the x-axis
    for key in list(poi_values.keys()):
        if key == 'Area':
            del poi_values[key]
        if key == 'Total':
            del poi_values[key]
        if key == 'Timestamp':
            del poi_values[key]

    # Setting the plotting values
    fig, ax = plt.subplots()
    plt.xlabel('Points of Interest', fontsize=18)
    plt.ylabel('Quantity', fontsize=18)
    ax.bar(range(len(poi_values)), list(poi_values.values()), align='center')
    ax.set_xticks(range(len(poi_values)), list(poi_values.keys()), rotation=90)
    ax.set_title('Region Co-ordinates: ' + poi_title, fontsize=20)

    # Plotting the graph with the attributes of tight layout
    plt.tight_layout()
    plt.show()


def compare(poi1, poi2):
    """Comparison of two region using a bar graph.

    :param poi1: A dictionary of POIS
    :type poi1: dict
    :param poi2: A dictionary of POIS
    :type poi2: dict
    :return: A bar graph with two legends and multiple bars for two regions
    """
    # Setting up variables for the graph
    # Copy of data
    poi_v1 = copy.copy(poi1)
    poi_v2 = copy.copy(poi2)

    # The region labels
    t1 = list(poi_v1.values())[0]
    t2 = list(poi_v2.values())[0]

    # Get rid of data in both dictionaries that won't be used in the graph
    for key in list(poi_v1.keys()):
        if key == 'Area':
            del poi_v1[key]
        if key == 'Total':
            del poi_v1[key]
        if key == 'Timestamp':
            del poi_v1[key]

    for key in list(poi_v2.keys()):
        if key == 'Area':
            del poi_v2[key]
        if key == 'Total':
            del poi_v2[key]
        if key == 'Timestamp':
            del poi_v2[key]

    # Setting up x-axis, doesn't matter which poi to choose as they both be same length
    x_axis = np.arange(len(poi_v1))
    fig, ax = plt.subplots()

    # Sets up the bars for each dictionary
    ax.bar(x_axis - 0.2, list(poi_v1.values()), 0.4, color='red')
    ax.bar(x_axis + 0.2, list(poi_v2.values()), 0.4, color='green')

    # The x-axis labels
    ax.set_xticks(range(len(poi_v1)), list(poi_v1.keys()), rotation=90)

    # Setting up the labels for the bars
    colors = {t1: 'red', t2: 'green'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
    plt.legend(handles, labels)

    # Title for the graph and then displaying the graph
    plt.xlabel('Points of Interest', fontsize=18)
    plt.ylabel('Quantity', fontsize=18)
    ax.set_title('Comparison', fontsize=20)

    # Plotting the graph with the attributes of tight layout and maximising the window
    plt.tight_layout()
    plt.show()
