from datetime import datetime


def process(area, data):
    """
    This will process information from the API request and put it into a dictionary that is more readable and
    available to use.

    :param area: This is the region
    :type area: str
    :param data: The API request result
    :type data: dict

    :return: A simplified dictionary of the POIS with a timestamp
    """
    # Elements needed for the totals
    elements = data['elements']

    # Setting up variables required for formatting the data
    dicts = {}
    values = []
    total = 0
    keys = ['Sustenance', 'Education', 'Transportation', 'Financial', 'Healthcare', 'Entertainment', 'Public Services',
            'Facilities', 'Waste Management', 'Other']

    # Gets each value of the pois and puts it into a list - range is hardcoded for now
    for i in range(10):
        tags = elements[i]
        tags = tags['tags']['total']
        values.append(int(tags))

    # Gets total of the values
    for n in values:
        total += n

    # Puts it into a dict
    for key in keys:
        for v in values:
            dicts[key] = v
            values.remove(v)
            break

    # Getting the current time and date to put into the dictionary
    current_dateandtime = datetime.now()
    current_time = current_dateandtime.strftime('%Y-%m-%d %H:%M')

    # Importing a Timestamp
    items = list(dicts.items())
    items.insert(0, ('Timestamp', current_time))
    dicts = dict(items)

    # Puts the Area code at the front of the dictionary
    items = list(dicts.items())
    items.insert(0, ('Area', area))
    dicts = dict(items)

    # Adds total to the end of the dictionary
    dicts["Total"] = total

    return dicts
