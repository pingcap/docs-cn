# TiDB 中文文档贡献指南

无论你是热爱技术的程序员，还是擅长书面表达的语言爱好者，亦或是纯粹想帮 TiDB 改进文档的热心小伙伴，都欢迎来为 TiDB 文档做贡献，一起打造更加易用友好的 TiDB 文档！

## 可贡献的内容

欢迎任何对提升 TiDB 文档质量、易用性、维护效率、翻译效率的贡献，比如，你可以在以下方面进行贡献：

- [改进中文文档](#改进中文文档)
- [翻译中文文档的更新](#翻译中文文档)
- 优化文档提交的流程、维护方式
- 建立 TiDB 文档的翻译记忆库、术语库

下面主要介绍了如何为前两项做出贡献。

### 改进中文文档

你可从以下任一方面入手：

- 修复文档格式（如标点、空格、缩进、代码块等）和错别字
- 修改过时或不当的内容描述
- 增加缺失的文档内容
- 回复或解决 [issue](https://github.com/pingcap/docs-cn/issues?q=is%3Aopen+is%3Aissue) 并提 PR 更新相关文档
- 其它改进

### 翻译中文文档

TiDB 中文文档的日常更新特别活跃，相应地，[TiDB 英文文档](https://pingcap.com/docs/stable/) 也需要进行频繁的更新。这一过程会涉及很多的**中译英**，即将 [pingcap/docs-cn](https://github.com/pingcap/docs) 里已 [merge](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/merging-a-pull-request) 但尚未进行翻译处理的 Pull Request 翻译为英文，并提交 Pull Request 至 [pingcap/docs](https://github.com/pingcap/docs) 中。**具体的认领方式**如下。

> **注意：**
>
> - 由于受众不同，TiDB 的中文文档与英文文档并非完全相同。但绝大数情况下，中英版本会保持一致。
> - 通常，TiDB 文档是先有中文版，后有英文版。但也有一小部分文档，是先有英文版，后有中文版。

#### 中文翻译任务的认领方式

目前，中文文档翻译任务以 [docs-cn 仓库的 Pull Request](https://github.com/pingcap/docs-cn/pulls) (PR) 为形式，通过仓库管理员为 PR 加上的 labels 来认领翻译任务、追踪翻译任务状态。

你可以通过以下简单几步来认领一个 PR 翻译任务：

1. 打开 [pingcap/docs-cn PR 翻译任务页面](https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atranslation%2Fwelcome+is%3Aopen+)，可以看到所有打上了 `translation/welcome` label 的 PR。
2. 打开你想认领的 PR，拉到底部留下这条 comment：`@yikeke: I'd like to translate this PR.`。
3. 仓库管理员 @yikeke 会及时联系你，并将 `translation/welcome` 改为 `translation/doing`，之后你便可以开始翻译了。

下文提供了往 docs 或者 docs-cn 仓库提交 PR 的快速上手指南。

## 快速上手资源

最常见的贡献方式就是提 Pull Request 了，那么提交流程是怎样的，又需要遵守哪些规范呢？我们已准备好齐全的快速上手指南，你也可以查阅 [docs-cn 现有的 Pull Request](https://github.com/pingcap/docs-cn/pulls) 作为参考。

- Pull Request (PR) 提交 ⭐️
    - [Pull Request 提交流程](#pull-request-提交流程)
    - [Pull Request Commit Message 规范](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)
    - [Pull Request 标题规范](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)
- [PingCAP 中文文档风格指南](/resources/pingcap-style-guide-zh.pdf)
- [TiDB 中文用户文档模板](/resources/tidb-docs-template-zh-v1.0.pdf)
- [必须遵循的 Markdown 规范](#必须遵循的-markdown-规范)
- [代码注释规范](https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md)

## Pull Request 提交流程

TiDB 文档的修改需要遵循一定的流程，具体如下。考虑到有些小伙伴是纯语言背景，命令行的流程掌握起来可能需要花些时间，之后我们也会提供更适合小白上手的 GitHub Desktop 客户端版提交流程（在添加至这里之前，可暂时参考 [lilin90](https://github.com/lilin90) 撰写的[小白上手流程](https://zhuanlan.zhihu.com/p/64880410)）。

> **注意：**
>
> 目前 TiDB 主要维护四个版本的文档：dev（最新开发版），v3.1（3.1 Beta 版），v3.0（最新稳定版），v2.1（最新 2.1 版）。提 Pull Request 前请务必考虑修改会影响的文档版本，并据此修改所有相应的版本。

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
2. 点击 `Compare & pull request` 按钮即可创建 PR。参考[如何写 PR title 和描述](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md)。

> **注意：**
>
> - 如果你的修改影响多个文档版本 (dev, *v4.0, v3.1, v3.0, v2.1)，务必在 PR 描述框中勾选相应的版本，或者在页面右侧选择相应的 label (dev, *v4.0, v3.1, v3.0, v2.1) 来注明。v4.0 为尚未发布的新版本。
> - 如果你的修改也同样适用于[英文版文档](https://github.com/pingcap/docs)，需要在提 PR 时添加 label `pending-aligning`；也非常欢迎同时更新中文版和英文版。

## 必须遵循的 Markdown 规范

TiDB 中文文档使用 Markdown 语言进行编写，为了保证文档质量和格式规范，你修改的文档需要遵循一定的 Markdown 规则。我们为 docs-cn 仓库设置了检测 markdown 文件规范的 CI check，即 [markdownlint check](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)。如果你提交的 PR 不符合规范，很可能**无法通过 markdownlint check**，最终导致无法合并 PR。

假如你提 PR 之前没有熟悉相关 Markdown 规范，提 PR 时遇到了 markdownlint check 失败，也不必担心，报错信息里会明确告诉你哪个文件的哪一行出了什么问题，根据提示在 PR 里更新一下文档内容即可搞定。此外，你还可以选择在本地进行 markdownlint check：

```bash
./scripts/markdownlint [FILE...]
```

👇以下是我们为 TiDB 中文文档提前设置的 25 条 [markdownlint 规则](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)，附上了简单易懂的解释，相信你花几分钟快速浏览一遍 🤓即可基本掌握。

| NO. | 规则 | 描述 |
| :--- | :--- | :--- |
| 1 | [MD001 - Heading levels should only increment by one level at a time](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md001---heading-levels-should-only-increment-by-one-level-at-a-time) | 标题从一级开始递增使用，禁止跳级使用。例如：一级标题下面不能直接使用三级标题；二级标题下面不能直接使用四级标题。 |
| 2 | [MD003 - Heading style](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md003---heading-style) | 标题必须统一使用 ATX 风格，即在标题前加 `#` 号来表示标题级别。 |
| 3 | [MD018 - No space after hash on atx style heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md018---no-space-after-hash-on-atx-style-heading) | 标题的引导符号 `#` 后必须**空一格**再接标题内容。 |
| 4 | [MD019 - Multiple spaces after hash on atx style heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md019---multiple-spaces-after-hash-on-atx-style-heading) | 标题的引导符号“#”后只能空**一格**后再接标题内容，不能有多个空格。 |
| 5 | [MD023 - Headings must start at the beginning of the line](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md023---headings-must-start-at-the-beginning-of-the-line) | 标题必须出现在一行行首，即标题的 `#` 号前不能有任何空格。 |
| 6 | [MD026 - Trailing punctuation in heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md026---trailing-punctuation-in-heading) | 标题末尾仅能出现中英文问号、反引号、中英文单双引号等符号。其余如**冒号**、逗号、句号、感叹号等符号均不能在标题末尾使用。 |
| 7 | [MD022 - Headings should be surrounded by blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md022---headings-should-be-surrounded-by-blank-lines) | 标题上下均须空一行。 |
| 8 | [MD024 - Multiple headings with the same content](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md024---multiple-headings-with-the-same-content) | 文档中不能连续出现内容重复的标题，如一级标题为 `# TiDB 架构`，紧接着的二级标题就不能是 `## TiDB 架构`。如果不是连续的标题，则标题内容可重复。 |
| 9 | [MD025 - Multiple top level headings in the same document](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md025---multiple-top-level-headings-in-the-same-document) | 文档中只能出现一个一级标题。一级标题前的元数据（写明了 `title` 和 `category`）不会违反该规则。 |
| 10 | [MD041 - First line in file should be a top level heading](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md041---first-line-in-file-should-be-a-top-level-heading) | 文档正文一开始必须是一级标题。这条规则会自动忽略文档中头几行的元数据，直接检查后面是否有一级标题。 |
| 11 | [MD007 - Unordered list indentation](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md007---unordered-list-indentation) | 一般来说，除 `TOC.md` 文件可缩进 2 个空格外，其余所有 `.md` 文件每缩进一级，默认须缩进 4 个空格。 |
| 12 | [MD010 - Hard tabs](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md010---hard-tabs) | 文档中（包括代码块内）禁止出现 **Tab 制表符**，如需缩进，必须统一用**空格**代替。 |
| 13 | [MD012 - Multiple consecutive blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md012---multiple-consecutive-blank-lines) | 禁止出现连续的空行。 |
| 14 | [MD027 - Multiple spaces after blockquote symbol](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md027---multiple-spaces-after-blockquote-symbol) | 块引用符号 `>` 后禁止出现多个空格，只能使用**一个**空格，后接引用内容。 |
| 15 | [MD029 - Ordered list item prefix](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md029---ordered-list-item-prefix) | 使用有序列表时，必须从 1 开始，按顺序递增。 |
| 16 | [MD030 - Spaces after list markers](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md030---spaces-after-list-markers) | 使用列表时，每一列表项的标识符（`+`、`-`、`*` 或数字）后只能**空一格**，后接列表内容。|
| 17 | [MD032 - Lists should be surrounded by blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md032---lists-should-be-surrounded-by-blank-lines) | 列表（包括有序和无序列表）前后必须各空一行。 |
| 18 | [MD031 - Fenced code blocks should be surrounded by blank lines](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md031---fenced-code-blocks-should-be-surrounded-by-blank-lines) | 代码块前后必须各空一行。 |
| 29 | [MD034 - Bare URL used](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md034---bare-url-used) | 文档中禁止出现裸露的 URL。如果希望用户能直接点击并打开该 URL，则使用一对尖括号 (`<URL>`) 包裹该 URL。如果由于特殊情况必须使用裸露的 URL，不需要用户通过点击打开，则使用一对反引号 (``` `URL` ```) 包裹该 URL。 |
| 20 | [MD037 - Spaces inside emphasis markers](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md037---spaces-inside-emphasis-markers) | 使用加粗、斜体等强调效果时，在强调标识符内禁止出现多余的空格。如不能出现 ``` `** 加粗文本 **` ```。 |
| 21 | [MD038 - Spaces inside code span elements](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md038---spaces-inside-code-span-elements) | 单个反引号包裹的代码块内禁止出现多余的空格。如不能出现 ``` ` 示例文本 ` ```。 |
| 22 | [MD039 - Spaces inside link text](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md039---spaces-inside-link-text) | 链接文本两边禁止出现多余的空格。如不能出现 `[ 某链接 ](https://www.example.com/)`。 |
| 23 | [MD042 - No empty links](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md042---no-empty-links) | 链接必须有链接路径。如不能出现`[空链接]()`或`[空链接](#)`等情况。 |
| 24 | [MD045 - Images should have alternate text (alt text)](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md045---images-should-have-alternate-text-alt-text) | 图片链接必须添加描述文本（即 `[]()` 的 `[]` 内必须有描述文字），这是为了让无法加载出图片的人看到图片的描述性文字。 |
| 25 | [MD046 - Code block style](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md046---code-block-style) | 文档中的代码块统一使用**三个反引号** ` ``` ` 进行包裹，**禁止**使用**缩进四格**风格的代码块。 |
