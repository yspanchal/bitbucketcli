
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
import logging
from os.path import expanduser
from cliff.command import Command


class Logout(Command):
   """
   * Logout user & remove saved credentials
   """

	log = logging.getLogger(__name__ + '.Logout')

	def take_action(self):
		self.log.debug('take_action()')

		home = expanduser("~")
		filename = os.path.join(home, '.bitbucket.py')
		os.remove(filename)
		if not filename:
			print "\n Logout Successfully\n\n"