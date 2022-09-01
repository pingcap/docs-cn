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

* 功能标题

    功能描述

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