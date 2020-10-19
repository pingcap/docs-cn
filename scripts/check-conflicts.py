import re
import sys
import os

lineNum = 0
flag = 0
pos = []
single = []
mark = 0

for filename in sys.argv[1:]:
    single = []
    lineNum = 0
    if os.path.isfile(filename):
        with open(filename,'r') as file:
            for line in file:
                lineNum += 1
                if re.match(r'<{7}.*\n', line):
                    flag = 1
                    single.append(lineNum)
                elif re.match(r'={7}\n', line) :
                    flag = 2
                elif re.match(r'>{7}', line) and flag == 2:
                    single.append(lineNum)
                    pos.append(single)
                    single = []
                    flag = 0
                else:
                    continue
            

    if len(pos):
        mark = 1
        print("\n" + filename + ": this file has conflicts in the following lines:\n")
        for conflict in pos:
            if len(conflict) == 2:
                print("CONFLICTS: line " + str(conflict[0]) + " to line " + str(conflict[1]) + "\n")
    
    pos = []

if mark:
    print("The above conflicts will cause website build failure. Please fix them.")
    exit(1)
