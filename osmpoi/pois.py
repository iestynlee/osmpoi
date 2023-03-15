# Imports required libraries
import requests
import json
from .api import api
from .dicts import process
import time
import logging

# This is the overpass url to do queries from - in api
overpass_url = api()


def collect(location):
    """This will make an API request for using a query to Overpass API. This query is split into 10 queries within a
    request. This is to get categories of the POIs and their totals. This is compiled into a dictionary at the end.

    :param location: This is a string of min long, min lat, max long, max lat for API request
    :type location: str

    :return: A dictionary of the POIs
    """
    # One query to stop issues with too many requests
    overpass_query = """
    [out:json][timeout:600];
    (
    node["amenity"~"cafe|bar|biergarten|fast_food|food_court|ice_cream|pub|restaurant"]({0});
    way["amenity"~"cafe|bar|biergarten|fast_food|food_court|ice_cream|pub|restaurant"]({0});
    relation["amenity"~"cafe|bar|biergarten|fast_food|food_court|ice_cream|pub|restaurant"]({0});
    );
    out count;
    (
    node["amenity"~"college|driving_school|kindergarden|language_school|library|toy_library|training|music_school|school|university"]({0});
    way["amenity"~"college|driving_school|kindergarden|language_school|library|toy_library|training|music_school|school|university"]({0});
    relation["amenity"~"college|driving_school|kindergarden|language_school|library|toy_library|training|music_school|school|university"]({0});
    );
    out count;
    (
    node["amenity"~"bicycle_parking|bicycle_repair_station|bicycle_rental|boat_rental|boat_sharing|bus_station|car_rental|car_sharing|car_wash|compressed_air|vehicle_inspection|charging_station|ferry_terminal|fuel|grit_bin|motorcycle_parking|parking|parking_entrance|parking_space|taxi"]({0});
    way["amenity"~"bicycle_parking|bicycle_repair_station|bicycle_rental|boat_rental|boat_sharing|bus_station|car_rental|car_sharing|car_wash|compressed_air|vehicle_inspection|charging_station|ferry_terminal|fuel|grit_bin|motorcycle_parking|parking|parking_entrance|parking_space|taxi"]({0});
    relation["amenity"~"bicycle_parking|bicycle_repair_station|bicycle_rental|boat_rental|boat_sharing|bus_station|car_rental|car_sharing|car_wash|compressed_air|vehicle_inspection|charging_station|ferry_terminal|fuel|grit_bin|motorcycle_parking|parking|parking_entrance|parking_space|taxi"]({0});
    );
    out count;
    (
    node["amenity"~"atm|bank|bureau_de_change"]({0});
    way["amenity"~"atm|bank|bureau_de_change"]({0});
    relation["amenity"~"atm|bank|bureau_de_change"]({0});
    );
    out count;
    (
    node["amenity"~"baby_hatch|clinic|dentist|doctors|hospital|nursing_home|pharmacy|social_facility|veterinary"]({0});
    way["amenity"~"baby_hatch|clinic|dentist|doctors|hospital|nursing_home|pharmacy|social_facility|veterinary"]({0});
    relation["amenity"~"baby_hatch|clinic|dentist|doctors|hospital|nursing_home|pharmacy|social_facility|veterinary"]({0});
    );
    out count;
    (
    node["amenity"~"arts_centre|brothel|casino|cinema|community_centre|conference_centre|events_venue|fountain|gambling|love_hotel|music_venue|nightclub|planetarium|public_bookcase|social_centre|stripclub|studio|swingerclub|theatre"]({0});
    way["amenity"~"arts_centre|brothel|casino|cinema|community_centre|conference_centre|events_venue|fountain|gambling|love_hotel|music_venue|nightclub|planetarium|public_bookcase|social_centre|stripclub|studio|swingerclub|theatre"]({0});
    relation["amenity"~"arts_centre|brothel|casino|cinema|community_centre|conference_centre|events_venue|fountain|gambling|love_hotel|music_venue|nightclub|planetarium|public_bookcase|social_centre|stripclub|studio|swingerclub|theatre"]({0});
    );
    out count;
    (
    node["amenity"~"courthouse|fire_station|police|post_box|post_depot|post_office|prison|ranger_station|townhall"]({0});
    way["amenity"~"courthouse|fire_station|police|post_box|post_depot|post_office|prison|ranger_station|townhall"]({0});
    relation["amenity"~"courthouse|fire_station|police|post_box|post_depot|post_office|prison|ranger_station|townhall"]({0});
    );
    out count;
    (
    node["amenity"~"bbq|bench|dog_toilet|dressing_room|drinking_water|give_box|mailroom|parcel_locker|shelter|shower|telephone|toilets|water_point|watering_place"]({0});
    way["amenity"~"bbq|bench|dog_toilet|dressing_room|drinking_water|give_box|mailroom|parcel_locker|shelter|shower|telephone|toilets|water_point|watering_place"]({0});
    relation["amenity"~"bbq|bench|dog_toilet|dressing_room|drinking_water|give_box|mailroom|parcel_locker|shelter|shower|telephone|toilets|water_point|watering_place"]({0});
    );
    out count;
    (
    node["amenity"~"sanitary_dump_station|recycling|waste_basket|waste_disposal|waste_transfer_station"]({0});
    way["amenity"~"sanitary_dump_station|recycling|waste_basket|waste_disposal|waste_transfer_station"]({0});
    relation["amenity"~"sanitary_dump_station|recycling|waste_basket|waste_disposal|waste_transfer_station"]({0});
    );
    out count;
    (
    node["amenity"~"animal_boarding|animal_breeding|animal_shelter|baking_oven|childcare|clock|crematorium|dive_centre|funeral_hall|grave_yard|hunting_stand|internet_cafe|kitchen|kneipp_water_cure|lounger|marketplace|monastery|photo_booth|place_of_mourning|place_of_worship|public_bath|refugee_site|vending_machine"]({0});
    way["amenity"~"animal_boarding|animal_breeding|animal_shelter|baking_oven|childcare|clock|crematorium|dive_centre|funeral_hall|grave_yard|hunting_stand|internet_cafe|kitchen|kneipp_water_cure|lounger|marketplace|monastery|photo_booth|place_of_mourning|place_of_worship|public_bath|refugee_site|vending_machine"]({0});
    relation["amenity"~"animal_boarding|animal_breeding|animal_shelter|baking_oven|childcare|clock|crematorium|dive_centre|funeral_hall|grave_yard|hunting_stand|internet_cafe|kitchen|kneipp_water_cure|lounger|marketplace|monastery|photo_booth|place_of_mourning|place_of_worship|public_bath|refugee_site|vending_machine"]({0});
    );
    out count;
    """

    query = overpass_query.format(location)  # Formats query to allow change of location

    # This is to get exceptions when calling as there can be errors when calling apis
    try:
        # Checks on if the status code is 200 and if not restart process for this
        response = requests.get(overpass_url, params={'data': query})  # Requests with api and the query set
        if response.status_code == 200:
            data = response.json()  # Json from the request

            # Uses the helper process the data to get all the values into a dictionary - uses dicts
            result = process(location, data)
            return result  # End result
        elif response.status_code == 504:
            # This status code is server side time out
            logging.warning("Timed Out - Restarting request")
            time.sleep(1)
            return collect(location)
        else:
            # This will happen when it hasn't timed out or not successful
            logging.warning("Status code not 2XX or 504 - Ending Request")
            return None

    except requests.exceptions.ConnectionError as e:
        # If there is a connection error it will log it to the console
        print('Connection error occurred: {}'.format(str(e)))
        return None

    except json.decoder.JSONDecodeError as e:
        # JSON decode error happens when there are too many API calls to Overpass, so it will retry after a second
        print('JSON Decode error occurred: {}'.format(str(e)))
        return None


