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


class Sshkeyget(Command):

    """
    * Get list of all ssh keys associated with users account
    * Get ssh key from ssh key id
    """
    log = logging.getLogger(__name__ + '.Sshkeyget')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Sshkeyget, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--key_id',
            '-i',
            metavar='<key_id>',
            help='Get individual key from key id')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        if parsed_args.key_id:
            url = "https://bitbucket.org/api/1.0/users/%s/ssh-keys/%s" % (
                parsed_args.account, parsed_args.key_id)
            r = requests.get(url, auth=(user, passwd))
            if r.status_code == 200:
                data = json.loads(r.text)
                print "\nKey ID: %s" % (parsed_args.key_id)
                print "Key: %s" % (data['key'])
                print "Key Label: %s" % (data['label'])
                sys.exit(0)
            else:
                self.app.stdout.write(
                    '\n Error: ' + '"' + str(r.status_code) + '"' +
                    ' Invalid request\n\n')
                sys.exit(1)
        else:
            url = "https://bitbucket.org/api/1.0/users/%s/ssh-keys/" % (
                parsed_args.account)
            r = requests.get(url, auth=(user, passwd))
            if r.status_code == 200:
                data = json.loads(r.text)

                loopmsg = """
Key ID: {k[pk]}
Key: {k[key]}
Key Label: {k[label]}
=======================================================
"""
                for key in data:
                    print loopmsg.format(k=key)
                sys.exit(0)
            else:
                msg = '\n Error: "{r.status_code}" Invalid request\n\n'
                self.app.stdout.write(msg.format(r=r))
                sys.exit(1)


class Sshkeypost(Command):

    """
    * Add new ssh key to users account
    """
    log = logging.getLogger(__name__ + '.Sshkeypost')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Sshkeypost, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--key',
            '-k',
            required=True,
            metavar='<key>',
            help='Ssh key')
        parser.add_argument(
            '--label',
            '-l',
            required=True,
            metavar='<key_lebel>',
            help='name or label of key')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        args = {}
        args['key'] = parsed_args.key
        args['label'] = parsed_args.label

        url = ("https://bitbucket.org/api/1.0/"
               "users/{a.account}/ssh-keys/").format(a=parsed_args)
        r = requests.post(url, data=args, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            msg = """
 Key added to your account"

Key ID: {d[pk]}
Key: {d[key]}
Key Label: {d[label]}
"""
            print msg.format(d=data)
            sys.exit(0)
        elif r.status_code == 400:
            msg = ('\n Error: "{r.status_code}"'
                   ' Someone has already registered that SSH key\n\n')
            self.app.stdout.write(msg.format(r=r))
            sys.exit(1)
        else:
            msg = '\n Error: "{r.status_code}" Invalid request\n\n'
            self.app.stdout.write(msg.format(r=r))
            sys.exit(1)


class Sshkeydelete(Command):

    """
    * Delete ssh key from account
    """
    log = logging.getLogger(__name__ + '.Sshkeydelete')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Sshkeydelete, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--key_id',
            '-i',
            required=True,
            metavar='<key_id>',
            help='Delete key from key id')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        url = ("https://bitbucket.org/api/1.0/"
               "users/{a.account}/"
               "ssh-keys/{a.key_id}").forma(a=parsed_args)
        r = requests.delete(url, auth=(user, passwd))
        if r.status_code == 204:
            print "\n Key ID '{a.key_id}' deleted.\n".format(a=parsed_args)
            sys.exit(0)
        else:
            msg = '\n Error: "{r.status_code}" Invalid request\n\n'
            self.app.stdout.write(msg.format(r=r))
            sys.exit(1)
