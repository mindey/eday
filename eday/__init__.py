"""
Module providing functions for handling epoch days.

This module includes functions for converting between dates and epoch days.
"""
import datetime
import sys

SECONDS_IN_DAY = 86400.0

if sys.version_info[0] < 3:
    # Import dateutil for Python 2
    from dateutil.tz import tzutc
    from dateutil import parser


def _timestamp(date):
    """
    Calculates the timestamp from a datetime object.

    Parameters:
    date (datetime.datetime): The datetime object.

    Returns:
    float: The timestamp.
    """
    if sys.version_info[0] < 3:
        epoch = datetime.datetime(1970, 1, 1, tzinfo=tzutc())
        delta = date - epoch
        return delta.total_seconds()

    if sys.platform == 'win32':
        if date < datetime.datetime(1970, 1, 2, tzinfo=datetime.timezone.utc):
            epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
            delta = date - epoch
            return delta.total_seconds()

    return date.timestamp()

def from_date(date):
    """
    Converts a date object or ISO format string to an equivalent number of days since the epoch.

    Parameters:
    date (str or datetime.datetime): The date to convert.

    Returns:
    float: The number of days since the epoch.
    """
    if isinstance(date, str):
        if sys.version_info[0] < 3:
            date = parser.parse(date)
        else:
            date = datetime.datetime.fromisoformat(date)

    if date.tzinfo is None:
        if sys.version_info[0] < 3:
            date = date.replace(tzinfo=tzutc())
        else:
            date = date.replace(tzinfo=datetime.timezone.utc)

    return _timestamp(date) / SECONDS_IN_DAY

def to_date(eday):
    """
    Converts a number of days since the epoch to a datetime object in UTC.

    Parameters:
    eday (str, int, or float): The number of days since the epoch.

    Returns:
    datetime.datetime: The datetime object in UTC.
    """
    if any(isinstance(eday, type) for type in [str, int, float]):
        eday = float(eday)

    seconds = eday * SECONDS_IN_DAY

    if sys.platform == 'win32' and seconds < -43200.0:
        # Handle the OSError for invalid argument on Windows for timestamps less than -43200.0
        if sys.version_info[0] < 3:
            epoch = datetime.datetime(1970, 1, 1, tzinfo=tzutc())
        else:
            epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        return epoch + datetime.timedelta(seconds=seconds)

    if sys.version_info[0] < 3:
        return datetime.datetime.utcfromtimestamp(seconds).replace(
            tzinfo=tzutc())

    return datetime.datetime.utcfromtimestamp(seconds).replace(
        tzinfo=datetime.timezone.utc)

def now():
    """
    Returns the current UTC time as a number of days since the epoch.

    Returns:
    float: The number of days since the epoch representing the current UTC time.
    """
    if sys.version_info[0] < 3:
        return from_date(datetime.datetime.utcnow().replace(tzinfo=tzutc()))

    return from_date(datetime.datetime.utcnow())
