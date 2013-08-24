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


class Changesetget(Command):
	log = logging.getLogger(__name__ + '.Changesetget')
			
	def get_parser(self, prog_name):
		parser = super(Changesetget, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--limit', '-l', metavar='<limit>', required=True, type=int, help='The limit number')
		parser.add_argument('--start', '-s', metavar='<start node>', help='The start node hash')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		if parsed_args.start:
			url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets?limit=%s&start=%s" % (parsed_args.account,parsed_args.reponame,parsed_args.limit,parsed_args.start)
		else:
			url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets?limit=%s" % (parsed_args.account,parsed_args.reponame,parsed_args.limit)

		r = requests.get(url, auth=(user, passwd))
		if r.status_code != 200:
			print "\n Error: '%s' No Changeset Found." % (r.status_code)
			sys.exit(1)
		else:
			data = json.loads(r.text)
			print "\nTotal Changeset: %s, Start: %s, Limit: %s\n" % (data['count'],data['start'],data['limit'])

			for i in data['changesets']:
				newdata = prettytable.PrettyTable(["Type", "File"])
				newdata.padding_width = 1
				for f in i['files']:
					newdata.add_row([f['type'], f['file']])

				print newdata
				print "Author: %s" % (i['author'])
				print "Timestamp: %s" % (i['timestamp'])
				print "Commit ID: %s" % (i['raw_node'])
				print "Commit Message: %s" % (i['message'])
				print "-------------------------------------------------------"


class Commitget(Command):
	log = logging.getLogger(__name__ + '.Commitget')
			
	def get_parser(self, prog_name):
		parser = super(Commitget, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--commit', '-c', metavar='<commit_id>', required=True, help='The commit id or commit hash')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.commit)
		
		r = requests.get(url, auth=(user, passwd))
		if r.status_code != 200:
			print "\n Error: '%s' No Commit ID Found." % (r.status_code)
			sys.exit(1)
		else:
			data = json.loads(r.text)
			print "\nCommit ID: %s\n" % (data['raw_node'])

			for i in data['files']:
				newdata = prettytable.PrettyTable(["Type", "File"])
				newdata.padding_width = 1
				newdata.add_row([i['type'], i['file']])

			print newdata
			print "Author: %s" % (data['author'])
			print "Timestamp: %s" % (data['timestamp'])
			print "Branches: %s" % (data['branches'])
			print "Commit Message: %s" % (data['message'])
			print "-------------------------------------------------------"