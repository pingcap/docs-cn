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

# This file is originally hosted at https://github.com/CharLotteiu/pingcap-docs-checks/blob/main/check-zh-punctuation.py.

import sys, os, zhon.hanzi

# Check Chinese punctuation in English files.

def check_zh_punctuation(filename):

    lineNum = 0
    pos = []
    zh_punc = []
    acceptable_punc = ['–','—'] # em dash and en dash
    flag = 0

    with open(filename, 'r') as file:
        for line in file:

            count = 0
            lineNum += 1
            punc_inline = ""

            for char in line:

                if char in zhon.hanzi.punctuation and char not in acceptable_punc :
                    flag = 1
                    if count != 1:
                        pos.append(lineNum)
                    punc_inline += char
                    count = 1

            if punc_inline != "":
                zh_punc.append(punc_inline)

    if flag:
        print("\n" + filename + ": this file has Chinese punctuation in the following lines:\n")

        count = 0
        for lineNum in pos:
            print("Chinese punctuation: L" + str(lineNum) + " has " + zh_punc[count])
            count += 1

    return flag

if __name__ == "__main__":

    count = 0

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            flag = check_zh_punctuation(filename)
            if flag:
                count+=1

    if count:
        print("\nThe above issues will ruin your article. Please convert these marks into English punctuation.")
        exit(1)