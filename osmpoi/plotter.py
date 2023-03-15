import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import copy
import numpy as np
from .retrieve import pois_percent


def plot(poi, percent=True):
    """Plots a bar graph of POIs in a region. Choice between a natural number bar graph or a percentage bar graph

    :param poi: Dictionary of POIs
    :type poi: dict
    :param percent: Determine if percent is added
    :type percent: bool
    :return: A bar graph
    """
    # Setting up variables for the graph
    poi_values = copy.copy(poi)
    poi_title = list(poi.values())[0]

    # Ensure the data doesn't have useless data for the x-axis
    poi_values = remove_keys(poi_values)

    # Setting the plotting values
    fig, ax = plt.subplots(figsize=(10, 6))  # Changing figure size
    plt.xlabel('Points of Interest', fontsize=18)
    plt.ylabel('Quantity', fontsize=18)
    ax.set_title('Region Co-ordinates: ' + poi_title, fontsize=20)

    # Setting percentages above bars
    if percent is True:
        lat_s, long_w, lat_n, long_e = coordinates(poi_title)  # Get co-ordinates for percentage
        poi_percent = pois_percent(lat_s, long_w, lat_n, long_e)  # Percentage call

        poi_percent = remove_keys(poi_percent)  # Get rid of values not needed

        poi_list = list(poi_percent.values())

        removed_percent = [float(percent[:-1]) for percent in poi_list]

        for key in poi_percent:
            poi_percent[key] = removed_percent.pop(0)

        bars = ax.bar(range(len(poi_percent)), list(poi_percent.values()), align='center', color='#1f77b4')
        ax.set_xticks(range(len(poi_percent)), list(poi_percent.keys()), rotation=90)

        # Adjust y limits
        y1 = list(poi_percent.values())
        plt.ylim(top=max(y1) * 1.2)

        # Loop to add values on top of bars
        for i, (key, value) in enumerate(poi_percent.items()):
            plt.text(i, bars[i].get_height() + 0.5, f"{value}%", ha='center', va='bottom', fontsize=10)

        # Formats graph into percentages
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    else:
        ax.set_xticks(range(len(poi_values)), list(poi_values.keys()), rotation=90)
        bars = ax.bar(range(len(poi_values)), list(poi_values.values()), align='center')

        # Loop to add values on top of bars
        for i, (key, value) in enumerate(poi_values.items()):
            plt.text(i, bars[i].get_height() + 0.5, value, ha='center', va='bottom', fontsize=10)

        # Adjust y limits
        y1 = list(poi_values.values())
        plt.ylim(top=max(y1) * 1.2)

    # Plotting the graph with the attributes of tight layout
    plt.show()


def compare(poi1, poi2, percent=True):
    """Comparison of two region using a bar graph. There is a choice between seeing a percentage bar graph or a natural
    number bar graph

    :param poi1: A dictionary of POIS
    :type poi1: dict
    :param poi2: A dictionary of POIS
    :type poi2: dict
    :param percent: A choice for percentages in the graph
    :type percent: bool
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
    poi_v1 = remove_keys(poi_v1)
    poi_v2 = remove_keys(poi_v2)

    # Setting up x-axis, doesn't matter which poi to choose as they both be same length
    x_axis = np.arange(len(poi_v1))
    fig, ax = plt.subplots(figsize=(10, 6))  # Changing figure size

    # Setting percentages above bars
    if percent is True:
        # Get co-ordinates for percentage
        lat_s1, long_w1, lat_n1, long_e1 = coordinates(t1)
        lat_s2, long_w2, lat_n2, long_e2 = coordinates(t2)

        # Percentage call
        poi_percent1 = pois_percent(lat_s1, long_w1, lat_n1, long_e1)
        poi_percent2 = pois_percent(lat_s2, long_w2, lat_n2, long_e2)

        # Get rid of values not needed
        poi_v1 = remove_keys(poi_percent1)
        poi_v2 = remove_keys(poi_percent2)

        # Remove percentages and turn it into a float as the percentages were saved as strings
        poi_v1, poi_v2 = remove_percentages(poi_v1, poi_v2)

        # Formats graph into percentages
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    # Sets up the bars for each dictionary
    bars1 = ax.bar(x_axis - 0.2, list(poi_v1.values()), 0.4, color='red')
    bars2 = ax.bar(x_axis + 0.2, list(poi_v2.values()), 0.4, color='green')

    # The x-axis labels
    ax.set_xticks(range(len(poi_v1)), list(poi_v1.keys()), rotation=90)

    # Setting up the labels for the bars - Formatting
    colors = {t1: 'red', t2: 'green'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
    plt.legend(handles, labels, loc='upper right')
    plt.subplots_adjust(right=0.8)

    # Adjust y limits
    y1 = list(poi_v1.values())
    y2 = list(poi_v2.values())
    y1.extend(y2)
    plt.ylim(top=max(y1) * 1.2)

    # Title for the graph and then displaying the graph
    plt.xlabel('Points of Interest', fontsize=18)
    plt.ylabel('Quantity', fontsize=18)
    ax.set_title('Comparison', fontsize=20)

    # Needed this to be here as the bars need to be created before the data is called
    if percent is True:
        for i, (key, value) in enumerate(poi_v1.items()):
            getx = bars1[i].get_x()
            width = bars1[i].get_width()
            plt.text(getx + width / 2.0, bars1[i].get_height() + 0.5, f"{value}%", rotation=90, ha='center',
                     va='bottom',
                     fontsize=10)

        for i, (key, value) in enumerate(poi_v2.items()):
            getx = bars2[i].get_x()
            width = bars2[i].get_width()
            plt.text(getx + width / 2.0, bars2[i].get_height() + 0.5, f"{value}%", rotation=90, ha='center',
                     va='bottom',
                     fontsize=10)

    # This will add natural numbers on top of the bars
    else:
        for i, (key, value) in enumerate(poi_v1.items()):
            getx = bars1[i].get_x()
            width = bars1[i].get_width()
            plt.text(getx + width / 2.0, bars1[i].get_height() + 0.5, value, rotation=90, ha='center',
                     va='bottom',
                     fontsize=10)

        for i, (key, value) in enumerate(poi_v2.items()):
            getx = bars2[i].get_x()
            width = bars2[i].get_width()
            plt.text(getx + width / 2.0, bars2[i].get_height() + 0.5, value, rotation=90, ha='center',
                     va='bottom',
                     fontsize=10)

    # Plotting the graph
    plt.show()


def remove_keys(pois):
    """Removes the keys that are not necessary for graph

    :param pois: Dictionary of POIs
    :type pois: dict
    :return: Remove the keys in dictionary that are Area, Timestamp and Total
    """
    for key in list(pois.keys()):
        if key == 'Area':
            del pois[key]
        if key == 'Total':
            del pois[key]
        if key == 'Timestamp':
            del pois[key]

    return pois


def remove_percentages(poi1, poi2):
    poi_v1_list = list(poi1.values())
    poi_v2_list = list(poi2.values())

    removed_percent1 = [float(percent[:-1]) for percent in poi_v1_list]
    removed_percent2 = [float(percent[:-1]) for percent in poi_v2_list]

    for key in poi1:
        poi1[key] = removed_percent1.pop(0)

    for key in poi2:
        poi2[key] = removed_percent2.pop(0)

    return poi1, poi2


def coordinates(poi_title):
    """Gets the co-ordinates out of the poi title

    :param poi_title: Region code
    :type poi_title: str
    :return: lat_s, long_w, lat_n, long_e these are the co-ordinates
    """
    split = poi_title.split(",")
    lat_s = float(split[0])
    long_w = float(split[1])
    lat_n = float(split[2])
    long_e = float(split[3])

    return lat_s, long_w, lat_n, long_e
