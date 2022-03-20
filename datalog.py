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
parser.add_argument('-i', '--instrument', metavar='SN', required=True, help='Instrument serial number')
args = parser.parse_args()

# create API client
api = inetclient.client( args.url, args.acc )

# use credentials from file to obtain access_token for API
api.authorize(args.cred, pyDir)

# list datalog sessions uploaded in the past 30 days (default restriction) for an instrument
datalogId = ''
r = api.list_datalog(params={'q': '{{"sn":"{0}"}}'.format(args.instrument), 'maxResults': '5'})
if api.get_response_json():
    print("response_json={0}".format(json.dumps(api.get_response_json(), indent=2)))
if r.status_code == 200:
    # find the first datalog session and display details for it, replacing codes
    datalogId = api.get_response_json()[0].get('id')
    api.display(api.get_datalog(datalogId, headers={'X-replaceCodes':'true'}))

sys.exit()
