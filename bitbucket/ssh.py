import logging
import requests
import os
import sys
import getpass
import json
import imp
import argparse
import prettytable
from os.path import expanduser
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne


home = expanduser("~")
filename = os.path.join(home, '.bitbucket.py')
creds = imp.load_source('.bitbucket', filename)
user = creds.username
passwd = creds.passwd


class Sshkeyget(Command):
	log = logging.getLogger(__name__ + '.Sshkeyget')

	def get_parser(self, prog_name):
		parser = super(Sshkeyget, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--key_id', '-i', metavar='<key_id>', help='Get individual key from key id')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		if parsed_args.key_id:
			url = "https://bitbucket.org/api/1.0/users/%s/ssh-keys/%s" % (parsed_args.account,parsed_args.key_id)
			r = requests.get(url, auth=(user,passwd))
			if r.status_code == 200:
				data = json.loads(r.text)
				print "\nKey ID: %s" % (parsed_args.key_id)
				print "Key: %s" % (data['key'])
				print "Key Label: %s" % (data['label'])
				sys.exit(0)
			else:
				self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request\n\n')
				sys.exit(1)
		else:
			url = "https://bitbucket.org/api/1.0/users/%s/ssh-keys/" % (parsed_args.account)
			r = requests.get(url, auth=(user,passwd))
			if r.status_code == 200:
				data = json.loads(r.text)
				for key in data:
					print "\nKey ID: %s" % (key['pk'])
					print "Key: %s" % (key['key'])
					print "Key Label: %s" % (key['label'])
					print "======================================================="
				sys.exit(0)
			else:
				self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request\n\n')
				sys.exit(1)


class Sshkeypost(Command):
	log = logging.getLogger(__name__ + '.Sshkeypost')

	def get_parser(self, prog_name):
		parser = super(Sshkeypost, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--key', '-k', required=True, metavar='<key>', help='Ssh key')
		parser.add_argument('--label', '-l', required=True, metavar='<key_lebel>', help='name or label of key')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		args = {}
		args['key'] = parsed_args.key
		args['label'] = parsed_args.label

		url = "https://bitbucket.org/api/1.0/users/%s/ssh-keys/" % (parsed_args.account)
		r = requests.post(url, data=args, auth=(user,passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n Key added to your account"
			print "\nKey ID: %s" % (data['pk'])
			print "Key: %s" % (data['key'])
			print "Key Label: %s" % (data['label'])
			sys.exit(0)
		elif r.status_code == 400:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Someone has already registered that SSH key\n\n')
			sys.exit(1)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request\n\n')
			sys.exit(1)


class Sshkeydelete(Command):
	log = logging.getLogger(__name__ + '.Sshkeydelete')

	def get_parser(self, prog_name):
		parser = super(Sshkeydelete, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--key_id', '-i', required=True, metavar='<key_id>', help='Delete key from key id')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/users/%s/ssh-keys/%s" % (parsed_args.account,parsed_args.key_id)
		r = requests.delete(url, auth=(user,passwd))
		if r.status_code == 204:
			print "\n Key ID " + "'" + str(parsed_args.key_id) + "'" + " deleted.\n"
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request\n\n')
			sys.exit(1)