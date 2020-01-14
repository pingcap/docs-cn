---
title: 中文文档贡献指南
category: contribute
---

# 中文文档贡献指南

我们欢迎更多贡献者来帮助改进文档！

如要对中文文档进行贡献，请先 fork [docs-cn 仓库](https://github.com/pingcap/docs-cn)，再提交您的 Pull Request。

TiDB 中文文档使用 Markdown 语言进行编写，为了保证文档质量和格式规范，您修改的文档需要遵循一定的 Markdown 风格。

## 参考资源

- [PingCAP 中文技术文档风格指南](resources/pingcap-style-guide-zh-v1.1.pdf)
- [TiDB 中文文档模板](resources/tidb-docs-template-zh-v1.0.pdf)
- [Pull Request 提交流程](#pull-request-提交流程)

## 必须遵循的 markdownlint 规则

我们为 docs-cn 仓库设置了检测 markdown 文件规范的 CI check，如果您提交的 PR 不符合规范，很可能**无法通过 markdownlint check**，最终导致无法合并 PR。

您也可以在本地进行 markdownlint check：

``` bash
./scripts/markdownlint [FILE...]
```

以下是我们为 TiDB 中文文档提前设置的 26 条 [markdownlint 规则](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)：

1. [MD001 - Heading levels should only increment by one level at a time](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md001---heading-levels-should-only-increment-by-one-level-at-a-time)

    标题从一级开始递增使用，禁止跳级使用。例如：一级标题下面不能直接使用三级标题；二级标题下面不能直接使用四级标题。

2. [MD003 - Heading style](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md003---heading-style)

    必须统一使用 ATX heading style。

3. [MD007 - Unordered list indentation](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md007---unordered-list-indentation)

    一般来说，除 TOC.md 文件缩进 2 格外，其余所有 .md 文件默认缩进 4 个空格。

4. [MD009 - Trailing spaces](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md009---trailing-spaces)

    行尾禁止出现多余的空格。

5. [MD010 - Hard tabs](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md010---hard-tabs)

    文档中（包括代码块内）禁止出现 **tab 制表符**，如需缩进，必须统一用**空格**代替。

6. [MD012 - Multiple consecutive blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md012---multiple-consecutive-blank-lines)

    禁止出现连续的空行。

7. [MD018 - No space after hash on atx style heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md018---no-space-after-hash-on-atx-style-heading)

    标题的引导符号“#”后必须**空一格**后再接标题内容。

8. [MD019 - Multiple spaces after hash on atx style heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md019---multiple-spaces-after-hash-on-atx-style-heading)

    标题的引导符号“#”后只能空**一格**后再接标题内容，不能有多个空格。

9. [MD022 - Headings should be surrounded by blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md022---headings-should-be-surrounded-by-blank-lines)

    标题上下必须均空一行。

10. [MD023 - Headings must start at the beginning of the line](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md023---headings-must-start-at-the-beginning-of-the-line)

    标题必须出现在一行行首，即标题前不能有任何空格。

11. [MD024 - Multiple headings with the same content](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md024---multiple-headings-with-the-same-content)

    文档中不能连续出现内容重复的标题，如一级标题为“# TiDB 架构”，紧接着的二级标题就不能是“# TiDB 架构”。如果不是连续的标题，则标题内容可重复。(`siblings_only`=`true`)

12. [MD025 - Multiple top level headings in the same document](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md025---multiple-top-level-headings-in-the-same-document)

    文档中只能出现一个一级标题。一级标题前的元数据（写明了 `title` 和 `category`）不会违反该规则。(front_matter_title: '')

13. [MD026 - Trailing punctuation in heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md026---trailing-punctuation-in-heading)

    标题末尾仅能出现中英文问号、反引号、中英文单双引号 ("”'‘) 等符号。其余如**冒号**、逗号、句号、感叹号等符号均不能在标题末尾使用。(punctuation: '.,;:!。，；：！')

14. [MD027 - Multiple spaces after blockquote symbol](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md027---multiple-spaces-after-blockquote-symbol)

    块引用符“>”后禁止出现多个空格，只能使用**一个**空格后接引用内容。

15. [MD029 - Ordered list item prefix](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md029---ordered-list-item-prefix)

    使用有序列表时，必须从 1 开始，按顺序递增。(style: ordered)

16. [MD030 - Spaces after list markers](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md030---spaces-after-list-markers)

    使用列表时，每一列表项的标识符（+、-、* 或数字）后只能**空一格**，后接列表内容。

17. [MD031 - Fenced code blocks should be surrounded by blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md031---fenced-code-blocks-should-be-surrounded-by-blank-lines)

    代码块前后必须各空一行。

18. [MD032 - Lists should be surrounded by blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md032---lists-should-be-surrounded-by-blank-lines)

    列表（包括有序和无序列表）前后必须各空一行。

19. [MD034 - Bare URL used](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md034---bare-url-used)

    文档中禁止出现裸露的 URL。如果希望用户能直接点击并打开该 URL，则用一对尖括号 (`<URL>`) 包裹该 URL。如果由于特殊情况必须使用裸露的 URL，可以用一对反引号 (``` `URL` ```) 包裹该 URL。

20. [MD037 - Spaces inside emphasis markers](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md037---spaces-inside-emphasis-markers)

    使用加粗、斜体等强调效果时，在强调标识符内禁止出现多余的空格。如不能出现 ``` `** 加粗文本 **` ```。

21. [MD038 - Spaces inside code span elements](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md038---spaces-inside-code-span-elements)

    单个反引号包裹的代码块内禁止出现多余的空格。如不能出现 ``` ` 示例文本 ` ```。

22. [MD039 - Spaces inside link text](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md039---spaces-inside-link-text)

    链接文本两边禁止出现多余的空格。如不能出现 `[ 某链接 ](https://www.example.com/)`。

23. [MD041 - First line in file should be a top level heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md041---first-line-in-file-should-be-a-top-level-heading)

    文档正文一开始必须是一级标题。这条规则会自动忽略文档中头几行的元数据，直接检查后面是否有一级标题。

24. [MD042 - No empty links](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md042---no-empty-links)

    链接必须有链接路径。如不能出现`[空链接]()`或`[空链接](#)`等情况。

25. [MD045 - Images should have alternate text (alt text)](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md045---images-should-have-alternate-text-alt-text)

    链接的图片必须写上链接文本（即 [] 内必须有描述文字），这是为了让无法加载出图片的人看到图片的描述性文字。

26. [MD046 - Code block style](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md046---code-block-style)

    文档中代码块统一使用**三个反引号**进行包裹，**禁止**使用**缩进四格**风格的代码块。(`style`=`fenced`)

## Pull Request 提交流程

TiDB 文档的修改需要遵循一定的流程，具体如下。

> **注意：**
>
> 目前 TiDB 主要维护三个版本的文档：dev（最新开发版），v3.0（最新稳定版），v2.1（最新 2.1 版）。提 Pull Request 前请务必考虑修改会影响的文档版本，并据此修改所有相应的版本。

### 第 1 步：Fork pingcap/docs-cn 仓库

1. 打开 pingcap/docs-cn 项目[仓库](https://help.github.com/articles/github-glossary/#repository)：<https://github.com/pingcap/docs-cn>
2. 点击右上角的 [**Fork**](https://help.github.com/articles/github-glossary/#fork) 按钮，等待 Fork 完成即可。

### 第 2 步：将 Fork 的仓库克隆至本地

```
cd $working_dir # 将 $working_dir 替换为你想放置 repo 的目录。例如，`cd ~/Documents/GitHub`
git clone git@github.com:$user/docs-cn.git # 将 `$user` 替换为你的 GitHub ID

cd $working_dir/docs-cn
git remote add upstream git@github.com:pingcap/docs-cn.git # 添加上游仓库
git remote -v
```

### 第 3 步：新建一个 Branch

1. 确保本地 master branch 与 upstream/master 保持最新。

    ```
    cd $working_dir/docs-cn
    git fetch upstream
    git checkout master
    git rebase upstream/master
    ```

2. 基于 master branch 新建一个 branch，名称格式为：aaa-bbb-ccc。

    ```
    git checkout -b new-branch-name
    ```

### 第 4 步：编辑文档进行增删或修改

在建好的 `new-branch-name` branch 上进行编辑，可使用 Markdown 编辑器（如 Visual Studio Code）打开 docs-cn repo，对相应文档进行增、删，或修改，并保存你的修改。

### 第 5 步：提交你的修改

```
git status
git add <file> ... # 如果你想提交所有的文档修改，可直接使用 `git add .`
git commit -m "commit-message: update the xx"
```

参考[如何写 commit message](https://github.com/pingcap/community/blob/master/commit-message-pr-style.md#how-to-write-a-good-commit-message)。

### 第 6 步：保持新建 branch 与 upstream/master 一致

```
# 在新建 branch 上
git fetch upstream
git rebase upstream/master
```

### 第 7 步：将你的修改推至远程

```
git push -u origin new-branch-name
```

### 第 8 步：创建一个 Pull Request

1. 打开你 Fork 的仓库：<https://github.com/$user/docs-cn>（将 `$user` 替换为你的 GitHub ID）
2. 点击 `Compare & pull request` 按钮即可创建 PR。参考[如何写 PR title 和描述](https://github.com/pingcap/community/blob/master/commit-message-pr-style.md#pull-request-title-style)。

    > **注意：**
    >
    > - 如果你的修改影响多个文档版本 (dev, v3.0, v2.1)，务必在 PR 描述框相应的问题下注明，或者在页面右侧选择相应的 label (dev, v3.0, v2.1) 来注明。
    > - 如果你的修改也同样适用于[英文版文档](https://github.com/pingcap/docs)，需要在提 PR 时添加 label `pending-aligning`；也非常欢迎同时更新中文版和英文版。
