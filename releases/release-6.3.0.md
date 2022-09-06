---
title: TiDB 6.3.0 Release Notes
---

# TiDB v6.3.0 Release Notes

发版日期：2022 年 x 月 xx 日

TiDB 版本：6.3.0-DMR

在 6.3.0-DMR 版本中，你可以获得以下关键特性：

- 关键特性 1
- 关键特性 2
- 关键特性 3
- ......

## 新功能

### SQL

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

* 完善基于 SQL 的数据放置规则功能的兼容性

    TiDB 在 v6.0.0 版本提供基于 SQL 的数据放置规则功能，但是由于实现机制冲突，该功能和构建 TiFlash 副本功能不兼容。v6.3.0 版本进行改进优化，完善了这两个功能的兼容性。

    [用户文档](/placement-rules-in-sql.md#使用限制) [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

* 增加支持以下窗口分析函数：

    * `LEAD()`
    * `LAG()`

  [用户文档](/tiflash/tiflash-supported-pushdown-calculations.md)，[#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise)

### 安全

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 可观测性

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 性能

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

* TiFlash 调整 FastScan 功能使用方式（实验特性）

    TiFlash 从 v6.2.0 版本开始引入的快速扫描功能 (FastScan)，性能上符合预期，但是使用方式上缺乏灵活性。因此，TiFlash 在 v6.3.0 版本调整 FastScan 功能的使用方式，停止使用对表设定是否开启 FastScan 功能的方式，改为使用变量 `tiflash_fastscan` 控制是否开启 FastScan 功能。

    从 v6.2.0 版本升级到 v6.3.0 版本时，在 v6.2.0 版本的所有 FastScan 设定将失效，需要重新使用变量方式进行 FastScan 设定，但不影响数据的正常读取。从更早版本升级到 v6.3.0 时，所有会话默认不开启 FastScan 功能，而是保持一致性的数据扫描功能。

    [用户文档](/develop/dev-guide-use-fastscan.md) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

* TiFlash 优化提升多并发场景下的数据扫描性能

    TiFlash 通过合并相同数据的读取操作，减少对于相同数据的重复读取，优化了多并发任务情况下的资源开销，提升多并发下的数据扫描性能。避免了以往在多并发任务下，如果涉及相同数据，同一份数据需要在每个任务中分别进行读取的情况，以及可能出现在同一时间内对相同数据进行多次读取的情况。
    该功能在 v6.2.0 版本以实验特性发布，并在 v6.3.0 版本作为正式功能发布。

    [用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

### 事务

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 稳定性

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 易用性

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### MySQL 兼容性

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 数据迁移

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 数据共享与订阅

* TiCDC 支持对多个异地目标数据源进行数据复制的复杂部署形态

    为了提供一套 TiDB 集群的数据能复制到多个不同的异地数据系统的能力，自 v6.3.0 开始，TiCDC 节点可以部署到多个不同的异地的机房中，来分别负责对应机房的数据复制任务，以支撑各种复杂的异地数据复制使用场景和部署形态。

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 部署及运维

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

## 兼容性变更

### 系统变量

| 变量名 | 修改类型（包括新增/修改/删除） | 描述 |
| ------ | ------ | ------ |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 其他

## 废弃功能

## 改进提升

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()

## 错误修复

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
