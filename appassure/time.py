"""Python wrapper for the AppAssure 5 REST API.

Helps developers deal with time in the AppAssure API in various ways.
"""

import datetime

def formatTime(time):
    """Convert a datetime object to a string in the format expected
    by the AppAssure API.
    """
    return time.isoformat()[:-7]

def deformatTime(string):
    """Convert a string in the format used by the AppAssure API to a
    datetime object.
    """
    if '.' in string and string.endswith('Z'):
        return datetime.datetime.strptime(string[:-1][:26],
                "%Y-%m-%dT%H:%M:%S.%f")
    elif '.' in string:
        return datetime.datetime.strptime(string[:26],
                "%Y-%m-%dT%H:%M:%S.%f")
    elif 'Z' in string:
        return datetime.datetime.strptime(string[:-1][:19],
                "%Y-%m-%dT%H:%M:%S")
    else:
        return datetime.datetime.strptime(string[:19],
                "%Y-%m-%dT%H:%M:%S")

def reformatTime(string):
    """Convert a string in the format used by the AppAssure API to a
    datetime object, then back to a human readable string.
    """
    return formatTime(deformatTime(string)).replace('T', ' ') + ' UTC'

def now():
    """Return the current time as a string in the format expected by
    the AppAssure API.
    """
    return formatTime(datetime.datetime.utcnow())

