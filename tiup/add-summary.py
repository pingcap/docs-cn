import re
import sys
import os
import linecache

def get_line_context(file_path, line_number):
    return linecache.getline(file_path, line_number).strip()

def not_has_summary(filename):

    no_summary = 1
    line_three = get_line_context(filename, 3)

    if re.match(r'summary: .*',line_three):
        no_summary = 0

    return no_summary

def get_summary(filename):

    metadata = 0

    with open(filename,'r') as f:
        for line in f:

            if metadata < 2 :
                if re.match(r'(\s|\t)*(-){3}', line):
                    metadata += 1
                continue
            else:
                if re.match(r'[^#][\u4e00-\u9fa5_a-zA-Z0-9\[\]\(\)\-\.]+',line):
                    #re.replace()
                    summary = re.sub(r'\([^\s]*\)','',line)
                    summary = "summary: " + re.sub(r'(\[)([\u4e00-\u9fa5_a-zA-Z0-9\s\`]+)(\])',r'\2',summary)
                    return summary

def insert_summary(filename):

    summary = get_summary(filename)
    lines=[]
    f=open(filename,'r')  #your path!
    for line in f:
        lines.append(line)
    f.close()
    lines.insert(2,summary)
    s=''.join(lines)
    f=open(filename,'w+') #重新写入文件
    f.write(s)
    f.close()

if __name__ == "__main__":

    for root,dirs,files in os.walk(r'./'):
        for file in files:
            if '.md' in file and not_has_summary(file):
                print(file)
                print(get_summary(file))
                insert_summary(file)



