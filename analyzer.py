"""
    Written by Debojit Kaushik (1st April 2018)
    Script to analyze patch files and analyze what changes were made.
"""
import os, sys, traceback, requests, time, re, json
try:
    import numpy as np
except ImportError:
    print("Package 'numpy' missing..\nInstalling system-wide.")
    os.system('sudo pip3 install numpy')
try:
    import pygal
except Exception:
    os.system('sudo pip3 install pygal')
try:
    from progress.bar import ChargingBar
except ImportError:
    os.system('sudo pip3 install progress')
except Exception:
    print(traceback.format_exc())


'''
    List of keywords to check for in patches.
'''
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

#Initiate the dictionaries.
for item in KEYWORDS:
    pos_keys[item], neg_keys[item] = 0, 0

#Function to plot the values.
def plot_it(x, y):
    try:
        bar_chart = pygal.Bar()
        bar_chart.title = "Repository patch analysis"
        bar_chart.x_labels = list(x.keys())
        bar_chart.add("Additions", list(x.values()))
        bar_chart.add("Deletions", list(y.values()))
        bar_chart.render_to_file('../analysis.svg')
    except Exception:
        print(traceback.format_exc())


patterns = ["if  no_LHS_change  (operator)         no_RHS_change:",
                "if  no_LHS_change  (operator)           changed_RHS:",
                "if  no_LHS_change  (operator_change)  no_RHS_change:",
                "if  no_LHS_change  (operator_change)    changed_RHS:",
                "if    changed_LHS  (operator)         no_RHS_change:",
                "if    changed_LHS  (operator)           changed_RHS:",
                "if    changed_LHS  (operator_change)  no_RHS_change:",
                "if    changed_LHS  (operator_change)    changed_RHS:"]

def plot_repo_analysis(result_dict,repo):
    try:
        bar_chart = pygal.Bar()
        bar_chart.title = "If pattern analysis"
        bar_chart.x_labels = patterns
        bar_chart.add("If Patterns", list(result_dict.values()))
        bar_chart.render_to_file('../analysis'+repo+'.svg')
    except Exception:
        print(traceback.format_exc())

class File:
    '''
        Class which captures file  and establishes a File -> Changes heirarchy.
        File <> Change  relationship.
        File (FKey) into Change.
        ** This is repository independent.
        Constructor params:
            file_name: name of the file. Effectively represents the file entity.
            changes: change objects which represents culmination of channges wrt of a file.
    '''
    def __init__(self, **kwargs):
        self.file_name = kwargs['file_name']
        self.changes = kwargs['changes']

class Changes:
    """
        Class which captures changes with respect to every keyword.
        Serialize this class. 
    """
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
        Public class with different methods to analyze patch files.
        Contains different methods to deal with analysis of patch files.
        Class is specific to Python patch files only.
        
        - frequency_analyzer():
            Naive Method to analyze occurrance of different language 
            keywords over patches. Indicates Patches contain what changes from a very high level.
        
        - change_analyzer():
            Naive method to analyze changes in code and their propertie which
            were added/removed. Generates a analysis sugar out of the patch files.
    """

    patterns = ["if  no_LHS_change  (operator)         no_RHS_change:",
                "if  no_LHS_change  (operator)           changed_RHS:",
                "if  no_LHS_change  (operator_change)  no_RHS_change:",
                "if  no_LHS_change  (operator_change)    changed_RHS:",
                "if    changed_LHS  (operator)         no_RHS_change:",
                "if    changed_LHS  (operator)           changed_RHS:",
                "if    changed_LHS  (operator_change)  no_RHS_change:",
                "if    changed_LHS  (operator_change)    changed_RHS:"]

    pattern_look_up = {'LopR':"if  no_LHS_change  (operator)         no_RHS_change:",
                'Lop!R':"if  no_LHS_change  (operator)           changed_RHS:",
                'L!opR':"if  no_LHS_change  (operator_change)  no_RHS_change:",
                'L!op!R':"if  no_LHS_change  (operator_change)    changed_RHS:",
                '!LopR':"if    changed_LHS  (operator)         no_RHS_change:",
                '!Lop!R':"if    changed_LHS  (operator)           changed_RHS:",
                '!L!opR':"if    changed_LHS  (operator_change)  no_RHS_change:",
                '!L!op!R':"if    changed_LHS  (operator_change)    changed_RHS:"
}

    result_dict = {'LopR':0,'Lop!R':0,'L!opR':0,'L!op!R':0,'!LopR':0,'!Lop!R':0,'!L!opR':0,'!L!op!R':0}

    def __str__(self):
        print("<CodeAnalysis Class>")
    
    @staticmethod
    def frequency_analyzer(pat_lines):
        """
            Method to perform frequency analysis on keywords occurring
            over input patch file.
            Input: 
                List of code-patch lines.
                [
                    -, 
                    +, 
                    +, 
                    -,
                    .
                    .
                    .
                ]
            Returns:
                None
            Performs changes to global variable, pos_keys & neg_keys.
        """
        try:
            for item in pat_lines:
                for item2 in item.strip().split()[1:]:
                    if item2 and item2 in KEYWORDS:
                        #Check for keyword in pre-defined list of keywords.
                        #Select non-empty lines based on 
                        #first character being '+' or '-'.
                        if item.strip().split()[0] == "+":
                            pos_keys[item2] += 1
                        elif item.strip().split()[0] == "-":
                            neg_keys[item2] += 1
                        else:
                            pass
        except Exception:
            print(traceback.format_exc())

    @staticmethod
    def diff_extract(diff_lines):
        try:
            """
                Construct workable data structure.
                Params:
                diff_extract: list of lines from a patch file.
                [
                    '+ line 1',
                    '+ line 2', 
                    '- line 3'
                    .
                    .
                    .
                    '+/- line n'
                ]
                Returns:
                    Dictionary of diff blocks of lines where every key is
                    a diff block line and value is a list of diff lines
                    {
                        'diff --git a/file b/file':[line1, line2, line3..line_n]
                    }
            """
            key = 0
            state = False
            diff_blocks = {}
            for item in diff_lines:
                '''
                    Selects only file with .py extensions. Ignores readmes, Gitignores 
                    and other none code artifacts.
                    For every time 'diff' is encountered, collect the successive lines
                    starting with "+/-" until next 'diff' is encountered, then redo the process
                    as the next diff block of lines.
                    State is flag variable taking care of the first diff encountered or not. 
                '''
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
            '''
                CHANGE_TEMPLATE: Change stub dictionnary.
                Generates JSON for every change detected WRT to every
                type of change.
                Params:
                    file_name: File name of every change detected.
                    change_dict: Dictionary of change recorded 
            '''
            global CHANGE_TEMPLATE
            CHANGE_TEMPLATE = CHANGE_TEMPLATE.fromkeys(list(CHANGE_TEMPLATE.keys()), None)
            for item in change_dict:
                CHANGE_TEMPLATE[item] = change_dict[item]
            ch = Changes(CHANGE_TEMPLATE)
            return ch.__dict__
        except Exception:
            print(traceback.format_exc())
    
    @staticmethod
    def change_analyzer(diff_extract = []):
        '''
            Method to extract changes and generate a JSON.
            Writes JSON dump into a file ('extract.json')
            Returns:
                None
        '''
        try:
            global PATCH_DUMP
            assert diff_extract
            '''For every file.'''
            for _file in diff_extract:
                dump = []
                
                '''Looping every file object in diff_extract'''
                for diff in diff_extract[_file]:
                    if len(diff_extract[_file][diff]):
                        for line in diff_extract[_file][diff]:
                            if len(line.split()[1:]) > 1 :
                                '''
                                    Conditional Statements to check for every case.
                                    Checking Keywords:
                                        if, elif, raise, except, for, while, import
                                    Detects every keywords here for each line and extracts
                                    properties using ReGex or string analysis.
                                '''
                                keyword = line.split()[1]
                                if keyword == 'if' or keyword == 'elif':
                                    match_object = re.match(r'([elif]+)\s*(.*)]:', line[1:].strip()) 
                                    if match_object:
                                        # temp is a stub dictionary to generate Change().__dict__
                                        #Generate Changes() and serialize it.
                                        groups = match_object.groups()
                                        temp = {}
                                        #First element of every string denontes if the line was added or removed.
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
                                        #Generate Changes() and serialize it.
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
                                        #Generate Changes() and serialize it.
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
                                    #Genreate Dictionary temp to make Changes() instance.
                                    #Same process for every keyword detected.
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
                    #If dump is a non-empty list, create File() class and append to
                    #Global dictionary of PATCH_DUMP with changes of the file instance as dump.
                    fl = File(file_name = _file, changes = dump)
                    PATCH_DUMP.append(fl.__dict__)
                else:
                    dump = []
                    pass

            #Dump JSON into file. If file exists then open and dump,
            #If file doesn't exist create file and dump JSON after opening it. 
            try:
                f = open('../extract.json', 'w')
            except Exception:
                os.system('touch ../extract.json')
                f = open('../extract.json', 'w')

            try:
                f.write(json.dumps(PATCH_DUMP))
                print("\033[1;32m...JSON dumped!\033[1;m")
            except Exception:
                print(traceback.format_exc())

        except AssertionError:
            print('Bad Parameters. Please check parameters.')
        except Exception:
            print(traceback.format_exc())

    @staticmethod
    def analyze_if(patlines):
        '''
            Result Dict is used to store one of the 9 possible patterns in if conditions between + and - lines
            Result lookup dict is used to identify the pattern and increment the appropriate pattern in result dict
        '''
        
        result_lookup_dict = {'111':'LopR','110':'Lop!R','101':'L!opR','100':'L!op!R','011':'!LopR','010':'!Lop!R','001':'!L!opR','000':'!L!op!R'}
        pat_lines = []
        
        '''
            Remove all the " and ' from the lines so that the detection of 
            pattern of change is not due to a change in the type of quote
        '''
        
        for line in patlines:
            line = line.replace('\'','').replace('\"','')
            pat_lines.append(line)
        
        patlines = pat_lines

        '''
            We need to check if we have enough + and - lines containing a pattern --> if .*(operator).*:, 
            only then proceed to detect the particular change. 

            First we'll check the line for the pattern with regex and 
            then check if we have enough lines to analyze. If not we'll return
        '''
        
        new_patlines = []
        if_regex = re.compile('if.*(>|<|<=|>=|!=|==).*:')
        num_lines_with_if = 0
        for line in patlines:
            nline = line.replace('+','').replace('-','')
            if(if_regex.match(nline.strip())):
                new_patlines.append(line.strip())
                num_lines_with_if = num_lines_with_if + 1
        if(num_lines_with_if <=1):
            # print("not enough lines with if")
            return
        
        lineDict = {}
        
        # Creating a dictionary of lines and their corresponding state( addition -> + or removal -> -)
        newLines = []
        for line in new_patlines:
            newline = line[1:]
            lineDict[newline.strip()] = {'sign':line[0]}
            newLines.append(newline.strip())
        patlines = newLines
        if(patlines == []):
            # print("0 lines with if")
            return
        
        '''
            Checking for the comparision operator in the of condition and recording the 
            respective operator and its location. Location of the operator helps in 
            detecting if LHS of the operator is different while comparing with another line
        '''
        
        comps = ['==','>=','<=','!=','>','<',]
        for line in lineDict.keys():
            for op in comps:
                if(line.find(op) != -1):
                    lineDict[line]['op_loc'] = line.find(op)
                    lineDict[line]['op'] = op
                    break

        '''
            We now store lines with if pattern and +, and lines with if pattern and - in 
            respective lists. If any one of them have less than one, we don't have enough 
            data to compare between + and - lines. So we return. Else, we'll proceed.
        '''
        
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
            # print("not enough data to proceed")
            return

        '''
            We'll take each addition line containing if pattern and check how different it is from each of the removal line
            and see how different the lines are and which pattern it belongs to.
        '''
        
        for pLine in pLines:
            for nLine in nLines:
                res_pat = ''
                # print(lineDict[pLine])
                if(pLine[:lineDict[pLine]['op_loc']] == nLine[:lineDict[nLine]['op_loc']]):
                    res_pat = res_pat + '1'
                    # print("\n*******************************************************************\n")
                    # print(pLine + " and " + nLine + " has same LHS variables")
                    if(lineDict[pLine]['op'] == lineDict[nLine]['op']):
                        res_pat = res_pat + '1'
                        # print(pLine + " and " + nLine + " has same comparision operators")
                    else:
                        res_pat = res_pat + '0'
                        # print(pLine + " and " + nLine + " has different comparision operators")
                    p_op_loc = lineDict[pLine]['op_loc']
                    p_op_len = len(lineDict[pLine]['op'])
                    n_op_loc = lineDict[nLine]['op_loc']
                    n_op_len = len(lineDict[nLine]['op'])
                    if(pLine[p_op_loc+p_op_len:] == nLine[n_op_loc+n_op_len:]):
                        res_pat = res_pat + '1'
                        # print(pLine + " and " + nLine + " has same RHS evaluating parameter")
                    else:
                        res_pat = res_pat + '0'
                        # print(pLine + " and " + nLine + " has different RHS evaluating parameter")
                else:
                    # print("\n*******************************************************************\n")
                    res_pat = res_pat + '0'
                    # print(pLine + " and " + nLine + " has different LHS variables")
                    if(lineDict[pLine]['op'] == lineDict[nLine]['op']):
                        res_pat = res_pat + '1'
                        # print(pLine + " and " + nLine + " has same comparision operators")
                    else:
                        res_pat = res_pat + '0'
                        # print(pLine + " and " + nLine + " has different comparision operators")
                    p_op_loc = lineDict[pLine]['op_loc']
                    p_op_len = len(lineDict[pLine]['op'])
                    n_op_loc = lineDict[nLine]['op_loc']
                    n_op_len = len(lineDict[nLine]['op'])
                    if(pLine[p_op_loc+p_op_len:] == nLine[n_op_loc+n_op_len:]):
                        res_pat = res_pat + '1'
                        # print(pLine + " and " + nLine + " has same RHS evaluating parameter")
                    else:
                        res_pat = res_pat + '0'
                        # print(pLine + " and " + nLine + " has different RHS evaluating parameter")
                pat_cond = result_lookup_dict[res_pat]
                # print(CodeAnalysis.result_dict)
                CodeAnalysis.result_dict[pat_cond] = CodeAnalysis.result_dict[pat_cond] + 1

    @staticmethod
    def analyze_if_patterns():
        final_result = {}

        dirs = os.listdir()
        if 'Repos' not in dirs:
            print('Please download patch files for repositories')
            exit()

        # Get the list of all the repositories so that we can iterate over patch files of the repositories
        # and then analyze them.
        repo_list = os.listdir('./Repos')

        if repo_list == []:
            print('Please download the patch files and run the script again')
            exit()

        for repo in repo_list:
            if '.DS_Store' in repo:
                continue
            print('Analysing Repo: '+repo+'\n')
            patch_files = os.listdir('./Repos/'+repo)
            

            for patch in patch_files:
                patch_file = open('./Repos/'+repo+'/'+patch)
                blob = patch_file.read().split('\n')
                patlines = []
                for line in blob:
                    if line.split(' ')[0] in ['+', '-']:
                        patlines.append(line)
                
                CodeAnalysis.analyze_if(patlines)
            plot_it(CodeAnalysis.result_dict,repo)
            CodeAnalysis.result_dict = {'LopR':0,'Lop!R':0,'L!opR':0,'L!op!R':0,'!LopR':0,'!Lop!R':0,'!L!opR':0,'!L!op!R':0}
            
            final_result[repo] = CodeAnalysis.result_dict


'''Routine entry point.'''
if __name__ == "__main__":
    try:
        dirs = os.listdir()
        if 'Repos' not in dirs:
            print('Please download patch files for repositories')
            exit()

        # Get the list of all the repositories so that we can iterate over patch files of the repositories
        # and then analyze them.
        repo_list = os.listdir('./Repos')

        if repo_list == []:
            print('Please download the patch files and run the script again')
            exit()

        
        
        metric_dict = {}
        final_result = {}
        for repo in repo_list:
            if '.DS_Store' in repo:
                continue
            print('Analysing Repo: '+repo+'\n')
            
            patch_files = os.listdir('./Repos/'+repo)
            bar = ChargingBar("\033[1;33mProgress\033[1;m", max = len(patch_files))
            curr_time = time.time()    
            for patch in patch_files:
                patch_file = open('./Repos/'+repo+'/'+patch)
                blob = patch_file.read().split('\n')
                patlines = []
                for line in blob:
                    if line.split(' ')[0] in ['+', '-']:
                        patlines.append(line)
                bar.next()
                CodeAnalysis.analyze_if(patlines)
            bar.finish()
            plot_repo_analysis(CodeAnalysis.result_dict,repo)
            CodeAnalysis.result_dict = {'LopR':0,'Lop!R':0,'L!opR':0,'L!op!R':0,'!LopR':0,'!Lop!R':0,'!L!opR':0,'!L!op!R':0}
            final_result[repo] = CodeAnalysis.result_dict
                
        
            bar = ChargingBar("\033[1;33mProgress\033[1;m", max = len(patch_files))
            curr_time = time.time()    
            print('\033[1;32m-------------------------------------------------------------------------\033[1;m', end = '\n')
            print("\n\033[1;33mInitializing Change Analysis\033[1;m")
            for item in patch_files:
                patch_file = './Repos/'+repo+'/'+item
                f = open(patch_file)
                blob = f.read().split('\n')
                ext = CodeAnalysis.diff_extract(blob)
                if ext and len(list(ext.values())):
                    extract[item] = ext
                else:
                    pass
                bar.next()
            bar.finish()
            #Initiate Change Analyzer routine.
            CodeAnalysis.change_analyzer(extract)


            print('\n\033[1;32m-------------------------------------------------------------------------\033[1;m', end = '\n')
            bar = ChargingBar("\033[1;33mProgress\033[1;m", max = len(patch_files))
            print("\n\033[1;33mInitializing Frequency Analysis\033[1;m")
            '''Frequency analysis.'''
            for item in patch_files:
                patch_file = './Repos/'+repo+'/'+item
                f = open(patch_file)
                blob = f.read().split('\n')
                patlines = []
                for item2 in blob:
                    if item2.split(' ')[0] in ['+', '-']:
                        patlines.append(item2)
                CodeAnalysis.frequency_analyzer(patlines)
                bar.next()
            bar.finish()

            print("\n\033[1;32mTime Elapsed:\033[1;m", (time.time() - curr_time)/60, 'mins')
            print("\n\033[1;36mDo you want to plot the result of your analysis? [Y/N]\033[1;m", end = ' ')
            
            plot = input()
            if plot and plot.strip().lower() == 'y' or plot.strip().lower() == 'yes':
                plot_it(pos_keys, neg_keys)
                print('\n\033[1;32mGenerated analysis.svg file. Please open with a suitable party.\033[1;m')
            else:
                print('\033[1;33mByypassing plotting.\033[1;m')
                print("\n\033[1;35mPostive Keys:\033[1;m\n", pos_keys)
                print("\n\033[1;35mNegative Keys:\033[1;m\n", neg_keys)


    except Exception:
        print(traceback.format_exc())