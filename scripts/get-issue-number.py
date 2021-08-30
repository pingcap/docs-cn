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

# This file is originally hosted at https://github.com/CharLotteiu/pingcap-docs-checks/blob/main/get-issue-number.py.

import re, os, sys
import requests
from tempfile import mkstemp
from shutil import move
from os import remove
from bs4 import BeautifulSoup

def get_issue_link(pr_url):

    print("Connecting to " + pr_url + " ...")

    response = requests.get(pr_url)

    if response:

        resp = BeautifulSoup(response.text, "html.parser")

        table = resp.find("table", "d-block")

        paragraphs = table.findAll("p")

        flag = 0
        match = 0

        for p in  paragraphs:
            # print(p.contents[0])

            if isinstance(p.contents[0], str):
                match = re.search(r'(Issue Number)|(fix)|(bug).*', p.contents[0], re.I)

            if match or p.find('span', attrs = {"class": "issue-keyword"}):
                issue_link = p.find('a', attrs = {"data-hovercard-type":"issue"}) or p.find('a', attrs = {"class": "issue-link"})
                if issue_link:
                    flag = 1
                    link = issue_link['href']
                break

        if flag:
            print('Related issue number: ' + link)
            return link
        else:
            print("No related issue number.\n")
            return 0

        #print(paragraphs)

    else:
        print('Connection failed. No html content')
        return 0

def change_pr_to_issue(filename):

    fh, target_file_path = mkstemp()
    source_file_path = filename
    match_start = 1
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        with open(source_file_path,'r', encoding='utf-8') as source_file:

            for line in source_file:

                if re.match(r'## Bug',line):
                    match_start = 0
                    print("Match Start\n")

                if match_start == 0:
                    matchObj = re.search(r'\[#\d+\]\([a-zA-z]+://[^\s]*\)',line)
                    if matchObj:
                        link = re.search(r'[a-zA-z]+://[^\s]*[^\)]', matchObj.group())
                        pr_url = link.group()
                        issue_url = get_issue_link(pr_url)

                        # 判断有记录 issue link 的在原文件中替换
                        if issue_url:
                            issue_num = re.search(r'\d+', issue_url)
                            issue_md = '[#' + issue_num.group() + ']' + '(' + issue_url + ')'
                            line = re.sub(r'\[#\d+\]\([a-zA-z]+://[^\s]*\)', issue_md, line)
                            print(issue_md + '\n')

                target_file.write(line)

    remove(source_file_path)
    move(target_file_path, source_file_path)

# get_issue_link("https://github.com/pingcap/tidb/pull/22924")

# change_pr_to_issue('./releases/release-4.0.13.md')

if __name__ == "__main__":

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            change_pr_to_issue(filename)
