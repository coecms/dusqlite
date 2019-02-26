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

import pytest

from dusql.db import connect
from dusql.scan import scan

@pytest.fixture
def conn():
    return connect('sqlite:///:memory:', echo=False)


@pytest.fixture(scope="session")
def sample_data(tmp_path_factory):
    root = tmp_path_factory.mktemp('sample_data')
    a = root / 'a'
    b = a / 'b'
    c = a / 'c'
    d = c / 'd'

    for p in [a,b,c,d]:
        p.mkdir()

    return root


@pytest.fixture
def sample_db(conn, sample_data):
    scan(sample_data, conn)
