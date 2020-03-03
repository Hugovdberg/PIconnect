History
=======

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
