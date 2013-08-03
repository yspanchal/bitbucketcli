import logging
import requests
import os
import sys
import getpass
import json
import imp
import argparse
from os.path import expanduser
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

home = expanduser("~")
filename = os.path.join(home, '.bitbucket.py')
creds = imp.load_source('.bitbucket', filename)
user = creds.username
passwd = creds.passwd

class User(ShowOne):
	log = logging.getLogger(__name__ + '.User')

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