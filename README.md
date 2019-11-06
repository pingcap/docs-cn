# TiDB 文档

欢迎来到 [TiDB](https://github.com/pingcap/tidb) 文档库！这里存放的是 [PingCAP 官网上 TiDB 中文文档](https://pingcap.com/docs-cn/)的源文件。[官网上 TiDB 英文文档](https://pingcap.com/docs/)的源文件存放于 [pingcap/docs](https://github.com/pingcap/docs)。

如果你发现或遇到 TiDB 文档的问题，可随时[提 Issue](https://github.com/pingcap/docs-cn/issues/new/choose) 来反馈，或者直接[提交 Pull Request](/CONTRIBUTING.md#pull-request-提交流程) 来进行修改。

无论你是热爱技术的程序员，还是擅长书面表达的语言爱好者，亦或是纯粹想帮 TiDB 改进文档的热心小伙伴，TiDB 文档社区都非常欢迎你的加入！

## TiDB 文档结构

目前，TiDB 的文档维护以下三个版本：

- `dev`：最新开发版
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
│   ├── releases
│   ├── tidb-in-kubernetes
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

你提交的第一个 Pull Request 合并以后，即可成为 TiDB 文档的 Contributor。

### 完善文档

你可从以下任一方面入手：

- 修复文档格式（如标点、空格、缩进、代码块等）和错别字
- 修改过时或不当的内容描述
- 增加缺失的文档内容
- 其它完善

### 翻译文档

TiDB 中文文档的日常更新特别活跃，相应地，[TiDB 英文文档](https://pingcap.com/docs/) 也需要进行更新。这一过程会涉及很多的**中译英**，即将 [pingcap/docs-cn](https://github.com/pingcap/docs) 里已 [merge](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/merging-a-pull-request) 但尚未处理（标有 `pending-aligning` label）的 Pull Request 翻译为英文，并提交 Pull Request 至 [pingcap/docs](https://github.com/pingcap/docs) 中。

> **注意：**
>
> - 由于受众不同，TiDB 的中文文档与英文文档并非完全相同。但绝大数情况下，中英版本会保持一致。
> - 通常，TiDB 文档是先有中文版，后有英文版。但也有一小部分文档，是先有英文版，后有中文版。
