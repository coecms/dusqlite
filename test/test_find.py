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

from dusqlite.find import *
from dusqlite import model

from conftest import count_files
import os


def to_relpath(path, base):
    return os.path.relpath(base / path, base / '..')


def test_find_empty(conn):
    # Empty DB has no files
    q = find(path=None, connection=conn)
    results = conn.execute(q)
    assert len(list(results)) == 0


def test_find_all(conn, sample_db, sample_data):
    # Find all files in the DB
    q = find(path=None, connection=conn)
    results = conn.execute(q)

    paths = [r.path for r in results]

    assert len(paths) == count_files(sample_data)


def test_find_subtree(conn, sample_data, sample_db):
    # Find all files under 'a/c'
    q = find(path=sample_data / 'a' / 'c', connection=conn)
    results = [r.path for r in conn.execute(q)]
    assert str(sample_data / 'a/c/d/e') in results
    assert str(sample_data / 'a/b/f') not in results
    assert len(results) == count_files(sample_data / 'a' / 'c')


def test_exclude(conn, sample_data, sample_db):
    # Find all files except those under 'a/c'
    q = find(conn, path=sample_data, exclude='c')
    results = [r.path for r in conn.execute(q)]
    assert 'a/c' not in results
    assert 'a/c/d/e' not in results
    assert len(results) == count_files(sample_data) - \
        count_files(sample_data / 'a' / 'c')


def test_ncdu(conn, sample_data, sample_db):
    q = find(conn, path=sample_data/'a')
    ncdu = to_ncdu(q, conn)
    print(ncdu)

    assert ncdu[3][0]['name'] == '.'
    assert ncdu[3][1][0]['name'] == sample_data.name
    assert ncdu[3][1][1][0]['name'] == 'a'
