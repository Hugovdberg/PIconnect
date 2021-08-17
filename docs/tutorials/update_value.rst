##############################
Update value in PI
##############################

Writing a value back to PI using Python is an interesting feature.
Having this capability we can use PIconnect for implementing collecting data
process it someway (e.g. a prediction model) and write back the results someway
it can be used by final users.

After discussion with @Hugovdberg & with contribution of @ldariva we finally implemented an interface for the AFSDK UpdateValue method with 4 parameters
value as AFValue
time as python datetime.datetime with specified timezone
replace_option as AFUpdateOption
buffer_option as AFBufferOption.


.. code-block:: python

    from datetime import datetime

    import PIconnect as PI
    from PIconnect.PIConsts import UpdateMode, BufferMode


    with PI.PIServer(server='foo') as server:
        point = server.search('foo')[0]  # the tag has to be created
        point.update_value(
            1.0,
            datetime.now(),
            UpdateMode.NO_REPLACE,
            BufferMode.BUFFER_IF_POSSIBLE,
        )
