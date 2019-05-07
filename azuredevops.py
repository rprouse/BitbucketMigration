import configparser
import pprint

from azure.devops.connection import Connection
from azure.devops.released.git import GitRepositoryCreateOptions, GitRepository
from msrest.authentication import BasicAuthentication
from paver.path import path

class AzureDevOps():
    '''Work with Azure DevOps'''
    def __init__(self):
        self.config = self.get_config()

        personal_access_token = self.config['azuredevops']['pat']
        organization_url = self.config['azuredevops']['organization']
        project = self.config['azuredevops']['project']

        self.connection = self.login(personal_access_token, organization_url)
        self.git_client = self.connection.clients.get_git_client()
        self.core_client = self.connection.clients.get_core_client()
        self.project = self.core_client.get_project(project)

    def get_config(self):
        '''Gets the config file'''
        cfg = configparser.ConfigParser()
        cfg_filename = path('~/.azuredevopsrc').expanduser()
        if not cfg.read(cfg_filename):
            raise RuntimeError('Did not find configuration file {}'.format(cfg_filename))

        return cfg

    def login(self, personal_access_token, organization_url):
        '''Logs into Azure DevOps and returns a connection'''
        # Create a connection to the org
        credentials = BasicAuthentication('', personal_access_token)
        connection = Connection(base_url=organization_url, creds=credentials)

        return connection

    def create_repository(self, name):
        '''Creates a repository in the Azure DevOps project
        :param str name: The repository name
        :rtype: [GitRepository]
        '''
        create_options = GitRepositoryCreateOptions(name=name, project=self.project)
        return self.git_client.create_repository(create_options)