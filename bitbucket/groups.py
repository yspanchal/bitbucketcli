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


import sys
import json
import logging
import requests
import prettytable
from cliff.command import Command
from .utils import read_creds


class Groups(Command):

    """
    * Get list groups & respective members
    """
    log = logging.getLogger(__name__ + '.Groups')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Groups, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--name',
            '-n',
            metavar='<group_name>',
            help='The group name')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "groups/{a.account}/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            if len(data) != 0:
                for group in data:
                    newdata = prettytable.PrettyTable(["Group Name", "Members"])
                    newdata.padding_width = 1
                    newdata.add_row([group['name'], ""])
                    for member in group['members']:
                        newdata.add_row(["", member['username']])
                    print(newdata)
                sys.exit(0)
            else:
                print("\n No groups found.\n")
        else:
            self.app.stdout.write(
                '\n Error: ' + '"' + str(r.status_code) + '"' +
                ' Invalid request, Invalid Account name ' + '"' +
                parsed_args.account + '\n\n')
            sys.exit(1)


class Creategroup(Command):

    """
    * Create new group
    """
    log = logging.getLogger(__name__ + '.Creategroup')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Creategroup, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--name',
            '-n',
            required=True,
            metavar='<group name>',
            help='The group name')
        parser.add_argument(
            '--permission',
            '-p',
            required=True,
            metavar='<repo_permission>',
            choices=[
                'read',
                'write',
                'admin'],
            help='The group name')
        parser.add_argument(
            '--autoadd',
            '-A',
            metavar='<auto_add>',
            choices=[
                'true',
                'false'],
            help='Auto add')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "groups/{a.account}/").format(a=parsed_args)

        args = {}
        args['name'] = parsed_args.name
        args['permission'] = parsed_args.permission

        if parsed_args.autoadd:
            args['auto_add'] = parsed_args.autoadd
        user, passwd = read_creds()
        r = requests.post(url, data=args, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)

            msg = """
 New group created."

Group Name: {d[name]}
Group Owner: {d[owner][username]}
Group Permission: {d[permission]}
"""
            print(msg.format(d=data))
            sys.exit(0)
        elif r.status_code == 400:

            msg = """
 Error: {r.status_code} Bad request."

 A group with name '{a.name}' already exists.
"""
            print(msg.format(r=r, a=parsed_args))
            sys.exit(1)
        else:

            msg = """
 Error: "{r.status_code}" Invalid request, Invalid Account name "{a.account}"

"""
            self.app.stdout.write(msg.format(r=r, a=parsed_args))
            sys.exit(1)


class Deletegroup(Command):

    """
    * Delete existing group
    """
    log = logging.getLogger(__name__ + '.Deletegroup')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Deletegroup, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--name',
            '-n',
            required=True,
            metavar='<group name>',
            help='The group name')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "groups/{a.account}/{a.name}/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.delete(url, auth=(user, passwd))
        if r.status_code == 204:
            print("\n Group '{a.name}' deleted.\n".format(a=parsed_args))
            sys.exit(0)
        else:

            msg = """
 Error: "{r.status_code}" Invalid request

"""
            self.app.stdout.write(msg.format(r=r))
            sys.exit(1)


class Groupmembers(Command):

    """
    * Get members for group
    """
    log = logging.getLogger(__name__ + '.Groupmembers')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Groupmembers, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--name',
            '-n',
            required=True,
            metavar='<group name>',
            help='The group name')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "groups/{a.account}/{a.name}/members/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            print("\n Group Name: {a.name}".format(a=parsed_args))
            newdata = prettytable.PrettyTable()
            newdata.padding_width = 1
            newdata.add_column("Members", [i['username'] for i in data])
            print(newdata)
        else:
            self.app.stdout.write(
                '\n Error: ' + '"' + str(r.status_code) + '"' +
                ' Invalid request \n\n')
            sys.exit(1)


class Addgroupmember(Command):

    """
    * Add new member in group
    """
    log = logging.getLogger(__name__ + '.Addgroupmember')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Addgroupmember, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--name',
            '-n',
            required=True,
            metavar='<group_name>',
            help='The group name')
        parser.add_argument(
            '--member',
            '-m',
            required=True,
            metavar='<member_account>',
            help='The member name')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "groups/{a.account}/{a.name}/"
               "members/{a.member}/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.put(url, auth=(user, passwd))
        if r.status_code == 200:
            msg = """
 User '{a.member}' added to group '{a.name}'
 """
            print(msg.format(a=parsed_args))
            sys.exit(0)
        elif r.status_code == 409:
            msg = """
 'Conflict/Duplicate' User '{a.member}' present in group
 """
            print(msg.format(a=parsed_args))
            sys.exit(1)
        else:

            msg = """
 Error: "{r.status_code}" Invalid request

 """
            self.app.stdout.write(msg.format(r=r))
            sys.exit(1)


class Deletegroupmember(Command):

    """
    * Delete member from group
    """
    log = logging.getLogger(__name__ + '.Deletegroupmember')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Deletegroupmember, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--name',
            '-n',
            required=True,
            metavar='<group_name>',
            help='The group name')
        parser.add_argument(
            '--member',
            '-m',
            required=True,
            metavar='<member_account>',
            help='The member name')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "groups/{a.account}/{a.name}/"
               "members/{a.member}/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.delete(url, auth=(user, passwd))
        if r.status_code == 204:
            msg = """
 User '{a.member}' removed from group '{a.name}'
"""
            print(msg.format(a=parsed_args))
            sys.exit(0)
        else:

            msg = """
 Error: "{r.status_code}" Invalid request

 """
            self.app.stdout.write(msg.format(r=r))
            sys.exit(1)
