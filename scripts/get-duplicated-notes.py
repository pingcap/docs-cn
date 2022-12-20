# This script compares an on-going release notes file with published release notes files.
# If the ongoing release notes file has a duplicate note with the published one, the script reports the note and replaces it with the published one.

import re, os
from tempfile import mkstemp
from shutil import move
from os import remove


# 获取已发布的 release notes Issue 号和 PR 号
def store_exst_rn(ext_path,main_path):

    exst_notes = []
    exst_issue_nums = []
    exst_note_levels = []

    for maindir, subdir, files in os.walk(ext_path):
        for afile in files:
            file_path = (os.path.join(maindir, afile))
            if file_path.endswith('.md') and not os.path.samefile(file_path,main_path):
                with open(file_path,'r', encoding='utf-8') as fp:
                    level1 = level2 = level3 = ""
                    for line in fp:
                        exst_issue_num = re.search(r'https://github.com/(pingcap|tikv)/\w+/(issues|pull)/\d+', line)
                        if exst_issue_num:
                            if exst_issue_num.group() not in exst_issue_nums:
                                note_level = level1 + level2 + level3
                                note_pair = [exst_issue_num.group(),line,afile, note_level]
                                exst_issue_nums.append(exst_issue_num.group())
                                exst_notes.append(note_pair)
                            else:
                                continue
                        elif line.startswith("##"):
                            level1 = "> " + line.replace("##","").strip()
                            level2 = level3 = ""
                        elif line.startswith ("+") or line.startswith ("-"):
                            level2 = "> " + line.replace("+","").replace("-","").strip()
                            level3 = ""
                        elif line.startswith ("    +") or line.startswith ("    -"):
                            level3 = "> " + line.replace("    +","").replace("    -","").strip()
                        else:
                            continue
            else:
                pass

    if len(exst_issue_nums) != 0:
        return exst_notes
    else:
        return 0


# 检查当前准备中的 release notes 的 Issue 号和 PR 号是否有重复，如果有就进行替换
def check_exst_rn(note_pairs, main_path):
    DupNum = 0
    NoteNum = 0
    target_file_path = mkstemp()[1]
    source_file_path = main_path
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        with open(source_file_path, 'r', encoding='utf-8') as source_file:
            LineNum = 0
            for line in source_file:
                LineNum += 1
                issue_num = re.search('https://github.com/(pingcap|tikv)/\w+/(issues|pull)/\d+', line)
                if issue_num:
                     NoteNum +=1
                     for note_pair in note_pairs:
                        if issue_num.group() == note_pair[0] and not line.strip().startswith("(dup"):
                            print('A duplicated note is found in line ' + str(LineNum) + " from " + note_pair[2] + note_pair[1])
                            match = re.fullmatch(r'(\s*)(?:- .+?)( @.+?)?\s*', line)
                            if match:
                                line = '{}(dup: {} {}){}{}\n'.format(match.group(1), note_pair[2], note_pair[3], note_pair[1].strip(), match.group(2) or "")
                                print('The duplicated note is replaced with ' + line)
                                DupNum += 1
                            else:
                                continue
                            break
                target_file.write(line)

    remove(source_file_path)
    move(target_file_path, source_file_path)
    DupRate = "%.0f%%" % (DupNum/NoteNum*100) #计算 release notes 重复率
    print (str(DupNum) + " duplicated notes are found in " + str(NoteNum) + " notes. The duplicated rate is " + str(DupRate) + ".")


if __name__ == "__main__":

    ext_path = r'/Users/aaa/Documents/GitHub/githubid/docs/releases'  # 已发布的 release notes 文件夹
    main_path = r'/Users/aaa/Documents/GitHub/githubid/docs/releases/release-5.3.1.md'  # 当前正在准备的release notes 文档路径
    note_pairs = store_exst_rn(ext_path,main_path)
    check_exst_rn(note_pairs, main_path)
