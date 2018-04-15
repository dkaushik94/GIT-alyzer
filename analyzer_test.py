import os, traceback, time, re
from issues import get_repos

def ATest():
    try:
        print("This is a unit test, please select small number of repository.")
        timer = time.time()
        # os.system('python3 analyzer.py')
        found = 0
        for item in os.listdir():
            match_e1 = re.match(r'.*.svg', item)
            match_e2 = re.match(r'.*.json', item)
            if match_e1 or  match_e2:
                found += 1
            else:
                pass
        if found:
            print('\n------------------------------------\n')
            print('Test cleared in:', time.time() - timer)
            print('Tearing down.')
            os.system('rm -r *.svg')
            os.system('rm *.json')
        else:
            print('Test Failed!', time.time() - timer)
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    try:
        print("\033[1;32mInitiating test\033[1;m")
        ATest()
    except Exception:
        print(traceback.format_exc())