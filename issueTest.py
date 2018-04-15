

import os

os.system(' python3 issues.py')

directories = os.listdir()

# Check if patch files for repositories were downloaded or not
try:
    assert('Repos' in directories)    
except :
    print('Repos directory was not created by the issues.py script')


os.chdir('Repos')

# Check if patch files for individual repositories were created or not
try:
    repo_list = os.listdir()
    assert(repo_list != [])
except:
    print('Individual directories were not created')

    