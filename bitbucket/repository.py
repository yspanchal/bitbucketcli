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

class Repolist(Lister):
	log = logging.getLogger(__name__ + '.Repolist')

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
		url = "https://bitbucket.org/api/1.0/user/repositories/"
		r = requests.get(url, auth=(user, passwd))
		data = json.loads(r.text)
		return (('Owner', 'Repo Name', 'Created On' ),
			((i['owner'], i['name'], i['created_on']) for i in data)
			)

class Repodetail(ShowOne):
	log = logging.getLogger(__name__ + '.Repodetail')

	def get_parser(self, prog_name):
		parser = super(Repodetail, self).get_parser(prog_name)
		parser.add_argument('--reponame', '-r', required=True, metavar='<reponame>', help='The repository name')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
		url = "https://bitbucket.org/api/1.0/user/repositories/"		
		r = requests.get(url, auth=(user, passwd))
		data = json.loads(r.text)
		for i in data:
			if i['name'] == parsed_args.reponame:
				i.pop('logo')
				i.pop('resource_uri')
				columns = i.viewkeys()
				data = i.viewvalues()
				return (columns, data)
		self.app.stdout.write('\nError: ' + '"' + parsed_args.reponame + '"' + ' No such repository found.\n\n')
		sys.exit(1)

class Repotag(Command):
	log = logging.getLogger(__name__ + '.Repotag')
			
	def get_parser(self, prog_name):
		parser = super(Repotag, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/tags/" % (parsed_args.account,parsed_args.reponame)
		r = requests.get(url, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			if data == {}:
				self.app.stdout.write('\nNo Tags Found for ' + '"' + parsed_args.reponame + '"' + '.\n\n')
				sys.exit(0)
			else:
				for i in data:
					newdata = prettytable.PrettyTable(["Fields", "Values"])
					newdata.padding_width = 1
					newdata.add_row(["Tag Name", i])
					newdata.add_row(["Author", data[i]['raw_author']])
					newdata.add_row(["TimeStamp", data[i]['timestamp']])
					newdata.add_row(["Commit ID", data[i]['raw_node']])
					newdata.add_row(["Message", data[i]['message']])
					print newdata
		else:
			self.app.stdout.write('\nInvalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')


class Repobranch(Command):
	log = logging.getLogger(__name__ + '.Repobranch')
			
	def get_parser(self, prog_name):
		parser = super(Repobranch, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/branches" % (parsed_args.account,parsed_args.reponame)
		r = requests.get(url, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			if data == {}:
				self.app.stdout.write('\nNo branches Found for ' + '"' + parsed_args.reponame + '"' + '.\n\n')
				sys.exit(0)
			else:
				for i in data:
					newdata = prettytable.PrettyTable(["Fields", "Values"])
					newdata.padding_width = 1
					newdata.add_row(["Branch Name", i])
					newdata.add_row(["Author", data[i]['raw_author']])
					newdata.add_row(["TimeStamp", data[i]['timestamp']])
					newdata.add_row(["Commit ID", data[i]['raw_node']])
					newdata.add_row(["Message", data[i]['message']])
					print newdata
		else:
			self.app.stdout.write('\nInvalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')