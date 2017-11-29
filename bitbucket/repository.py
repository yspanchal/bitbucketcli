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
from cliff.lister import Lister
from cliff.show import ShowOne
from .utils import read_creds


class Repocreate(ShowOne):

    """
    * Create new repository
    """
    log = logging.getLogger(__name__ + '.Repocreate')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Repocreate, self).get_parser(prog_name)
        parser.add_argument(
            '--reponame',
            '-r',
            required=True,
            metavar='<reponame>',
            help='The repository name')
        parser.add_argument(
            '--description',
            '-d',
            metavar='<description>',
            help='The repository description')
        parser.add_argument(
            '--owner',
            '-o',
            metavar='<owner>',
            help='Repository Owner')
        parser.add_argument(
            '--is_private',
            '-p',
            metavar='<is_private>',
            choices=[
                'true',
                'false'],
            required=False,
            help='repository is private ?')
        parser.add_argument(
            '--scm',
            '-s',
            metavar='<scm>',
            choices=[
                'git',
                'hg'],
            required=False,
            help='The repository scm')
        parser.add_argument(
            '--has_issues',
            '-i',
            metavar='<has_issues>',
            choices=[
                'true',
                'false'],
            required=False,
            help='The repository has issues ?')
        parser.add_argument(
            '--has_wiki',
            '-w',
            metavar='<has_wiki>',
            choices=[
                'true',
                'false'],
            required=False,
            help='The repository has wiki ?')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        args = {}

        if parsed_args.reponame:
            args['name'] = parsed_args.reponame

        if parsed_args.owner:
            args['owner'] = parsed_args.owner

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
        user, passwd = read_creds()
        r = requests.post(url, data=args, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            data.pop('logo')
            data.pop('resource_uri')
            columns = data.keys()
            data = data.values()
            msg = "\nRepository '{a.reponame}' Created.\n"
            print(msg.format(a=parsed_args))
            return (columns, data)
        elif r.status_code == 400:

            msg = ("\n Error: '{r.status_code}' "
                   "You already have a repository with name ' {a.reponame}'.\n")

            self.app.stdout.write(msg.format(a=parsed_args, r=r))
            sys.exit(0)
        else:
            self.app.stdout.write('\nError: Bad request.\n')
            sys.exit(1)


class Repoedit(ShowOne):

    """
    * Edit existing repository information, add issues & wiki modules to
    repository
    """
    log = logging.getLogger(__name__ + '.Repoedit')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Repoedit, self).get_parser(prog_name)
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The account name')
        parser.add_argument(
            '--reponame',
            '-r',
            required=True,
            metavar='<reponame>',
            help='The repository name')
        parser.add_argument(
            '--description',
            '-d',
            metavar='<description>',
            help='The repository description')
        parser.add_argument(
            '--is_private',
            '-p',
            metavar='<is_private>',
            choices=[
                'true',
                'false'],
            required=False,
            help='repository is private ?')
        parser.add_argument(
            '--has_issues',
            '-i',
            metavar='<has_issues>',
            choices=[
                'true',
                'false'],
            required=False,
            help='The repository has issues ?')
        parser.add_argument(
            '--has_wiki',
            '-w',
            metavar='<has_wiki>',
            choices=[
                'true',
                'false'],
            required=False,
            help='The repository has wiki ?')
        parser.add_argument(
            '--language',
            '-l',
            metavar='<language>',
            required=False,
            help='The repository language')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

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

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.}/{a.}/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.put(url, data=args, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            data.pop('logo')
            data.pop('resource_uri')
            columns = data.keys()
            data = data.values()
            msg = "\nRepository '{a.reponame}' Edited.\n"
            print(msg.format(a=parsed_args))
            return (columns, data)
        if r.status_code == 400:
            msg = "'{a.language}' is not valid language choice."
            print(msg .format(a=parsed_args))
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
        parser.add_argument(
            '--account',
            '-a',
            required=True,
            metavar='<account>',
            help='The repository account name')
        parser.add_argument(
            '--reponame',
            '-r',
            required=True,
            metavar='<reponame>',
            help='The repository name')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))
        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.delete(url, auth=(user, passwd))
        if r.status_code == 204:
            msg = "\n Repository '{a.reponame}' Deleted.\n"
            print(msg.format(a=parsed_args))
            sys.exit(0)
        else:
            msg = (" Error: Invalid requests, '{r.status_code}'"
                   " or No such repository found.")
            print(msg.format(r=r))
            sys.exit(1)


class Repolist(Lister):

    """
    * List all repository associated with users account
    """
    log = logging.getLogger(__name__ + '.Repolist')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def take_action(self, parsed_args):
        user, passwd = read_creds()
        self.log.debug('take_action({a})'.format(a=parsed_args))
        url = ("https://bitbucket.org/api/1.0/"
               "user/repositories/")
        r = requests.get(url, auth=(user, passwd))
        data = json.loads(r.text)
        return (('Owner', 'Repo Name', 'Created On'),
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
        parser.add_argument(
            '--reponame',
            '-r',
            required=True,
            metavar='<reponame>',
            help='The repository name')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))
        url = ("https://bitbucket.org/api/1.0/"
               "user/repositories/")
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        data = json.loads(r.text)
        for i in data:
            if i['name'] == parsed_args.reponame:
                i.pop('logo')
                i.pop('resource_uri')
                columns = i.keys()
                data = i.values()
                return (columns, data)

        msg = '\nError: "{a.reponame}" No such repository found.\n\n'
        self.app.stdout.write(msg.format(a=parsed_args))
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
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "tags/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            if data == {}:
                msg = '\nNo Tags Found for "{a.reponame}".\n\n'
                self.app.stdout.write(msg.format(a=parsed_args))
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
                    print(newdata)
        else:
            msg = ('\n Error: "{r.status_code}" Invalid request,'
                   ' Invalid Account name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(a=parsed_args, r=r))


class Repobranch(Command):

    """
    * Returns repository branches
    """
    log = logging.getLogger(__name__ + '.Repobranch')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Repobranch, self).get_parser(prog_name)
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
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "branches").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            if data == {}:
                msg = '\nNo branches Found for "{a.reponame}".\n\n'
                self.app.stdout.write(msg.format(a=parsed_args))
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
                    print(newdata)
        else:
            msg = ('\n Error: "{r.status_code}" Invalid request,'
                   ' Invalid Account name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(r=r, a=parsed_args))


class Repodeploykeysget(Command):

    """
    * Get list of repository deployment keys
    """
    log = logging.getLogger(__name__ + '.Repodeploykeysget')
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    def get_parser(self, prog_name):
        parser = super(Repodeploykeysget, self).get_parser(prog_name)
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
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "deploy-keys/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)
            if len(data) != 0:
                loopmsg = """
Key ID: {k[pk]}
Key: {k[key]}
Key Label: {k[label]}
=======================================================
"""
                for key in data:
                    print(loopmsg.format(k=key))
                sys.exit(0)
            else:
                print("\n No deployment key found.\n")
                sys.exit(0)
        else:
            msg = ('\n'
                   ' Error: {r.status_code} {reason}\n'
                   ' Account name: "{a.account}'
                   ' Repository name: "{a.reponame}'
                   '\n\n')
            msg = msg.format(r=r, a=parsed_args, reason=get_reason(r))
            self.app.stdout.write(msg)
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
            '--key',
            '-k',
            metavar='<key>',
            required=True,
            help='The repository deploy-key')
        parser.add_argument(
            '--label',
            '-l',
            metavar='<key-label>',
            required=True,
            help='The repository deploy-key label')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "deploy-keys/").format(a=parsed_args)

        args = {}

        if parsed_args.key:
            args['key'] = parsed_args.key

        if parsed_args.label:
            args['label'] = parsed_args.label
        user, passwd = read_creds()
        r = requests.post(url, data=args, auth=(user, passwd))
        print(r.text)
        if r.status_code == 200:
            data = json.loads(r.text)

            msg = """
New deployment key added."

Key ID: {d[pk]}

Key: {d[key]}

Key Label: {d[label]}
"""
            print(msg.format(d=data))
            sys.exit(0)
        elif r.status_code == 400:
            print ("\n Error: Someone has already registered"
                   " this as an account SSH key.\n")
            sys.exit(1)
        else:
            msg = ('\n Error: "{r.status_code}"'
                   ' Invalid request, Invalid Account name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(r=r, a=parsed_args))
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
            '--key',
            '-k',
            metavar='<key>',
            required=True,
            help='The repository deploy-key')
        parser.add_argument(
            '--label',
            '-l',
            metavar='<key-label>',
            required=True,
            help='The repository deploy-key label')
        parser.add_argument(
            '--key_id',
            '-i',
            metavar='<key_id>',
            required=True,
            help='The repository deploy-key ID')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "deploy-keys/{a.key_id}").format(a=parsed_args)

        args = {}

        if parsed_args.key:
            args['key'] = parsed_args.key

        if parsed_args.label:
            args['label'] = parsed_args.label
        user, passwd = read_creds()
        r = requests.put(url, data=args, auth=(user, passwd))
        print(r.text)
        if r.status_code == 200:
            data = json.loads(r.text)
            msg = """
Deployment key edited."

Key ID: {d[pk]}

Key: {d[key]}

Key Label: {d[label]}
"""
            print(msg.format(d=data))
            sys.exit(0)
        elif r.status_code == 400:
            print ("\n Error: Someone has already"
                   " registered this as an account SSH key.\n")
            sys.exit(1)
        else:
            msg = ('\n Error: "{r.status_code}" Invalid request,'
                   ' Invalid aaAccount name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(r=r, a=parsed_args))
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
            '--key_id',
            '-i',
            metavar='<key_id>',
            required=True,
            help='The repository deploy-key ID')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "deploy-keys/{a.key_id}").format(a=parsed_args.account)
        user, passwd = read_creds()
        r = requests.delete(url, auth=(user, passwd))
        if r.status_code == 204:
            msg = """
 Success: Repository deployment key '{a.key_id}' deleted.
"""
            print(msg.format(a=parsed_args))
            sys.exit(0)
        else:
            msg = ('\n Error: "{r.status_code}"'
                   ' Invalid request, Invalid Account name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(a=parsed_args, r=r))
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
            '--name',
            '-n',
            metavar='<name>',
            required=True,
            help='The repository name')
        parser.add_argument(
            '--description',
            '-d',
            metavar='<description>',
            help='The repository description')
        parser.add_argument(
            '--is_private',
            '-p',
            metavar='<is_private>',
            choices=[
                'true',
                'false'],
            help='The repository is private ?')
        parser.add_argument(
            '--language',
            '-l',
            metavar='<language>',
            help='The repository language')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "repositories/{a.account}/{a.reponame}/"
               "fork/").format(a=parsed_args)

        args = {}

        args['name'] = parsed_args.name

        if parsed_args.description:
            args['description'] = parsed_args.description

        if parsed_args.is_private:
            args['is_private'] = parsed_args.is_private

        if parsed_args.language:
            args['language'] = parsed_args.language
        user, passwd = read_creds()
        r = requests.post(url, data=args, auth=(user, passwd))

        if r.status_code == 200:
            data = json.loads(r.text)
            data.pop('logo')
            data.pop('resource_uri')
            data.pop('fork_of')
            columns = data.keys()
            data = data.values()
            msg = "\nRepository '{a.reponame}' Forked.\n"
            print(msg.format(a=parsed_args))
            return (columns, data)
        else:

            msg = ('\n Error: "{r.status_code}" Invalid request,'
                   ' Invalid Account name "{a..account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(r=r, a=parsed_args))
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
            '--revision',
            '-R',
            metavar='<revision>',
            required=True,
            help='The repository revision or branch name')
        parser.add_argument(
            '--path',
            '-p',
            metavar='<path>',
            help='File or directory path')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        if parsed_args.path:
            url = ("https://bitbucket.org/api/1.0/"
                   "repositories/{a.account}/{a.reponame}/"
                   "src/{a.revision}/{a.path}").format(a=parsed_args)
        else:
            url = ("https://bitbucket.org/api/1.0/"
                   "repositories/{a.account}/{a.reponame}/"
                   "src/{a.revision}/").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.get(url, auth=(user, passwd))

        if r.status_code == 200:
            data = json.loads(r.text)
            msg = """
 Repository Source Details:

Revision: '{d[node]}'
Path: '{d[path]}'
directories: {d[directories]}
Files:
"""
            print(msg.format(d=data))
            for f in data['files']:
                newdata = prettytable.PrettyTable(["Fields", "Values"])
                newdata.padding_width = 1
                newdata.add_row(["Size", f['size']])
                newdata.add_row(["Path", f['path']])
                newdata.add_row(["TimeStamp", f['timestamp']])
                newdata.add_row(["Revision", f['revision']])
                print(newdata)
            sys.exit(0)
        else:
            msg = ('\n Error: "{r.status_code}" Invalid request,'
                   ' Invalid Account name "{a..account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(r=r, a=parsed_args))
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
            '--share',
            '-s',
            metavar='<share_with>',
            required=True,
            help='Share repository with user')
        parser.add_argument(
            '--permission',
            '-p',
            metavar='<permission>',
            required=True,
            choices=[
                'read',
                'write',
                'admin'],
            help='Repository permission')
        return parser

    def take_action(self, parsed_args):
        print("enters")
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "privileges/{a.account}/{a.reponame}/"
               "{a.share}").format(a=parsed_args)

        args = {}
        args['permission'] = parsed_args.permission
        user, passwd = read_creds()
        r = requests.put(url, data=parsed_args.permission, auth=(user, passwd))
        print(r.text)
        if r.status_code == 200:
            data = json.loads(r.text)

            msg = """
 Repository '{a.reponame}' shared with '{a.share}'

Repository: {d[0][repo]}
Shared with: {d[0][user][username]}
Permission: {d[0][privilege]}"""
            print(msg.format(d=data))
            sys.exit(0)
        else:
            msg = ('\n Error: "{r.status_code}" Invalid request,'
                   ' Invalid Account name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(a=parsed_args, r=r))
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
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "privileges/{a.account}/{a.reponame}").format(a=parsed_args)
        user, passwd = read_creds()

        r = requests.get(url, auth=(user, passwd))
        if r.status_code == 200:
            data = json.loads(r.text)

            loopmsg = """
Repository: {i[repo]}
Shared with: {i[user][username]}
Permission: {i[privilege]}
================================================"
"""
            for i in data:
                print(loopmsg.format(i=i))
            sys.exit(0)
        else:
            msg = ('\n Error: "{r.status_code}" Invalid request,'
                   ' Invalid Account name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(r=r, a=parsed_args))
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
            '--share',
            '-s',
            metavar='<share_with>',
            required=True,
            help='Share repository with user')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action({a})'.format(a=parsed_args))

        url = ("https://bitbucket.org/api/1.0/"
               "privileges/{a.account}/{a.reponame}/"
               "{a.share}").format(a=parsed_args)
        user, passwd = read_creds()
        r = requests.delete(url, auth=(user, passwd))
        if r.status_code == 204:
            msg = ("\n Privileges for user '{a.share}'"
                   " removed on repository '{a.reponame}'")
            print(msg.format(a=parsed_args))
            sys.exit(0)
        else:
            msg = ('\n Error: "{r.status_code}"'
                   ' Invalid request, Invalid Account name "{a.account}"'
                   ' or Repository Name "{a.reponame}"\n\n')
            self.app.stdout.write(msg.format(r=r, a=parsed_args))
            sys.exit(1)


def get_reason(r):
    """Get reason, why an http request failed.

    r is response as returned by requests library
    """
    try:
        return r.json().get("error").get("message")
    except (ValueError, TypeError):
        maxlen = 200
        maxlines = 3
        lines = r.text[:maxlen].splitlines()[:maxlines]
        reason = "\n".join(lines).strip()
        if len(reason):
            return reason
        else:
            return r.reason
