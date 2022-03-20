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

# parse command-line arguments
args = inetclient.get_parser().parse_args()

# create API client
api = inetclient.client( args.url, args.acc )

# use credentials from file to obtain access_token for API
api.authorize(args.cred, pyDir)

# list people associated with the current account
api.display(api.list_people())
for row in list(api.get_response_json()):
    api.display(api.get_person(row.get('id'), headers={'X-replaceCodes':'true'}))

# count people associated with the current account
r = api.count_people()
api.display(r)
print("INFO: Found {0} people associated with account {1}".format(r.text, api.get_account_id()))

sys.exit()
