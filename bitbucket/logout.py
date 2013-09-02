
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
import json
import getpass
import logging
import requests
from os.path import expanduser
from cliff.command import Command

try:
   home = expanduser("~")
   filename = os.path.join(home, '.bitbucket.py')
except (IOError, NameError):
   pass

class Login(Command):
   """
   * Login to bitbucket account
   """
   log = logging.getLogger(__name__ + '.Login')
   requests_log = logging.getLogger("requests")
   requests_log.setLevel(logging.WARNING)   

   def take_action(self, parsed_args):
      if not os.path.exists(filename):
         print "Login to Your BitBucket Account.\n"
         url = "https://bitbucket.org/api/1.0/user/"
         user = raw_input('Enter BitBucket Username or Email [%s]:' % getpass.getuser())
         if not user:
            user = getpass.getuser()

         p1 = getpass.getpass('Enter Password: ')
         p2 = getpass.getpass('Enter Password (Again): ')

         if p1 != p2:
            print "\n Password do not match. Try Again\n"
            sys.exit(1)
         else:
            passwd = p1

         r = requests.get(url, auth=(user, passwd))
         status = r.status_code

         if status == 200:
            f = open(filename,'w')
            f.write("username = " + "'" + user + "'" + "\n")
            f.write("passwd = " + "'" + p1 + "'" + "\n")
            print("Login Successful.")
            data = json.loads(r.text)
            print "\nUsername: " + data['user']['username']
            print "Display Name: " + data['user']['display_name']
            sys.exit(0)
         else:
            print "\n Authentication Error. Invalid Username or Password\n"
            sys.exit(1)
      else:
         print "\n You are logged in\n"
         sys.exit(0)


class Logout(Command):
   """
   * Logout user & remove saved credentials
   """
   log = logging.getLogger(__name__ + '.Logout')
   requests_log = logging.getLogger("requests")
   requests_log.setLevel(logging.WARNING)   

   def take_action(self, parsed_args):
      home = expanduser("~")
      filename = os.path.join(home, '.bitbucket.py')
      os.remove(filename)
      print "\n Logout Successfully\n\n"