import copy
import json
import os
from datetime import date
import numpy as np

# Filename of the data file used - hardcoded
filename = "data.json"


def concat(lat_s, long_w, lat_n, long_e):
    """Returns the concatenation of the coordinates into 1 string.

    :param lat_s: Latitude of Southern Edge
    :type lat_s: float
    :param long_w: Longitude of Western Edge
    :type long_w: float
    :param lat_n: Latitude of Northern Edge
    :type lat_n: float
    :param long_e: Longitude of Eastern Edge
    :type long_e: float
    :return: A string of these integers with 6 decimal places
    """
    return "{:.6f},{:.6f},{:.6f},{:.6f}".format(lat_s, long_w, lat_n, long_e)


def exists(filename):
    """Checks the existence of a filename.

    :param filename: This is the filename
    :type filename: str
    :return: It will return a bool of either True or False
    """
    return os.path.exists(filename)


def file_exist():
    """This is used to check if the file exists using the exists function.

    :return: It will either pass the function or create a file with a list inside
    """
    if exists(filename):
        pass
    else:
        # If not make a file with a list inside the file
        file = open(filename, 'w')
        json.dump([], file)
        file.close()


def download(poi):
    """Loads then appends to a current list of dictionaries then writes it to a file.

    :param poi: This is a dictionary of the POI
    :type poi: dict
    :return: Appends to file
    """
    # Loads up the file
    with open(filename, "r") as f:
        data = json.load(f)

    data.append(poi)  # Appends the data to the list of dictionaries

    # Writes appended data to the file
    with open(filename, "w") as f:
        json.dump(data, f)

    return data


def loader(poi):
    """Loads a file then checks if the areas of all downloaded data and finds if it one of the downloaded areas already
    exists.

    :param poi: String of the area bbox
    :type poi: str
    :return: One Area if it exists within the file
    """
    # Loads up file
    with open(filename) as file:
        data = json.load(file)

    d = copy.copy(data)  # Copying data to not interfere with downloading and deleting

    # Finding if the area in the file is the one being searched for
    for i in range(len(d)):
        result = d[i]['Area']
        if result == str(poi):
            return d[i]


def has_expired(data):
    """Checks the current date of the data then if it is 1 month old then replace the data as it needs to be up-to-date.

    :param data: This is the dictionary of the POI
    :type data: dict
    :return: True or False if it is more than 1 month old
    """
    timestamp = data['Timestamp']  # Collects timestamp from loaded data

    # Gets only the year and month
    file_date = timestamp[0:7]
    file_date = np.datetime64(file_date)

    # Collecting today's year and month
    today = date.today()
    today = today.strftime("%Y-%m")
    today = np.datetime64(today)

    # Calculating the amount of months between today's date and in file date
    duration = today - file_date

    # Returns True if the more than 1 month old data to make sure it's up-to-date
    if duration > 0:
        return True
    else:
        return False


def deleter(poi):
    """Deletes data in the file using the Area code, used for updating information in the file.

    :param poi: String of POI
    :type poi: str
    :return: Deletes a record
    """
    # Loads file
    with open(filename) as file:
        data = json.load(file)

    # Getting size of list in file
    size = len(data)

    # Looks for the area searched for based on the expiry date
    for i in range(size):
        result = data[i]['Area']
        if result == str(poi):
            del data[i]  # Deletes the desired file
            break  # IndexError will come up if not break

    # Write it to file
    with open(filename, 'w') as file:
        json.dump(data, file)

    return data


def manual_delete(lat_s, long_w, lat_n, long_e):
    """Manually delete records in the system

    :param lat_s: Latitude of Southern Edge
    :type lat_s: float
    :param long_w: Longitude of Western Edge
    :type long_w: float
    :param lat_n: Latitude of Northern Edge
    :type lat_n: float
    :param long_e: Longitude of Eastern Edge
    :type long_e: float
    :return: Deleted record
    """
    area = concat(lat_s, long_w, lat_n, long_e)
    loaded = loader(area)
    if loaded is not None:
        deleter(loaded)
