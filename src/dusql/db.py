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
from __future__ import print_function

from .model import metadata
import sqlalchemy as sa
import pkg_resources
import os.path

def connect():
    engine = sa.create_engine('sqlite:///dusql.sqlite')

    def load_closure(dbapi_conn, unused):
        dbapi_conn.enable_load_extension(True)
        ext, _ = os.path.splitext(pkg_resources.resource_filename(__name__, 'closure.so'))
        dbapi_conn.load_extension(ext)
        dbapi_conn.enable_load_extension(False)

    sa.event.listen(engine, 'connect', load_closure)

    metadata.create_all(engine)

    return engine.connect()
