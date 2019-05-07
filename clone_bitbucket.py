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

# Set this to the directory that you want to use for your backups
backup_dir = 'C:/Src/Backup'

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

# Find all the teams that I am an admin for
teams = Team.find_teams_for_role(role='admin', client=client)

# Find all of the repos for the teams I am an admin for
repos = set()
for team in teams:
    for repo in team.repositories():
        if isinstance(repo, Repository):
            repos.add(repo)

# Create the backup directory if it doesn't exist
if not os.path.exists(backup_dir):
    os.mkdir(backup_dir)

# Git clone each repo to the backup directory deleting old backups
for repo in repos:
    dir = os.path.join(backup_dir, repo.full_name)
    if os.path.exists(dir):
        shutil.rmtree(dir)

    print('Cloning {} to {}'.format(repo.full_name, dir))
    Repo.clone_from(repo.clone['ssh'], dir)
