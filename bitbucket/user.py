
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


import os
import sys
import imp
import json
import logging
import requests
import argparse
from os.path import expanduser
from cliff.show import ShowOne

try:
	home = expanduser("~")
	filename = os.path.join(home, '.bitbucket.py')
	creds = imp.load_source('.bitbucket', filename)
	user = creds.username
	passwd = creds.passwd
except (IOError, NameError):
	pass


class User(ShowOne):
	"""
	* Returns logged in user information
	"""
	log = logging.getLogger(__name__ + '.User')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
		url = "https://bitbucket.org/api/1.0/user/"		
		r = requests.get(url, auth=(user, passwd))
		jsondata = json.loads(r.text)
		userdata = jsondata['user']
		userdata.pop('resource_uri')
		userdata.pop('avatar')
		columns = userdata.viewkeys()
		data = userdata.viewvalues()
		return (columns, data)

class Userprivileges(ShowOne):
	"""
	* Returns logged in user privileges
	"""
	log = logging.getLogger(__name__ + '.User')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
		url = "https://bitbucket.org/api/1.0/user/privileges/"
		r = requests.get(url, auth=(user, passwd))
		jsondata = json.loads(r.text)
		userdata = jsondata['teams']
		columns = userdata.viewkeys()
		data = userdata.viewvalues()
		return (columns, data)