
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


"""Command-line interface to the BitBucket."""

import os
import sys
import json
import logging
import requests
import getpass
from os.path import expanduser
from cliff.app import App
from cliff import help
from cliff.commandmanager import CommandManager


class BitBucketApp(App):
    """
    * BitBucket global app
    """ 

    log = logging.getLogger(__name__)

    def __init__(self):
        super(BitBucketApp, self).__init__(
            description='BitBucket Command Line Tool',
            version='1.0',
            command_manager=CommandManager('cliff.bitbucket'),
            )

    def auth(self):
        """
        * Make sure user is authenticated before executing any command
        """
        home = expanduser("~")
        filename = os.path.join(home, '.bitbucket.py')
        if not os.path.exists(filename):
            print "Login to Your BitBucket Account.\n"
            url = "https://bitbucket.org/api/1.0/user/"
            user = raw_input('Enter BitBucket Username or Email [%s]:' % getpass.getuser())
            if not user:
                user = getpass.getuser()

            p1 = getpass.getpass('Enter Password: ')
            p2 = getpass.getpass('Enter Password (Again): ')
            if p1 != p2:
                print "Password do not match. Try Again.\n"
                sys.exit(1)
            else:
                passwd = p1
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.WARNING)    
            r = requests.get(url, auth=(user, passwd))
            status = r.status_code
            if status != 200:
                print "Authentication Error. Invalid Username or Password.\n"
                sys.exit(1)
            else:
                f = open(filename,'w')
                f.write("username = " + "'" + user + "'" + "\n")
                f.write("passwd = " + "'" + p1 + "'" + "\n")
                print("Login Successful.\n")
                data = json.loads(r.text)
                print "Username: " + data['user']['username']
                print "Display Name: " + data['user']['display_name']
        else:
            pass

    def initialize_app(self, argv):
        """
        * Initialize bitbucket app 
        """
        self.log.debug('initialize_app')
        command_name = None
        if argv:
            cmd_info = self.command_manager.find_command(argv)
            cmd_factory, cmd_name, sub_argv = cmd_info
        if self.interactive_mode or command_name != 'help':
            if self.interactive_mode or command_name != 'login':
                self.auth()

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = BitBucketApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))