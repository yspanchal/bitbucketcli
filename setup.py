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
            'commit_detail = bitbucket.changeset:Commitget',
            'commit_comments = bitbucket.changeset:Changesetcommentsget',
            'commit_comments_post = bitbucket.changeset:Changesetcommentpost',
            'commit_comments_delete = bitbucket.changeset:Changesetcommentdelete',
            'groups = bitbucket.groups:Groups',
            'group_create = bitbucket.groups:Creategroup',
            'group_delete = bitbucket.groups:Deletegroup',
            'group_members = bitbucket.groups:Groupmembers',
            'group_member_add = bitbucket.groups:Addgroupmember',
            'group_member_delete = bitbucket.groups:Deletegroupmember',
            'issue = bitbucket.issues:Getissue',
            'issue_create = bitbucket.issues:Createissue',
            'issue_edit = bitbucket.issues:Editissue',
            'issue_delete = bitbucket.issues:Deleteissue',
            'issue_getcomment = bitbucket.issues:Getcomment',
            'issue_postcomment = bitbucket.issues:Postcomment',
            'repo_changeset = bitbucket.changeset:Changesetget',
            'repo_create = bitbucket.repository:Repocreate',
            'repo_edit = bitbucket.repository:Repoedit',
            'repo_delete = bitbucket.repository:Repodelete',
            'repo_list = bitbucket.repository:Repolist',
            'repo_detail = bitbucket.repository:Repodetail',
            'repo_tag = bitbucket.repository:Repotag',
            'repo_branch = bitbucket.repository:Repobranch',
            'repo_deploykey = bitbucket.repository:Repodeploykeyspost',
            'repo_deploykey_list = bitbucket.repository:Repodeploykeysget',
            'repo_deploykey_edit = bitbucket.repository:Repodeploykeysedit',
            'repo_deploykey_delete = bitbucket.repository:Repodeploykeysdelete',
            'repo_fork = bitbucket.repository:Repofork',
            'repo_revision = bitbucket.repository:Reporevision',
            'repo_share = bitbucket.repository:Reposhareget',
            'repo_share_with = bitbucket.repository:Reposharepost',
            'repo_share_remove = bitbucket.repository:Reposharedelete',
            'sshkey = bitbucket.ssh:Sshkeyget',
            'sshkey_add = bitbucket.ssh:Sshkeypost',
            'sshkey_delete = bitbucket.ssh:Sshkeydelete',
            'user_info = bitbucket.user:User',
            'user_privileges = bitbucket.user:Userprivileges',
            'wiki_get = bitbucket.wiki:Wikiget',
            'wiki_post = bitbucket.wiki:Wikipost',
            ],
        },

    zip_safe=False,
    )