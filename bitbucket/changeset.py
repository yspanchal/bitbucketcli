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
            '--limit',
            '-l',
            metavar='<limit>',
            required=True,
            type=int,
            help='The limit number')
        parser.add_argument(
            '--start',
            '-s',
            metavar='<start node>',
            help='The start node hash')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        if parsed_args.start:
            url = ("https://bitbucket.org/api/1.0/"
                   "repositories/{a.account}/{a.reponame}/"
                   "changesets"
                   "?limit={a.limit}&start={a.start}").format(a=parsed_args)
        else:
            url = ("https://bitbucket.org/api/1.0/"
                   "repositories/{a.account}/{a.reponame}/"
                   "changesets"
                   "?limit={a.limit}").format(a=parsed_args)

        r = requests.get(url, auth=(user, passwd))
        if r.status_code != 200:
            print "\n Error: '{r.status_code}' No Changeset Found.".format(r=r)
            sys.exit(1)
        else:
            data = json.loads(r.text)
            msg = """
Total Changeset:"
d[count], Start: d[start], Limit: [d[limit]"
"""
            print msg.format(d=data)
            msg = """{newdata}
Author: {i[author]}
Timestamp: {i[timestamp]}
Commit ID: {i[raw_node]}
Commit Message: {i[message]}
-------------------------------------------------------"""

            for i in data['changesets']:
                newdata = prettytable.PrettyTable(["Type", "File"])
                newdata.padding_width = 1
                for f in i['files']:
                    newdata.add_row([f['type'], f['file']])

                print msg.format(newdata=newdata, i=i)


class Commitget(Command):

    """
    * Get commit details from commit id
    """
    log = logging.getLogger(__name__ + '.Commitget')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Commitget, self).get_parser(prog_name)
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
            '--commit',
            '-c',
            metavar='<commit_id>',
            required=True,
            help='The commit id or commit hash')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/changesets/{a.commit}")
        url = url.format(a=parsed_args)

        r = requests.get(url, auth=(user, passwd))
        if r.status_code != 200:
            print "\n Error: '{r.status_code}' No Commit ID Found.".format(r=r)
            sys.exit(1)
        else:
            data = json.loads(r.text)
            print "\nCommit ID: {d[raw_node]}\n".format(d=data)

            for i in data['files']:
                newdata = prettytable.PrettyTable(["Type", "File"])
                newdata.padding_width = 1
                newdata.add_row([i['type'], i['file']])

            msg = """{newdata}
Author: {d[author]}
Timestamp: {d[timestamp]}
Branches: {d[branches]}
Commit Message: {d[message]}
-------------------------------------------------------"""
            print msg.format(newdata=newdata, d=data)


class Changesetcommentsget(Command):

    """
    * Get comments for changeset
    """
    log = logging.getLogger(__name__ + '.Changesetcommentsget')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Changesetcommentsget, self).get_parser(prog_name)
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
            '--commit',
            '-c',
            metavar='<commit_id>',
            required=True,
            help='The commit id or commit hash')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({p})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "changesets/{a.commit}/comments/").format(a=parsed_args)

        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            for comment in data:
                if 'content' not in comment:
                    print "\n No Any Comments Found.\n"
                    sys.exit(1)
            else:
                msg = """
Commit ID: {comment[node]}
Comment: {comment[content]}
{newdata}
------------------------------------------------------
"""
                for comment in data:
                    newdata = prettytable.PrettyTable(["Fields", "Values"])
                    newdata.add_row(["Name", comment['display_name']])
                    newdata.add_row(["Comment ID", comment['comment_id']])
                    newdata.add_row(["Created On", comment['utc_created_on']])
                    newdata.add_row(["Updated On", comment['utc_last_updated']])
                    print msg.format(comment=comment, newdata=newdata)

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
            '--commit',
            '-c',
            metavar='<commit_id>',
            required=True,
            help='The commit id or commit hash')
        parser.add_argument(
            '--comment',
            '-C',
            metavar='<comment>',
            required=True,
            help='The comment content')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "changesets/{a.commit}/comments/").format(a=parsed_args)

        args = {}
        args['content'] = parsed_args.comment
        r = requests.post(url, data=args, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            newdata = prettytable.PrettyTable(["Fields", "Values"])
            newdata.add_row(["Name", data['display_name']])
            newdata.add_row(["Comment ID", data['comment_id']])
            newdata.add_row(["Created On", data['utc_created_on']])
            newdata.add_row(["Updated On", data['utc_last_updated']])
            msg = """
Commit ID: {d[node]}
Comment: {d[content]}
{newdata}"""
            print msg.format(newdata=newdata, d=data)
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
            '--commit',
            '-c',
            metavar='<commit_id>',
            required=True,
            help='The commit id or commit hash')
        parser.add_argument(
            '--comment_id',
            '-id',
            metavar='<comment_id>',
            required=True,
            help='The comment content id')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "changesets/{a.commit}/"
               "comments/{a.comment_id}").format(a=parsed_args)

        r = requests.delete(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)

            msg = """
Commit ID: {data[node]}
Comment ID: {data[comment_id]}
Comment '{data[comment_id]}' deleted successfully."""
            print msg.format(data=data)
            sys.exit(0)
        else:
            print """
Error: Invalid request, or invalid commit id or invalid comment id."""
            sys.exit(1)
