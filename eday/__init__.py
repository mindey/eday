"""
Module providing functions for handling epoch days.

This module includes functions for converting between dates and epoch days.
"""
import datetime
import sys
import re
from typing import Union

from . import utils

SECONDS_IN_DAY = 86400.0
DAYS_0000_TO_1970 = 719162.0
DAYS_1970_TO_9999 = 2932896.0

def from_date(date: Union[str, datetime.datetime]) -> float:
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
        date, negative, is_iso, bce_zero = utils._time_to_date(date)

        date = datetime.datetime.fromisoformat(date)

    if date.tzinfo is None:
        date = date.replace(tzinfo=datetime.timezone.utc)

    seconds = utils._timestamp(date) / SECONDS_IN_DAY

    if is_str:
        if bce_zero:
            # Treat 'N' prefix as using 0001-01-01 as zero, instead of 1970-01-01.
            zero = DAYS_0000_TO_1970
            seconds = zero + seconds

        if negative:
            # Treat "-" before as zero.
            zero = 0.
            if bce_zero:
                zero = -DAYS_0000_TO_1970
            return zero - seconds

    return seconds

def to_date(eday: Union[str, int, float]) -> datetime.datetime:
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
        epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        return epoch + datetime.timedelta(seconds=seconds)

    return datetime.datetime.utcfromtimestamp(seconds).replace(
        tzinfo=datetime.timezone.utc)


class EdayConverter(type):
    """
    Metaclass for Eday class. Makes imported "eday" be callable.
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
    def _timestamp(cls, arg):
        return utils._timestamp(arg)

    @classmethod
    def _time_to_date(cls, arg):
        return utils._time_to_date(arg)

    @classmethod
    def now(cls):
        return now()

    def __new__(cls, arg):
        if any(isinstance(arg, it) for it in [int, float]):
            day = float(arg)
        if any(isinstance(arg, it) for it in [str, datetime.datetime]):
            day = from_date(arg)

        obj = super().__new__(cls, day)

        if (-DAYS_0000_TO_1970 <= day) and (day <= DAYS_1970_TO_9999):
            # In range 0001-01-01 ~ 9999-12-31, provide Gregorian date as fake arg for eyes.
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

def now() -> Eday:
    """
    Returns the current UTC time as a number of days since the epoch.

    Returns:
    Eday: The number of days since the epoch representing the current UTC time.
    """
    return Eday(from_date(datetime.datetime.utcnow()))
