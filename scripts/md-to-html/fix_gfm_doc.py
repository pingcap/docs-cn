#!/usr/bin/env python3
# coding: utf8
#

from __future__ import print_function, unicode_literals

import re
import os

contents = []

# match all missing headings
missing_heading_patthern = re.compile(r'(^\\#+|\n\\#+)\s(.*)')

entry_file = ".build/gfm-doc-pre.md"

# match all punctuation other than "-", "_", space and zh/en characters
def get_heading_identifier(heading):
    return re.sub(r'[^\w\s\-_\u4e00-\u9fa5]', '', heading.replace(' ', '-')).lower()

def replace_missing_heading(match):
    title = match.group(2).strip()
    identifier = get_heading_identifier(title)

    return '\n' + '<div class="h7" id="' + identifier +'">' + title + '</div>'

def remove_yaml_metadata_block(chapter):
    return re.sub(r'\n## title\b.*\n\n', '\n', chapter)

try:
    with open(entry_file) as fp:
        chapter = fp.read()
        chapter = missing_heading_patthern.sub(replace_missing_heading, chapter)
        chapter = remove_yaml_metadata_block(chapter)
        contents.append(chapter)
        # add an empty line
        contents.append('')
except Exception as e:
        print(e)
        print("fix gfm doc pre file error: ignore!")

target_doc_file = '.build/gfm-doc.md'

with open(target_doc_file, 'w') as fp:
    fp.write('\n'.join(contents))
