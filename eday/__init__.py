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

    if arg.startswith('-'):
        negative = True
        arg = arg[1:]
    else:
        negative = False

    # If the input string is in ISO format, return it
    if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$', arg):
        return (arg, negative)  # If it's already in ISO format, return it as is

    # If the input string ends with a time expression (HH:MM, HH:MM:SS, or HH:MM:SS.microseconds)
    if re.match(r'^\d{1,2}:\d{2}(:\d{2}(\.\d+)?)?$', arg):
        # Prepend '1970-01-01T' and append 'Z' to indicate Zulu time
        if arg.find(':') == 1:
            arg = '0' + arg
        return (f'1970-01-01T{arg}+00:00', negative)

    return (arg, negative)

def from_date(date):
    """
    Converts a date object or ISO format string to an equivalent number of days since the epoch.

    Parameters:
    date (str or datetime.datetime): The date to convert.

    Returns:
    float: The number of days since the epoch.
    """
    if isinstance(date, str):
        date, negative = _time_to_date(date)

        if sys.version_info[0] < 3:
            date = parser.parse(date)
        else:
            date = datetime.datetime.fromisoformat(date)
    else:
        negative = False

    if date.tzinfo is None:
        if sys.version_info[0] < 3:
            date = date.replace(tzinfo=tzutc())
        else:
            date = date.replace(tzinfo=datetime.timezone.utc)

    seconds = _timestamp(date) / SECONDS_IN_DAY
    if negative:
        return -seconds
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


def _time_interval(value):
    value = abs(value)
    YEAR = 365.2425; MONTH = 30.436875; DAY = 1
    HOUR = 1/24; MINUTE = 1/1440; SECOND = 1/86400

    years = int(value / YEAR); value -= YEAR*years
    months = int(value / MONTH); value -= MONTH*months
    days = int(value / DAY); value -= DAY*days
    hours = int(value / HOUR); value -= HOUR*hours
    minutes = int(value / MINUTE); value -= MINUTE*minutes
    seconds = value / SECOND; value -= SECOND*seconds

    second, millis = ("%.12f" % round(seconds, 11)).split('.')

    # Backpropagating
    if second == '60':
        minutes += 1
        second = '0'
        if minutes == 60:
            hours += 1
            minutes = 0
            if hours == 24:
                days += 1
                hours = 0
                if days == MONTH:
                    months += 1
                    days = 0
                    if months == YEAR:
                        years += 1
                        months = 0

    second = second.rjust(2,'0')

    time_delta_str = ''
    if years:
        time_delta_str += '%d years ' % years
    if months:
        time_delta_str += '%d months ' % months
    if days:
        time_delta_str += '%d days ' % days
    time_delta_str += "%02d:%02d:%s.%s" % (hours, minutes, second, millis)

    return time_delta_str

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

    @classmethod
    def time(cls, arg):
        return _time_interval(arg)

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
        if self < 0:
            minus = '-'
        else:
            minus = ''
        return '%s (%s%s) <%s>' % (float(self), minus, self.time(self), self._converted_from)

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
