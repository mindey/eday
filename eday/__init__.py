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

    @classmethod
    def now(cls) -> float:
        """Return an Eday instance with the current time."""
        return cls(datetime.datetime.now(datetime.timezone.utc))

    def to_jd(self) -> float:
        """Convert epoch days to a Julian days"""
        return JDAYS_ATZERO+self

    def to_date(self) -> datetime.datetime:
        """Convert epoch days to a UTC datetime object."""
        seconds = self * SECONDS_IN_DAY
        return datetime.datetime.utcfromtimestamp(seconds).replace(tzinfo=datetime.timezone.utc)

    def __new__(cls, arg):
        if isinstance(arg, (int, float)):
            day = float(arg)
        elif isinstance(arg, (str, datetime.datetime)):
            day = cls.from_date(arg)
        else:
            try:
                # Convertable to float?
                day = float(arg)
            except:
                raise TypeError("Unsupported type for Eday creation")

        obj = super().__new__(cls, day)
        return obj

    def __repr__(self):
        """Display epoch days and corresponding date if in valid range."""
        if MIN_DATETIME <= self <= MAX_DATETIME:
            date = self.to_date().isoformat()
        else:
            dt = jd.to_gregorian(self + JDAYS_ATZERO)
            ds = dt[5] + dt[6] / 10e6
            date = f"{dt[0]}-{dt[1]:02d}-{dt[2]:02d}T{dt[3]:02d}:{dt[4]:02d}:{dt[5]:02d}.{dt[6]:06d}+00:00"
        return '%s <%s>' % (float(self), date)

    def format(self: float) -> str:
        """Return decimal time formatted similar to isoformat."""
        whole, fraction = (str(float(self)).split('.') + [''])[:2]
        formatted_whole = "{:,}".format(int(whole))
        fraction_padded = fraction.ljust(5, '0')
        result = "{} T {}:{}:{}".format(formatted_whole, fraction_padded[0], fraction_padded[1:3], fraction_padded[3:5])
        return result + (".{}".format(fraction[5:]) if len(fraction) > 5 else '')

    @classmethod
    def from_jd(cls, jday: Union[int, float]) -> float:
        """Convert Julian day to Eday."""
        return cls(jday-JDAYS_ATZERO)


    @classmethod
    def from_date(cls, date: Union[str, datetime.datetime]) -> float:
        """
        Convert a date object or ISO format string to epoch days.
        """
        negative = False

        if isinstance(date, str):

            # The negative sign is handled only for time-only expressions and julian date expressions
            negative = date.startswith('-')
            if negative:
                date = date[1:]

            if not negative:
                try:
                    # Return, if it is already an ISO 8601 string supported by datetime.
                    date = datetime.datetime.fromisoformat(date)
                    return cls._timestamp(date) / SECONDS_IN_DAY

                except ValueError:
                    pass

            # Handle time-only expressions (HH:MM[:SS[.ffffff]])
            match = re.match(
                r'^([-+]?\d+(?:\.\d+)?):([-+]?\d+(?:\.\d+)?)(?::([-+]?\d+(?:\.\d+)?))?$', date)
            if match:
                hours = float(match.group(1))
                minutes = float(match.group(2))
                seconds = float(match.group(3) or 0.)

                days = (hours * 3600 + minutes * 60 + seconds) / SECONDS_IN_DAY
                time_as_date = datetime.datetime(1970, 1, 1) + datetime.timedelta(days=days)
                date = time_as_date.isoformat() + '+00:00'

                days = cls._timestamp(time_as_date) / SECONDS_IN_DAY

                if negative:
                    return -days

                return days

            # Handle date strings with Julian dates
            try:
                iso_date = re.compile(
                    r'^(\d{1,})(?:-(\d{2}))?(?:-(\d{2}))?(?:[ T](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?)?(?:[ Z]|([+-]\d{2}:\d{2}))?$'
                )
                result = iso_date.match(date)
                if result:
                    year, month, day, hour, minute, second, fraction, tz = result.groups()

                    if fraction is not None and isinstance(fraction, str):
                        millis = fraction[:6] + '.' + fraction[6:]
                    else:
                        millis = 0

                    if tz is None:
                        tz = '+00:00'

                    if negative:
                        year = -int(year)

                    timetuple = (int(year), int(month or 1), int(day or 1), int(hour or 0),
                                 int(minute or 0), int(second or 0), float(millis))

                    # Figuring out timezone offset to Julian date, if it was provided in generic form
                    O = cls._timestamp(datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc))
                    X = cls._timestamp(datetime.datetime.fromisoformat('1970-01-01T00:00:00' + tz))
                    tzoffset = (X - O) / SECONDS_IN_DAY

                    jday = jd.from_gregorian(*timetuple) + tzoffset
                    eday = jday - JDAYS_ATZERO

                    return eday

            except ValueError:
                pass

            raise ValueError(f"Unable to parse date string: {date}")


        if date.tzinfo is None:
            date = date.replace(tzinfo=datetime.timezone.utc)

        days = cls._timestamp(date) / SECONDS_IN_DAY

        if negative:
            # This is for convenience of time calculations, e.g.: eday('-1:15') as dates before Epoch zero.
            # Note: adding minus sign to dates is treated as ISO 8601 dates BCE (before common era).
            return -days

        return days

    def __add__(self, other):
        """Add epoch days."""
        if isinstance(other, (int, float)):
            return Eday(float(self) + other)
        if isinstance(other, Eday):
            return Eday(float(self) + float(other))

        raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        """Subtract epoch days."""
        if isinstance(other, (int, float)):
            return Eday(float(self) - other)
        if isinstance(other, Eday):
            return Eday(float(self) - float(other))

        raise TypeError("Unsupported operand type for -")


# Override the module itself to make it callable
import sys
sys.modules[__name__] = Eday
