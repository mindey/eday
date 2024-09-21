"""
Module for converting between dates and epoch days.

This module provides functions for converting between dates and epoch days.
"""
import re
import datetime
from typing import Union

import juliandate as jd

SECONDS_IN_DAY = 86400.0
MIN_DATETIME = -719162.0
MAX_DATETIME = 2932896.0
JDAYS_ATZERO = 2440587.5 # Julian Days at Eday(0), 1970-01-01 0:00 UTC

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
    def _parse_time_expression(arg: str):
        """
        Convert time expressions (HH:MM, HH:MM:SS) into an ISO 8601 string.

        Handles times as if starting from 1970-01-01 if no years are provided.
        """
        negative = arg.startswith('-')
        if negative:
            arg = arg[1:]

        try:
            # Return, if it is already an ISO 8601 string.
            datetime.datetime.fromisoformat(arg)
            return arg, negative, True
        except ValueError:
            pass

        # Handle time expressions (HH:MM, HH:MM:SS, or HH:MM:SS.microseconds)
        match = re.match(
            r'^([-+]?\d+(?:\.\d+)?):([-+]?\d+(?:\.\d+)?)(?::([-+]?\d+(?:\.\d+)?))?$', arg)
        if match:
            hours = float(match.group(1))
            minutes = float(match.group(2))
            seconds = float(match.group(3) or 0.)

            days = (hours * 3600 + minutes * 60 + seconds) / SECONDS_IN_DAY
            arg = (datetime.datetime(1970, 1, 1) + datetime.timedelta(days=days)).isoformat() + '+00:00'
            return arg, negative, False

        return arg, negative, False

    @classmethod
    def now(cls) -> float:
        """Return an Eday instance with the current time."""
        return cls(datetime.datetime.now(datetime.timezone.utc))

    def __new__(cls, arg):
        if isinstance(arg, (int, float)):
            day = float(arg)
        elif isinstance(arg, (str, datetime.datetime)):
            day = cls.from_date(arg)
        else:
            raise TypeError("Unsupported type for Eday creation")

        obj = super().__new__(cls, day)
        return obj

    def __repr__(self):
        """Display epoch days and corresponding date if in valid range."""
        if MIN_DATETIME <= self <= MAX_DATETIME:
            date = self.to_date(self)
        else:
            dt = jd.to_gregorian(self + JDAYS_ATZERO)
            ds = dt[5] + dt[6] / 10e6
            date = f"{dt[0]}-{dt[1]:02d}-{dt[2]:02d} {dt[3]:02d}:{dt[4]:02d}:{ds:.6f} UTC"
        return '%s <%s>' % (float(self), date)

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
            date, negative, is_iso = cls._parse_time_expression(date)
            date = datetime.datetime.fromisoformat(date)
            # if [negatve and is_iso] OR [out of datetime range]:
            #   use juliandate

        if date.tzinfo is None:
            date = date.replace(tzinfo=datetime.timezone.utc)

        days = cls._timestamp(date) / SECONDS_IN_DAY

        if is_str and negative:
            # This is for convenience of time calculations, e.g.: eday('-1:15') + eday('1:15') = 0
            # It applies to date strings too, e.g.: eday('-1970-01-10') = 0 - eday('1970-01-10')
            # This is in conflict with ISO 8601, in that it is not meant to represent BCE dates.
            return -days

        return days

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
        return datetime.datetime.utcfromtimestamp(seconds).replace(tzinfo=datetime.timezone.utc)

    def __add__(self, other):
        """Add epoch days."""
        if isinstance(other, (int, float)):
            return Eday(float(self) + other)
        elif isinstance(other, Eday):
            return Eday(float(self) + float(other))
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        """Subtract epoch days."""
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
