#########
PIconnect
#########

A python connector to the OSISoft PI and PI-AF databases
========================================================

This connector allows access to the OSISoft PI System through their
proprietary SDK. It provides a number of classes, mostly mirroring the AF SDK
structure, but at the same time implementing the cool stuff we use Python for.
Connections to the database are therefore implemented as context managers, to
allow opening a connection using a with statement.

.. image:: https://img.shields.io/pypi/v/PIconnect.svg
    :target: https://pypi.python.org/pypi/PIconnect
    :alt: PIconnect on PyPI

.. image:: https://img.shields.io/conda/vn/conda-forge/piconnect
    :target: https://anaconda.org/conda-forge/piconnect
    :alt: PIconnect on conda-forge

.. image:: https://github.com/Hugovdberg/PIconnect/actions/workflows/ci.yml/badge.svg?branch=develop
    :target: https://github.com/Hugovdberg/PIconnect/actions/workflows/ci.yml
    :alt: Continuous Integration status

.. image:: https://readthedocs.org/projects/piconnect/badge/?version=develop
    :target: https://piconnect.readthedocs.io/en/latest/?badge=develop
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Hugovdberg/PIconnect/shield.svg
    :target: https://pyup.io/repos/github/Hugovdberg/PIconnect/
    :alt: Security Updates

.. image:: https://api.codacy.com/project/badge/Grade/568734c85e07467c99e0e791d8eb17b6
    :target: https://www.codacy.com/app/Hugovdberg/PIconnect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Hugovdberg/PIconnect&amp;utm_campaign=Badge_Grade
    :alt: Automated code review

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black

Python connector to OSIsoft PI SDK


* Free software: MIT license
* Documentation: https://piconnect.readthedocs.io.


Features
--------
Features below are for both: PI Server and PIAF Database:

* Extract recorded values
* Extract interpolated values
* Update a value
* Summarize data before extraction with help of OSIsoft PI SDK
* Filter data before extraction with help of OSIsoft PI SDK

Copyright notice
================
OSIsoft, the OSIsoft logo and logotype, Managed PI, OSIsoft Advanced Services,
OSIsoft Cloud Services, OSIsoft Connected Services, PI ACE, PI Advanced
Computing Engine, PI AF SDK, PI API, PI Asset Framework, PI Audit Viewer, PI
Builder, PI Cloud Connect, PI Connectors, PI Data Archive, PI DataLink, PI
DataLink Server, PI Developer's Club, PI Integrator for Business Analytics, PI
Interfaces, PI JDBC driver, PI Manual Logger, PI Notifications, PI ODBC, PI
OLEDB Enterprise, PI OLEDB Provider, PI OPC HDA Server, PI ProcessBook, PI
SDK, PI Server, PI Square, PI System, PI System Access, PI Vision, PI
Visualization Suite, PI Web API, PI WebParts, PI Web Services, RLINK and
RtReports are all trademarks of OSIsoft, LLC.

Credits
---------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
