#!/usr/bin/env python3
# coding: utf8
#
# Generate all-in-one Markdown file for ``doc-cn``
#

from __future__ import print_function, unicode_literals

import re
import os


entry_file = "TOC.md"
followups = []
in_toc = False
contents = []

hyper_link_pattern = re.compile(r'([\-\+]+)\s\[(.*?)\]\((.*?)(#.*?)?\)')
image_link_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
level_pattern = re.compile(r'(\s*[\-\+]+)\s')
# match all headings
heading_patthern = re.compile(r'(^#+|\n#+)\s')

# stage 1, parse toc
with open(entry_file) as fp:
    level = 0
    current_level = ""
    for line in fp:
        if line.startswith("## 目录"):
            in_toc = True
            print("in toc")
        elif in_toc and line.startswith('## '):
            # yes, toc processing done
            # contents.append(line[1:]) # skip 1 level TOC
            break
        elif in_toc and not line.startswith('#') and line.strip():
            level_str = level_pattern.findall(line)[0]
            print("level", level_str)
            if len(level_str) > len(current_level):
                level += 1
            elif len(level_str) < len(current_level):
                level -= 1
            current_level = level_str

            matches = hyper_link_pattern.findall(line)
            if matches:
                for match in matches:
                    fpath = match[2]
                    if fpath.endswith('.md'):
                        key = ('FILE', level, fpath)
                        if key not in followups:
                            print(key)
                            followups.append(key)
                #    else:
                #        followups.append(('RAW', level, line.strip()))
            else:
                name = line.strip().split(None, 1)[-1]
                key = ('TOC', level, name)
                if key not in followups:
                    print(key)
                    followups.append(key)


        else:
            pass

    # overview part in README.md
    followups.insert(1, ("RAW", 0, fp.read()))

for k in followups:
    print(k)

# stage 2, get file heading
file_link_name = {}
for tp, lv, f in followups:
    if tp != 'FILE':
        continue
    try:
        tag = open(f).read().strip().split('\n')[0]
    except Exception as e:
        tag = "ERROR"
    if tag.startswith('# '):
        tag = tag[2:]
    elif tag.startswith('## '):
        tag = tag[3:]
    file_link_name[f] = tag.lower().replace(' ', '-')

print(file_link_name)


def replace_link(match):
    full = match.group(0)
    link_name = match.group(1)
    link = match.group(2)
    frag = match.group(3)
    if link.endswith('.md'):
        if not frag:
            for fpath in file_link_name:
                if os.path.basename(fpath) == os.path.basename(link):
                    frag = '#' + file_link_name[fpath]

        return '[%s](%s)' % (link_name, frag)
    elif link.endswith('.png'):
        # special handing for pic
        fname = os.path.basename(link)
        return '[%s](./media/%s)' % (link_name, fname)
    else:
        return full

def replace_heading_func(diff_level=0):

    def replace_heading(match):
        if diff_level == 0:
            return match.group(0)
        else:
            return '\n' + '#' * (match.group(0).count('#') + diff_level) + ' '


    return replace_heading

def replace_img_link(match):
    full = match.group(0)
    link_name = match.group(1)
    link = match.group(2)

    if link.endswith('.png'):
        fname = os.path.basename(link)
        return '![%s](./media/%s)' % (link_name, fname)

# stage 3, concat files
for type_, level, name in followups:
    if type_ == 'TOC':
        contents.append("\n{} {}\n".format('#' * level, name))
    elif type_ == 'RAW':
        contents.append(name)
    elif type_ == 'FILE':
        try:
            with open(name) as fp:
                chapter = fp.read()
                chapter = hyper_link_pattern.sub(replace_link, chapter)
                chapter = image_link_pattern.sub(replace_img_link, chapter)

                # fix heading level
                diff_level = level - heading_patthern.findall(chapter)[0].count('#')

                print(name, type_, level, diff_level)
                chapter = heading_patthern.sub(replace_heading_func(diff_level), chapter)
                contents.append(chapter)
                contents.append('') # add an empty line
        except Exception as e:

            print("generate file error: ignore!")

# stage 4, generage final doc.md
with open("doc.md", 'w') as fp:
    fp.write('\n'.join(contents))
