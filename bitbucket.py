import configparser
import os
import shutil

from git import Repo

from paver.path import path

from pybitbucket import bitbucket
from pybitbucket.repository import Repository, RepositoryRole
from pybitbucket.auth import OAuth2Authenticator
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.team import Team, TeamRole

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise RuntimeError(exc_info)

def login():
    '''Logs into Bitbucket and returns a Bitbucket client'''
    # Log into Bitbucket using credentials in ~/.bitbucketrc
    cfg = configparser.ConfigParser()
    cfg_filename = path('~/.bitbucketrc').expanduser()
    if not cfg.read(cfg_filename):
            raise RuntimeError('Did not find configuration file {}'.format(cfg_filename))

    client = bitbucket.Client(BasicAuthenticator(
        cfg['bitbucket']['username'],
        cfg['bitbucket']['password'],
        cfg['bitbucket']['email']
    ))
    return client

def backup_repos(backup_dir):
    '''
    Clones all Bitbucket repositories from all the teams that the user
    is an admin for to the to the given backup directory

    backup_dir: The directory to clone the repos to
    returns: The repositories that were cloned
    '''
    # Find all of the repos for the teams I am an admin for
    repos = get_repos()

    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    retval = set()

    # Git clone each repo to the backup directory deleting old backups
    for repo in repos:
        dir = os.path.join(backup_dir, repo.full_name)
        if os.path.exists(dir):
            shutil.rmtree(dir, ignore_errors=False, onerror=onerror)

        print('Cloning {} to {}'.format(repo.full_name, dir))
        git_repo = Repo.clone_from(repo.clone['ssh'], dir)

        retval.add((repo, git_repo))

    return retval

def get_repos():
    '''
    Gets all Bitbucket repositories from all the teams that the user
    is an admin for to the to the given backup directory
    '''
    client = login()

    # Find all the teams that I am an admin for
    teams = Team.find_teams_for_role(role='admin', client=client)

    # Find all of the repos for the teams I am an admin for
    repos = set()
    for team in teams:
        for repo in team.repositories():
            if isinstance(repo, Repository):
                repos.add(repo)

    return repos