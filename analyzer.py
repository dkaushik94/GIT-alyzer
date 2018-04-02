"""
    Written by Debojit Kaushik (1st April 2018)
    Script to analyze patch files and analyze what changes were made.
"""
import os, sys, traceback, requests

def analyzer(patlines):
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
        'import'
    ]
    try:
        keys = {}
        for item in keywords:
            keys[item] = 0
        for item in patlines:
            for item2 in item.strip().split()[1:]:
                if item2 and item2 in keys:
                    keys[item2] += 1
                else:
                    pass
        print(keys)
    except Exception:
        print(traceback.format_exc())


if __name__ == "__main__":
    try:
        r = requests.get("https://patch-diff.githubusercontent.com/raw/pallets/flask/pull/2608.patch", auth=("dkaushik94","soundspace312"))
        blob = r.text.split('\n')
        patlines = []
        for item in blob:
            if item.split(' ')[0] in ['+', '-']:
                patlines.append(item)
        analyzer(patlines)
    except Exception:
        print(taceback.format_exc())