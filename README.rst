eday
====

The ``eday`` package provides functions for converting between dates and epoch days, a concept where dates are represented as the number of days since a reference epoch. This is useful for date arithmetic and conversion.

Installation
------------

Install `eday` using pip:

.. code:: bash

    pip install eday

Principle
---------

Method signature.

.. code:: python

    import eday

    eday(<datetime.datetime> | '<ISO-STRING>' | '<TIME-STRING>' | <float|int>) # -> Eday <float>

    eday.from_jd(<float>) # -> Eday <float>

    eday.now() # -> Eday <float>

    eday.to_date() # -> datetime.datetime

    eday.to_jd() # -> <float> (Julian day)

Usage
------

The imoprted ``eday`` can be called directly, and supports polymorphic creation from diferent types, and simple arithmetic.

.. code:: python

    import eday

    # Create from float
    eday(0) # 0.0 <1970-01-01 00:00:00+00:00>

    # Passing large numbers displays date representations as well
    eday(-2440587.5) # -2440587.5 <-4713-11-24 12:00:0.000000 UTC>

    # Create from datetime.datetime
    eday(datetime.datetime(1970,1,1))

    # Create from ISO dates
    eday('1969-12-31 17:00:00-07:00')

    # Create from Time string
    eday('-7:00') # 7 hours before "epoch 0". NOTE: If '-' is before ISO 8610 string, it means BC (before common era.)

    # Unrestricted float numbers of hours, minutes, seconds can be used
    eday('100.5:100.15:100.125') # (100.5 hours, 100.15 minutes, 100.125 seconds)

    # Create from Julian days:
    eday.from_jd(2459580.5) # 18993.0 <2022-01-01T00:00:00+00:00>

    # Date arithmetic
    eday('2024-10-04') - eday.now()

    # Time arithmetic
    eday('1:50') - eday('0:10:15.123')  # (1 hour 50 minutes - 10 minutes 15.123 seconds)

    # Convert to Julian day
    eday('2024-10-04').to_jd() # 2460587.5

    # Format as decimal unix day and time, for viewing as date and time string.
    eday('2024-10-04 12:15').format() # 20,000 T 5:10:41.6666668


About
-----
The ``eday`` package features the ``Eday`` class, which represents "epoch days" (Unix seconds in days). It inherits from ``float``, providing conversions to/from datetime, and supports arithmetic operations for quick date calculations.

Main Functions:

1. ``from_date``: Converts a date object or ISO format string to the number of days since the epoch.
2. ``from_jd``: Convets Julian day to number of days since the epoch.
3. ``now``: Returns the current UTC time as a number of days since the epoch.

Auxiliary Functions:

4. ``to_date``: Converts Eday object to ``datetime.datetime`` if possible.
5. ``to_jd``: Converts Eday object to Julian day.

Miscellanous Functions:

6. ``format``: Formats Eday as Decimal Unix day and time in a fashion similar to ``datetime.datetime.isoformat()``.

However, you can call the imported ``eday`` directly (as shown in the examples above) to use it with minimal typing to do time and calendar computations.


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
