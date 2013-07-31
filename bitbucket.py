#!/usr/bin/python

import requests
import pickle
import os
import sys
import getpass
from os.path import expanduser
from Crypto.Cipher import ARC4

home = expanduser("~")
filename = os.path.join(home, '.bitbucket-creds')

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
		if status != 200:
		print "Authentication Error. Invalid Username or Password."
	else:
		print "Login Successful."

def listofrepos():
	cred = ('ypanchal', '302#raj')
	url = "https://bitbucket.org/api/1.0/user/repositories/"
	r = requests.get(url, auth=cred)
	print r.text
	
if __name__ == '__main__':
	#login()
	listofrepos()




