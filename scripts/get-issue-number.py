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

def get_issue_link(repo, pr_num):
    pr_url = 'https://api.github.com/repos/{}/issues/{}'.format(repo, pr_num)
    response = requests.get(pr_url, auth = ("user", token)).json()
    body = response.get("body")
    if body:
        match_link = re.search(r'(?:(?:Issue Number)|(?:fix)|(?:bug)|(?:cc)|(?:ref)|(?:close)).*?(https?://(?:www\.)?github\.com/.*?/issues/(\d+))', body, re.I)
        if match_link:
            issue_url = match_link.group(1)
            issue_num = match_link.group(2)
            return issue_url, issue_num
        else:
            match_num = re.search(r'(?:(?:Issue Number)|(?:fix)|(?:bug)|(?:cc)|(?:ref)|(?:close)).*?#(\d+)', body, re.I)
            if match_num:
                issue_num = match_num.group(1)
                issue_url = 'https://github.com/{}/issues/{}'.format(repo, issue_num)
                return issue_url, issue_num
    return None, None

def change_pr_to_issue(filename):

    fh, target_file_path = mkstemp()
    source_file_path = filename
    match_start = 1
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        with open(source_file_path,'r', encoding='utf-8') as source_file:

            for line in source_file:

                if re.match(r'# TiDB .* Release Notes',line):
                    match_start = 0
                    print("Match Start\n")

                if match_start == 0:
                    matchObj = re.search(r'\[(#\d+)\]\(https?://(?:www\.)?github\.com/(.*?)/pull/(\d+).*?\)',line)
                    if matchObj:
                        repo = matchObj.group(2)
                        pr_num = matchObj.group(3)
                        issue_url, issue_num = get_issue_link(repo, pr_num)
                        # 判断有记录 issue link 的在原文件中替换
                        if issue_url and issue_num:
                            begin, end = matchObj.span(0)
                            line = line[:begin] + "[#{}]({})".format(issue_num, issue_url) + line[end:]
                target_file.write(line)

    remove(source_file_path)
    move(target_file_path, source_file_path)

# get_issue_link("pingcap/tidb","34111")

# change_pr_to_issue('./releases/release-4.0.13.md')

# Please add your GitHub token to environment variables.
# When you first use this script, you can execute the following command `export GitHubToken="your_token"` to add your token.

if __name__ == "__main__":
    token = os.environ["GitHubToken"]
    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            change_pr_to_issue(filename)
