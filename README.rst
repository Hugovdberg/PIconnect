A python connector to the OSISoft PI and PI-AF databases
========================================================

This connector allows access to the OSISoft PI System through their proprietary SDK. It
provides a number of classes, mostly mirroring the AF SDK structure, but at the same time
implementing the cool stuff we use Python for. Connections to the database are therefore
implemented as context managers, to allow opening a connection using a with statement.

Copyright notice
================
OSIsoft, the OSIsoft logo and logotype, Managed PI, OSIsoft Advanced Services,
OSIsoft Cloud Services, OSIsoft Connected Services, PI ACE, PI Advanced Computing Engine,
PI AF SDK, PI API, PI Asset Framework, PI Audit Viewer, PI Builder, PI Cloud Connect,
PI Connectors, PI Data Archive, PI DataLink, PI DataLink Server, PI Developer's Club,
PI Integrator for Business Analytics, PI Interfaces, PI JDBC driver, PI Manual Logger,
PI Notifications, PI ODBC, PI OLEDB Enterprise, PI OLEDB Provider, PI OPC HDA Server,
PI ProcessBook, PI SDK, PI Server, PI Square, PI System, PI System Access, PI Vision,
PI Visualization Suite, PI Web API, PI WebParts, PI Web Services, RLINK and RtReports are
all trademarks of OSIsoft, LLC.
