# Bitbucket Migration

Moves repositories from Bitbucket to Azure DevOps. Currently fairly hard-coded
to our environment as it will be a one off run.

## Setup for Development

### Install Python 3.7+ and setup a Virtual Environment

You only need to do the following once when you are setting up your development
environment.

1. Install the latest version of Python 3.7+
2. Open this directory on the command line
4. Create a virtual environment, `py -3 -m venv venv`

### Activate the Virtual Environment

You need to do this whenever you are starting development or running this project.

1. Activate the virtual environment, `.\venv\Scripts\Activate.ps1`

### Restore Pip Packages

You only need to do this if the imported packages in `requirements.txt` change. You
must have activated your environment first.

1. `pip install -r requirements.txt`

### Update Required Packages in `Requirements.txt`

You only need to do this if you are adding dependencies to new Python packages
or upgrading the existing packages. You must have activated your environment first.

1. Install new packages with `pip install packagename` or update existing packages
with `pip update packagename`
2. Develop and test with the new package.
3. Capture the package changes with `pip freeze > requirements.txt`