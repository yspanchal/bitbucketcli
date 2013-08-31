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


home = expanduser("~")
filename = os.path.join(home, '.bitbucket.py')
creds = imp.load_source('.bitbucket', filename)
user = creds.username
passwd = creds.passwd


class Groups(Command):
	log = logging.getLogger(__name__ + '.Groups')

	def get_parser(self, prog_name):
		parser = super(Groups, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--name', '-n', metavar='<group_name>', help='The group name')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/groups/%s/" % (parsed_args.account)
		r = requests.get(url, auth=(user,passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			if len(data) != 0:
				for group in data:
					newdata = prettytable.PrettyTable(["Group Name", "Members"])
					newdata.padding_width = 1
					newdata.add_row([group['name'],""])
					for member in group['members']:
						newdata.add_row(["", member['username']])
					print newdata
				sys.exit(0)
			else:
				print "\n No groups found.\n"
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '\n\n')
			sys.exit(1)


class Creategroup(Command):
	log = logging.getLogger(__name__ + '.Creategroup')

	def get_parser(self, prog_name):
		parser = super(Creategroup, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--name', '-n', required=True, metavar='<group name>', help='The group name')
		parser.add_argument('--permission', '-p', required=True, metavar='<repo_permission>', choices=['read', 'write', 'admin'], help='The group name')
		parser.add_argument('--autoadd', '-A', metavar='<auto_add>', choices=['true', 'false'], help='Auto add')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/groups/%s/" % parsed_args.account

		args = {}
		args['name'] = parsed_args.name
		args['permission'] = parsed_args.permission

		if parsed_args.autoadd:
			args['auto_add'] = parsed_args.autoadd

		r = requests.post(url, data=args, auth=(user,passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n New group created."
			print "\nGroup Name: %s" % (data['name'])
			print "Group Owner: %s" % (data['owner']['username'])
			print "Group Permission: %s\n" % (data['permission'])
			sys.exit(0)
		elif r.status_code == 400:
			print "\n Error: " + str(r.status_code) + " Bad request."
			print "\n A group with name " + "'" + parsed_args.name + "'" + " already exists.\n"
			sys.exit(1)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request, Invalid Account name ' + '"' +  parsed_args.account + '\n\n')
			sys.exit(1)


class Deletegroup(Command):
	log = logging.getLogger(__name__ + '.Deletegroup')

	def get_parser(self, prog_name):
		parser = super(Deletegroup, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--name', '-n', required=True, metavar='<group name>', help='The group name')
		return parser

	def take_action(self, parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/groups/%s/%s/" % (parsed_args.account,parsed_args.name)

		r = requests.delete(url, auth=(user,passwd))
		if r.status_code == 204:
			print "\n Group " + "'" + parsed_args.name + "'" + " deleted.\n"
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request \n\n')
			sys.exit(1)


class Groupmembers(Command):
	log = logging.getLogger(__name__ + '.Groupmembers')

	def get_parser(self, prog_name):
		parser = super(Groupmembers, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--name', '-n', required=True, metavar='<group name>', help='The group name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/groups/%s/%s/members/" % (parsed_args.account,parsed_args.name)

		r = requests.get(url, auth=(user,passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n Group Name: %s" % (parsed_args.name)
			newdata = prettytable.PrettyTable()
			newdata.padding_width = 1
			newdata.add_column("Members", [i['username'] for i in data])
			print newdata
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request \n\n')
			sys.exit(1)


class Addgroupmember(Command):
	log = logging.getLogger(__name__ + '.Addgroupmember')

	def get_parser(self, prog_name):
		parser = super(Addgroupmember, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--name', '-n', required=True, metavar='<group_name>', help='The group name')
		parser.add_argument('--member', '-m', required=True, metavar='<member_account>', help='The member name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/groups/%s/%s/members/%s/" % (parsed_args.account,parsed_args.name,parsed_args.member)

		r = requests.put(url, auth=(user,passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n User " + "'" + parsed_args.member + "'" + " added to group " + "'" + parsed_args.name + "'\n"
			sys.exit(0)
		elif r.status_code == 409:
			print "\n 'Conflict/Duplicate' User " + "'" + parsed_args.member + "'" + " present in group\n"
			sys.exit(1)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request \n\n')
			sys.exit(1)


class Deletegroupmember(Command):
	log = logging.getLogger(__name__ + '.Deletegroupmember')

	def get_parser(self, prog_name):
		parser = super(Deletegroupmember, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', required=True, metavar='<account>', help='The account name')
		parser.add_argument('--name', '-n', required=True, metavar='<group_name>', help='The group name')
		parser.add_argument('--member', '-m', required=True, metavar='<member_account>', help='The member name')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/groups/%s/%s/members/%s/" % (parsed_args.account,parsed_args.name,parsed_args.member)

		r = requests.delete(url, auth=(user,passwd))
		if r.status_code == 204:
			print "\n User " + "'" + parsed_args.member + "'" + " removed from group " + "'" + parsed_args.name + "'\n"
			sys.exit(0)
		else:
			self.app.stdout.write('\n Error: '+ '"' + str(r.status_code) + '"' + ' Invalid request \n\n')
			sys.exit(1)