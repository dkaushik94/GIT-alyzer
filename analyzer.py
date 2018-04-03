"""
    Written by Debojit Kaushik (1st April 2018)
    Script to analyze patch files and analyze what changes were made.
"""
import os, sys, traceback, requests
import pygal
import numpy as np
from progress.bar import Bar
import time

keywords = [
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
pos_keys, neg_keys = {}, {}

for item in keywords:
    pos_keys[item], neg_keys[item] = 0, 0



class Changes:
    """
        Class to capture changes and code patches.
    """
    def __init__



def plotit(x, y):
    try:
        bar_chart = pygal.Bar()
        bar_chart.title = "Repository patch analysis"
        bar_chart.x_labels = list(x.keys())
        bar_chart.add("Additions", list(x.values()))
        bar_chart.add("Deletions", list(y.values()))
        bar_chart.render_in_browser()
    except Exception:
        print(traceback.format_exc())

def analyzer(patlines):
    try:
        #Create empty frequency dictionaries.
        for item in patlines:
            for item2 in item.strip().split()[1:]:
                if item2 and item2 in keywords:
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



if __name__ == "__main__":
    try:
        metric_dict = {}
        l = os.listdir(os.chdir('PR_DATA/'))
        bar = Bar("Progress", max = len(l))
        curr_time = time.time()
        for item in l:
            f = open(item)
            blob = f.read().split('\n')
            patlines = []
            for item2 in blob:
                if item2.split(' ')[0] in ['+', '-']:
                    patlines.append(item2)
            # print("\033[1;033mAnalyzing:\033[1;m", item)
            analyzer(patlines)
            bar.next()
        print("\nTime Elapsed:", (time.time() - curr_time)/60, 'mins')
        bar.finish()
        print("\033[1;35mPostive Keys:\033[1;m\n", pos_keys)
        print("\033[1;35mNegative Keys:\033[1;m\n", neg_keys)

        plotit(pos_keys, neg_keys)

    except Exception:
        print(traceback.format_exc())