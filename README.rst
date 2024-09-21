eday
====

The ``eday`` package provides functions for converting between dates and epoch days, a concept where dates are represented as the number of days since a reference epoch. This is useful for date arithmetic and conversion.

Installation
------------

Install `eday` using pip:

.. code:: bash

    pip install eday

Simple Usage
------------

Basic examples:

.. code:: python

    import eday

    eday.from_date(<datetime.datetime>) # -> float

    eday.to_date(<float>) # -> datetime.datetime

    eday.now() # -> eday <float>


About
-----
The ``eday`` package features the ``Eday`` class, which represents "epoch days" (Unix seconds in days). It inherits from ``float``, providing conversions to/from datetime, and supports arithmetic operations for quick date calculations.

Main Functions:

1. ``from_date``: Converts a date object or ISO format string to the number of days since the epoch.
2. ``to_date``: Converts a number of days since the epoch to a datetime object in UTC.
3. ``now``: Returns the current UTC time as a number of days since the epoch.

However, you can call the imported ``eday`` directly (see below) to use it with minimal typing to do time and calendar computations.

Advanced Usage
--------------

The package allows advanced manipulations using ``eday`` objects:

.. code:: python

    import eday

    # Create from Epoch days
    eday(12345.67890)

    # Create from ISO dates
    eday('2003-10-20 09:17:36.96-07:00')

    # Date arithmetic
    eday('2024-10-04') - eday.now()

    # Time arithmetic
    eday('25:50') + eday('-0:05')  # (25:50 translates into 25 hours 50 minutes)

    # Unrestricted float numbers of hours, minutes, seconds
    eday('100.5:100.15:100.125') # (100.5 hours, 100.15 minutes, 100.125 seconds)

    # Out-of-range dates
    eday(-2440587.5) # -2440587.5 <-4713-11-24 12:00:0.000000 UTC>


Using Epoch Days without this package (Python 2 & Python 3)
-----------------------------------------------------------
If you don't need these extra features, and just need to convert dates to/from edays, you could simply use:

.. code:: python

    import time, datetime

    def d2e(date): # datetime.datetime -> float
        return time.mktime(date.utctimetuple()) / 86400.

    def e2d(eday): # datetime.datetime -> float
        return datetime.datetime.utcfromtimestamp(eday * 86400.)

    def eday():
        return d2e(datetime.datetime.utcnow())

Using Epoch Days from Terminal
-------------------------------

Linux users can use these ``zsh`` functions:

.. code-block:: bash

    function d2e { # isodate -> eday
     local n=$((($(date -u --date="$1" +%s%9N)/864)*1000))
     local day=${n:0:-14}; local hour=${n:(-14)}
     echo $day.${hour} | sed 's/\.\?0*$//'
    }

    function e2d { # eday -> isodate
     local second=$(printf "%f" $(($1*86400)))
     echo $(date -u +"%Y-%m-%dT%H:%M:%S.%N%:z" -d "@$second")
    }

Save these functions in ``eday.sh`` and source it or add to ``/usr/local/bin/eday``.

.. code-block:: bash

    #!/bin/bash
    function eday { # eday now
     local n=$((($(date +%s%9N)/864)*1000))
     local day=${n:0:-14}; local hour=${n:(-14)}
     echo $day.${hour:0:${1-11}} # $1: precision
    }
    eday

Compatibility
--------------

The package is compatible with Python 2 (up to version 1.0.1) and Python 3 (from version 1.0.2). Python 2 users will need the ``dateutil`` module for parsing ISO format strings.

License
-------

This package is licensed under the MIT License. See the LICENSE file for details.

Contributing
------------

Contributions are welcome! Feel free to open an issue or submit a pull request on GitHub.

GitHub Repository
------------------

You can find the source code and contribute to the development of this package on GitHub: https://github.com/mindey/eday

More Information
----------------

For more information on epoch days and their applications, you can visit the following link:

- `Simple Decimal Calendar <https://www.wefindx.com/event/17001/simple-decimal-calendar>`_
