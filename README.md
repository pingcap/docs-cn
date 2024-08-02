# TiDB 文档

欢迎来到 [TiDB](https://github.com/pingcap/tidb) 文档仓库！

这里存放的是 [PingCAP 官网 TiDB 中文文档](https://docs.pingcap.com/zh/tidb/stable)的源文件。[官网英文文档](https://docs.pingcap.com/tidb/stable)的源文件则存放于 [pingcap/docs](https://github.com/pingcap/docs)。

如果你发现或遇到了 TiDB 的文档问题，可随时[提 Issue](https://github.com/pingcap/docs-cn/issues/new/choose) 来反馈，或者直接[提交 Pull Request](/CONTRIBUTING.md#如何提-pull-request) 来进行修改。

如果你想在本地定制输出符合特定场景需求的 PDF 格式的 TiDB 文档，例如对 TiDB 文档目录进行自由排序和删减，请参考[自助生成 TiDB 文档 PDF 教程](/resources/tidb-pdf-generation-tutorial.md)。

## TiDB 文档维护方式及版本说明

目前，TiDB 的文档维护在以下 branch，对应着官网文档的不同版本：

| 文档仓库 branch | 对应 TiDB 文档版本 |
|:---------|:----------|
| [`master`](https://github.com/pingcap/docs-cn/tree/master) | dev 最新开发版 |
| [`release-8.1`](https://github.com/pingcap/docs-cn/tree/release-8.1) | 8.1 长期支持版 (LTS) |
| [`release-8.0`](https://github.com/pingcap/docs-cn/tree/release-8.0) | 8.0 开发里程碑版 (DMR) |
| [`release-7.6`](https://github.com/pingcap/docs-cn/tree/release-7.6) | 7.6 开发里程碑版 (DMR) |
| [`release-7.5`](https://github.com/pingcap/docs-cn/tree/release-7.5) | 7.5 长期支持版 (LTS) |
| [`release-7.4`](https://github.com/pingcap/docs-cn/tree/release-7.4) | 7.4 开发里程碑版 (DMR) （该版本文档已归档，不再提供任何更新）|
| [`release-7.3`](https://github.com/pingcap/docs-cn/tree/release-7.3) | 7.3 开发里程碑版 (DMR) （该版本文档已归档，不再提供任何更新）|
| [`release-7.2`](https://github.com/pingcap/docs-cn/tree/release-7.2) | 7.2 开发里程碑版 (DMR)（该版本文档已归档，不再提供任何更新） |
| [`release-7.1`](https://github.com/pingcap/docs-cn/tree/release-7.1) | 7.1 长期支持版 (LTS) |
| [`release-7.0`](https://github.com/pingcap/docs-cn/tree/release-7.0) | 7.0 开发里程碑版 (DMR)（该版本文档已归档，不再提供任何更新） |
| [`release-6.6`](https://github.com/pingcap/docs-cn/tree/release-6.6) | 6.6 开发里程碑版 (DMR)（该版本文档已归档，不再提供任何更新） |
| [`release-6.5`](https://github.com/pingcap/docs-cn/tree/release-6.5) | 6.5 长期支持版 (LTS) |
| [`release-6.4`](https://github.com/pingcap/docs-cn/tree/release-6.4) | 6.4 开发里程碑版 (DMR)（该版本文档已归档，不再提供任何更新） |
| [`release-6.3`](https://github.com/pingcap/docs-cn/tree/release-6.3) | 6.3 开发里程碑版 (DMR)（该版本文档已归档，不再提供任何更新） |
| [`release-6.2`](https://github.com/pingcap/docs-cn/tree/release-6.2) | 6.2 开发里程碑版 (DMR)（该版本文档已归档，不再提供任何更新） |
| [`release-6.1`](https://github.com/pingcap/docs-cn/tree/release-6.1) | 6.1 长期支持版 (LTS) |
| [`release-6.0`](https://github.com/pingcap/docs-cn/tree/release-6.0) | 6.0 开发里程碑版 (DMR)（该版本文档已归档，不再提供任何更新） |
| [`release-5.4`](https://github.com/pingcap/docs-cn/tree/release-5.4) | 5.4 稳定版 |
| [`release-5.3`](https://github.com/pingcap/docs-cn/tree/release-5.3) | 5.3 稳定版 |
| [`release-5.2`](https://github.com/pingcap/docs-cn/tree/release-5.2) | 5.2 稳定版 |
| [`release-5.1`](https://github.com/pingcap/docs-cn/tree/release-5.1) | 5.1 稳定版 |
| [`release-5.0`](https://github.com/pingcap/docs-cn/tree/release-5.0) | 5.0 稳定版（该版本文档已归档，不再提供任何更新） |
| [`release-4.0`](https://github.com/pingcap/docs-cn/tree/release-4.0) | 4.0 稳定版（该版本文档已归档，不再提供任何更新） |
| [`release-3.1`](https://github.com/pingcap/docs-cn/tree/release-3.1) | 3.1 稳定版（该版本文档已归档，不再提供任何更新） |
| [`release-3.0`](https://github.com/pingcap/docs-cn/tree/release-3.0) | 3.0 稳定版（该版本文档已归档，不再提供任何更新） |
| [`release-2.1`](https://github.com/pingcap/docs-cn/tree/release-2.1) | 2.1 稳定版（该版本文档已归档，不再提供任何更新） |

## 贡献文档

[<img src="media/contribution-map.png" alt="contribution-map" width="180"></img>](https://github.com/pingcap/docs-cn/blob/master/credits.md)

你提交的第一个 [Pull Request](https://help.github.com/en/github/getting-started-with-github/github-glossary#pull-request) (PR) 合并以后，即可成为 TiDB 文档的 Contributor。查看 [TiDB 中文文档贡献指南](/CONTRIBUTING.md)，开始你的贡献吧！

## 贡献者数量增长图

[![Contributor over time](https://contributor-graph-api.apiseven.com/contributors-svg?chart=contributorOverTime&repo=pingcap/docs-cn)](https://www.apiseven.com/en/contributor-graph?chart=contributorOverTime&repo=pingcap/docs-cn)

## License

自 TiDB v7.0 起，所有文档的许可证均为 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。
