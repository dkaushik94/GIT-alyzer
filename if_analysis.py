import os
import re
import pygal
import traceback

"""
    This script detects the a defined series of patterns in lines containing if conditions. 
    It detects the following patterns between addition and removal lines.

    1)    if  no_LHS_change  (operator)         no_RHS_change:  --> 0 0 0
    2)    if  no_LHS_change  (operator)           changed_RHS:  --> 0 0 1
    3)    if  no_LHS_change  (operator_change)  no_RHS_change:  --> 0 1 0
    4)    if  no_LHS_change  (operator_change)    changed_RHS:  --> 0 1 1
    5)    if    changed_LHS  (operator)         no_RHS_change:  --> 1 0 0
    6)    if    changed_LHS  (operator)           changed_RHS:  --> 1 0 1 
    7)    if    changed_LHS  (operator_change)  no_RHS_change:  --> 1 1 0
    8)    if    changed_LHS  (operator_change)    changed_RHS:  --> 1 1 1

    The following code detects one of above patterns in a pair of addition and 
    removal lines in each patch file for each repo. 
"""

patterns = ["if  no_LHS_change  (operator)         no_RHS_change:",
            "if  no_LHS_change  (operator)           changed_RHS:",
            "if  no_LHS_change  (operator_change)  no_RHS_change:",
            "if  no_LHS_change  (operator_change)    changed_RHS:",
            "if    changed_LHS  (operator)         no_RHS_change:",
            "if    changed_LHS  (operator)           changed_RHS:",
            "if    changed_LHS  (operator_change)  no_RHS_change:",
            "if    changed_LHS  (operator_change)    changed_RHS:"]

result_dict = {'LopR':0,'Lop!R':0,'L!opR':0,'L!op!R':0,'!LopR':0,'!Lop!R':0,'!L!opR':0,'!L!op!R':0}

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
        print("not enough lines with if")
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
        print("not enough data to proceed")
        return

    '''
        We'll take each addition line containing if pattern and check how different it is from each of the removal line
        and see how different the lines are and which pattern it belongs to.
    '''
    
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
            print(result_dict)
            result_dict[pat_cond] = result_dict[pat_cond] + 1
            # return result_dict

def plot_it(result_dict,repo):
    try:
        bar_chart = pygal.Bar()
        bar_chart.title = "If pattern analysis"
        bar_chart.x_labels = patterns
        bar_chart.add("If Patterns", list(result_dict.values()))
        # bar_chart.add("Deletions", list(y.values()))
        bar_chart.render_to_file('../analysis'+repo+'.svg')
    except Exception:
        print(traceback.format_exc())

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
        
        analyze_if(patlines)
    plot_it(result_dict,repo)
    result_dict = {'LopR':0,'Lop!R':0,'L!opR':0,'L!op!R':0,'!LopR':0,'!Lop!R':0,'!L!opR':0,'!L!op!R':0}
    
final_result[repo] = result_dict
