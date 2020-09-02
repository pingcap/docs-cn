import re
import sys

# 注意：本脚本只支持跳过检查 ``` ``` 格式的代码块，~~~ ~~~ 格式的代码块会被检查。

# reference: https://stackoverflow.com/questions/35761133/python-how-to-check-for-open-and-close-tags
def stack_tag(tag, stack):
    t = tag[1:-1] # 去掉左右括号
    first_space = t.find(' ') # 比如 t = 'span class="label__title"'；t.find(' ') = 4；只需要将属性名传入堆栈
    #print(t)
    # print(t + ' 的第一个空格在 ' + str(first_space))
    if t[-1] == '/':
        self_closed_tag = True # 为自闭合标签。这一行用来占位，实际上无效
    elif t[0:1] != '/': # 为开放标签，将属性名传入堆栈
        # Add tag to stack
        if first_space == -1:
            stack.append(t)
            # print("TRACE open", stack)
        else:
            stack.append(t[:first_space])
            # print("TRACE open", stack)
    else: # </xxx>类标签
        if first_space != -1:
            t = t[1:first_space]
        else:
            t = t[1:]

        if len(stack) == 0:
            # print("No blocks are open; tried to close", t)
            closed_tag = True # 这一行用来占位，实际上无效
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
    # pos = (7429, 7433) # tag 的位置
    # content 为整篇文档字符串
    # 这个函数要找出 tag 附近两边是否有 `` 包裹
    tag_start = pos[0]
    tag_end = pos[1]
    content_previous = content[:tag_start][::-1] # reverse content_previous
    content_later = content[tag_end:]

    left_wraps_findall = re.findall(r'`', content_previous)
    left_single_backtick = len(left_wraps_findall) % 2  # 如果为 0，则左侧没有单个的 backtick，即未被包裹
    right_wraps_findall = re.findall(r'`', content_later)
    right_single_backtick = len(right_wraps_findall) % 2  # 如果为 0，则右侧没有单个的 backtick，即未被包裹

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

def filter_content(content):
    # 该函数将原 content 的代码块以及 frontmatter 过滤掉
    # 由于代码块本身是三个 ``` 包裹，所以该格式内代码块的 tag 不会导致 ci 失败
    # 因此暂时只过滤掉 frontmatter
    content_findall = re.findall(r'\n---\n', content)
    # 如果有 frontmatter
    if len(content_findall):
        content_finditer = re.finditer(r'\n---\n', content)
        for i in content_finditer:
            meta_pos = i.span()[1]
            # print(content[meta_pos:])
            return content[meta_pos:]
    else:
        return content

status_code = 0

# print(sys.argv[1:])
for filename in sys.argv[1:]:
    #print("Checking " + filename + "......\n")
    file = open(filename, "r" )
    content = file.read()
    file.close()

    content = filter_content(content)
    result_findall = re.findall(r'<([^`>]*)>', content)
    if len(result_findall) == 0:
        # print("The edited markdown file " + filename + " has no tags!\n")
        status_code = 0
    else:
        result_finditer = re.finditer(r'<([^`>]*)>', content)
        stack = []
        for i in result_finditer: # i 本身也是可迭代对象，所以下面要使用 i.group()
            # print(i.group(), i.span())
            tag = i.group()
            pos = i.span() # 输出类似于 (7429, 7433)

            # 首先筛去特殊 tag，比如 <!-- xxx -->
            if tag[:4] == '<!--' and tag[-3:] == '-->':
                continue
            # 再筛去带 `` 的 tag
            # elif content[pos[0]-1] == '`' and content[pos[1]] == '`':
            elif tag_is_wrapped(pos, content):
                # print(content[int(pos[0])-1:int(pos[1]+1)])
                # print(tag, 'is wrapped by backticks!')
                continue

            # 其余的 tag 都需要放入堆栈确认是否闭合
            stack = stack_tag(tag, stack)

        if len(stack):
            stack = ['<' + i + '>' for i in stack]
            print("ERROR: " + filename + ' has unclosed tags: ' + ', '.join(stack) + '.\n')
            status_code = 1
        else:
            # print("The edited markdown file has tags. But all tags are closed, congratulations!\n")
            status_code = 0

if status_code:
    print("HINT: Unclosed tags will cause website build failure. Please fix the reported unclosed tags. You can use backticks `` to wrap them or close them. Thanks.")
    exit(1)
