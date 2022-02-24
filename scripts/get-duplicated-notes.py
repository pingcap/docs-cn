# This script compares an on-going release notes file with a previously published release notes file.
# If the ongoing release notes file has a duplicate note with the published one, the script reports the note and replaces it with the published one. 

import re, os
from tempfile import mkstemp
from shutil import move
from os import remove


# 获取已发布的 release notes Issue 号
def store_exst_rn(path):
    exst_notes = []
    flag = 0
    with open(path,'r', encoding='utf-8') as fp:
        for line in fp:
            exst_issue_num = re.search('\[#\d{4,5}\]', line)
            if exst_issue_num:
                flag = 1
                note_pair = [exst_issue_num.group(), line]
                exst_notes.append(note_pair)
            else:
                continue
        if flag == 1:
            return exst_notes
        else:
            return 0


# 检查当前准备中的 release notes 的 Issue 号是否有重复，如果有就进行替换
def check_exst_rn(ext_path, main_path):
    target_file_path = mkstemp()[1]
    source_file_path = main_path
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        with open(source_file_path, 'r', encoding='utf-8') as source_file:
            LineNum = 0
            for line in source_file:
                LineNum += 1
                issue_num = re.search('\[#\d{4,5}\]', line)
                if issue_num:
                     for note_pairs in store_exst_rn(ext_path):
                        if issue_num.group() == note_pairs[0]:
                            print('A duplicated note is found in line ' + str(LineNum) + note_pairs[1])
                            line = re.sub(r'-.*$', '(dup) ' + note_pairs[1].strip(), line)
                            print('The duplicated note is replaced with ' + line)
                target_file.write(line)

    remove(source_file_path)
    move(target_file_path, source_file_path)


if __name__ == "__main__":

    ext_path = r'D:\GitHub\upstream\docs1\releases\release-5.0.6.md'  # 已发布的 release notes
    main_path = r'D:\GitHub\upstream\docs1\releases\release-5.1.4.md'  # 当前正在准备的 release notes
    check_exst_rn(ext_path, main_path)
