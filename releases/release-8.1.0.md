---
title: TiDB 8.1.0 Release Notes
summary: 了解 TiDB 8.1.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.1.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.1.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.1.0#version-list)

TiDB 8.1.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 7.5.0 版本），8.1.0 版本包含 [7.6.0-DMR](/releases/release-7.6.0.md) 和 [8.0.0-DMR](/releases/release-8.0.0.md) 中已发布的新功能、提升改进和错误修复。当你从 7.5.x 升级到 8.1.0 时，可以下载 [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v7.6-to-v8.1-zh-release-notes.pdf) 查看两个 LTS 版本之间的所有 release notes。下表列出了从 7.6.0 到 8.1.0 的一些关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>可扩展性与性能</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/br-snapshot-guide#%E6%81%A2%E5%A4%8D%E5%BF%AB%E7%85%A7%E5%A4%87%E4%BB%BD%E6%95%B0%E6%8D%AE">提升 BR 快照恢复速度</a></td>
    <td>通过该功能，BR 可以充分利用集群的规模优势，使 TiKV 集群中的所有节点都能参与到数据恢复的准备阶段，从而显著提升大规模集群中大数据集的恢复速度。实际测试表明，该功能可将下载带宽打满，下载速度可提升 8 到 10 倍，端到端恢复速度大约提升 1.5 到 3 倍。</td>
  </tr>
  <tr>
    <td></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/ddl-v2">建表性能提升 10 倍</a><br></td>
    <td>在 v7.6.0 中引入了新的 DDL 架构，批量建表的性能提高了 10 倍。这一重大改进极大地缩短了创建大量表所需的时间。特别是在 SaaS 场景中，快速创建大量表（从数万到数十万不等）是一个常见的挑战，使用该特性能显著提升 SaaS 场景的建表速度。</td>
  </tr>
  <tr>
    <td></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tune-region-performance#%E9%80%9A%E8%BF%87-active-pd-follower-%E6%8F%90%E5%8D%87-pd-region-%E4%BF%A1%E6%81%AF%E6%9F%A5%E8%AF%A2%E6%9C%8D%E5%8A%A1%E7%9A%84%E6%89%A9%E5%B1%95%E8%83%BD%E5%8A%9B">通过 Active PD Follower 提升 PD Region 信息查询服务的扩展能力（实验特性）</a></td>
    <td>TiDB v7.6.0 实验性地引入了 Active PD Follower 特性，允许 PD follower 提供 Region 信息查询服务。在 TiDB 节点数量较多和 Region 数量较多的集群中，该特性可以提升 PD 集群处理 GetRegion、ScanRegions 请求的能力，减轻 PD leader 的 CPU 压力。</td>
  </tr>
  <tr>
    <td></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/system-variables#tidb_dml_type-%E4%BB%8E-v800-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5">用于处理更大事务的批量 DML 执行方式（实验特性）</a></td>
    <td>大批量的 DML 任务，例如大规模的清理任务、连接或聚合，可能会消耗大量内存，并且在非常大的规模上受到限制。批量 DML (tidb_dml_type = "bulk") 是一种新的 DML 类型，用于更高效地处理大批量 DML 任务，同时提供事务保证并减轻 OOM 问题。该功能与用于数据加载的导入、加载和恢复操作不同。</td>
  </tr>
  <tr>
    <td></td>
    <td>增强对大量数据表的支持</td>
    <td>对于使用 TiDB 作为多租户应用程序记录系统的 SaaS 公司，经常需要存储大量的表。在以前的版本中，大量数据表的存在会引入潜在的稳定性风险。TiDB v8.0.0 通过以下增强功能改善了这一问题：<br>引入新的 <a href="https://docs.pingcap.com/zh/tidb/v8.1/system-variables#tidb_schema_cache_size-%E4%BB%8E-v800-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5">schema 缓存系统</a>，为表元数据提供了懒加载的 LRU (Least Recently Used) 缓存，并更有效地管理 schema 版本变更。<br>支持在 auto analyze 中配置<a href="https://docs.pingcap.com/zh/tidb/v8.1/system-variables#tidb_enable_auto_analyze_priority_queue-%E4%BB%8E-v800-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5">优先队列</a>，使流程更加流畅，并在大量表的情况下提高稳定性。</td>
  </tr>
  <tr>
    <td></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tidb-global-sort">全局排序成为正式功能 (GA)</a><br></td>
    <td>全局排序功能旨在提高 IMPORT INTO 和 CREATE INDEX 的稳定性与效率。通过将任务需要处理的数据进行全局排序，可以提高数据写入 TiKV 的稳定性、可控性和可扩展性，从而提供更好的数据导入与 DDL 任务的用户体验及更高质量的服务。目前已经支持&nbsp;&nbsp;40 TiB 的数据进行导入或者添加索引</td>
  </tr>
  <tr>
    <td>稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/sql-plan-management#%E8%B7%A8%E6%95%B0%E6%8D%AE%E5%BA%93%E7%BB%91%E5%AE%9A%E6%89%A7%E8%A1%8C%E8%AE%A1%E5%88%92-cross-db-binding">跨数据库绑定执行计划</a> <br></td>
    <td>在处理上百个 schema 相同的数据库时，针对其中一个数据库的 SQL binding 通常也适用于其它的数据库。例如，在 SaaS 或 PaaS 数据平台中，每个用户通常各自维护单独的数据库，这些数据库具有相同的 schema 并运行着类似的 SQL。在这种情况下，逐一为每个数据库做 SQL 绑定是不切实际的。TiDB v7.6.0 引入跨数据库绑定执行计划，支持在所有 schema 相同的数据库之间匹配绑定计划。</td>
  </tr>
  <tr>
    <td></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tiproxy-overview">支持 TiProxy</a><br></td>
    <td>全面支持 TiProxy，可通过部署工具轻松部署。TiProxy 可以管理和维护客户端与 TiDB 的连接，在滚动重启、升级以及扩缩容过程中保持连接。</td>
  </tr>
  <tr>
    <td></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/dm-compatibility-catalog">Data Migration (DM) 正式支持迁移 MySQL 8.0 (GA)</a><br></td>
    <td>在 v7.6.0 之前，DM 迁移 MySQL 8.0 仅为实验特性，不能用于生产环境。TiDB v7.6.0 增强了该功能的稳定性、兼容性，可在生产环境帮助你平滑、快速地将数据从 MySQL 8.0 迁移到 TiDB。在 v7.6.0 中，该功能正式 GA。</td>
  </tr>
  <tr>
    <td></td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.1/tidb-resource-control#%E7%AE%A1%E7%90%86%E8%B5%84%E6%BA%90%E6%B6%88%E8%80%97%E8%B6%85%E5%87%BA%E9%A2%84%E6%9C%9F%E7%9A%84%E6%9F%A5%E8%AF%A2-runaway-queries">管理资源消耗超出预期的查询</a> 成为正式功能 (GA)</td>
    <td>通过资源组的规则，TiDB 能够自动识别出运行超出预期的查询，并对该查询进行限流或取消处理。 即使没有被规则识别，用户仍旧可以手工添加查询特征以及对应的手段措施，从而降低突发的查询性能对整个数据库的影响。 </td>
  </tr>
  <tr>
    <td>数据库管理与可观测性</td>
    <td>支持观测索引使用情况</td>
    <td>正确的索引设计是提升数据库性能的重要前提。TiDB v8.0.0 引入内存表 <a href="https://docs.pingcap.com/zh/tidb/v8.1/information-schema-tidb-index-usage">INFORMATION_SCHEMA.TIDB_INDEX_USAGE</a> 和视图 <a href="https://docs.pingcap.com/zh/tidb/v8.1/sys-schema-unused-indexes">sys.schema_unused_indexes</a> ，用于记录索引的使用情况。该功能有助于用户评估数据库中索引的效率并优化索引设计。</td>
  </tr>
  <tr>
    <td>数据迁移</td>
    <td>TiCDC 支持 <a href="https://docs.pingcap.com/zh/tidb/v8.1/ticdc-simple-protocol">Simple 协议</a></td>
    <td>TiCDC 支持了新的 Simple 消息协议，该协议通过在 DDL 和 BOOTSTRAP 事件中嵌入表的 schema 信息，实现了对 schema 信息的动态追踪 (in-band schema tracking)。</td>
  </tr>
  <tr>
    <td></td>
    <td>TiCDC 支持 <a href="https://docs.pingcap.com/zh/tidb/v8.1/ticdc-debezium">Debezium 协议</a></td>
    <td>TiCDC 支持了新的 Debezium 协议，TiCDC 可以使用该协议生成 Debezium 格式的数据变更事件并发送给 Kafka sink。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.0.0 升级至当前版本 (v8.1.0) 所需兼容性变更信息。如果从 v7.6.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|        |                              |      |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 其他

## 离线包变更

## 废弃功能

* 废弃功能 1

* 废弃功能 2

* 废弃功能 3

* 废弃功能 4

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 性能测试

如需了解 TiDB v8.1.0 的性能表现，你可以参考 TiDB Dedicated 集群的 [TPC-C 性能测试报告](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-tpcc)和 [Sysbench 性能测试报告](https://docs.pingcap.com/tidbcloud/v8.1.0-performance-benchmarking-with-sysbench)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
