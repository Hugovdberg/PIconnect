#####################
Configuring timezones
#####################

.. warning::
   Default timezone changed from Europe/Amsterdam to UTC in 0.8.0

By default the data is extracted in the UTC timezone.
This is done since no fool proof way is available to detect the local timezone.
It is however possible to configure the timezone used by `PIconnect`.
This is done using the
:data:`PIConfig.DEFAULT_TIMEZONE <PIconnect.config.PIConfigContainer.DEFAULT_TIMEZONE>`
option.
It takes any valid `pytz <https://pythonhosted.org/pytz/#helpers>`_ timezone name,
such as `Europe/Amsterdam` or `America/Sao_Paulo`.

.. code-block:: python

   import PIconnect as PI

   print(PI.PIConfig.DEFAULT_TIMEZONE)
   with PI.PIServer() as server:
       points = server.search('*')
       data = points[0].recorded_values('-1h', '*')

   print(data.index.tz)

   PI.PIConfig.DEFAULT_TIMEZONE = 'Etc/GMT-1'

   with PI.PIServer() as server:
       points = server.search('*')
       data = points[0].recorded_values('-1h', '*')

   print(data.index.tz)

The output is always a :any:`pandas.Series` object with a timezone aware
:any:`pandas.DatetimeIndex`, so it is also possible to convert the timezone
afterwards like:

.. code-block:: python

   data.index = data.index.tz_convert('Europe/Amsterdam')
