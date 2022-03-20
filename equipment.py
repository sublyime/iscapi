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

import argparse
import datetime

# allow packages to be imported relative to this file's directory
import os
pyDir = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(pyDir)

# convenience package
import inetclient

# parse command-line arguments, after adding example-specific args
parser = inetclient.get_parser()
parser.add_argument('--start', metavar='TIMESTAMP', help='Start date for queries [1 week ago]')
parser.add_argument('--end', metavar='TIMESTAMP', help='End date for queries [today]')
args = parser.parse_args()

# create API client
api = inetclient.client( args.url, args.acc )

# datetime range
endtime = api.date_from_string(args.end, datetime.datetime.combine(datetime.date.today(), datetime.time(23,59,59,999)))
starttime = api.date_from_string(args.start, (endtime - datetime.timedelta(weeks=1)))
timeframe = api.date_range(starttime,endtime)

# use credentials from file to obtain access_token for API
api.authorize(args.cred, pyDir)

# list equipment/alarms for specified time period
total_alarms = 0
api.set_assoc_date(timeframe)
r = api.list_equipment(max_calls=5, params={'q':'{"type":"Instrument"}'})
for inst in list(api.get_response_json()):
    instSn = inst.get('sn')
    r = api.list_equipment_alarms(instSn, params={"q": '{{"time": "{0}", "peakReading": ">0"}}'.format(timeframe) })
    if r.status_code == 200:
        total_alarms = len(r.json())
        if total_alarms > 0:
            api.display(r)
            api.display(api.get_alarm(r.json()[0].get('id'), params={'replaceCodes': 'true'}))
            break 
            