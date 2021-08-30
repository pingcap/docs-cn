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

# This file is originally hosted at https://github.com/CharLotteiu/pingcap-docs-checks/blob/main/check-control-char.py.

import re, sys, os

# Check control characters.
def check_control_char(filename):

    lineNum = 0
    pos = []
    flag = 0

    with open(filename,'r') as file:
        for line in file:

            lineNum += 1

            if re.search(r'[\b]', line):
                pos.append(lineNum)
                flag = 1

    if flag:
        print("\n" + filename + ": this file has control characters in the following lines:\n")
        for cc in pos:
            print("CONTROL CHARACTERS: L" + str(cc))
        print("\nPlease delete these control characters.")

    return flag

if __name__ == "__main__":

    count = 0

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            flag = check_control_char(filename)
            if flag:
                count+=1

    if count:
        print("\nThe above issues will cause website build failure. Please fix them.")
        exit(1)