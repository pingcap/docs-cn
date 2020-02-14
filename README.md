# TiDB 文档

欢迎来到 [TiDB](https://github.com/pingcap/tidb) 文档库！这里存放的是 [PingCAP 官网上 TiDB 中文文档](https://pingcap.com/docs-cn/)的源文件。[英文文档](https://pingcap.com/docs/)的源文件则存放于 [pingcap/docs](https://github.com/pingcap/docs)。如果你发现或遇到了 TiDB 的文档问题，可随时[提 Issue](https://github.com/pingcap/docs-cn/issues/new/choose) 来反馈，或者直接[提交 Pull Request](/CONTRIBUTING.md#pull-request-提交流程) 来进行修改。

## TiDB 文档结构

目前，TiDB 的文档维护以下四个版本：

- `dev`：最新开发版
- `v3.1`：3.1 Beta 版
- `v3.0`：最新稳定版
- `v2.1`：2.1 稳定版

TiDB 的文档结构如下：

```
├── dev
│   ├── TOC.md
│   ├── how-to
│       ├── get-started
│       ├── deploy
│           ├── orchestrated
│               ├── ansible.md
│               ├── offline-ansible.md
│               ├── docker.md
│       ├── configure
│       ├── maintain
│       ├── troubleshoot
│       ├── ...
│   ├── reference
│      ├── tools
│       ├── tidb-binlog
│       ├── ...
│   ├── releases
│   ├── tidb-in-kubernetes
│   ├── faq
│   ├── ...
├── v3.0
│   ├── TOC.md
│   ├── how-to
│   ├── ...
├── v2.1
│   ├── TOC.md
│   ├── how-to
│   ├── ...
...
```

## 贡献文档

你提交的第一个 Pull Request (PR) 合并以后，即可成为 TiDB 文档的 Contributor。

### 完善文档

你可从以下任一方面入手：

- 修复文档格式（如标点、空格、缩进、代码块等）和错别字
- 修改过时或不当的内容描述
- 增加缺失的文档内容
- 回复或解决 [issue](https://github.com/pingcap/docs-cn/issues?q=is%3Aopen+is%3Aissue) 并提 PR 更新相关文档
- 其它完善

### 翻译文档

TiDB 中文文档的日常更新特别活跃，相应地，[TiDB 英文文档](https://pingcap.com/docs/) 也需要进行更新。这一过程会涉及很多的**中译英**，即将 [pingcap/docs-cn](https://github.com/pingcap/docs) 里已 [merge](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/merging-a-pull-request) 但尚未进行翻译处理的 Pull Request 翻译为英文，并提交 Pull Request 至 [pingcap/docs](https://github.com/pingcap/docs) 中。**具体的认领方式即将公布。**

> **注意：**
>
> - 由于受众不同，TiDB 的中文文档与英文文档并非完全相同。但绝大数情况下，中英版本会保持一致。
> - 通常，TiDB 文档是先有中文版，后有英文版。但也有一小部分文档，是先有英文版，后有中文版。
