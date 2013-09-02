
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
from cliff.lister import Lister
from cliff.show import ShowOne

try:
	home = expanduser("~")
	filename = os.path.join(home, '.bitbucket.py')
	creds = imp.load_source('.bitbucket', filename)
	user = creds.username
	passwd = creds.passwd
except (IOError, NameError):
	pass



class Repocreate(ShowOne):
	"""
	* Create new repository
	"""
	log = logging.getLogger(__name__ + '.Repocreate')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

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
			print "\nRepository " + "'" + parsed_args.reponame + "'" " Created.\n"
			return (columns, data)
		elif r.status_code == 400:
			self.app.stdout.write("\n Error: " + "'" + str(r.status_code) + "'" + " You already have a repository with name " + "'" + parsed_args.reponame + "'" + ".\n")
			sys.exit(0)
		else:
			self.app.stdout.write('\nError: Bad request.\n')
			sys.exit(1)


class Repoedit(ShowOne):
	"""
	* Edit existing repository information, add issues & wiki modules to repository 
	"""
	log = logging.getLogger(__name__ + '.Repoedit')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def get_parser(self, prog_name):
		parser = super(Repoedit, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--reponame', '-r', required=True, metavar='<reponame>', help='The repository name')
		parser.add_argument('--description', '-d', metavar='<description>', help='The repository description')
		parser.add_argument('--is_private', '-p', metavar='<is_private>', choices=['true', 'false'], required=False, help='repository is private ?')
		parser.add_argument('--has_issues', '-i', metavar='<has_issues>', choices=['true', 'false'], required=False, help='The repository has issues ?')
		parser.add_argument('--has_wiki', '-w', metavar='<has_wiki>', choices=['true', 'false'], required=False, help='The repository has wiki ?')
		parser.add_argument('--language', '-l', metavar='<language>', required=False, help='The repository language')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		args = {}

		if parsed_args.description:
			args['description'] = parsed_args.description

		if parsed_args.is_private:
			args['is_private'] = parsed_args.is_private

		if parsed_args.has_issues:
			args['has_issues'] = parsed_args.has_issues

		if parsed_args.has_wiki:
			args['has_wiki'] = parsed_args.has_wiki

		if parsed_args.language:
			args['language'] = parsed_args.language

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/" % (parsed_args.account,parsed_args.reponame)		
		r = requests.put(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			data.pop('logo')
			data.pop('resource_uri')
			columns = data.viewkeys()
			data = data.viewvalues()
			print "\nRepository " + "'" + parsed_args.reponame + "'" " Edited.\n"
			return (columns, data)
		if r.status_code == 400:
			print "'" + parsed_args.language + "'" + " is not valid language choice."
			sys.exit(1)
		else:
			self.app.stdout.write('\nError: Bad request.\n')
			sys.exit(1)


class Repodelete(Command):
	"""
	* Delete existing repository
	"""
	log = logging.getLogger(__name__ + '.Repodelete')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

	def get_parser(self, prog_name):
		parser = super(Repodelete, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The repository account name')
		parser.add_argument('--reponame', '-r', required=True, metavar='<reponame>', help='The repository name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
		url = "https://bitbucket.org/api/1.0/repositories/%s/%s" % (parsed_args.account,parsed_args.reponame)
		r = requests.delete(url, auth=(user, passwd))
		if r.status_code == 204:
			print "\n Repository " + "'" + parsed_args.reponame + "'" " Deleted.\n"
			sys.exit(0)
		else:
			print " Error: Invalid requests, " + "'" + str(r.status_code) + "'" + " or No such repository found."
			sys.exit(1)


class Repolist(Lister):
	"""
	* List all repository associated with users account 
	"""
	log = logging.getLogger(__name__ + '.Repolist')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)
		url = "https://bitbucket.org/api/1.0/user/repositories/"
		r = requests.get(url, auth=(user, passwd))
		data = json.loads(r.text)
		return (('Owner', 'Repo Name', 'Created On' ),
			((i['owner'], i['name'], i['created_on']) for i in data)
			)

class Repodetail(ShowOne):
	"""
	* Provide individual repository details
	"""
	log = logging.getLogger(__name__ + '.Repodetail')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	

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
	"""
	* Returns repository tags
	"""
	log = logging.getLogger(__name__ + '.Repotag')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
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
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')


class Repobranch(Command):
	"""
	* Returns repository branches
	"""
	log = logging.getLogger(__name__ + '.Repobranch')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
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
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')


class Repodeploykeysget(Command):
	"""
	* Get list of repository deployment keys
	"""
	log = logging.getLogger(__name__ + '.Repodeploykeysget')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Repodeploykeysget, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/deploy-keys/" % (parsed_args.account,parsed_args.reponame)

		r = requests.get(url, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			if len(data) != 0:
				for key in data:
					print "\nKey ID: %s" % (key['pk'])
					print "Key: %s" % (key['key'])
					print "Key Label: %s" % (key['label'])
					print "======================================================="
				sys.exit(0)
			else:
				print "\n No deployment key found.\n"
				sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)

class Repodeploykeyspost(Command):
	"""
	* Add new repository deployment key
	"""
	log = logging.getLogger(__name__ + '.Repodeploykeyspost')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Repodeploykeyspost, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--key', '-k', metavar='<key>', required=True, help='The repository deploy-key')
		parser.add_argument('--label', '-l', metavar='<key-label>', required=True, help='The repository deploy-key label')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/deploy-keys/" % (parsed_args.account,parsed_args.reponame)
		
		args = {}

		if parsed_args.key:
			args['key'] = parsed_args.key

		if parsed_args.label:
			args['label'] = parsed_args.label

		r = requests.post(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\nNew deployment key added."
			print "\nKey ID: %s\n" % (data['pk'])
			print "Key: %s\n" % (data['key'])
			print "Key Label: %s\n" % (data['label'])
			sys.exit(0)
		elif r.status_code == 400:
			print "\n Error: Someone has already registered this as an account SSH key.\n"
			sys.exit(1)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)


class Repodeploykeysedit(Command):
	"""
	* Edit existing repository deployment key
	"""
	log = logging.getLogger(__name__ + '.Repodeploykeysedit')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Repodeploykeysedit, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--key', '-k', metavar='<key>', required=True, help='The repository deploy-key')
		parser.add_argument('--label', '-l', metavar='<key-label>', required=True, help='The repository deploy-key label')
		parser.add_argument('--key_id', '-i', metavar='<key_id>', required=True, help='The repository deploy-key ID')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/deploy-keys/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.key_id)
		
		args = {}

		if parsed_args.key:
			args['key'] = parsed_args.key

		if parsed_args.label:
			args['label'] = parsed_args.label

		r = requests.put(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\nDeployment key edited."
			print "\nKey ID: %s\n" % (data['pk'])
			print "Key: %s\n" % (data['key'])
			print "Key Label: %s\n" % (data['label'])
			sys.exit(0)
		elif r.status_code == 400:
			print "\n Error: Someone has already registered this as an account SSH key.\n"
			sys.exit(1)
		else:
			self.app.stdout.write('\n Error: ' + '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)


class Repodeploykeysdelete(Command):
	"""
	* Delete existing repository deployment key
	"""
	log = logging.getLogger(__name__ + '.Repodeploykeysdelete')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Repodeploykeysdelete, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--key_id', '-i', metavar='<key_id>', required=True, help='The repository deploy-key ID')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/deploy-keys/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.key_id)

		r = requests.delete(url, auth=(user, passwd))
		if r.status_code == 204:
			print "\n Success: Repository deployment key " + "'" + parsed_args.key_id + "'" " deleted.\n"
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)


class Repofork(ShowOne):
	"""
	* Fork repository
	"""
	log = logging.getLogger(__name__ + '.Repofork')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Repofork, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--name', '-n', metavar='<name>', required=True, help='The repository name')
		parser.add_argument('--description', '-d', metavar='<description>', help='The repository description')
		parser.add_argument('--is_private', '-p', metavar='<is_private>', choices=['true', 'false'], help='The repository is private ?')
		parser.add_argument('--language', '-l', metavar='<language>', help='The repository language')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/fork/" % (parsed_args.account,parsed_args.reponame)

		args = {}

		args['name'] = parsed_args.name

		if parsed_args.description:
			args['description'] = parsed_args.description

		if parsed_args.is_private:
			args['is_private'] = parsed_args.is_private

		if parsed_args.language:
			args['language'] = parsed_args.language

		r = requests.post(url, data=args, auth=(user, passwd))

		if r.status_code == 200:
			data = json.loads(r.text)
			data.pop('logo')
			data.pop('resource_uri')
			data.pop('fork_of')
			columns = data.viewkeys()
			data = data.viewvalues()
			print "\nRepository " + "'" + parsed_args.reponame + "'" " Forked.\n"
			return (columns, data)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)


class Reporevision(Command):
	"""
	* Returns repository revision details
	"""
	log = logging.getLogger(__name__ + '.Reporevision')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Reporevision, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--revision', '-R', metavar='<revision>', required=True, help='The repository revision or branch name')
		parser.add_argument('--path', '-p', metavar='<path>', help='File or directory path')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		if parsed_args.path:
			url = "https://bitbucket.org/api/1.0/repositories/%s/%s/src/%s/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.revision,parsed_args.path)
		else:
			url = "https://bitbucket.org/api/1.0/repositories/%s/%s/src/%s/" % (parsed_args.account,parsed_args.reponame,parsed_args.revision)

		r = requests.get(url, auth=(user, passwd))

		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n Repository Source Details: \n"
			print "Revision: '%s'" % (data['node'])
			print "Path: '%s'" % (data['path'])
			print "directories: %s" % (data['directories'])
			print "Files: "
			for f in data['files']:
				newdata = prettytable.PrettyTable(["Fields", "Values"])
				newdata.padding_width = 1
				newdata.add_row(["Size", f['size']])
				newdata.add_row(["Path", f['path']])
				newdata.add_row(["TimeStamp", f['timestamp']])
				newdata.add_row(["Revision", f['revision']])
				print newdata
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)


class Reposharepost(Command):
	"""
	* Share repository with other users
	"""
	log = logging.getLogger(__name__ + '.Reposharepost')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Reposharepost, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--share', '-s', metavar='<share_with>', required=True, help='Share repository with user')
		parser.add_argument('--permission', '-p', metavar='<permission>', required=True, choices=['read', 'write', 'admin'], help='Repository permission')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/privileges/%s/%s/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.share)

		args = {}
		args['permission'] = parsed_args.permission
		r = requests.put(url, data=parsed_args.permission, auth=(user,passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n Repository " + "'" + parsed_args.reponame + "'" + " shared with " + "'" + parsed_args.share + "'"
			print "\nRepository: %s" % (data[0]['repo'])
			print "Shared with: %s" % (data[0]['user']['username'])
			print "Permission: %s" % (data[0]['privilege'])
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)


class Reposhareget(Command):
	"""
	* Get list of users repository shared with
	"""
	log = logging.getLogger(__name__ + '.Reposhareget')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Reposhareget, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/privileges/%s/%s" % (parsed_args.account,parsed_args.reponame)

		r = requests.get(url, auth=(user,passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			for i in data:
				print "\nRepository: %s" % (i['repo'])
				print "Shared with: %s" % (i['user']['username'])
				print "Permission: %s" % (i['privilege'])
				print "================================================"
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)


class Reposharedelete(Command):
	"""
	* Remove users access to repository
	"""
	log = logging.getLogger(__name__ + '.Reposharedelete')
	requests_log = logging.getLogger("requests")
	requests_log.setLevel(logging.WARNING)	
			
	def get_parser(self, prog_name):
		parser = super(Reposharedelete, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--share', '-s', metavar='<share_with>', required=True, help='Share repository with user')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/privileges/%s/%s/%s" % (parsed_args.account,parsed_args.reponame,parsed_args.share)

		r = requests.delete(url, auth=(user,passwd))
		if r.status_code == 204:
			print "\n Privileges for user " + "'" + parsed_args.share + "'" + " removed on repository " + "'" + parsed_args.reponame + "'"
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')
			sys.exit(1)