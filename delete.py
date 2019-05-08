# Deletes old Bitbucket repos

import datetime

import bitbucket
import datetime

# Delete all repos older than...
min = datetime.datetime(2018, 12, 31, tzinfo=datetime.timezone.utc)

repos = bitbucket.get_repos()
for repo in repos:
    updated = datetime.datetime.strptime(repo.updated_on, '%Y-%m-%dT%H:%M:%S.%f%z')
    if(updated < min):
        print('Deleting {} which was last updated {}'.format(repo.name, updated))
        repo.delete()