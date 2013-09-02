
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
import csv
import json
import imp
import urllib
import tablib
import argparse
import logging
import requests
import prettytable
from os.path import expanduser
from cliff.command import Command
from cliff.show import ShowOne

try:
	home = expanduser("~")
	filename = os.path.join(home, '.bitbucket.py')
	creds = imp.load_source('.bitbucket', filename)
	user = creds.username
	passwd = creds.passwd
except (IOError, NameError):
	pass


class Getissue(ShowOne):
	"""
	* Get list of issues
	"""
	log = logging.getLogger(__name__ + '.Getissue')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def get_parser(self, prog_name):
		parser = super(Getissue, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--limit', '-l', metavar='<issue limit>', type=int, help='The number of issue to get, you can choose 0-50, default is 15')
		parser.add_argument('--status', '-s', metavar='<issue status>', choices=['new', 'open', 'resolved', 'on hold', 'invalid', 'duplicate', 'wontfix'], required=False, help='The list of issues sort by  status')
		parser.add_argument('--kind', '-k', metavar='<kind>', choices=['bug', 'enhancement', 'proposal', 'task'], required=False, help='The list of issues sort by kind')
		parser.add_argument('--priority', '-p', metavar='<priority>', choices=['trivial', 'minor', 'major', 'critical', 'blocker'], required=False, help='The list of issues sort by priority')
		parser.add_argument('--reported_by', '-R', metavar='<reported_by>', required=False, help='The list of issues sort by reported_by')
		parser.add_argument('--is_spam', '-I', metavar='<true or false>', choices=['true', 'false'], required=False, help='The list of issues marked as spam')
		parser.add_argument('--search', '-S', metavar='<search string>', required=False, help='Search issues based on search string')
		parser.add_argument('--id', '-i', metavar='<issue_id>', type=int, required=False, help='Get issue details from issue id')
		parser.add_argument('--followers', '-F', action='store_true', required=False, help='Get follower details from issue id')
		parser.add_argument('--export', '-x', action='store_true', help='Export as CSV [Note:Does not work with issue detail & issue followers]')
		return parser	

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
 		
		args = {}
		args_id = {}
		args_followers = {}

		if parsed_args.limit:
			args['limit'] = parsed_args.limit

		if parsed_args.status:
			args['status'] = parsed_args.status

		if parsed_args.kind:
			args['kind'] = parsed_args.kind

		if parsed_args.priority:
			args['priority'] = parsed_args.priority

		if parsed_args.reported_by:
			args['reported_by'] = parsed_args.reported_by

		if parsed_args.is_spam:
			args['is_spam'] = parsed_args.is_spam

		if parsed_args.search:
			args['search'] = parsed_args.search

		if parsed_args.id:
			args_id['id'] = parsed_args.id

		if parsed_args.followers:
			args_followers['followers'] = parsed_args.followers

		issuelist_url = {}
		issuedetail_url = {}
		issuefilter_url = {}
		issuefollowers_url = {}

		if args == {} and args_id == {} and args_followers == {}:
			url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/?" % (parsed_args.account,parsed_args.reponame)
			issuelist_url['url'] = url
		elif args == {} and args_followers == {} and args_id != {}:
			url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.id)
			issuedetail_url['url'] = url
		elif args_id == {} and args_followers == {} and args != {}:
			primaryurl = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/?" % (parsed_args.account,parsed_args.reponame)
			params = urllib.urlencode(args)
			url = primaryurl + params
			issuefilter_url['url'] = url
		elif args == {} and args_id != {} and args_followers != {}:
			url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/%s/followers" % (parsed_args.account,parsed_args.reponame,parsed_args.id)
			issuefollowers_url['url'] = url
		else:
			self.app.stdout.write('\nInvalid argument supplied.\n')
			sys.exit(1)

		r = requests.get(url, auth=(user, passwd))
		
		try:
			data = json.loads(r.text)
		except:
			print "\n Error: '404' No Issues Found 'or' Invalid argument supplied.\n"
			sys.exit(1)
		
		if issuelist_url != {} and issuedetail_url == {} and issuefilter_url == {} and issuefollowers_url == {}:
			if parsed_args.export:
				csvdata = tablib.Dataset()
				csvdata.headers = ["ID", "Status", "Kind", "Priority", "Version", "Component", "Milestone", "Reported By", "Created On", "Last Updated", "Responsible", "Comment Count", "is_spam", "Followers Count"]
				
				with open('issues.xls', 'wb') as f:
					for i in data['issues']:
						row = []
						if i.has_key('local_id'):
							row.append(i['local_id'])
						else:
							row.append('None')

						if i.has_key('status'):
							row.append(i['status'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['kind'])
						else:
							row.append('None')

						if i.has_key('priority'):
							row.append(i['priority'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['version'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['component'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['milestone'])
						else:
							row.append('None')

						if i.has_key('reported_by'):
							row.append(i['reported_by']['username'])
						else:
							row.append('None')

						if i.has_key('utc_created_on'):
							row.append(i['utc_created_on'])
						else:
							row.append('None')

						if i.has_key('utc_last_updated'):
							row.append(i['utc_last_updated'])
						else:
							row.append('None')

						if i.has_key('responsible'):
							row.append(i['responsible']['username'])
						else:
							row.append('None')

						if i.has_key('comment_count'):
							row.append(i['comment_count'])
						else:
							row.append('None')

						if i.has_key('is_spam'):
							row.append(i['is_spam'])
						else:
							row.append('None')

						if i.has_key('follower_count'):
							row.append(i['follower_count'])
						else:
							row.append('None')

						csvdata.append(row)
					f.write(csvdata.csv)
					f.close()
					print "\n CSV File created.\n"
					sys.exit(0)
			else:
				print "\nTotal Issues: %s\n" % (data['count'])
				for i in data['issues']:
					print """Issue_ID: %s\nIssue_Status: %s\nIssue_Title: %s\n=======================================================================""" %(i['local_id'],i['status'],i['title'])
		    	sys.exit(0)	
		elif issuedetail_url != {} and issuelist_url == {} and issuefilter_url == {} and issuefollowers_url == {}:
			newdata = {}
			newdata['issue id'] = data['local_id']
			newdata['status'] = data['status']
			newdata['kind'] = data['metadata']['kind']
			newdata['priority'] = data['priority']
			newdata['version'] = data['metadata']['version']
			newdata['component'] = data['metadata']['component']
			newdata['milestone'] = data['metadata']['milestone']
			newdata['reported by'] = data['reported_by']['username']
			newdata['utc_created_on'] = data['utc_created_on']
			newdata['utc_last_updated'] = data['utc_last_updated']
			newdata['responsible'] = data['responsible']['username']
			newdata['created on'] = data['created_on']
			newdata['comment_count'] = data['comment_count']
			newdata['is_spam'] = data['is_spam']
			newdata['follower_count']  = data['follower_count']
			columns = newdata.viewkeys()
			columndata = newdata.viewvalues()
			print "\nTitle: %s\n" % (data['title'])
			print "Content: %s\n" % (data['content'])
			return (columns, columndata)
		elif issuefilter_url != {} and issuelist_url == {} and issuedetail_url == {} and issuefollowers_url == {}:
			if parsed_args.export:
				csvdata = tablib.Dataset()
				csvdata.headers = ["ID", "Status", "Kind", "Priority", "Version", "Component", "Milestone", "Reported By", "Created On", "Last Updated", "Responsible", "Title", "Content", "Comment Count", "is_spam", "Followers Count"]
				
				with open('issues.xls', 'wb') as f:
					for i in data['issues']:
						row = []
						if i.has_key('local_id'):
							row.append(i['local_id'])
						else:
							row.append('None')

						if i.has_key('status'):
							row.append(i['status'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['kind'])
						else:
							row.append('None')

						if i.has_key('priority'):
							row.append(i['priority'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['version'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['component'])
						else:
							row.append('None')

						if i.has_key('metadata'):
							row.append(i['metadata']['milestone'])
						else:
							row.append('None')

						if i.has_key('reported_by'):
							row.append(i['reported_by']['username'])
						else:
							row.append('None')

						if i.has_key('utc_created_on'):
							row.append(i['utc_created_on'])
						else:
							row.append('None')

						if i.has_key('utc_last_updated'):
							row.append(i['utc_last_updated'])
						else:
							row.append('None')

						if i.has_key('responsible'):
							row.append(i['responsible']['username'])
						else:
							row.append('None')

						if i.has_key('title'):
							row.append(i['title'])
						else:
							row.append('None')

						if i.has_key('content'):
							row.append(i['content'])
						else:
							row.append('None')

						if i.has_key('comment_count'):
							row.append(i['comment_count'])
						else:
							row.append('None')

						if i.has_key('is_spam'):
							row.append(i['is_spam'])
						else:
							row.append('None')

						if i.has_key('follower_count'):
							row.append(i['follower_count'])
						else:
							row.append('None')

						csvdata.append(row)
					f.write(csvdata.csv)
					f.close()
					print "\n CSV File created.\n"
				sys.exit(0)
			else:
				print "\nTotal Issues: %s\n" % (data['count'])
				for i in data['issues']:
					print """Issue_ID: %s\nIssue_Status: %s\nIssue_Title: %s\n=======================================================================""" %(i['local_id'],i['status'],i['title'])
				sys.exit(0)
		elif issuefollowers_url != {} and issuelist_url == {} and issuedetail_url == {} and issuefilter_url == {}:
			print "\nFollowers Count: %s\n" %(data['count'])
			for i in data['followers']:
				print "Followers Name: %s" % (i['username'])
			print "\n"
			sys.exit(0)
		else:
			print "Invalid Request no data received."		
			sys.exit(1)


class Createissue(ShowOne):
	"""
	* Create new issue
	"""
	log = logging.getLogger(__name__ + '.Createissue')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def get_parser(self, prog_name):
		parser = super(Createissue, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--title', '-t', metavar='<issue title>', required=True, help='Issue title')
		parser.add_argument('--content', '-d', metavar='<issue content>', required=False, help='Description about issue')
		parser.add_argument('--status', '-s', metavar='<issue status>', choices=['new', 'open', 'resolved', 'on hold', 'invalid', 'duplicate', 'wontfix'], required=False, help='The list of issues sort by  status')
		parser.add_argument('--kind', '-k', metavar='<kind>', choices=['bug', 'enhancement', 'proposal', 'task'], required=False, help='The list of issues sort by kind')
		parser.add_argument('--priority', '-p', metavar='<priority>', choices=['trivial', 'minor', 'major', 'critical', 'blocker'], required=False, help='The list of issues sort by priority')
		parser.add_argument('--responsible', '-R', metavar='<issue responsible>', required=False, help='The list of issues sort by reported_by')
		parser.add_argument('--component', '-C', required=False, help='A string containing a component value')
		parser.add_argument('--milestone', '-m', required=False, help='A string containing a milestone value')
		parser.add_argument('--version', '-v', required=False, help='A string containing a version value')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		args = {}

		if parsed_args.title:
			args['title'] = parsed_args.title

		if parsed_args.content:
			args['content'] = parsed_args.content

		if parsed_args.status:
			args['status'] = parsed_args.status

		if parsed_args.kind:
			args['kind'] = parsed_args.kind

		if parsed_args.priority:
			args['priority'] = parsed_args.priority

		if parsed_args.responsible:
			args['responsible'] = parsed_args.responsible

		if parsed_args.component:
			args['component'] = parsed_args.component

		if parsed_args.milestone:
			args['milestone'] = parsed_args.milestone

		if parsed_args.version:
			args['version'] = parsed_args.version

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues" % (parsed_args.account,parsed_args.reponame)

		r = requests.post(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)

			newdata = {}
			newdata['issue id'] = data['local_id']
			newdata['status'] = data['status']
			newdata['kind'] = data['metadata']['kind']
			newdata['priority'] = data['priority']
			newdata['version'] = data['metadata']['version']
			newdata['component'] = data['metadata']['component']
			newdata['milestone'] = data['metadata']['milestone']
			newdata['reported by'] = data['reported_by']['username']
			newdata['utc_created_on'] = data['utc_created_on']
			newdata['utc_last_updated'] = data['utc_last_updated']
			newdata['created on'] = data['created_on']
			newdata['comment_count'] = data['comment_count']
			newdata['is_spam'] = data['is_spam']
			newdata['follower_count']  = data['follower_count']
			columns = newdata.viewkeys()
			columndata = newdata.viewvalues()
			print "\nNew Issue Created.\n"
			print "\nTitle: %s\n" % (data['title'])
			print "Content: %s\n" % (data['content'])
			return (columns, columndata)
		else:
			self.app.stdout.write("\nInvalid Request. Invalid argument supplied.\n")
			sys.exit(1)


class Editissue(ShowOne):
	"""
	* Edit existing issue
	"""
	log = logging.getLogger(__name__ + '.Editissue')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)

	def get_parser(self, prog_name):
		parser = super(Editissue, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--id', '-i', metavar='<issue id>', required=True, help='The Issue ID')
		parser.add_argument('--title', '-t', metavar='<issue title>', required=False, help='Issue title')
		parser.add_argument('--content', '-d', metavar='<issue content>',required=False, help='Description about issue')
		parser.add_argument('--status', '-s', metavar='<issue status>', choices=['new', 'open', 'resolved', 'on hold', 'invalid', 'duplicate', 'wontfix'], required=False, help='The list of issues sort by  status')
		parser.add_argument('--kind', '-k', metavar='<kind>', choices=['bug', 'enhancement', 'proposal', 'task'], required=False, help='The list of issues sort by kind')
		parser.add_argument('--priority', '-p', metavar='<priority>', choices=['trivial', 'minor', 'major', 'critical', 'blocker'], required=False, help='The list of issues sort by priority')
		parser.add_argument('--responsible', '-R', metavar='<issue responsible>', required=False, help='The list of issues sort by reported_by')
		parser.add_argument('--component', '-C', required=False, help='A string containing a component value')
		parser.add_argument('--milestone', '-m', required=False, help='A string containing a milestone value')
		parser.add_argument('--version', '-v', required=False, help='A string containing a version value')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		args = {}

		if parsed_args.title:
			args['title'] = parsed_args.title

		if parsed_args.content:
			args['content'] = parsed_args.content

		if parsed_args.status:
			args['status'] = parsed_args.status

		if parsed_args.kind:
			args['kind'] = parsed_args.kind

		if parsed_args.priority:
			args['priority'] = parsed_args.priority

		if parsed_args.responsible:
			args['responsible'] = parsed_args.responsible

		if parsed_args.component:
			args['component'] = parsed_args.component

		if parsed_args.milestone:
			args['milestone'] = parsed_args.milestone

		if parsed_args.version:
			args['version'] = parsed_args.version

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/%s/" % (parsed_args.account,parsed_args.reponame,parsed_args.id)

		r = requests.put(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)

			newdata = {}
			newdata['issue id'] = data['local_id']
			newdata['status'] = data['status']
			newdata['kind'] = data['metadata']['kind']
			newdata['priority'] = data['priority']
			newdata['version'] = data['metadata']['version']
			newdata['component'] = data['metadata']['component']
			newdata['milestone'] = data['metadata']['milestone']
			newdata['reported by'] = data['reported_by']['username']
			newdata['utc_created_on'] = data['utc_created_on']
			newdata['utc_last_updated'] = data['utc_last_updated']
			newdata['created on'] = data['created_on']
			newdata['comment_count'] = data['comment_count']
			newdata['is_spam'] = data['is_spam']
			newdata['follower_count']  = data['follower_count']
			columns = newdata.viewkeys()
			columndata = newdata.viewvalues()
			print "\nIssue Edited.\n"
			print "\nTitle: %s\n" % (data['title'])
			print "Content: %s\n" % (data['content'])
			return (columns, columndata)
		else:
			self.app.stdout.write("\nInvalid Request. Invalid argument supplied.\n")
			sys.exit(1)


class Deleteissue(Command):
	"""
	* Delete issue
	"""
	log = logging.getLogger(__name__ + '.Deleteissue')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)

	def get_parser(self, prog_name):
		parser = super(Deleteissue, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--id', '-i', metavar='<issue id>', required=True, help='The Issue ID')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/%s/" % (parsed_args.account,parsed_args.reponame,parsed_args.id)
		r = requests.delete(url, auth=(user, passwd))
		if r.status_code == 204:
			self.app.stdout.write("\nIssue Deleted Successfully.\n\n")
			sys.exit(0)
		else:
			print "\n" + r.text + "\n"
			self.app.stdout.write("Invalid Issue ID Supplied.\n\n")
			sys.exit(1)


class Getcomment(Command):
	"""
	* Get all comments for issue
	"""
	log = logging.getLogger(__name__ + '.Getcomment')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)

	def get_parser(self, prog_name):
		parser = super(Getcomment, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--id', '-i', metavar='<issue id>', required=True, help='The Issue ID')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/%s/comments/" % (parsed_args.account,parsed_args.reponame,parsed_args.id)
		r = requests.get(url, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			for comment in data:
				print "\n"
				print "Comment: %s" % (comment['content'])
				newdata = prettytable.PrettyTable(["Fields", "Values"])
				newdata.padding_width = 1
				newdata.add_row(["Comment Author", comment['author_info']['display_name']])
				newdata.add_row(["Comment ID", comment['comment_id']])
				newdata.add_row(["UTC Updated on", comment['utc_updated_on']])
				newdata.add_row(["UTC Created on", comment['utc_created_on']])
				print newdata
				print "---------------------------------------------------------------"
			sys.exit(0)
		else:
			self.app.stdout.write("\nInvalid Request. Invalid argument supplied.\n")
			sys.exit(1)


class Postcomment(Command):
	"""
	* Add new comment for issue
	"""
	log = logging.getLogger(__name__ + '.Postcomment')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def get_parser(self, prog_name):
		parser = super(Postcomment, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--id', '-i', metavar='<issue id>', required=True, help='The Issue ID')
		parser.add_argument('--content', '-c', metavar='<issue content>', required=True, help='The Issue Content')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/issues/%s/comments/" % (parsed_args.account,parsed_args.reponame,parsed_args.id)
		r = requests.post(url, data=parsed_args.content, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n"
			print "Comment: %s" % (data['content'])
			newdata = prettytable.PrettyTable(["Fields", "Values"])
			newdata.padding_width = 1
			newdata.add_row(["Comment Author", data['author_info']['display_name']])
			newdata.add_row(["Comment ID", data['comment_id']])
			newdata.add_row(["UTC Updated on", data['utc_updated_on']])
			newdata.add_row(["UTC Created on", data['utc_created_on']])
			print newdata
			print "---------------------------------------------------------------"
			sys.exit(0)
		else:
			self.app.stdout.write("\nInvalid Request. Invalid argument supplied.\n")
			sys.exit(1)