import logging
import requests
import os
import sys
import getpass
import json
import imp
from os.path import expanduser
from cliff.command import Command
from cliff.lister import Lister


class Repolist(Lister):
	log = logging.getLogger(__name__)

	def take_action(self, parsed_args):
		home = expanduser("~")
		filename = os.path.join(home, '.bitbucket.py')
		creds = imp.load_source('.bitbucket', filename)
		user = creds.username
		passwd = creds.passwd
		url = "https://bitbucket.org/api/1.0/user/repositories/"
		r = requests.get(url, auth=(user, passwd))
		data = json.loads(r.text)
		return (('Owner', 'Repo Name', 'Created On' ),
			((i['owner'], i['name'], i['created_on']) for i in data)
			)

class Repodetail(Command):
	log = logging.getLogger(__name__)

	def take_action(self, parsed_args):
		print parsed_argsx
