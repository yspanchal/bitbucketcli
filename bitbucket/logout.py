import os
import sys
import logging
from os.path import expanduser
from cliff.command import Command


class Logout(Command):
	log = logging.getLogger(__name__ + '.Logout')

	def take_action(self):
		self.log.debug('take_action()')

		home = expanduser("~")
		filename = os.path.join(home, '.bitbucket.py')
		os.remove(filename)
		if not filename:
			print "\n Logout Successfully\n\n"