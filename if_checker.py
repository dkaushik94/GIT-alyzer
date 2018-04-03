import re


line1 = "if(x>10):"
line2 = "if(x<10):"
line3 = "if(current_time==3):"
line4 = "if(x<10):"
line5 = "if(y!=34):"

lineDict = {line1:{'sign':'+'},line2:{'sign':'-'},line3:{'sign':'-'},line4:{'sign': '-'},line5:{'sign': '+'}}
comps = ['==','>','<','>=','<=','!=']
comp_regex = re.compile('if(.*(>|<|<=|>=|!=|==).*):')

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

for pLine in pLines:
    for nLine in nLines:
        if(pLine[:lineDict[pLine]['op_loc']] == nLine[:lineDict[nLine]['op_loc']]):
            print("\n*******************************************************************\n")
            print(pLine + " and " + nLine + " has same LHS variables")
            if(lineDict[pLine]['op'] == lineDict[nLine]['op']):
                print(pLine + " and " + nLine + " has same comparision operators")
            else:
                print(pLine + " and " + nLine + " has different comparision operators")
            p_op_loc = lineDict[pLine]['op_loc']
            p_op_len = len(lineDict[pLine]['op'])
            n_op_loc = lineDict[nLine]['op_loc']
            n_op_len = len(lineDict[nLine]['op'])
            if(pLine[p_op_loc+p_op_len:] == nLine[n_op_loc+n_op_len:]):
                print(pLine + " and " + nLine + " has same RHS evaluating parameter")
            else:
                print(pLine + " and " + nLine + " has different RHS evaluating parameter")
        else:
            print("\n*******************************************************************\n")
            print(pLine + " and " + nLine + " has different LHS variables")
            if(lineDict[pLine]['op'] == lineDict[nLine]['op']):
                print(pLine + " and " + nLine + " has same comparision operators")
            else:
                print(pLine + " and " + nLine + " has different comparision operators")
            p_op_loc = lineDict[pLine]['op_loc']
            p_op_len = len(lineDict[pLine]['op'])
            n_op_loc = lineDict[nLine]['op_loc']
            n_op_len = len(lineDict[nLine]['op'])
            if(pLine[p_op_loc+p_op_len:] == nLine[n_op_loc+n_op_len:]):
                print(pLine + " and " + nLine + " has same RHS evaluating parameter")
            else:
                print(pLine + " and " + nLine + " has different RHS evaluating parameter")
        







