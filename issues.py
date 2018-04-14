
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
from urllib.request import urlopen
from urllib.request import URLError

try:
    import requests
except:
    os.system('pip3 install requests')

try:
    import git
except:
    os.system('pip3 install git')

try:
    import csv
except:
    os.system('pip3 install csv')


import requests
import csv
import git




no_repos_to_analyze = 5

GITHUB_REPOS = 'https://api.github.com/search/repositories?q=language:python&page='
GITHUB_COMMIT_LIST = 'https://api.github.com/repos/'



def get_repos(username,password):
    if 'Repos' not in os.listdir():
        os.mkdir('Repos')
    os.chdir('Repos')
    for i in range(1,int(no_repos_to_analyze)+1):
        repos = requests.get('https://api.github.com/search/repositories?q=language:python&page='+str(i), auth = (username,password))
        repos = repos.json()['items']
        all_data = []
        all_data.append(["pr_id","title","url","diff_url","patch_url","issue_url","state","body","merge_commit_sha"])
        for repo in repos:
        
            print('Downloading patch files for the REPO - ' + repo['name'])
            os.mkdir(repo['name'])
            os.chdir(repo['name'])
            for i in range(0,8):
                prs_url = 'https://api.github.com/repos/'+repo['owner']['login']+"/"+repo['name']+"/"+'pulls?state=closed&page='+str(i)
                pr_json = requests.get(prs_url, auth=(username,password))
                if(pr_json.json() == []):
                    break
                for pr in pr_json.json():
                    if 'issue_url' in pr:
                        file = str(pr['id'])+'.txt'
                        os.system('touch ' + file)
                        pr_data = []
                        pr_data.append(pr['id'])
                        pr_data.append(pr['title'])
                        pr_data.append(pr['url'])
                        pr_data.append(pr['diff_url'])
                        pr_data.append(pr['patch_url'])
                        pr_data.append(pr['issue_url'])
                        pr_data.append(pr['state'])
                        pr_data.append(pr['body'])
                        pr_data.append(pr['merge_commit_sha'])
                        all_data.append(pr_data)
                        patch = requests.get(pr['patch_url'],auth=(username,password))
                        p_file = open(file,'w')
                        p_file.write(patch.text)
                        p_file.close
            os.chdir('../')



def validate_username(username):
    if username == None or username == '' or (not username.isalnum()):
        return False
    else:
        return True

def validate_password(pwd):
    if pwd == None or pwd == '':
        return False
    else:
        return True




def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err: 
        return False

if (not internet_on):
    print('Network Connection not available... Please make sure internet connection is working properly and run again')
    exit()


username = ''
password = ''


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
    
no_repos_to_analyze = input('Enter the number of repositories to be analyzed\n')
get_repos(username,password)

