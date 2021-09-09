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

# This file is originally hosted at https://github.com/CharLotteiu/pingcap-docs-checks/blob/main/check-tags.py.

import re
import sys
import os

# reference: https://stackoverflow.com/questions/35761133/python-how-to-check-for-open-and-close-tags
def stack_tag(tag, stack):
    t = tag[1:-1]
    first_space = t.find(' ')
    #print(t)
    if t[-1:] == '/':
        self_closed_tag = True
    elif t[:1] != '/':
        # Add tag to stack
        if first_space == -1:
            stack.append(t)
            # print("TRACE open", stack)
        else:
            stack.append(t[:first_space])
            # print("TRACE open", stack)
    else:
        if first_space != -1:
            t = t[1:first_space]
        else:
            t = t[1:]

        if len(stack) == 0:
            # print("No blocks are open; tried to close", t)
            closed_tag = True
        else:
            if stack[-1] == t:
                # Close the block
                stack.pop()
                # print("TRACE close", t, stack)
            else:
                # print("Tried to close", t, "but most recent open block is", stack[-1])
                if t in stack:
                    stack.remove(t)
                    # print("Prior block closed; continuing")

    # if len(stack):
    #     print("Blocks still open at EOF:", stack)
    return stack

def tag_is_wrapped(pos, content):
    tag_start = pos[0]
    tag_end = pos[1]
    content_previous = content[:tag_start][::-1] # reverse content_previous
    content_later = content[tag_end:]

    left_wraps_findall = re.findall(r'`', content_previous)
    left_single_backtick = len(left_wraps_findall) % 2
    right_wraps_findall = re.findall(r'`', content_later)
    right_single_backtick = len(right_wraps_findall) % 2
    # print(left_single_backtick, right_single_backtick)

    if left_single_backtick != 0 and right_single_backtick != 0:
        # print(content_previous.find('`'), content_later.find('`'))
        # print(content_previous)
        # print(content_later)
        return True
    else:
        # print(content_previous.find('`'), content_later.find('`'))
        # print(content_previous)
        # print(content_later)
        return False

def filter_frontmatter(content):
    # if there is frontmatter, remove it
    if content.startswith('---'):
        collect = []
        content_finditer = re.finditer(r'---\n', content)
        for i in content_finditer:
            meta_pos = i.span()[1]
            collect.append(meta_pos)

        # if the number of "---" >= 2
        if len(collect) >= 2:
            filter_point = collect[1]
            content = content[filter_point:]

    return content

def filter_backticks(content, filename):
    # remove content wrapped by backticks
    backticks = []
    content_findall = re.findall(r'```', content)
    if len(content_findall):
        content_finditer = re.finditer(r'```', content)
        for i in content_finditer:
            pos = i.span()
            backticks.append(pos)
        # e.g. backticks = [[23, 26],[37, 40],[123, 126],[147, 150]]
        if len(backticks) % 2 != 0:
            # print(len(content_findall))
            # print(backticks)
            # print(backticks[0][0], backticks[0][1])
            print(filename, ": Some of your code blocks ``` ```  are not closed. Please close them.")
            exit(1)
        elif len(backticks) != 0:
            backticks_start = backticks[0][0]
            backticks_end = backticks[1][1]
            # print(backticks_start, backticks_end)
            content = content.replace(content[backticks_start:backticks_end],'')
            content = filter_backticks(content, filename)
    return content

status_code = 0

# print(sys.argv[1:])
for filename in sys.argv[1:]:
    # print("Checking " + filename + "......\n")
    if os.path.isfile(filename):
        file = open(filename, "r", encoding='utf-8')
        content = file.read()
        file.close()

        content = filter_frontmatter(content)
        content = filter_backticks(content, filename)
        # print(content)
        result_findall = re.findall(r'<([^\n`>]*)>', content)
        if len(result_findall) == 0:
            # print("The edited markdown file " + filename + " has no tags!\n")
            continue
        else:
            result_finditer = re.finditer(r'<([^\n`>]*)>', content)
            stack = []
            for i in result_finditer:
                # print(i.group(), i.span())
                tag = i.group()
                pos = i.span()

                if tag[:4] == '<!--' and tag[-3:] == '-->':
                    continue
                elif content[pos[0]-2:pos[0]] == '{{' and content[pos[1]:pos[1]+2] == '}}':
                    # print(tag) # filter copyable shortcodes
                    continue
                elif tag[:5] == '<http': # or tag[:4] == '<ftp'
                    # filter urls
                    continue
                elif tag_is_wrapped(pos, content):
                    # print(content[int(pos[0])-1:int(pos[1]+1)])
                    # print(tag, 'is wrapped by backticks!')
                    continue

                stack = stack_tag(tag, stack)

            if len(stack):
                stack = ['<' + i + '>' for i in stack]
                print("ERROR: " + filename + ' has unclosed tags: ' + ', '.join(stack) + '.\n')
                status_code = 1

if status_code:
    print("HINT: Unclosed tags will cause website build failure. Please fix the reported unclosed tags. You can use backticks `` to wrap them or close them. Thanks.")
    exit(1)
