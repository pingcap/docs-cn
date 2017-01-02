#!/usr/bin/env python3
#
# Generate all-in-one Markdown file for ``doc-cn``
#

import re
import os


entry_file = "TOC.md"

hyper_link_pattern = re.compile(r'\[(.*?)\]\((.*?)(#.*?)?\)')

followup_files = []

in_toc = False

with open(entry_file) as fp:
    for line in fp:
        if line.startswith("## 目录"):
            in_toc = True
        elif in_toc:
            if line.startswith('#'):
                in_toc = False
                continue
            matches = hyper_link_pattern.findall(line)
            for match in matches:
                fpath = match[1]
                if fpath.endswith('.md'):
                    if fpath not in followup_files:
                        followup_files.append(fpath)

print(followup_files)

file_link_name = {}
for f in followup_files:
    tag = open(f).read().strip().split('\n')[0]
    if tag.startswith('# '):
        tag = tag[2:]
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
        # FIXME: better add media or static dir
        fname = os.path.basename(link)
        return '[%s](./op-guide/%s)' % (link_name, fname)
    else:
        return full

contents = []

for fname in followup_files:
    with open(fname) as fp:
        chapter = fp.read()
        chapter = hyper_link_pattern.sub(replace_link, chapter)
        contents.append(chapter)

with open("doc.md", 'w') as fp:
    fp.write('\n'.join(contents))