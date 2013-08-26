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
			print "\nRepository " + "'" + parsed_args.reponame + "'" " Created.\n"
			return (columns, data)
		elif r.status_code == 400:
			self.app.stdout.write("\n Error: " + "'" + str(r.status_code) + "'" + " You already have a repository with name " + "'" + parsed_args.reponame + "'" + ".\n")
			sys.exit(0)
		else:
			self.app.stdout.write('\nError: Bad request.\n')
			sys.exit(1)


class Repoedit(ShowOne):
	log = logging.getLogger(__name__ + '.Repoedit')

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
	log = logging.getLogger(__name__ + '.Repodelete')

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
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')


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
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '" or Repository Name ' + '"' + parsed_args.reponame + '"' + '\n\n')


class Repodeploykeysget(Command):
	log = logging.getLogger(__name__ + '.Repodeploykeysget')
			
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
	log = logging.getLogger(__name__ + '.Repodeploykeyspost')
			
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
	log = logging.getLogger(__name__ + '.Repodeploykeysedit')
			
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
	log = logging.getLogger(__name__ + '.Repodeploykeysdelete')
			
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


class Repofork(Command):
	log = logging.getLogger(__name__ + '.Repofork')
			
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
