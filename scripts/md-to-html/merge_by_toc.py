#!/usr/bin/env python3
# coding: utf8
#
# Generate all-in-one Markdown file for ``doc-cn``
# Tip: 不支持中文文件名
# readme.md 中的目录引用的md多次（或者md的sub heading)，以第一次出现为主

from __future__ import print_function, unicode_literals

import re
import os


followups = []
in_toc = False
contents = []

hyper_link_pattern = re.compile(r'\[(.*?)\]\((.*?)(#.*?)?\)')
toc_line_pattern = re.compile(r'([\-\+]+)\s\[(.*?)\]\((.*?)(#.*?)?\)')
image_link_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
level_pattern = re.compile(r'(\s*[\-\+]+)\s')
# match all headings
heading_prefix_pattern = re.compile(r'(^#+|\n#+)\s')
heading_patthern = re.compile(r'(^#+|\n#+)\s(.*)')
# match copyable snippet code
copyable_snippet_pattern = re.compile(r'{{< copyable .* >}}')
# match <div label="xxx"> tag of MDX `SimpleTab`
simple_tab_pane_pattern = re.compile(r'<div label="(.*)">')

entry_file = "TOC.md"

# stage 1, parse toc
with open(entry_file) as fp:
    level = 0
    current_level = ""
    for line in fp:
        if not in_toc and not line.startswith("<!-- "):
            in_toc = True
        elif in_toc and not line.startswith('#') and line.strip():
            ## get level from space length
            level_space_str = level_pattern.findall(line)[0][:-1]
            level = len(level_space_str) // 2 + 1 ## python divide get integer

            matches = toc_line_pattern.findall(line)
            if matches:
                for match in matches:
                    fpath = match[2]
                    if fpath.endswith('.md'):
                        # remove the first slash in the relative path
                        fpath = fpath[1:]
                        key = ('FILE', level, fpath)
                        if key not in followups:
                            followups.append(key)
                    elif fpath.startswith('http'):
                        ## remove list format character `- `, `+ `
                        followups.append(('TOC', level, line.strip()[2:]))
            else:
                name = line.strip().split(None, 1)[-1]
                key = ('TOC', level, name)
                if key not in followups:
                    followups.append(key)

        else:
            pass

# remove version mark in heading
def fix_heading(heading):
    return heading.replace('<span class="version-mark">', '').replace('</span>', '')

# match all punctuation other than "-", "_", space and zh/en characters
def get_heading_identifier(heading):
    fixed_heading = fix_heading(heading)
    return re.sub(r'[^\w\s\-_\u4e00-\u9fa5]', '', fixed_heading.replace(' ', '-')).lower()

# stage 2, get file heading
file_link_name = {}
title_pattern = re.compile(r'(^#+)\s.*')
for tp, lv, f in followups:
    if tp != 'FILE':
        continue
    try:
        for line in open(f).readlines():
            if line.startswith("#"):
                tag = line.strip()
                break
    except Exception as e:
        print(e)
        tag = ""
    if tag.startswith('# '):
        tag = tag[2:]
    elif tag.startswith('## '):
        tag = tag[3:]
    fixed_tag = get_heading_identifier(tag)
    file_link_name[f] = fixed_tag

def replace_link_wrap(chapter, name):

    # Note: 仅仅支持 hash 匹配，如果在多个文档中有同名 heading 会碰撞
    # 支持 chapter 文档中的 ./ddd.md, xxx.md, xxx.md#xxx 等
    def replace_link(match):
        full = match.group(0)
        link_name = match.group(1)
        link = match.group(2)
        frag = match.group(3)

        if link.startswith('http'):
            return full
        elif link.endswith('.md') or '.md#' in link:
            if not frag:
                link = link[1:]
                for fpath in file_link_name:
                    if link == fpath:
                        frag = '#' + file_link_name[fpath]
            else:
                # remove "." of internal links
                frag = frag.replace('.', '')
            return '[%s](%s)' % (link_name, frag)
        elif link.endswith('.png') or link.endswith('.PNG') or link.endswith('.jpeg') or link.endswith('.svg') or link.endswith('.gif') or link.endswith('.jpg'):
            # special handing for pic
            img_link = re.sub(r'[\.\/]*media\/', './media/', link, count=0, flags=0)
            return '[%s](%s)' % (link_name, img_link)
        else:
            return full

    return hyper_link_pattern.sub(replace_link, chapter)

def replace_heading_func(diff_level=0):

    def replace_heading(match):
        title = match.group(2).strip()
        fixed_title = fix_heading(title)

        if diff_level == 0:
            return match.group(0).replace(title, fixed_title)
        else:
            total_level = match.group(1).count('#') + diff_level
            return '\n' + '#' * total_level + ' ' + fixed_title

    return replace_heading

# remove copyable snippet code
def remove_copyable(match):
    return ''

# pick SimpleTab title and add them to content
def add_simple_tab_title(chapter):
    def add_simple_tab_title_repl(match):
        full = match.group(0)
        label = match.group(1)
        return full + '\n\n' + '<div class="mdx-simple-tab-title">' + label + '</div>\n'

    return simple_tab_pane_pattern.sub(add_simple_tab_title_repl, chapter)

# add data-external="1" to <video> tag for pandoc PDF generation
def add_external_attr_to_video(chapter):
    return chapter.replace('<video src', '<video data-external="1" src')

def remove_video_tag(chapter):
    return re.sub(r'<video\s.*></video>', '', chapter)

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
                chapter = replace_link_wrap(chapter, name)
                chapter = copyable_snippet_pattern.sub(remove_copyable, chapter)
                chapter = add_simple_tab_title(chapter)
                chapter = remove_video_tag(chapter)

                # fix heading level
                heading_matched = heading_prefix_pattern.findall(chapter)
                diff_level = level - heading_prefix_pattern.findall(chapter)[0].count('#')

                chapter = heading_patthern.sub(replace_heading_func(diff_level), chapter)
                contents.append(chapter)
                contents.append('') # add an empty line
        except Exception as e:
            print(e)
            print("generate file error: ignore!")

# stage 4, generage final doc.md
target_doc_file = '.build/full-doc.md'
with open(target_doc_file, 'w') as fp:
    fp.write('\n'.join(contents))
