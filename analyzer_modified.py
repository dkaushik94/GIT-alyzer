"""
    Written by Debojit Kaushik (1st April 2018)
    Script to analyze patch files and analyze what changes were made.
"""
import os, sys, traceback, requests
import pygal
import numpy as np
from progress.bar import Bar
import time
import re

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



# class Changes:
#     """
#         Class to capture changes and code patches.
#     """
#     def __init__



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

def analyze_if(patlines):
    if_regex = re.compile('if(.*(>|<|<=|>=|!=|==).*):')
    num_lines_with_if = 0
    for line in patlines:
        line = line.replace('+','')
        line = line.replace('-','')
        if(if_regex.match(line.replace(' ',''))):
            num_lines_with_if = num_lines_with_if + 1
    if(num_lines_with_if <=1):
        print("not enough lines with if")
        return
    
    lineDict = {}
    resultDict = {'LopR':0,'Lop!R':0,'L!opR':0,'L!op!R':0,'!LopR':0,'!Lop!R':0,'!L!opR':0,'!L!op!R':0}
    result_lookup_dict = {'111':'LopR','110':'Lop!R','101':'L!opR','100':'L!op!R','011':'!LopR','010':'!Lop!R','001':'!L!opR','000':'!L!op!R'}
    newLines = []
    for line in patlines:
        newline = line[1:].replace(" ","")
        lineDict[newline] = {'sign':line[0]}
        newLines.append(newline)
    patlines = newLines
    if(patlines == []):
        print("0 lines with if")
        return
    
    comps = ['==','>','<','>=','<=','!=']
    for line in lineDict.keys():
        for op in comps:
            if(line.find(op) != -1):
                lineDict[line]['op_loc'] = line.find(op)
                lineDict[line]['op'] = op

    pLines = []
    nLines = []
    for line in lineDict.keys():
        if(lineDict[line]['sign'] == '+'):
            pLines.append(line)
        else:
            nLines.append(line)
    
    if(len(pLines) >= 1 and len(nLines) >=1 ):
        pass
    else:
        print("not enough data to proceed")
        return

    for pLine in pLines:
        for nLine in nLines:
            res_pat = ''
            print(lineDict[pLine])
            if(pLine[:lineDict[pLine]['op_loc']] == nLine[:lineDict[nLine]['op_loc']]):
                res_pat = res_pat + '1'
                print("\n*******************************************************************\n")
                print(pLine + " and " + nLine + " has same LHS variables")
                if(lineDict[pLine]['op'] == lineDict[nLine]['op']):
                    res_pat = res_pat + '1'
                    print(pLine + " and " + nLine + " has same comparision operators")
                else:
                    res_pat = res_pat + '0'
                    print(pLine + " and " + nLine + " has different comparision operators")
                p_op_loc = lineDict[pLine]['op_loc']
                p_op_len = len(lineDict[pLine]['op'])
                n_op_loc = lineDict[nLine]['op_loc']
                n_op_len = len(lineDict[nLine]['op'])
                if(pLine[p_op_loc+p_op_len:] == nLine[n_op_loc+n_op_len:]):
                    res_pat = res_pat + '1'
                    print(pLine + " and " + nLine + " has same RHS evaluating parameter")
                else:
                    res_pat = res_pat + '0'
                    print(pLine + " and " + nLine + " has different RHS evaluating parameter")
            else:
                print("\n*******************************************************************\n")
                res_pat = res_pat + '0'
                print(pLine + " and " + nLine + " has different LHS variables")
                if(lineDict[pLine]['op'] == lineDict[nLine]['op']):
                    res_pat = res_pat + '1'
                    print(pLine + " and " + nLine + " has same comparision operators")
                else:
                    res_pat = res_pat + '0'
                    print(pLine + " and " + nLine + " has different comparision operators")
                p_op_loc = lineDict[pLine]['op_loc']
                p_op_len = len(lineDict[pLine]['op'])
                n_op_loc = lineDict[nLine]['op_loc']
                n_op_len = len(lineDict[nLine]['op'])
                if(pLine[p_op_loc+p_op_len:] == nLine[n_op_loc+n_op_len:]):
                    res_pat = res_pat + '1'
                    print(pLine + " and " + nLine + " has same RHS evaluating parameter")
                else:
                    res_pat = res_pat + '0'
                    print(pLine + " and " + nLine + " has different RHS evaluating parameter")
            pat_cond = result_lookup_dict[res_pat]
            resultDict[pat_cond] = resultDict[pat_cond] + 1
    print(resultDict)




if __name__ == "__main__":
    try:
        metric_dict = {}
        l = os.listdir(os.chdir('PR_DATA/'))
        bar = Bar("Progress", max = len(l))
        curr_time = time.time()
        i = 0
        for item in l:
            # if(i>50):
            #     break
            f = open(item)
            blob = f.read().split('\n')
            patlines = []
            for item2 in blob:
                if item2.split(' ')[0] in ['+', '-']:
                    patlines.append(item2)
            print("\033[1;033mAnalyzing:\033[1;m\n", item)
            # analyzer(patlines)
            analyze_if(patlines)
            bar.next()
            # i = i+1
        print("\nTime Elapsed:", (time.time() - curr_time)/60, 'mins')
        bar.finish()
        # print("\033[1;35mPostive Keys:\033[1;m\n", pos_keys)
        # print("\033[1;35mNegative Keys:\033[1;m\n", neg_keys)

        # plotit(pos_keys, neg_keys)

    except Exception:
        print(traceback.format_exc())