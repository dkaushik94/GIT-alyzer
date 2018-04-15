
"""
    The script takes in GitHub credentials and downloads patch files corresponding to pull requests of issues of repositories 
    The downloaded patch files are stored as follows.
        --/Repos
            --/repo-1
                --patch1.txt
                --patch2.txt
            --/repo-2
                --patch1.txt
                --patch2.txt
"""


import sys
import os
import traceback
from urllib.request import urlopen
from urllib.request import URLError

try:
    import pygal
except Exception:
    os.system('sudo pip3 install pygal')

try:
    import requests
except ImportError:
    os.system('pip3 install requests')



try:
    import csv
except ImportError:
    os.system('pip3 install csv')


import requests
import csv

try:
    from progress.bar import ChargingBar
except ImportError:
    os.system('sudo pip3 install progress')

no_repos_to_analyze = 5
no_pages_to_analyze = 1

GITHUB_REPOS = 'https://api.github.com/search/repositories?q=language:python&page='
GITHUB_COMMIT_LIST = 'https://api.github.com/repos/'



def get_repos(username,password):
    try:
        no_of_repos_processed = 0
        # Create a folder 'Repos' so that we can download patch files for each repo.
        if 'Repos' not in os.listdir():
            os.mkdir('Repos')
        os.chdir('Repos')
        # Paginate based on no of repositories.
        for i in range(1,no_pages_to_analyze):
            repos = requests.get('https://api.github.com/search/repositories?q=language:python&page='+str(i), auth = (username,password))
            repos = repos.json()['items']
            
            for repo in repos:
                if(no_of_repos_processed >= int(no_repos_to_analyze)):
                    break
                bar = ChargingBar("\033[1;33mProgress\033[1;m", max = 450)
                print('Downloading patch files for the REPO - ' + repo['name'])
                
                if repo['name'] not in os.listdir():
                    os.mkdir(repo['name'])
                
                os.chdir(repo['name'])
                # We are paginating only first 15 pages of pull requests per repository. 
                for i in range(0,15):
                    prs_url = 'https://api.github.com/repos/'+repo['owner']['login']+"/"+repo['name']+"/"+'pulls?state=closed&page='+str(i)
                    pr_json = requests.get(prs_url, auth=(username,password))
                    if(pr_json.json() == []):
                        break
                    print(len(pr_json.json()))
                    for pr in pr_json.json():
                        if 'issue_url' in pr:
                            file = str(pr['id'])+'.txt'
                            os.system('touch ' + file)
                            patch = requests.get(pr['patch_url'],auth=(username,password))
                            p_file = open(file,'w')
                            p_file.write(patch.text)
                            p_file.close
                        bar.next()
                bar.finish()
                no_of_repos_processed = no_of_repos_processed + 1
                os.chdir('../')
    except:
        print(traceback.format_exc())
    
                


# Basic validation of username
def validate_username(username):
    if username == None or username == '':
        return False
    else:
        return True
# Basic validation of password
def validate_password(pwd):
    if pwd == None or pwd == '':
        return False
    else:
        return True

# Checks if the network connection is working
def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err: 
        return False


# Proceed only if network connection is working
if (not internet_on()):
    print('Network Connection not available... Please make sure your internet connection is working properly and run again')
    exit()


username = ''
password = ''


# Get username and password from the user.
username_is_valid = False
while(not username_is_valid):
    username = input('\033[1;033mPlease Enter your github username\033[1;m\n')
    if validate_username(username):
        username_is_valid = True
    else:
        print('Invalid username\n')

password_is_valid = False
while(not password_is_valid):
    pwd = input('\033[1;033mPlease Enter your github password\033[1;m\n')
    if (validate_password(pwd)):
        password_is_valid = True
    else:
        print('Invalid Password\n')
    
# Get no of repositories to analyze from the user
no_repos_to_analyze = input('Enter the number of repositories to be analyzed\n')
no_repos_to_analyze = int(no_repos_to_analyze)

# Calculate no of pages for pagination so that we download the patch files for no of repositorues specified.
no_pages_to_analyze = int(int(no_repos_to_analyze)/15)
if no_pages_to_analyze == 0:
    no_pages_to_analyze = 1
else:
    if no_repos_to_analyze % 15 != 0:
        no_pages_to_analyze = no_pages_to_analyze + 1

# incremneting jsut for the sake of looping
no_pages_to_analyze = no_pages_to_analyze + 1

get_repos(username,password)

