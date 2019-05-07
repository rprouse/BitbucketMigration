import bitbucket

# Set this to the directory that you want to use for your backups
backup_dir = 'C:/Src/Backup'

repos = bitbucket.backup_repos(backup_dir)
