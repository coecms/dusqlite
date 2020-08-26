dusqlite - SQL Based Disk Usage Analyser
================================================================================

.. image:: https://img.shields.io/travis/com/coecms/dusqlite/master.svg
    :target: https://travis-ci.com/coecms/dusqlite
    :alt: Build Status
.. image:: https://img.shields.io/codacy/grade/427f425167b34f1a88c0d352e2709e52.svg
    :target: https://www.codacy.com/app/ScottWales/dusqlite
    :alt: Code Style
.. image:: https://img.shields.io/codecov/c/github/coecms/dusqlite/master.svg
    :target: https://codecov.io/gh/coecms/dusqlite
    :alt: Code Coverage
.. image:: https://img.shields.io/conda/v/coecms/dusqlite.svg
    :target: https://anaconda.org/coecms/dusqlite
    :alt: Conda

Scan all files under ``$DIR`` into the database (or update existing records
under ``$DIR``)::

    $ dusqlite scan $DIR

Print a summary of disk usage scanned into the database::

    $ dusqlite report
    Tags:
        umdata                    11.7 gb    65266
        conda                      8.8 gb   263338
    Scanned Paths:
        /home/562/saw562
            saw562   w35           1.4 gb    18179
            saw562   w48           0.0 gb        4
            saw562   S.U           0.0 gb       29
        /short/w35/saw562
            saw562   w35        1278.4 gb   659444
            saw562   w48         158.2 gb     2737
            hxw599   w48           6.4 gb       16
        mdss://w35/saw562
            saw562   w35         305.3 gb        6

Find files under ``$DIR``::

    $ dusqlite find --older_than 1y --group w35 $DIR

Run a check on a path::

    $ dusqlite check directory-group-readable $DIR

Configuration
-------------

``dusqlite`` reads a yaml config file from ``$HOME/.config/dusqlite.yaml`` to set the
database path etc.

To see the current configuration run::

    dusqlite print-config

Tagging Directories
-------------------

You can tag directories to add summaries to ``dusqlite report``. This is done
through the `Configuration`_, a config file to create the report above is::

    tags:
        umdata:
            paths:
              - /short/w35/saw562/UM_ROUTDIR
              - /short/w35/saw562/cylc-run
        conda:
            paths:
              - /short/w35/saw562/conda

The meaning of tags is up to the user - they could help monitor the size of
temporary directories, or allow you to find files related to a specific project
more easily.

Scanning Tape Storage
---------------------

``dusqlite`` can be extended to support other types of storage, such as tape
stores, provided there is a way to get directory information (e.g. by running
``ls -lir``)

To scan a tape store pass a URL as the path to scan, which specifies the
storage system and path. Supported URL types are:

* `NCI <https://nci.org.au>`_ MDSS: ``mdss://$PROJECT/$PATH``

TODO:
-----

* Add check reports
* Handle multiple paths in cli arguments
* Checks idea: temporary files of failed NCO/CDO commands
* Add more find arguments, e.g. size, mode
