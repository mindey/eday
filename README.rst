eday
====

The `eday` package provides functions for converting between dates and epoch days.

Epoch days represent the number of days since the Unix epoch (January 1, 1970, UTC).

Installation
------------

You can install `eday` using pip:

.. code:: bash

    pip install eday

Usage
-----

The package provides three main functions:

1. `from_date`: Converts a date object or ISO format string to an equivalent number of days since the epoch.
2. `to_date`: Converts a number of days since the epoch to a datetime object in UTC.
3. `now`: Returns the current UTC time as a number of days since the epoch.

Example usage:

.. code:: python

    import eday
    import datetime

    date = datetime.datetime(1968, 12, 31)

    # Convert a date to epoch days
    eday.from_date(date) # float

    # Convert epoch days to a datetime object
    eday.to_date(20000) # datetime

    # Get the current UTC time in epoch days
    eday.now()


Shorthands
----------

The package presents a converter aliased to package, that inherits from `float`, making the computations of date differences easier.

.. code:: python

    import eday

    # Create from Epoch days
    eday(12345.67890)

    # Create from ISO dates
    eday('2003-10-20 09:17:36.96-07:00')

    # Subtract or add dates:
    eday('2024-10-04') - eday.now()

    # Create from number of hours, minutes, seconds
    eday('198:30:15.445') # (translates as 198 hours, 30 minutes, 15.445 seconds)

    # Subtract or add times:
    eday('25:50') + eday('-0:05')  # (25:50 translates into 25 hours 50 minutes)


Negative times (experimental)
-----------------------------

Adding minus symbol ('-') and/or ('N') symbol to ISOString works currently like so:

.. code:: python

    # If "-" is prepended, then days since 1970-01-01 get mirrored around 1970-01-01
    eday('-2024-10-04') # negative number of days in [1970-01-01, 2024-10-04]

    # If "N" is added, then number of days since 0001-01-01 are returned.
    eday('N2024-10-04') # positive number of days in [0001-01-01, 2024-10-04]

    # If "-" and "N' is added, then days sine 0001-01-01 get mirrored around 0001-01-01
    eday('-N2024-10-04') # negative number of days in [-2024-10-04, 1970-01-01]

However, this behavior is experimental, and may be updated in the future.

Limitations
-----------

When using "N" prefix, negative days are mirrored, so B.C.E. seasons get inversed. This is something that in the future version we might fix, but it is not in the short term horizon.


Compatibility
--------------

The package is compatible with Python 2 (up to version 1.0.1) and Python 3 (from version 1.0.2). Under Python2, it relies on the `dateutil` module for Python 2 compatibility when parsing ISO format strings.

Using Epoch Days from Terminal
-------------------------------

Linux users can also use the following `zsh <https://ohmyz.sh/>`_ functions directly from the terminal to compute epoch days.

.. code-block:: bash

    #!/bin/zsh
    function eday { # eday now
     local n=$((($(date +%s%9N)/864)*1000))
     local day=${n:0:-14}; local hour=${n:(-14)}
     echo $day.${hour:0:${1-11}} # $1: precision
    }

    function d2e { # isodate -> eday
     local n=$((($(date -u --date="$1" +%s%9N)/864)*1000))
     local day=${n:0:-14}; local hour=${n:(-14)}
     echo $day.${hour} | sed 's/\.\?0*$//'
    }

    function e2d { # eday -> isodate
     local second=$(printf "%f" $(($1*86400)))
     echo $(date -u +"%Y-%m-%dT%H:%M:%S.%N%:z" -d "@$second")
    }

To use these functions, save them in a file named `eday.sh` and source the file to make the functions available in your terminal session.

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
