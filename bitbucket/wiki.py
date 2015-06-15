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


class Wikiget(Command):

    """
    * Get wiki page created for repository
    """
    log = logging.getLogger(__name__ + '.Wikiget')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Wikiget, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            metavar='<account name>',
            required=True,
            help='Your account name')
        parser.add_argument(
            '--reponame',
            '-r',
            metavar='<repo name>',
            required=True,
            help='The repository name')
        parser.add_argument(
            '--page',
            '-p',
            metavar='<page name>',
            required=True,
            help='The page title')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "wiki/{a.page}/").format(a=parsed_args)
        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            msg = """
Markup: {d[markup]}

Revision: {d[rev]}

Page Content: {d[data]}

"""
            print msg.format(d=data)
        else:
            print ("\n Error: '404' No Wiki Pages Found"
                   " 'or' Invalid argument supplied.\n")
            sys.exit(1)


class Wikipost(Command):

    """
    * Post new wiki page for repositorys
    """
    log = logging.getLogger(__name__ + '.Wikipost')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Wikipost, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            metavar='<account name>',
            required=True,
            help='Your account name')
        parser.add_argument(
            '--reponame',
            '-r',
            metavar='<repo name>',
            required=True,
            help='The repository name')
        parser.add_argument(
            '--page',
            '-p',
            metavar='<page name>',
            required=True,
            help='The page title')
        parser.add_argument(
            '--content',
            '-c',
            metavar='<page content>',
            required=True,
            help='The page content')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a}s)'.format(a=parsed_args))

        args = {}
        args['content'] = parsed_args.content

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "wiki/{a.page}/").format(a=parsed_args)
        r = requests.post(url, data=args, auth=(user, passwd))
        if r.status_code == 200:
            print "\n Wiki Page Created Successfully.\n"
        else:
            msg = ("\n Error: '{r.status_code}' "
                   "Something Went Wrong -- Bitbucket.\n")
            print msg.format(r=r)
            sys.exit(1)
