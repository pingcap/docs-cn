# TiDB 中文文档贡献指南

无论你是热爱技术的程序员，还是擅长书面表达的语言爱好者，亦或是纯粹想帮 TiDB 改进文档的热心小伙伴，都欢迎来为 TiDB 文档做贡献，一起打造更加易用友好的 TiDB 文档！

## 我能为 TiDB 文档做什么贡献？

你可以在提升 TiDB 文档质量、易用性、维护效率、翻译效率等方面做贡献，比如：

- [改进中文文档](#改进中文文档)
- [翻译中文文档](#翻译中文文档)
- 优化文档提交的流程、维护方式
- 建立文档翻译记忆库、术语库

下面主要介绍了如何改进和翻译中文文档。

### 改进中文文档

你可从以下任一方面入手：

- 提 [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) (PR) 更新过时内容
- 提 PR 补充缺失内容
- 提 PR 修正文档格式，如标点、空格、缩进、代码块等
- 提 PR 改正错别字
- 回复或解决 [issue](https://github.com/pingcap/docs-cn/issues?q=is%3Aopen+is%3Aissue) 并提 PR 更新相关文档
- 其它改进

### 翻译中文文档

TiDB 中文文档的日常更新特别活跃，相应地，[TiDB 英文文档](https://docs.pingcap.com/tidb/dev/)也需要频繁更新。这一过程会涉及很多的**中译英**，即将 pingcap/docs-cn 仓库里已 merge 但尚未进行翻译处理的 [PR](https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atranslation%2Fwelcome+is%3Aclosed) 翻译为英文，并在 [pingcap/docs 仓库](https://github.com/pingcap/docs)中提交 Pull Request。

> **注意：**
>
> - 绝大多数情况下，中英文档需要保持完全一致。但个别文档由于受众不同，可能会有差异。
> - 通常，TiDB 文档先完成中文版后再完成英文版。但也偶有例外。
> - [参考资料](#参考资料)一节中汇总了**中英术语表**和**风格指南**等参考文档，建议译前阅读。

关于如何认领翻译任务的详细步骤，请参见[参考资料](#参考资料)。

## 如何提 Pull Request？

最常见的贡献方式就是提 Pull Request 了，那么提交流程是怎样的，又需要遵守哪些规范呢？下面的视频教程可以帮你快速上手 GitHub 的 Pull Request 流程：

- [Git 与 GitHub 基础概念](https://www.bilibili.com/video/BV1h5411E7pM/?p=1)
- [如何创建一个 Pull Request (PR)](https://www.bilibili.com/video/BV1h5411E7pM?p=2)
- [跟进 PR 的后续操作](https://www.bilibili.com/video/BV1h5411E7pM?p=3)
- [批量接受 Review 建议和处理 CI 检查](https://www.bilibili.com/video/BV1h5411E7pM?p=4)

你也可以查阅 [docs-cn 仓库现有的 Pull Requests](https://github.com/pingcap/docs-cn/pulls) 作为参考。关于提 Pull Request 的详细步骤，请查阅[提交 Pull Request 的详细流程](#提交-pull-request-的详细流程)。

## PR Checklist

在合入 (Merge) PR 之前，请务必检查以下内容：

- [ ] 文档内容准确、清晰、简洁，遵循写作规范。参考 [PingCAP 中文技术文档风格 — 极简指南](#pingcap-中文技术文档风格--极简指南)。
- [ ] PR 的各元素完整、准确，包括：
    - [ ] 标题清晰、有意义，包括修改的类型+文档所属的模块。参考 [Commit Message and Pull Request Style](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md)。例如：
        - Fix typos in tidb-monitoring-api.md
        - benchmark: add the v5.3.0 benchmark document
    - [ ] 有简要描述，例如修改背景等，并添加对应的 issue 号（如果有）
    - [ ] 选择正确的 label
    - [ ] cherry-pick 到适用且必要的分支版本
- [ ] 如果新增文档、删除文档，需要同时更新 `TOC.md`，删除文档时需要在文件开头添加 `aliases` 确保旧链接能够正常跳转。
- [ ] 预览文档，确保文档格式正确、清晰、可读，特别注意表格、图片、列表等特殊样式能够正常显示。

## PingCAP 中文技术文档风格 — 极简指南

![One Page Style Guide](/media/one-page-style-guide.png)

参考文档：

- [PingCAP 中文文档风格指南](/resources/pingcap-style-guide-zh.pdf)
- [TiDB 中文用户文档模板](/resources/doc-templates)

## 提交 Pull Request 的详细流程

TiDB 文档的修改需要遵循一定的流程，具体如下。考虑到有些小伙伴是纯语言背景，命令行的流程掌握起来可能需要花些时间，之后我们也会提供更适合小白上手的 GitHub Desktop 客户端版提交流程（在添加至这里之前，可暂时参考 [lilin90](https://github.com/lilin90) 撰写的[小白上手流程](https://zhuanlan.zhihu.com/p/64880410)）。

> **注意：**
>
> 目前（2023 年 12 月）TiDB 主要维护以下几个版本的文档：dev（最新开发版，对应文档仓库的 master 分支）、v7.5、v7.4、v7.3、v7.1、v6.5、v6.1、v6.0、v5.4、v5.3、v5.2、v5.1、v5.0。提 Pull Request 前请务必考虑修改会影响的文档版本，并据此修改所有相应的版本。选择版本时，请参考[参考资料](#参考资料)中的**如何选择文档适用的版本分支？**。

### 第 0 步：签署 Contributor License Agreement

首次在本仓库提 PR 时，请务必签署 [Contributor License Agreement](https://cla-assistant.io/pingcap/docs-cn) (CLA)，否则我们将无法合并你的 PR。成功签署 CLA 后，可继续进行后续操作。

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

参考[如何写 commit message](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)。

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

1. 打开你 Fork 的仓库：`https://github.com/$user/docs-cn`（将其中的 `$user` 替换为你的 GitHub ID）
2. 点击 `Compare & pull request` 按钮即可创建 PR。参考[如何写 PR title 和描述](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md)。

> **注意：**
>
> - 如果你的修改影响多个文档版本 (如 dev、v7.5、v7.4 等)，务必**在 PR 描述框中勾选相应的版本**，后续仓库管理员会为你的 PR 打上相应的 cherry-pick label。

## 预览 EBNF 格式的 SQL 语法图

[TiDB 文档](https://docs.pingcap.com/zh/tidb/stable)提供了大量 SQL 语法图，以帮助用户理解 SQL 语法。例如，[`ALTER INDEX` 文档](https://docs.pingcap.com/zh/tidb/stable/sql-statement-alter-index#语法图)中的语法图。

这些语法图的源代码是使用[扩展巴科斯范式 (EBNF)](https://zh.wikipedia.org/wiki/扩展巴科斯范式) 编写的。在为 SQL 语句添加 EBNF 代码时，可以将代码复制到 <https://kennytm.github.io/website-docs/dist/> 并点击 **Render**，即可轻松预览 EBNF 效果图。

## 参考资料

<details>
<summary>如何认领中文翻译任务？</summary>

目前，中文文档翻译任务以 [docs-cn 仓库的 Pull Request](https://github.com/pingcap/docs-cn/pulls) (PR) 为形式，通过仓库管理员为 PR 加上的 labels 来认领翻译任务及追踪翻译任务状态。

你可以通过以下简单几步来认领并提交一个 PR 翻译任务：

> **注意：**
>
> 关于下面步骤中所提到的 comment 式命令，详细说明请参考[参考资料](#参考资料)中的**常用 bot 命令**。

1. 查看待认领 PR

    打开 [pingcap/docs-cn PR 翻译任务页面](https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atranslation%2Fwelcome+-label%3Atranslation%2Fdone+)，即可看到所有打上了 `translation/welcome` label 的 PR。这类 PR 只要没有 `translation/done` 的 label，无论是处于 open 还是 closed 状态，均可认领。

2. 认领 PR

    打开你想认领的 PR，拉到底部留下这条 comment：`/assign`，即可将此 PR 的翻译任务分配给自己。

3. 修改 PR label

    PR 认领成功后，继续在底部 comment 区域依次发送：`/remove-translation welcome` 及 `/translation doing`，即可将右侧 Labels 栏中的 `translation/welcome` 改为 `translation/doing`，之后你便可以开始翻译了。

4. 翻译 PR 并提交

    由于 TiDB 的中英文文档分别存放于 [pingcap/docs-cn](https://github.com/pingcap/docs-cn) 和 [pingcap/docs](https://github.com/pingcap/docs) 中，并且两个仓库的文件结构完全对应。如果你是首次认领翻译任务，需先 fork docs 仓库，并将 fork 的 docs 仓库克隆到本地，然后找到源 PR 中对应的改动文件再开始翻译。翻译完毕后，创建新 PR，将翻译好的文件提交至 docs 仓库。

5. 填写 PR 描述并修改 label

    新建 PR 成功后，先按照模板说明完整填写 PR 描述，接着在底部发送：`/translation from-docs-cn`，为 PR 添加 `translation/from-docs-cn` label，表明此 PR 是从中文翻译过来的。然后回到源 PR 依次发送：`/remove-translation doing` 及 `/translation done`，将源 PR label 修改为 `translation/done`，表明翻译已完成。

6. 分配 Reviewer（推荐，非必需）

    每个 PR 都需要经过 Review 后才能合并，分配 Reviewer 一般由文档仓库管理员负责，但我们也十分欢迎你来主动承担这个任务。

    具体操作为：在新建的 PR 下发送 `/cc @lilin90 @technical-reviewer`（将 technical-reviewer 替换为源 PR 作者的 GitHub ID），即可将 Review 任务分配给 docs 仓库管理员 @lilin90 及源 PR 的作者。

</details>

<details>
<summary>如何选择文档适用的版本分支？</summary>

创建 Pull Request 时，你需要在 Pull Request 的描述模版中选择文档改动适用的版本分支。

如果你的 PR 改动符合以下任一情况，推荐**只选择 master 分支**。此 PR 的改动在合并后将显示到[官网文档 Dev 页面](https://docs.pingcap.com/zh/tidb/dev/)，在下一次 TiDB 发新版本时将显示到新版本的文档页面。

- 完善文档，例如补充缺失或不完整的信息。
- 改正错误，例如默认值错误、描述不准确、示例错误、拼写错误等。
- 重构文档，例如“部署标准集群”、“数据迁移”、“TiDB 数据迁移工具”等。

如果你的 PR 改动符合以下任一情况，请**选择 master 分支以及受影响的 release 分支**：

- 涉及与版本相关的功能行为变化。
- 涉及与版本相关的兼容性变化，例如更改某个配置项或变量的默认值。
- 修复文档页面的渲染或显示错误。
- 修复文档内的死链。

</details>

<details>
<summary>Markdown 规范</summary>

TiDB 中文文档使用 Markdown 语言进行编写，为了保证文档质量和格式规范，你修改的文档需要遵循一定的 Markdown 规则。我们为 docs-cn 仓库设置了检测 markdown 文件规范的 CI check，即 [markdownlint check](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)。如果你提交的 PR 不符合规范，很可能**无法通过 markdownlint check**，最终导致无法合并 PR。

我们为 TiDB 中文文档提前设置了 25 条 [markdownlint 规则](/resources/markdownlint-rules.md)，并附上了简单易懂的解释，强烈推荐花 5 分钟通读一遍。

假如你提 PR 之前没有熟悉相关 Markdown 规范，提 PR 时遇到了 markdownlint check 失败，也不必担心，报错信息中有错误详情、出错的文件和位置，帮你快速定位和解决问题。

此外，你还可以选择在本地进行 markdownlint check：

```bash
./scripts/markdownlint [FILE...]
```

</details>

<details>
<summary>常用 bot 命令</summary>

我们为 docs 和 docs-cn 仓库提前设置了一些命令语句，只要按照一定的格式在 PR 中留言，就能触发 bot 完成相应操作。详情见下表。

| 命令 | 含义 | 示例 |
| ------ | ------ | ------ |
| `/label` | 给 PR 添加 label，多个 label 间需要用逗号分隔。如果 label 中有斜线 `/`，则命令为 `/[label 的第一个单词] [label 其他部分]` | `/label contribution`，`/translation from-docs` |
| `/remove-label` | 删除 PR label。如果 label 中有斜线 `/`，则命令为 `/remove-[label 的第一个单词] [label 其他部分]` | `/remove-label contribution`，`/remove-translation welcome` |
| `/assign` | 将 PR 分配给指定的人，需 @指定用户的 GitHub ID，多个 GitHub ID 间用逗号分隔。如果想要将 PR 分配给自己，`/assign`后可不跟 GitHub ID。 | `/assign @lilin90` |
| `/unassign` | 移除 PR 之前指定的 assignee。 | `/unassign @lilin90` |
| `/cc` | 将 PR 分配给指定的 reviewer，需 @指定用户的 GitHub ID，多个 GitHub ID 间用逗号分隔。 | `/cc @lilin90, @hfxsd` |
| `/uncc` | 移除 PR 之前指定的 reviewer。  | `/uncc @lilin90`|

</details>

其他快速上手资源

- [TiDB 中英术语表](/resources/tidb-terms.md)
- [GitHub Docs](https://docs.github.com/en)
- [Pull Request Commit Message 规范](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)
- [Pull Request 标题规范](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)
- [代码注释规范](https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md)
- [Figma 快速上手教程](/resources/figma-quick-start-guide.md)
- [EBNF 语法图在线渲染](https://kennytm.github.io/website-docs/dist/)
