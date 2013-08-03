import sys
import logging
import requests
import os
import getpass
import json
from os.path import expanduser
from cliff.app import App
from cliff import help
from cliff.commandmanager import CommandManager


class BitBucketApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(BitBucketApp, self).__init__(
            description='BitBucket Command Line Script',
            version='1.0',
            command_manager=CommandManager('cliff.bitbucket'),
            )

    def auth(self):
        home = expanduser("~")
        filename = os.path.join(home, '.bitbucket.py')
        if not os.path.exists(filename):
            print "Login to Your BitBucket Account.\n"
            url = "https://bitbucket.org/api/1.0/user/"
            user = raw_input('Enter BitBucket Username or Email [%s]:' % getpass.getuser())
            if not user:
                user = getpass.getuser()

            p1 = getpass.getpass('Enter Password: ')
            p2 = getpass.getpass('Retype Password: ')
            if p1 != p2:
                print "Password do not match. Try Again.\n"
                sys.exit(1)
            else:
                passwd = p1
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
        self.log.debug('initialize_app')
        command_name = None
        if self.interactive_mode or command_name != 'help':
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