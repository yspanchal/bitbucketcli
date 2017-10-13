# Copyright (c) 2013 Yogesh Panchal, yspanchal@gmail.com

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import logging
import requests
from cliff.show import ShowOne
from .utils import read_creds


class User(ShowOne):

    """
    * Returns logged in user information
    """
    log = logging.getLogger(__name__ + '.User')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))
        url = ("https://bitbucket.org/api/1.0/"
               "user/")
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        jsondata = json.loads(r.text)
        userdata = jsondata['user']
        userdata.pop('resource_uri')
        userdata.pop('avatar')
        columns = userdata.keys()
        data = userdata.values()
        return (columns, data)


class Userprivileges(ShowOne):

    """
    * Returns logged in user privileges
    """
    log = logging.getLogger(__name__ + '.User')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))
        url = ("https://bitbucket.org/api/1.0/"
               "user/"
               "privileges/")
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        jsondata = json.loads(r.text)
        userdata = jsondata['teams']
        columns = userdata.keys()
        data = userdata.values()
        return (columns, data)
