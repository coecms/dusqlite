Python Functions
================

Connecting to the database
--------------------------

The Dusql python interface is build around a SQLAlchemy database connection.
Call :func:`dusqlite.db.connect` before anything else, and pass the connection
object it returns to the other functions.

.. autofunction:: dusqlite.db.connect

Configuration
-------------

.. autodata:: dusqlite.config.schema
    :annotation:
.. autodata:: dusqlite.config.defaults
    :annotation:
.. autofunction:: dusqlite.config.get_config

Importing paths
---------------

.. autofunction:: dusqlite.scan.scan

.. autofunction:: dusqlite.scan.autoscan

Finding files
-------------

.. autofunction:: dusqlite.find.find

Reporting Usage
---------------

.. autofunction:: dusqlite.report.report
