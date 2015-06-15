===============================
README for Testing bitbucketcli
===============================

This README deals only with testing, not with actual bitbucketcli code.

Aim
===

- have test suite, which can automatically test most of `bitbucket` command functionality
- use `tox` to allow running tests in different python version

Installation
============

Best used in virtual environment.

::

    $ pip install pytest pyyaml

If you are going to use `tox`, you shall install it into global Python (as it
will try to install the whole suite into its own virtual environment)::

    $ sudo pip install tox

(or use ready-made system package for it, if available)


Prepare personal Bitbucket configuration file
=============================================

To make relevant tests, one must use it on some real bitbucket account.

To provide information about expected repositories, accessible accounts etc.
for given user account, you must create a file with extension `.acc_cfg` and
describe there your account and expected content.

The file shall live in project root.

See the sample `vlcinsky_acc_cfg` file and replace it with another one for your
account. You shall then remove the `vlcinsky.acc_cfg` file as you probably have
no access to it.


The test suite attempts to use all `*.acc_cfg` fields in project root.

Running py.test
===============

All tests shall be started from project root directory.

Just run the `py.test` command.

Running tox
===========

Just run the `tox` command and it shall do all the testing.

Open issues
===========

Possible problems with content encoding/decoding
------------------------------------------------

`bitbucketcli` is a command line tool written in Python 2.7. It might happen,
that running the test runs into problems with encoding/decoding strings on
console.

This issue is not resolved properly yet.

You might configure your console to use proper encoding e.g. by env. variable `PYTHONIOENCODING`::

    $ export PYTHONIOENCODING=utf-8:replace

what shall configure stdin/stdout to use utf-8 and in case, there are troubles
to encode a character, replace it with a question-mark.


Note, that this method might fail with tox (not sure, if it shares the
environmental variables you set up before running the `tox` command - I have
problem with that.

Running tox for other python versions
-------------------------------------

`tox.ini` used to declare environments to use for python 2.7 and 3.4.

However, as current `bitbucketcli` package is not really ready for Python 3.4,
this version was removed. You shall add it there as soon as you are ready to
make it running properly there.


How to deal with personal bitbucket account config
--------------------------------------------------

Bitbucket content is really sensitive information.

However, real testing must use some account.

Existing design requires a `*.acc_cfg` file to state, what content is to be expected, but this works only for one user and will not work in general for everybody.

Possible solution is to create piece of code, which would create such a file.
However, such a task is not trivial, as it requires duplication of many
features provided by the command `bitbucket`.

How to run the test suite against different `bitbucketcli` versions
-------------------------------------------------------------------

Currently there are at least two different versions of code for `bitbucketcli`:

- https://github.com/yspanchal/bitbucketcli - master branch
- https://github.com/vlcinsky/bitbucketcli - pep008 branch

Provided functionality shall be the same, but we cannot be sure untill really tested.

Test suite is currently not part of any of these versions.


Possible solutions is to simply copy `*.acc_cfg`, `tox.ini` and directory `tests` (e.g. over `tests.tar.gz` file) and use it (manually) in the project you work with.

As soon as we complete first tests, we shall continue using `pep008` version (integrated into master of `yspanchal`) and keep it there. At that time the tests shall be included into that branch too.

Poor test coverage
------------------

Initial test suite version is more proof of concept and does not cover many situation.

The test suite shall be extended to cover more.
