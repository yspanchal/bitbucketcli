#!/usr/bin/python

import requests
import pickle
import os
import sys
import getpass
from os.path import expanduser

home = expanduser("~")
filename = os.path.join(home, '.bitbucket-cookies')

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def login():
	url = "https://bitbucket.org/api/1.0/user/"
	user = raw_input('Enter BitBucket Username or Email [%s]:' % getpass.getuser())
	if not user:
		user = getpass.getuser()

	p1 = getpass.getpass('Enter Password: ')
	p2 = getpass.getpass('Retype Password: ')
	if p1 != p2:
		print "Password do not match. Try Again."
		sys.exit(2)
	else:
		passwd = p1
	r = requests.get(url, auth=(user, passwd))
	status = r.status_code
	msg = "Authentication Error. Invalid Username or Password."
	if status != 200:
		#print "Authentication Error. Invalid Username or Password."
		sys.stdout.write(msg); sys.stdout.flush()
	else:
		sys.stdout.flush()
		save_cookies(r.cookies, filename)
		print "Login Successful."

if __name__ == '__main__':
	login()




