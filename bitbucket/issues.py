import os
import sys
import getpass
import json
import imp
import argparse
import logging
import requests
import urllib
from os.path import expanduser
from cliff.show import ShowOne
from cliff.command import Command
from cliff.lister import Lister


home = expanduser("~")
filename = os.path.join(home, '.bitbucket.py')
creds = imp.load_source('.bitbucket', filename)
user = creds.username
passwd = creds.passwd


class Getissue(ShowOne):
	log = logging.getLogger(__name__ + '.Getissue')

	def get_parser(self, prog_name):
		parser = super(Getissue, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>',  required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>',  required=True, help='The repository name')
		parser.add_argument('--status', '-s', metavar='<issue status>', choices=['new', 'open', 'resolved', 'on hold', 'invalid', 'duplicate', 'wontfix'], required=False, help='The list of issues sort by  status')
		parser.add_argument('--kind', '-k', metavar='<kind>', choices=['bug', 'enhancement', 'proposal', 'task'], required=False, help='The list of issues sort by kind')
		parser.add_argument('--priority', '-p', metavar='<priority>', choices=['trivial', 'minor', 'major', 'critical', 'blocker'], required=False, help='The list of issues sort by priority')
		parser.add_argument('--reported_by', '-b', metavar='<reported_by>', required=False, help='The list of issues sort by reported_by')
		parser.add_argument('--is_spam', '-i', metavar='<true or false>', choices=['true', 'false'], required=False, help='The list of issues marked as spam')
		parser.add_argument('--search', '-e', metavar='<search string>', required=False, help='Search issues based on search string')
		parser.add_argument('--id', metavar='<issue_id>', type=int, required=False, help='Get issue details from issue id')
		parser.add_argument('--followers', '-o', action='store_true', required=False, help='Get follower details from issue id')
		return parser	

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
 		
		args = {}
		args_id = {}
		args_followers = {}

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
		data = json.loads(r.text)
		
		if issuelist_url != {} and issuedetail_url == {} and issuefilter_url == {} and issuefollowers_url == {}:
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
		