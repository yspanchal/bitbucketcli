from os.path import expanduser
import os
import imp
import logging


def get_filename():
    """
    Returns the default filepath where the credentials are going to be stored.
    :return: String (filepath)
    """
    home = expanduser("~")
    filename = os.path.join(home, '.bitbucket.py')
    return filename


def read_creds():
    """
    Load the credentials from the filepath returned by get_filename
    :return: tuple of strings (user, passwrd)
    """
    log = logging.getLogger(__name__ + '.Wikiget')
    try:
        filename = get_filename()
        creds = imp.load_source('.bitbucket', filename)
        user = creds.username
        passwd = creds.passwd
        return user, passwd
    except (IOError, NameError), e:
        log.error("Error with variable or file: " + str(e))
        raise e
    except Exception, e:
        log.error("Unhandled error" + str(e))
        raise e
    pass

