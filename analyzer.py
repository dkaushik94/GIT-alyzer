"""
    Written by Debojit Kaushik (1st April 2018)
    Script to analyze patch files and analyze what changes were made.
"""
import os, sys, traceback, requests, time, re
import json

try:
    import pygal
except Exception:
    os.system('sudo pip3 install pygal')

import numpy as np

try:
    from progress.bar import ChargingBar
except ImportError:
    os.system('sudo pip3 install progress')
except Exception:
    print(traceback.format_exc())


KEYWORDS = [
        'for', 
        'if', 
        'else:', 
        'while', 
        'try:',
        'except',
        'class', 
        'def', 
        'elif',
        'import',
        'raise',
        'finally',
        'del',
        'assert',
        'break',
        'raise'
    ]

pos_keys, neg_keys, extract= {}, {}, {}

for item in KEYWORDS:
    pos_keys[item], neg_keys[item] = 0, 0



def plot_it(x, y):
    try:
        bar_chart = pygal.Bar()
        bar_chart.title = "Repository patch analysis"
        bar_chart.x_labels = list(x.keys())
        bar_chart.add("Additions", list(x.values()))
        bar_chart.add("Deletions", list(y.values()))
        bar_chart.render_in_browser()
    except Exception:
        print(traceback.format_exc())



class CodeAnalysis:
    """
        Class with different methods to analyze patch files. 
        args: [Patch lines] 
    """
    def __str__(self):
        print("<CodeAnalysis Object>")
    
    @staticmethod
    def frequency_analyzer(pat_lines):
        """
            Input: 
                List of code patch lines.
                [+, +,+, +, +, +, -, -, -, -, -, -, -]
        """
        try:
            #Create empty frequency dictionaries.
            for item in pat_lines:
                for item2 in item.strip().split()[1:]:
                    if item2 and item2 in KEYWORDS:
                        if item.strip().split()[0] == "+":
                            pos_keys[item2] += 1
                        elif item.strip().split()[0] == "-":
                            neg_keys[item2] += 1
                        else:
                            pass
                    else:
                        pass
        except Exception:
            print(traceback.format_exc())

    @staticmethod
    def change_analyzer(diff_lines):
        try:
            """
                Construct workable data structure.
                Dict{"diff --git a/file b/file": [+,+,+,+,+,-,-,-,-,....]}
            """
            key = 0
            state = False
            diff_blocks = {}
            for item in diff_lines:
                if item.split(' ')[0] == 'diff' and re.match(r'.*.py', item.split(' ')[2]):
                    key = item
                    state = True
                    diff_blocks[key] = []
                elif item.split(' ')[0] == 'diff' and re.match(r'.*.py', item.split(' ')[2]):
                    state = False
                elif item.split(' ')[0] != 'diff' and state:
                    if item.split(' ')[0] in ['+', '-']:
                        diff_blocks[key].append(item[:1] + item[1:].strip())
                    else:
                        pass
            return diff_blocks
            
     
        except Exception:
            print(traceback.format_exc())


if __name__ == "__main__":
    try:
        metric_dict = {}
        l = os.listdir(os.chdir('PR_DATA/'))
        bar = ChargingBar("\033[1;33mProgress\033[1;m", max = len(l))
        curr_time = time.time()
        
        '''Change Analysis.'''
        print("\033[1;33mPerforming change analysis.\033[1;m")
        for item in l:
            f = open(item)
            blob = f.read().split('\n')
            ext = CodeAnalysis.change_analyzer(blob)
            extract[item] = ext
            bar.next()
        bar.finish()

        try:
            f = open('extract.json', 'w')
        except Exception:
            os.system('touch extract.json')
            f = open('extract.json', 'w')

        try:
            f.write(json.dumps(extract))
            #   
        except Exception:
            print(traceback.format_exc())

        # '''Frequency analysis.'''
        # for item in l:
        #     f = open(item)
        #     blob = f.read().split('\n')
        #     patlines = []
        #     for item2 in blob:
        #         if item2.split(' ')[0] in ['+', '-']:
        #             patlines.append(item2)
        #     CodeAnalysis.frequency_analyzer(patlines)
        #     bar.next()

        # print("\nTime Elapsed:", (time.time() - curr_time)/60, 'mins')
        # bar.finish()
        
        # print("\033[1;35mPostive Keys:\033[1;m\n", pos_keys)
        # print("\033[1;35mNegative Keys:\033[1;m\n", neg_keys)

        # plot_it(pos_keys, neg_keys)

    except Exception:
        print(traceback.format_exc())