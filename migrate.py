from azuredevops import AzureDevOps
import bitbucket

# Set this to the directory that you want to use for your backups
backup_dir = 'C:/Src/Backup'
azuredevops_project = 'Backup'

repos = bitbucket.backup_repos(backup_dir)

print()
print("=== All repositories Cloned ===")
print()

ado = AzureDevOps(azuredevops_project)
for (bitbucket_repo, git_repo) in repos:
    print('Creating {} repo on Azure DevOps'.format(bitbucket_repo.name))
    azure_repo = ado.create_repository(bitbucket_repo.name)
    remote = git_repo.create_remote('azuredevops', azure_repo.remote_url)
    assert remote.exists()
    print('Pushing {} to Azure DevOps'.format(bitbucket_repo.name))
    remote.push(refspec='refs/remotes/origin/*:refs/heads/*')

print()
print("=== All repositories Pushed ===")
print()