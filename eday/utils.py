import re
import sys
import datetime
from typing import Tuple

def _timestamp(date: datetime.datetime) -> float:
    """
    Calculates the timestamp from a datetime object.

    Parameters:
    date (datetime.datetime): The datetime object.

    Returns:
    float: The timestamp.
    """

    if sys.platform == 'win32':
        if date < datetime.datetime(1970, 1, 2, tzinfo=datetime.timezone.utc):
            epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
            delta = date - epoch
            return delta.total_seconds()

    return date.timestamp()

def _time_to_date(arg: str) -> Tuple[str, bool, bool, bool]:
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
