import datetime
import sys

SECONDS_IN_DAY = 86400.0

if sys.version_info[0] < 3:
    # Import dateutil for Python 2
    from dateutil.tz import tzutc
    from dateutil import parser

    # Define custom _timestamp() function for Python 2
    def _timestamp(date):
        """
        Calculates the timestamp from a datetime object.

        Parameters:
        date (datetime.datetime): The datetime object.

        Returns:
        float: The timestamp.
        """
        epoch = datetime.datetime(1970, 1, 1, tzinfo=tzutc())
        time_delta = date - epoch
        return time_delta.total_seconds()

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
            # Parse ISO format string with timezone information using dateutil.parser for Python 2
            date = parser.parse(date)
        else:
            date = datetime.datetime.fromisoformat(date)

    if sys.version_info[0] < 3:
        # Use custom _timestamp() function for Python 2

        if date.tzinfo is None:
            date = date.replace(tzinfo=tzutc())

        return _timestamp(date) / SECONDS_IN_DAY

    return date.timestamp() / SECONDS_IN_DAY

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

    if sys.version_info[0] < 3:
        # Convert to UTC using UTC class for Python 2
        return datetime.datetime.utcfromtimestamp(eday * SECONDS_IN_DAY).replace(
            tzinfo=tzutc())

    return datetime.datetime.utcfromtimestamp(eday * SECONDS_IN_DAY).replace(
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
