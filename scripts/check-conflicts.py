# Copyright 2021 PingCAP, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# MIT License

# Copyright (c) 2021 Charlotte Liu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# This file is originally hosted at https://github.com/CharLotteiu/pingcap-docs-checks/blob/main/check-conflicts.py.

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
