Command Line Tools
==================

Configuration
-------------

Dusql checks the following paths for configuration information:

 - $XDG_CONFIG_HOME/dusqlite.yaml
 - $HOME/.config/dusqlite.yaml
 - ./dusqlite.yaml

You can see the current configuration by running::

    $ dusqlite print-config

The configuration file is in YAML format, and should be structured like::

    # Path to the database
    database: sqlite:////short/a12/abc123/tmp/dusqlite.db

    # Tag definitions
    tags:
        umdata:
            - /short/w35/saw562/UM_ROUTDIR
            - /short/w35/saw562/cylc-run
        conda:
            - /short/w35/saw562/conda

Tags are used to categorise data in ``dusqlite report`` - files under the listed
directories are included in the tag total

Importing paths
---------------

Scan all files under ``$DIR`` into the database (or update existing records
under ``$DIR``)::

    $ dusqlite scan $DIR

Finding files
-------------

Find files under ``$DIR``::

    $ dusqlite find --older_than 1y --group w35 $DIR

Reporting Usage
---------------

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
