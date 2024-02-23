"""
Module providing functions for handling epoch days.

This module includes functions for converting between dates and epoch days.
"""
import datetime
import sys
import re

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

def _time_to_date(arg):
    """
    Handle times as if they were starting at 1970-01-01, if no years provided.
    """

    negative = False
    if arg.startswith('-'):
        negative = True
        arg = arg[1:]

    bce_zero = False  # Before common era.
    if arg.startswith('N'):
        arg = arg[1:]
        bce_zero = True

    try:
        # If the input string is in ISO format, return it
        datetime.datetime.fromisoformat(arg)
        is_iso = True
        return (arg, negative, is_iso, bce_zero)  # If it's already in ISO format, return it as is
    except:
        is_iso = False

    # If the input string ends with a time expression (HH:MM, HH:MM:SS, or HH:MM:SS.microseconds)
    if re.match(r'^\d+:\d{2}(:\d{2}(\.\d+)?)?$', arg):
        if arg.find(':') == 1:
            arg = '0' + arg

        match = re.match(r'^(\d+):(\d{2})(?::(\d{2})(?:\.(\d+))?)?$', arg)

        HH = int(match.group(1))
        MM = int(match.group(2))
        SS = int(match.group(3)) if match.group(3) is not None else 0

        if match.group(4) is not None:
            SS += float("0." + match.group(4))

        days = (HH * 3600 + MM * 60 + SS)/86400.

        arg = (datetime.datetime(1970,1,1)+datetime.timedelta(days=days)).isoformat() + '+00:00'

        return (arg, negative, is_iso, bce_zero)

    return (arg, negative, is_iso, bce_zero)

def from_date(date):
    """
    Converts a date object or ISO format string to an equivalent number of days since the epoch.

    Parameters:
    date (str or datetime.datetime): The date to convert.

    Returns:
    float: The number of days since the epoch.
    """
    negative = False
    is_str = False
    bce_zero = False
    if isinstance(date, str):
        is_str = True
        date, negative, is_iso, bce_zero = _time_to_date(date)

        if sys.version_info[0] < 3:
            date = parser.parse(date)
        else:
            date = datetime.datetime.fromisoformat(date)

    if date.tzinfo is None:
        if sys.version_info[0] < 3:
            date = date.replace(tzinfo=tzutc())
        else:
            date = date.replace(tzinfo=datetime.timezone.utc)

    seconds = _timestamp(date) / SECONDS_IN_DAY

    if is_str:
        if bce_zero:
            # Treat 'Z' before date as if it's B.C.E. (Before Common Era), using 0001-01-01 as zero.
            # zero = -719162.0 * 2
            zero = 719162.0
            seconds = zero + seconds

        if negative:
            # Treat "-" before date as if ti is B.E.E. (Before Epoch Era), using 1970-01-01 as zero.
            zero = 0.
            if bce_zero:
                zero = -719162.0
            return zero - seconds

    return seconds

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

    if sys.platform == 'win32' and ((seconds < -43200.0) or (seconds > 376583.91666666)):
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


class EdayConverter(type):
    """
    Metaclass for Eday class.

    Makes imported "eday" be callable.
    """
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        sys.modules[__name__] = cls
        return cls


class Eday(float, metaclass=EdayConverter):
    """
    Eday class for quick eday <-> date conversion.
    """
    @classmethod
    def from_date(cls, arg):
        return from_date(arg)

    @classmethod
    def to_date(cls, arg):
        return to_date(arg)

    @classmethod
    def now(cls):
        return now()

    def __new__(cls, arg):
        if any(isinstance(arg, it) for it in [int, float]):
            day = float(arg)
        if any(isinstance(arg, it) for it in [str, datetime.datetime]):
            day = from_date(arg)

        obj = super().__new__(cls, day)

        if (-719162.0 <= day) and (day <= 2932896.0):
            # In range 0001-01-01 ~ 9999-12-31, provide Gregorian date as fake arg.
            setattr(obj, '_converted_from', str(Eday.to_date(day)))
        else:
            setattr(obj, '_converted_from', str(arg))

        return obj

    def __repr__(self):
        return '%s <%s>' % (float(self), self._converted_from)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Eday(float(self) + other)
        elif isinstance(other, Eday):
            return Eday(float(self) + float(other))
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Eday(float(self) - other)
        elif isinstance(other, Eday):
            return Eday(float(self) - float(other))
        else:
            raise TypeError("Unsupported operand type for -")
