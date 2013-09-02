
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
import prettytable
from os.path import expanduser
from cliff.command import Command


try:
	home = expanduser("~")
	filename = os.path.join(home, '.bitbucket.py')
	creds = imp.load_source('.bitbucket', filename)
	user = creds.username
	passwd = creds.passwd
except (IOError, NameError):
	pass


class Changesetget(Command):
	"""
	* Get list of changeset
	"""
	log = logging.getLogger(__name__ + '.Changesetget')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
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
	"""
	* Get commit details from commit id
	"""
	log = logging.getLogger(__name__ + '.Commitget')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
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


class Changesetcommentsget(Command):
	"""
	* Get comments for changeset
	"""
	log = logging.getLogger(__name__ + '.Changesetcommentsget')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def get_parser(self, prog_name):
		parser = super(Changesetcommentsget, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--commit', '-c', metavar='<commit_id>', required=True, help='The commit id or commit hash')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets/%s/comments/" % (parsed_args.account,parsed_args.reponame,parsed_args.commit)

		r = requests.get(url, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			for comment in data:
				if not 'content' in comment:
					print "\n No Any Comments Found.\n"
					sys.exit(1)
			else:
				for comment in data:
					print "\nCommit ID: %s\n" % (comment['node'])
					print "Comment: %s\n" % (comment['content'])
					newdata = prettytable.PrettyTable(["Fields", "Values"])
					newdata.add_row(["Name", comment['display_name']])
					newdata.add_row(["Comment ID", comment['comment_id']])
					newdata.add_row(["Created On", comment['utc_created_on']])
					newdata.add_row(["Updated On", comment['utc_last_updated']])
					print newdata
					print "------------------------------------------------------"

				sys.exit(0)
		else:
			print "\n Error: Invalid request, or invalid commit id"
			sys.exit(1)


class Changesetcommentpost(Command):
	"""
	* Add new comment for changeset
	"""
	log = logging.getLogger(__name__ + '.Changesetcommentpost')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)

	def get_parser(self, prog_name):
		parser = super(Changesetcommentpost, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--commit', '-c', metavar='<commit_id>', required=True, help='The commit id or commit hash')
		parser.add_argument('--comment', '-C', metavar='<comment>', required=True, help='The comment content')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets/%s/comments/" % (parsed_args.account,parsed_args.reponame,parsed_args.commit)

		args = {}
		args['content'] = parsed_args.comment
		r = requests.post(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\nCommit ID: %s\n" % (data['node'])
			print "Comment: %s\n" % (data['content'])
			newdata = prettytable.PrettyTable(["Fields", "Values"])
			newdata.add_row(["Name", data['display_name']])
			newdata.add_row(["Comment ID", data['comment_id']])
			newdata.add_row(["Created On", data['utc_created_on']])
			newdata.add_row(["Updated On", data['utc_last_updated']])
			print newdata
			sys.exit(0)
		else:
			print "\n Error: Invalid request, or invalid commit id"
			sys.exit(1)


class Changesetcommentdelete(Command):
	"""
	* Delete comment for changeset
	"""
	log = logging.getLogger(__name__ + '.Changesetcommentdelete')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)

	def get_parser(self, prog_name):
		parser = super(Changesetcommentdelete, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--commit', '-c', metavar='<commit_id>', required=True, help='The commit id or commit hash')
		parser.add_argument('--comment_id', '-id', metavar='<comment_id>', required=True, help='The comment content id')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets/%s/comments/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.commit,parsed_args.comment_id)

		r = requests.delete(url, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\nCommit ID: %s\n" % (data['node'])
			print "Comment ID: %s" % (data['comment_id'])
			print "Comment " + "'" + str(data['comment_id']) + "'" " deleted successfully."
			sys.exit(0)
		else:
			print "\n Error: Invalid request, or invalid commit id or invalid comment id."
			sys.exit(1)