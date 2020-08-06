##############################
Writing values to PI
##############################

Writing a value back to PI using Python is a interesting feature.
Having this capability we can use PIconnect for implementing collecting data
process it someway (e.g. a prediction model) and write back the results someway
it can be used by final users

It was implemented a interface for the AFSDK UpdateValeu method with 3 parameters
value as AFValue
replace_option as AFUpdateOption
buffer_option as AFBufferOption

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import UpdateOption
    from PIconnect.PIConsts import BufferOption

    tag = 'TesteTag01'

    server = PI.PIServer(server='piserver_alias')

    points = server.search(tag)[0]
    # teste write

    points.update_value(1.0,UpdateOption.REPLACE,BufferOption.BUFFERIFPOSSIBLE)