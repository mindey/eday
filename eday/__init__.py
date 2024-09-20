"""
Module providing functions for handling epoch days.

This module includes functions for converting between dates and epoch days.
"""
from __future__ import division  # For Python 2 compatibility

import sys
import re
import datetime

from typing import Union

SECONDS_IN_DAY = 86400.0
DAYS_0000_TO_1970 = 719162.0
DAYS_1970_TO_9999 = 2932896.0
JD = 2440587.5 # JD on 1970-01-01


class Eday(float):
    """
    Eday class for quick eday <-> date conversion.
    """

    @staticmethod
    def _timestamp(dt):
        """Get a POSIX timestamp from a datetime object."""
        if hasattr(dt, 'timestamp'):
            return dt.timestamp()
        else:
            # For Python versions < 3.3
            return (dt - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()

    @staticmethod
    def _time_to_date(arg: str):
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
        match = re.match(r'^([-+]?\d+(?:\.\d+)?):([-+]?\d+(?:\.\d+)?)(?::([-+]?\d+(?:\.\d+)?))?$', arg)

        if match:
            HH = float(match.group(1))
            MM = float(match.group(2))
            SS = float(match.group(3)) if match.group(3) is not None else 0.

            days = (HH * 3600 + MM * 60 + SS)/86400.
            arg = (datetime.datetime(1970,1,1)+datetime.timedelta(days=days)).isoformat() + '+00:00'
            return (arg, negative, is_iso, bce_zero)

        return (arg, negative, is_iso, bce_zero)


    @classmethod
    def now(cls):
        return Eday(datetime.datetime.now(datetime.timezone.utc))

    def __new__(cls, arg):
        if isinstance(arg, (int, float)):
            day = float(arg)
        elif isinstance(arg, (str, datetime.datetime)):
            day = cls.from_date(arg)
        else:
            raise TypeError("Unsupported type for Eday creation")

        obj = super().__new__(cls, day)

        if (-DAYS_0000_TO_1970 <= day) and (day <= DAYS_1970_TO_9999):
            # In range 0001-01-01 ~ 9999-12-31, provide Gregorian date as fake arg for eyes.
            setattr(obj, '_converted_from', str(Eday.to_date(day)))
        else:
            setattr(obj, '_converted_from', str(arg))

        return obj

    def __repr__(self):
        return '%s <%s>' % (float(self), self._converted_from)

    @classmethod
    def from_date(cls, date: Union[str, datetime.datetime]) -> float:
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
            date, negative, is_iso, bce_zero = cls._time_to_date(date)
            date = datetime.datetime.fromisoformat(date)

        if date.tzinfo is None:
            date = date.replace(tzinfo=datetime.timezone.utc)

        seconds = cls._timestamp(date) / SECONDS_IN_DAY

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

    @classmethod
    def to_date(cls, eday: Union[str, int, float]) -> datetime.datetime:
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
sys.modules[__name__] = Eday

# Expose main functions at module level for convenience
from_date = Eday.from_date
to_date = Eday.to_date
now = Eday.now
