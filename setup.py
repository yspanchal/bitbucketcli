#!/usr/bin/env python

PROJECT = 'bitbucket'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

from distutils.util import convert_path
from fnmatch import fnmatchcase
import os
import sys

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Bitbucket command line',
    long_description=long_description,

    author='Yogesh Panchal',
    author_email='yspanchal@gmail.com',

    url='https://github.com/dreamhost/cliff',
    download_url='https://github.com/dreamhost/cliff/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['distribute', 'cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'bitbucket = bitbucket.main:main'
            ],
        'cliff.bitbucket': [
            'commit-detail = bitbucket.changeset:Commitget',
            'commit-comments = bitbucket.changeset:Changesetcommentsget',
            'commit-comments-post = bitbucket.changeset:Changesetcommentpost',
            'commit-comments-delete = bitbucket.changeset:Changesetcommentdelete',
            'repo-changeset = bitbucket.changeset:Changesetget',
            'repo-create = bitbucket.repository:Repocreate',
            'repo-edit = bitbucket.repository:Repoedit',
            'repo-delete = bitbucket.repository:Repodelete',
            'repolist = bitbucket.repository:Repolist',
            'repodetail = bitbucket.repository:Repodetail',
            'repotag = bitbucket.repository:Repotag',
            'repobranch = bitbucket.repository:Repobranch',
            'repokeydeploy = bitbucket.repository:Repodeploykeyspost',
            'repokeydeploy-list = bitbucket.repository:Repodeploykeysget',
            'repokeydeploy-edit = bitbucket.repository:Repodeploykeysedit',
            'repokeydeploy-delete = bitbucket.repository:Repodeploykeysdelete',
            'repo-fork = bitbucket.repository:Repofork',
            'repo-revision = bitbucket.repository:Reporevision',
            'user-info = bitbucket.user:User',
            'user-privileges = bitbucket.user:Userprivileges',
            'issue = bitbucket.issues:Getissue',
            'issue-create = bitbucket.issues:Createissue',
            'issue-edit = bitbucket.issues:Editissue',
            'issue-delete = bitbucket.issues:Deleteissue',
            'issue-getcomment = bitbucket.issues:Getcomment',
            'issue-postcomment = bitbucket.issues:Postcomment',
            'wiki-get = bitbucket.wiki:Wikiget',
            'wiki-post = bitbucket.wiki:Wikipost',
            ],
        },

    zip_safe=False,
    )