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

TiDB 中文文档的日常更新特别活跃，相应地，[TiDB 英文文档](https://docs.pingcap.com/tidb/v4.0) 也需要进行频繁的更新。这一过程会涉及很多的**中译英**，即将 [pingcap/docs-cn](https://github.com/pingcap/docs) 里已 [merge](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/merging-a-pull-request) 但尚未进行翻译处理的 Pull Request 翻译为英文，并提交 Pull Request 至 [pingcap/docs](https://github.com/pingcap/docs) 中。**具体的认领方式**如下。

> **注意：**
>
> - 由于受众不同，TiDB 的中文文档与英文文档并非完全相同。但绝大数情况下，中英版本会保持一致。
> - 通常，TiDB 文档是先有中文版，后有英文版。但也有一小部分文档，是先有英文版，后有中文版。

#### 中文翻译任务的认领方式

目前，中文文档翻译任务以 [docs-cn 仓库的 Pull Request](https://github.com/pingcap/docs-cn/pulls) (PR) 为形式，通过仓库管理员为 PR 加上的 labels 来认领翻译任务、追踪翻译任务状态。

你可以通过以下简单几步来认领一个 PR 翻译任务：

1. 打开 [pingcap/docs-cn PR 翻译任务页面](https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atranslation%2Fwelcome+)，可以看到所有打上了 `translation/welcome` label 的 PR（这类 PR 无论是 open 还是 closed 状态，均在认领的范畴）。
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
- 图片风格：[Figma 快速上手教程](/resources/figma-quick-start-guide.md)

    为确保文档图片风格统一，建议使用 Figma 绘制图片。绘制图片时，请参考模板提供的图形元素和配色方案。

## Pull Request 提交流程

TiDB 文档的修改需要遵循一定的流程，具体如下。考虑到有些小伙伴是纯语言背景，命令行的流程掌握起来可能需要花些时间，之后我们也会提供更适合小白上手的 GitHub Desktop 客户端版提交流程（在添加至这里之前，可暂时参考 [lilin90](https://github.com/lilin90) 撰写的[小白上手流程](https://zhuanlan.zhihu.com/p/64880410)）。

> **注意：**
>
> 目前 TiDB 主要维护以下几个版本的文档：dev（最新开发版）、v4.0、v3.1、v3.0 以及 v2.1。提 Pull Request 前请务必考虑修改会影响的文档版本，并据此修改所有相应的版本。

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
> - 如果你的修改影响多个文档版本 (dev, v4.0, v3.1, v3.0, v2.1)，务必**在 PR 描述框中勾选相应的版本**，后续仓库管理员会为你的 PR 打上相应的 cherry-pick 标签。

## 必须遵循的 Markdown 规范

TiDB 中文文档使用 Markdown 语言进行编写，为了保证文档质量和格式规范，你修改的文档需要遵循一定的 Markdown 规则。我们为 docs-cn 仓库设置了检测 markdown 文件规范的 CI check，即 [markdownlint check](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)。如果你提交的 PR 不符合规范，很可能**无法通过 markdownlint check**，最终导致无法合并 PR。

我们为 TiDB 中文文档提前设置了 25 条 [markdownlint 规则](/resources/markdownlint-rules.md)，并附上了简单易懂的解释，强烈推荐花 5 分钟大致浏览一遍。

假如你提 PR 之前没有熟悉相关 Markdown 规范，提 PR 时遇到了 markdownlint check 失败，也不必担心，报错信息里会明确告诉你哪个文件的哪一行出了什么问题，根据提示在 PR 里更新一下文档内容即可搞定。

此外，你还可以选择在本地进行 markdownlint check：

```bash
./scripts/markdownlint [FILE...]
```

## 联系我们

加入 Slack channel：[#sig-docs](https://slack.tidb.io/invite?team=tidb-community&channel=sig-docs&ref=pingcap-docs-cn)
