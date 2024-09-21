"""
Module for converting between dates and epoch days.

This module provides functions for converting between dates and epoch days.
"""
import datetime
from typing import Union
import re

SECONDS_IN_DAY = 86400.0
MIN_DATETIME = -719162.0
MAX_DATETIME = 2932896.0

class Eday(float):
    """
    Eday class for quick conversion between epoch days and dates.
    """

    @staticmethod
    def _timestamp(date):
        """Get a POSIX timestamp from a datetime object."""
        if hasattr(date, 'timestamp'):
            return date.timestamp()
        # For Python versions < 3.3
        return (date - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()

    @staticmethod
    def _time_to_date(arg: str):
        """
        Convert a time expression or ISO format string to a date.

        Handles times as if starting from 1970-01-01 if no years are provided.
        """
        negative = False
        if arg.startswith('-'):
            negative = True
            arg = arg[1:]

        try:
            # If the input string is in ISO format, return it
            datetime.datetime.fromisoformat(arg)
            is_iso = True
            return (arg, negative, is_iso)
        except ValueError:
            is_iso = False

        # If the input string is time expression (HH:MM, HH:MM:SS, or HH:MM:SS.microseconds)
        match = re.match(
            r'^([-+]?\d+(?:\.\d+)?):([-+]?\d+(?:\.\d+)?)(?::([-+]?\d+(?:\.\d+)?))?$', arg)
        if match:
            hours = float(match.group(1))
            minutes = float(match.group(2))
            seconds = float(match.group(3)) if match.group(3) is not None else 0.

            days = (hours * 3600 + minutes * 60 + seconds) / SECONDS_IN_DAY
            arg = (datetime.datetime(1970, 1, 1) + datetime.timedelta(days=days)).isoformat() + '+00:00'
            return (arg, negative, is_iso)

        return (arg, negative, is_iso)

    @classmethod
    def now(cls):
        """Return the Eday instance with current time."""
        return Eday(datetime.datetime.now(datetime.timezone.utc))

    def __new__(cls, arg):
        if isinstance(arg, (int, float)):
            day = float(arg)
        elif isinstance(arg, (str, datetime.datetime)):
            day = cls.from_date(arg)
        else:
            raise TypeError("Unsupported type for Eday creation")

        obj = super().__new__(cls, day)

        # In range 0001-01-01 ~ 9999-12-31, provide Gregorian date in __repr__.
        if MIN_DATETIME <= day <= MAX_DATETIME:
            date = cls.to_date(day)
            setattr(obj, '_converted_from', str(date))
        else:
            setattr(obj, '_converted_from', str(arg))
        return obj

    def __repr__(self):
        """Return the string representation of the Eday instance."""
        if hasattr(self, '_converted_from'):
            # For Python versions < 3.6 not using f-strings
            return '%s <%s>' % (float(self), self._converted_from)
        return '%s' % float(self)


    @classmethod
    def from_date(cls, date: Union[str, datetime.datetime]) -> float:
        """
        Convert a date object or ISO format string to the number of days since the epoch.

        Parameters:
        date (str or datetime.datetime): The date to convert.

        Returns:
        float: The number of days since the epoch.
        """
        is_str = isinstance(date, str)

        if is_str:
            date, negative, is_iso = cls._time_to_date(date)
            date = datetime.datetime.fromisoformat(date)

        if date.tzinfo is None:
            date = date.replace(tzinfo=datetime.timezone.utc)

        seconds = cls._timestamp(date) / SECONDS_IN_DAY

        if is_str and negative:
            # We use minus sign ('-') for "before epoch" (before 1970-01-01 0:00 UTC) dates.
            return -seconds
            # This is very convenient for time calculations, e.g.:
            #    eday('-1:15') + eday('1:15') = 0
            # But may be confusing for dates:
            #    eday('-1970-01-10') = 0 - eday('1970-01-10')
            # Because some people may think '-' has to mean BCE (before comon era).
            # We'll use a different symbol in the future to represent BCE dates.

        return seconds

    @classmethod
    def to_date(cls, eday: Union[str, int, float]) -> datetime.datetime:
        """
        Convert a number of days since the epoch to a datetime object in UTC.

        Parameters:
        eday (str, int, or float): The number of days since the epoch.

        Returns:
        datetime.datetime: The datetime object in UTC.
        """
        eday = float(eday)
        seconds = eday * SECONDS_IN_DAY
        return datetime.datetime.utcfromtimestamp(seconds).replace(
            tzinfo=datetime.timezone.utc
        )

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

# Override the module itself to make it callable
import sys
sys.modules[__name__] = Eday

# Expose main functions at module level for convenience
from_date = Eday.from_date
to_date = Eday.to_date
now = Eday.now
