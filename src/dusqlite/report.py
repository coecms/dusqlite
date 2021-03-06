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

from . import model
from .find import find_roots, find_children
from .scan import autoscan
from .handler import get_path_id
from .tags import summarise_tags
from .config import get_config
import sqlalchemy as sa
import sqlalchemy.sql.functions as safunc
import pwd
import grp
import pandas
import os
import sys
from datetime import datetime


def report_root_ids(connection, root_ids):
    rep = []

    subq = sa.alias(find_children(root_ids))
    q = (
        sa.select([
            model.paths.c.uid.label('uid'),
            model.paths.c.gid.label('gid'),
            safunc.count().label('inodes'),
            safunc.coalesce(safunc.sum(model.paths.c.size), 0).label('size'),
            safunc.min(model.paths.c.last_seen).label('last seen'),
        ])
        .select_from(
            model.paths
            .join(subq, subq.c.id == model.paths.c.id)
        )
        .group_by(model.paths.c.uid, model.paths.c.gid)
        .order_by(sa.desc('size'))
    )

    for u in connection.execute(q):
        u = dict(u)
        u['user'] = pwd.getpwuid(u['uid']).pw_name
        u['cn'] = pwd.getpwuid(u['uid']).pw_gecos
        u['group'] = grp.getgrgid(u['gid']).gr_name
        if u['last seen'] is not None:
            u['last seen'] = datetime.fromtimestamp(u['last seen'])

        rep.append(u)

    return rep


def report(connection, config=None):
    """
    Collect information for a filesystem report
 
    Args:
        connection: Database connection from :func:`dusqlite.db.connect`
        config: Configuration information from :func:`dusqlite.config.get_config`

    Returns:
        A dict with usage information, following the pattern::
            
            { 'tags': {
                  'TAG': {
                    'size': 1024, # Size in bytes
                    'inodes': 10, # Number of files
                  },
                  'TAG': {...},
                },
              'total': {
                  'ROOT_PATH': {[
                    {
                      'user': 'abc123', # Username
                      'group': 'a12', # Group name
                      'size': 1024, # Size in bytes
                      'inodes': 10, # Number of files
                    },
                    {...}
                  ]},
                  'ROOT_PATH': {...},
                },
            }

        ``'tags'`` has a total for each tag defined by the ``config``, while
        ``'total'`` has a size by user/group for each top-level path in the
        database

    """
    if config is None:
        config = get_config()

    rep = {'tags': {}, 'total': {}}

    rep['tags'] = ((t, r) for t, r in summarise_tags(connection, config))

    root_ids = connection.execute(find_roots())
    rep['total'] = ((r.path, report_root_ids(connection, [r.id]))
                    for r in root_ids)

    return rep


def print_report(report, stream=sys.stdout):
    """
    Print a report
    """
    print("Tags:", file=stream)
    for t, r in report['tags']:
        print(f"{' '*4}%-8s {' '*13}% 8.1f gb % 8d" % (
            t, r['size'] / 1024**3, r['inodes']
        ), file=stream)

    print("Scanned Paths:", file=stream)
    for p, rs in report['total']:
        print(f"{' '*4}{p}", file=stream)
        for r in rs:
            print(f"{' '*8}%-8s %-8s % 8.1f gb % 8d" % (
                r['user'], r['group'], r['size'] / 1024**3, r['inodes']
            ), file=stream)
