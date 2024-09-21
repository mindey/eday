eday
====

The `eday` package provides functions for converting between dates and epoch days (see `About <#about>`_ section).

Installation
------------

You can install `eday` using pip:

.. code:: bash

    pip install eday

Simple Usage
------------

Example usage:

.. code:: python

    import eday

    eday.from_date(<datetime.datetime>) # -> float

    eday.to_date(<float>) # -> datetime.datetime

    eday.now() # -> eday <float>


About
-----
The package provides ``Eday`` class, that to represent "epoch day" (unix seconds in days). It inherits from ``float`` to provide it with conversions to and from datetime, as well as to display (when possible) and arithmetic operands (addition/subtraction) to enable simple quick date calculations using epoch days.

The package exposes three main functions:

1. ``from_date``: Converts a date object or ISO format string to an equivalent number of days since the epoch.
2. ``to_date``: Converts a number of days since the epoch to a datetime object in UTC.
3. ``now``: Returns the current UTC time as a number of days since the epoch.

However, you can call the imported ``eday`` directly (see below) to use it with minimal typing to do time and calendar computations.

Advanced Usage
--------------

The package presents a converter aliased to package, that inherits from `float`, making the computations of date differences easier.

.. code:: python

    import eday

    # Create from Epoch days
    eday(12345.67890)

    # Create from ISO dates
    eday('2003-10-20 09:17:36.96-07:00')

    # Subtract or add dates:
    eday('2024-10-04') - eday.now()

    # Subtract or add times:
    eday('25:50') + eday('-0:05')  # (25:50 translates into 25 hours 50 minutes)

    # Create from unrestricted float numbers of hours, minutes, seconds
    eday('100.5:100.15:100.125') # (100.5 hours, 100.15 minutes, 100.125 seconds)


Using Epoch Days without this package (Python2 & Python3)
---------------------------------------------------------
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

Linux users can also use the following `zsh <https://ohmyz.sh/>`_ functions directly from the terminal to compute epoch days.

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

To use these functions, save them in a file named `eday.sh` and source the file to make the functions available in your terminal session, or add ``/usr/local/bin/eday``:

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

The package is compatible with Python 2 (up to version 1.0.1) and Python 3 (from version 1.0.2). Under Python2, it relies on the `dateutil` module for Python 2 compatibility when parsing ISO format strings.

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
