import logging
import requests
import os
import sys
import getpass
import json
from os.path import expanduser
from cliff.command import Command


class Login(Command):
	log = logging.getLogger(__name__)

	def take_action(self, parsed_args):
		home = expanduser("~")
		filename = os.path.join(home, '.bitbucket.py')
		url = "https://bitbucket.org/api/1.0/user/"
		user = raw_input('Enter BitBucket Username or Email [%s]:' % getpass.getuser())
		if not user:
			user = getpass.getuser()

		p1 = getpass.getpass('Enter Password: ')
		p2 = getpass.getpass('Retype Password: ')
		if p1 != p2:
			print "Password do not match. Try Again.\n"
			sys.exit(2)
		else:
			passwd = p1
		r = requests.get(url, auth=(user, passwd))
		status = r.status_code
		if status != 200:
			print "Authentication Error. Invalid Username or Password.\n"
		else:
			f = open(filename,'w')
			f.write("username = " + "'" + user + "'" + "\n")
			f.write("passwd = " + "'" + p1 + "'" + "\n")
			print("Login Successful.\n")
			data = json.loads(r.text)
			print "Username: " + data['user']['username']
			print "Display Name: " + data['user']['display_name']

class Authentication(Command):
	def take_action(self, parsed_args):
		home = expanduser("~")
		filename = os.path.join(home, '.bitbucket.py')
		if not os.path.exists(filename):
			Login()
		else:
			print "Logged In \n\n"
			return

		