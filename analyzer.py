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
        'break'
    ]

pos_keys, neg_keys, extract= {}, {}, {}
PATCH_DUMP = []
CHANGE_TEMPLATE = {
            'action': None,
            'keywords': None, 
            'condition': None, 
            'value': None,
            'loop_entity': None,
            'exception_type': None,
            'raise_condition': None
        }


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



class File:
    def __init__(self, **kwargs):
        self.file_name = kwargs['file_name']
        self.changes = kwargs['changes']

class Changes:
    def __init__(self, args):
        self.action = args['action']
        self.keyword = args['keyword']
        self.conditions = args['condition']
        self.value = args['value']
        self.loop_entity = args['loop_entity']
        self.exception_type = args['exception_type']
        self.raise_condition = args['raise_condition'] 
   

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
    def diff_extract(diff_lines):
        try:
            """
                Construct workable data structure.
                Dict{"diff --git a/file b/file": [ +, +, +, +, +, -, -, -, -, . . . .]}
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
                        diff_blocks[key].append(item[:1] + ' ' + item[1:].strip())
                    else:
                        pass
            return diff_blocks
        except Exception:
            print(traceback.format_exc())



    @staticmethod
    def DumpGenerator(file_name, change_dict):
        try:
            global CHANGE_TEMPLATE
            CHANGE_TEMPLATE = CHANGE_TEMPLATE.fromkeys(list(CHANGE_TEMPLATE.keys()), None)
            for item in change_dict:
                CHANGE_TEMPLATE[item] = change_dict[item]
            ch = Changes(CHANGE_TEMPLATE)
            return ch.__dict__
        except Exception:
            print(traceback.format_exc())
    
    
    @staticmethod
    def change_analyzer(diff_extract):
        '''
            Method to extract changes and generate a JSON.
        '''
        try:
            global PATCH_DUMP
            for _file in diff_extract:
                dump = []
                for diff in diff_extract[_file]:
                    if len(diff_extract[_file][diff]):
                        for line in diff_extract[_file][diff]:
                            if len(line.split()[1:]) > 1 :
                                '''Conditional Statements.'''
                                keyword = line.split()[1]
                                if keyword == 'if' or keyword == 'elif':
                                    # CHANGE_TEMPLATE = CHANGE_TEMPLATE.fromkeys(list(CHANGE_TEMPLATE.keys()), None)
                                    # print(line[1:].strip())
                                    match_object = re.match(r'([elif]+)\s*(.*)]:', line[1:].strip()) 
                                    if match_object:
                                        groups = match_object.groups()
                                        temp = {}
                                        if line.split()[0] == '+':
                                            temp['action'] = 'added'
                                        elif line.split()[0] == '-':
                                            temp['action'] = 'removed'
                                        temp['keyword'] = groups[0]
                                        temp['condition'] = groups[1]
                                        dump.append(CodeAnalysis.DumpGenerator(_file ,temp))
                                elif keyword == 'for':
                                    match_object = re.match(r'for\s*(.*)\s*in\s*(.*):', line[1:].strip())
                                    if match_object:
                                        groups = match_object.groups()
                                        temp = {}
                                        if line.split()[0] == '+':
                                            temp['action'] = 'added'
                                        elif line.split()[0] == '-':
                                            temp['action'] = 'removed'
                                        temp['keyword'] = 'for'
                                        temp['loop_entity'] = groups[1]
                                        temp['value'] = groups[0] 
                                        dump.append(CodeAnalysis.DumpGenerator(_file ,temp))
                                elif keyword == 'while':
                                    match_object = re.match(r'while\s*(.*):', line[1:].strip())
                                    if match_object:
                                        groups = match_object.groups()
                                        temp = {}
                                        if line.split()[0] == '+':
                                            temp['action'] = 'added'
                                        elif line.split()[0] == '-':
                                            temp['action'] = 'removed'
                                        temp['keyword'] = 'while'
                                        temp['condition'] = groups[0] 
                                        dump.append(CodeAnalysis.DumpGenerator(_file ,temp))
                                elif keyword == 'except':
                                    match_object = re.match(r'except\s*([a-zA-Z0-9,.\s]+)\s*.*:', line[1:].strip())
                                    if len(line[1:].strip().replace(':', '').split()) == 1:
                                        exception_conditions = 'general'
                                    else:
                                        exception_conditions = line[1:].strip().replace(':', '').split()[1]
                                    if match_object:
                                        groups = match_object.groups()
                                        temp = {}
                                        if line.split()[0] == '+':
                                            temp['action'] = 'added'
                                        elif line.split()[0] == '-':
                                            temp['action'] = 'removed'
                                        temp['keyword'] = 'except'
                                        temp['exception_type'] = exception_conditions 
                                        dump.append(CodeAnalysis.DumpGenerator(_file ,temp))
                                elif keyword == 'raise':
                                    raise_conditions = line[1:].strip().replace(':', '').split()[1]
                                    temp = {}
                                    if line.split()[0] == '+':
                                        temp['action'] = 'added'
                                    elif line.split()[0] == '-':
                                        temp['action'] = 'removed'
                                    temp['keyword'] = 'raise'
                                    temp['raise_condition'] = raise_conditions 
                                    dump.append(CodeAnalysis.DumpGenerator(_file ,temp))
                                elif keyword == 'import':
                                    import_statement = line[1:].strip().replace(':', '').split()[1]
                                    temp = {}
                                    if line.split()[0] == '+':
                                        temp['action'] = 'added'
                                    elif line.split()[0] == '-':
                                        temp['action'] = 'removed'
                                    temp['keyword'] = 'import'
                                    temp['value'] = import_statement 
                                    dump.append(CodeAnalysis.DumpGenerator(_file ,temp))
                            else:
                                pass
                if dump:
                    fl = File(file_name = _file, changes = dump)
                    PATCH_DUMP.append(fl.__dict__)
                else:
                    dump = []
                    pass
            try:
                f = open('../extract.json', 'w')
            except Exception:
                os.system('touch ../extract.json')
                f = open('../extract.json', 'w')

            try:
                f.write(json.dumps(PATCH_DUMP))
                print("\033[1;33m..Dumped\033[1;m")
            except Exception:
                print(traceback.format_exc())            
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
            ext = CodeAnalysis.diff_extract(blob)
            if ext and list(ext.values()):
                extract[item] = ext
            else:
                pass
            bar.next()
        bar.finish()

        CodeAnalysis.change_analyzer(extract)

        try:
            f = open('extract.json', 'w')
        except Exception:
            os.system('touch extract.json')
            f = open('extract.json', 'w')

        try:
            f.write(json.dumps(extract))
            print("\033[1;33mFinished.\033[1;m")
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