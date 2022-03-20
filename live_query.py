#!/usr/bin/python3
#
# Copyright 2016 Industrial Scientific Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from time import sleep

import argparse
import datetime
import json

# allow packages to be imported relative to this file's directory
import os
pyDir = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(pyDir)

# convenience package
import inetclient

# parse command-line arguments, after adding example-specific args
parser = inetclient.get_parser()
parser.add_argument('--start', metavar='TIMESTAMP', help='Start date for initial query')
args = parser.parse_args()

# initial time (now)
starttime = datetime.datetime.now().strftime(inetclient.iso8601datetime)

# create API client
api = inetclient.client( args.url, args.acc )

# use credentials from file to obtain access_token for API
api.authorize(args.cred, pyDir)

# initial call to get the current state of all instruments
query = { "query": { "historyTime": starttime, "updateTime": starttime } }
print( query )
r = api.get_live_query(json=query)
api.display(r)

# loop for incremental updates, based on previous request time
count = 1
while count < 20 and r.status_code == 200:
    sleep(15)
    query = { "query": { "updateTime": r.json()['requestTime'] } }
    print( query )
    r = api.get_live_query(json=query)
    api.display(r)
    count = count + 1

sys.exit()
