#!/usr/bin/env python
# Copyright 2019 ARC Centre of Excellence for Climate Extremes
# author: Scott Wales <scott.wales@unimelb.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Configuration
=============

dusqlite uses a yaml configuration file

It will search the following paths in order:

    $XDG_CONFIG_HOME/dusqlite.yaml
    $HOME/.config/dusqlite.yaml
    ./dusqlite.yaml

An example config file::

    ---
    # Path to the sqlite database
    database: sqlite:////short/w35/saw562/dusqlite.db

"""

from __future__ import print_function

from jsonschema import validate
import os

import yaml
import tempfile

#: JSON schema of the configuration
schema = {
    'type': 'object',
    'properties': {
        'database': {
            'type': 'string',
            'pattern': '^sqlite:///.*$'
        },
        'tags': {
            'type': 'object',
            'additionalProperties': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string'},
                    'paths': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                    'checks': {
                        'type': 'object',
                    }
                },
            },
        },
    },
    'required': [
        'database',
    ],
}

#: Default configuration
defaults = {
    'database': f'sqlite:///{tempfile.gettempdir()}/{os.environ["USER"]}.dusqlite.db',
}


def _construct_config(yaml_data):
    config = {}
    config.update(defaults)

    data = yaml.safe_load(yaml_data)
    if data is not None:
        config.update(data)

    config['database'] = os.path.expandvars(config['database'])

    validate(config, schema)

    return config


def get_config(configfile=None):
    """
    Gets the configuration, either from a named file or from the default paths

    If ``configfile`` is not specified, the following paths will be searched in order:
     - $XDG_CONFIG_HOME/dusqlite.yaml
     - $HOME/.config/dusqlite.yaml
     - ./dusqlite.yaml

    Values not set in the config file will be defined from :obj:`defaults`

    Args:
        configfile: Path to a YAML configuration file

    Returns:
        A dict with the configuration values, matching schema :obj:`schema`
    """
    filename = 'dusqlite.yaml'

    if configfile is None:
        configfile = os.path.join(os.environ.get(
            'XDG_CONFIG_HOME', '/dev/null'), filename)
        if not os.path.isfile(configfile):
            configfile = None

    if configfile is None:
        configfile = os.path.join(os.environ.get(
            'HOME', '/dev/null'), '.config', filename)
        if not os.path.isfile(configfile):
            configfile = None

    if configfile is None:
        configfile = filename
        if not os.path.isfile(configfile):
            configfile = None

    if configfile is not None:
        with open(configfile, 'r') as f:
            config = _construct_config(f)
    else:
        config = _construct_config('')

    return config
