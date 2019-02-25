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

import sqlalchemy as sa

metadata = sa.MetaData()
paths = sa.Table('paths', metadata,
        sa.Column('id',sa.Integer,primary_key=True),
        sa.Column('name',sa.String),
        sa.Column('inode',sa.Integer),
        sa.Column('size',sa.Integer),
        sa.Column('mtime',sa.Integer),
        sa.Column('parent_inode',sa.Integer),
        sa.Column('uid', sa.Integer),
        sa.Column('gid', sa.Integer),
        )