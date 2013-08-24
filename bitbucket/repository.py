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


class Repocreate(ShowOne):
	log = logging.getLogger(__name__ + '.Repocreate')

	def get_parser(self, prog_name):
		parser = super(Repocreate, self).get_parser(prog_name)
		parser.add_argument('--reponame', '-r', required=True, metavar='<reponame>', help='The repository name')
		parser.add_argument('--description', '-d', metavar='<description>', help='The repository description')
		parser.add_argument('--is_private', '-p', metavar='<is_private>', choices=['true', 'false'], required=False, help='repository is private ?')
		parser.add_argument('--scm', '-s', metavar='<scm>', choices=['git', 'hg'], required=False, help='The repository scm')
		parser.add_argument('--has_issues', '-i', metavar='<has_issues>', choices=['true', 'false'], required=False, help='The repository has issues ?')
		parser.add_argument('--has_wiki', '-w', metavar='<has_wiki>', choices=['true', 'false'], required=False, help='The repository has wiki ?')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		args = {}

		if parsed_args.reponame:
			args['name'] = parsed_args.reponame

		if parsed_args.description:
			args['description'] = parsed_args.description

		if parsed_args.is_private:
			args['is_private'] = parsed_args.is_private

		if parsed_args.scm:
			args['scm'] = parsed_args.scm

		if parsed_args.has_issues:
			args['has_issues'] = parsed_args.has_issues

		if parsed_args.has_wiki:
			args['has_wiki'] = parsed_args.has_wiki

		url = "https://bitbucket.org/api/1.0/repositories"		
		r = requests.post(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			data.pop('logo')
			data.pop('resource_uri')
			columns = data.viewkeys()
			data = data.viewvalues()
			print "\nRepository " + "'" + parsed_args.reponame + "'" "Created.\n"
			return (columns, data)
		elif r.status_code == 400:
			self.app.stdout.write("\n Error: " + "'" + str(r.status_code) + "'" + " You already have a repository with name " + "'" + parsed_args.reponame + "'" + ".\n")
			sys.exit(0)
		else:
			self.app.stdout.write('\nError: Bad request.\n')
			sys.exit(1)


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