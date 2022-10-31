---
title: TiDB 6.4.0 Release Notes
---

# TiDB v6.4.0 Release Notes

发版日期：2022 年 x 月 xx 日

TiDB 版本：6.4.0-DMR

在 6.4.0-DMR 版本中，你可以获得以下关键特性：

- 关键特性 1
- 关键特性 2
- 关键特性 3
- ......

## 新功能

### SQL

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 安全

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 可观测性

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 性能

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 事务

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 稳定性

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 易用性

* TiKV API V2 GA

    在 v6.1.0 之前，TiKV 的 RawKV 接口仅存储客户端传入的原始数据，因此只提供基本的 Key Value 读写能力。此外，由于编码方式不同、数据范围没有隔离，因此在同一个 TiKV 集群中，TiDB、事务 KV、RawKV 无法同时使用，对于不同使用方式并存的场景，必须部署多套集群，增加了机器和部署成本。

    TiKV API V2 提供了新的存储格式，包括：

    * RawKV 数据以 MVCC 方式存储，记录数据的变更时间戳，并在此基础上提供 Change Data Capture 能力（实验特性，见 [TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)）。
    * 数据根据使用方式划分范围，支持单一集群 TiDB、事务 KV、RawKV 应用共存。
    * 预留 Key Space 字段，可以为多租户等特性提供支持。

    使用 TiKV API V2 请在 TiKV 的 `[storage]` 配置中增加或修改 `api-version = 2`。详见[用户文档](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)。

  <Warning>

    * 由于底层存储格式发生了重大变化，因此仅当 TiKV 只有 TiDB 数据时，可以平滑启用或关闭 API V2。其他情况下，需要新建集群，并使用 [TiKV-BR](https://github.com/tikv/migration/blob/main/br/README-cn.md) 进行数据迁移。

    * 启用 API V2 后，不能将 TiKV 集群回退到 v6.1.0 之前的版本，否则可能导致数据损坏。

  </Warning>

    [#11745](https://github.com/tikv/tikv/issues/11745) @[pingyu](https://github.com/pingyu)

    [用户文档](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)


* 优化 TiFlash 数据同步进度的准确性

    TiDB 的 `information_schema.tiflash_replica` 表中的 `PROGRESS` 字段表示 TiFlash 副本与 TiKV 中对应表数据的同步进度。在之前的版本中，`PROCESS` 字段只显示 TiFlash 副本创建过程中的数据同步进度。在 TiFlash 副本创建完后，当在 TiKV 相应的表中导入新的数据时，该值不会更新数据的同步进度。
    v6.3.0 版本改进了 TiFlash 副本数据同步进度更新机制，在创建 TiFlash 副本后，进行数据导入等操作，TiFlash 副本需要和 TiKV 数据进行同步时，[`information_schema.tiflash_replica`](/information-schema/information-schema-tiflash-replica.md) 表中的 `PROGRESS` 值将会更新，显示实际的数据同步进度。通过此优化，你可以方便地查看 TiFlash 数据同步的实际进度。

    [用户文档](/information-schema/information-schema-tiflash-replica.md) [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen)


* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### MySQL 兼容性

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 数据迁移

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 数据共享与订阅

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### 部署及运维

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

## 兼容性变更

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

## 废弃功能

## 改进提升

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

## 错误修复

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiKV

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ Tools

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()