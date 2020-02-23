# TiDB 文档

欢迎来到 [TiDB](https://github.com/pingcap/tidb) 文档库！这里存放的是 [PingCAP 官网 TiDB 中文文档](https://pingcap.com/docs-cn/stable/)的源文件。[官网英文文档](https://pingcap.com/docs/stable/)的源文件则存放于 [pingcap/docs](https://github.com/pingcap/docs)。如果你发现或遇到了 TiDB 的文档问题，可随时[提 Issue](https://github.com/pingcap/docs-cn/issues/new/choose) 来反馈，或者直接[提交 Pull Request](/CONTRIBUTING.md#pull-request-提交流程) 来进行修改。

## TiDB 文档结构

目前，TiDB 的文档维护以下四个版本，分别放置在相应的 branch：

- `master`：最新开发版
- `release-3.1`：3.1 Beta 版
- `release-3.0`：最新稳定版
- `release-2.1`：2.1 稳定版

TiDB 的文档结构如下：

```
├── TOC.md
├── how-to
    ├── get-started
    ├── deploy
        ├── orchestrated
            ├── ansible.md
            ├── offline-ansible.md
            ├── docker.md
    ├── configure
    ├── maintain
    ├── troubleshoot
    ├── ...
├── reference
   ├── tools
    ├── tidb-binlog
    ├── ...
├── releases
├── tidb-in-kubernetes
├── faq
├── ...
...
```

## 贡献文档

你提交的第一个 [Pull Request](https://help.github.com/en/github/getting-started-with-github/github-glossary#pull-request) (PR) 合并以后，即可成为 TiDB 文档的 Contributor。查看 [TiDB 中文文档贡献指南](/CONTRIBUTING.md)，开始你的贡献吧！
