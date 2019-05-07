import configparser

from paver.path import path

from pybitbucket import bitbucket
from pybitbucket.repository import Repository, RepositoryRole
from pybitbucket.auth import OAuth2Authenticator
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.team import Team, TeamRole

cfg = configparser.ConfigParser()
cfg_filename = path('~/.bitbucketrc').expanduser()
if not cfg.read(cfg_filename):
        raise RuntimeError('Did not find configuration file {}'.format(cfg_filename))

client = bitbucket.Client(BasicAuthenticator(
    cfg['bitbucket']['username'],
    cfg['bitbucket']['password'],
    cfg['bitbucket']['email']
))

teams = Team.find_teams_for_role(role='admin', client=client)

repos = set()
for team in teams:
    for repo in team.repositories():
        if isinstance(repo, Repository):
            repos.add(repo)

for repo in repos:
    print("git clone " + repo.clone['ssh'])