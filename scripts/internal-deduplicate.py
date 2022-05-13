# This script checks whether the same release notes file has duplicate note within itself.
# The check is based on issue number.

import re, os

def get_note_info(path):
    exst_notes = []
    with open(path,'r', encoding='utf-8') as fp:
        for line in fp:
            exst_issue_num = re.search('\[#\d{4,5}\]', line)
            if exst_issue_num:
                note_pair = exst_issue_num.group()
                exst_notes.append(note_pair)
        return exst_notes


if __name__ == "__main__":
    path = r'/Users/grcai/Documents/GitHub/qiancai/docs/releases/release-5.4.1.md'
    exst_note = get_note_info(path)
    mylist = exst_note
    myset = set(mylist)
    for item in myset:
        if mylist.count(item) > 1:
            print("the %s has found %d" % (item, mylist.count(item)))
        else:
            continue
