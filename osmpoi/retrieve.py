from .pois import *
from .downloader import *
import copy


def pois_bbox(min_long, min_lat, max_long, max_lat):
    """All the checks are passed through here to collect the final dictionary of the POIs of the region. It checks, file
    existence, expiry date and if it is downloaded. It will API call first if it doesn't exist and then download it.

    :param min_long: Minimum Longitude
    :type min_long: float
    :param min_lat: Minimum Latitude
    :type min_lat: float
    :param max_long: Maximum Longitude
    :type max_long: float
    :param max_lat: Maximum Latitude
    :type max_lat: float
    :return: A dictionary of the POIs
    """
    file_exist()  # Check if the file exists first
    area = concat(min_long, min_lat, max_long, max_lat)

    # Checks if region is in file
    in_file = loader(area)
    if in_file is not None:
        expiry = has_expired(in_file)  # Checks if it is a month-old data
        if expiry is False:
            return in_file  # Return the region data
        else:
            deleter(area)  # If it is old data, delete the data and replace it using api
            poi = collect(area)
            if poi is None:
                return
            else:
                download(poi)
                return poi
    else:
        # Collects the data by doing the api calls required
        poi = collect(area)
        if poi is None:
            return
        else:
            download(poi)
            return poi


def pois_percent(min_long, min_lat, max_long, max_lat):
    """Converts a dictionary of POIs values into percentage values.

    :param min_long: Minimum Longitude
    :type min_long: float
    :param min_lat: Minimum Latitude
    :type min_lat: float
    :param max_long: Maximum Longitude
    :type max_long: float
    :param max_lat: Maximum Latitude
    :type max_lat: float
    :return: A dictionary of POIs with the values being percentages
    """
    # Collecting the pois and copying the data
    dicts = pois_bbox(min_long, min_lat, max_long, max_lat)
    poi = copy.copy(dicts)

    # Getting the values that don't get affected by the percentage change
    total = poi['Total']
    area = poi['Area']
    times = poi['Timestamp']

    # Removing the values from the dictionary that don't need conversion
    for key in list(poi.keys()):
        if key == 'Area':
            del poi[key]
        if key == 'Total':
            del poi[key]
        if key == 'Timestamp':
            del poi[key]

    # Convert the values into strings and calculate the percentages
    for k, v in poi.items():
        poi[k] = str(round((v / total)*100, 2))

    # Add a percentage sign to these values
    for k, v in poi.items():
        poi[k] = v + '%'

    # Adding back Timestamp
    items = list(poi.items())
    items.insert(0, ('Timestamp', times))
    poi = dict(items)

    # Adding back Area code
    items = list(poi.items())
    items.insert(0, ('Area', area))
    poi = dict(items)

    # Adding total value
    poi['Total'] = total

    return poi
