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

    # Convert a date to epoch days
    eday_value = eday.from_date('2022-02-17')

    # Convert epoch days to a datetime object
    datetime_obj = eday.to_date(eday_value)

    # Get the current UTC time in epoch days
    current_time = eday.now()

Compatibility
--------------

The package is compatible with Python 2 and Python 3. It relies on the `dateutil` module for Python 2 compatibility when parsing ISO format strings.

Using Epoch Days from Terminal
-------------------------------

Linux users can also use the following bash functions directly from the terminal to compute epoch days.

.. code-block:: bash

    #!/bin/bash
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
