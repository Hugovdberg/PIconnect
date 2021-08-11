History
=======

0.9.1 (2021-08-11)
------------------

* Fixes the Exception type to swallow (related to #580)
* Fixes missing dependency in wheel (#595)

0.9.0 (2021-08-10)
------------------

.. warning:: This is the final version to support python 2.7

* Added support to write values to the databases (#573)
* Added support for extracting Event frames from PI-AF (#587)
* Added methods to extract a single historic value from both `PIPoint` and `PIAFAttribute` objects. (#523)
* Added options to login to the PI Server using provided credentials (#522)
* Added option to set the connection timeout for data extraction (#572)
* Better loading of the configured servers (#580)
* All data extracting functions now support both extraction using strings and `datetime` objects. (#574)

0.8.0 (2020-03-03)
------------------

* Added option to configure the timezone for the returned index. Changed default from Europe/Amsterdam to UTC! Adds `pytz` as new dependency(#499)
* More robust detection of the default PI AF server (#496, #501)
* Removed `pytest-runner` dependency unless explicitly requested (#503)
* Exiting the context manager for a `PIAFDatabase` no longer explicitly disconnects from the server, but leaves it up to SDK. (#487)
* Various updates of the package dependencies

0.7.1 (2019-08-16)
------------------

* Improved documentation
* Changed `PIData.PISeriesContainer` to an Abstract Base Class

0.7.0 (2018-11-14)
------------------

* Add `summary`, `summaries`, and `filtered_summaries` methods to `PIPoint`
    and `PIAFAttribute`

0.6.0 (2018-07-05)
------------------

0.5.1 (2017-11-25)
------------------


0.4.0 (2017-11-25)
------------------

* First release on PyPI.
