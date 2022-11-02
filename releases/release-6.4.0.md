---
title: TiDB 6.4.0 Release Notes
---

# TiDB v6.4.0 Release Notes

发版日期：2022 年 x 月 xx 日

TiDB 版本：6.4.0-DMR

在 6.4.0-DMR 版本中，你可以获得以下关键特性：

- TiFlash 静态加密支持国密算法 SM4。
- 支持通过 FLASHBACK CLUSTER 命令将集群快速回退到过去某一个指定的时间点
- 关键特性 3
- ......

## 新功能

### SQL

* 支持通过 SQL 语句对指定 Partition 的 TiFlash 副本立即触发物理数据整理 (Compaction)

    v6.2.0 版本发布了针对全表的 TiFlash 副本立即触发 [物理数据整理 (Compaction)](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) 功能，支持用户自行选择合适的时机、手动执行 SQL 语句来对 TiFlash 中的物理数据立即进行整理，从而减少存储空间占用，并提升查询性能。v6.4.0 版本细化了 TiFlash 副本物理数据整理的粒度，支持对表中的指定 Partition 的 TiFlash 副本立即触发物理数据整理。
    通过 SQL 语句 `ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]` 可以立即触发指定 Partition 的 TiFlash 副本物理数据整理。

    [用户文档](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [#5315](https://github.com/pingcap/tiflash/issues/5315) @[hehechen](https://github.com/hehechen)

* 支持通过 FLASHBACK CLUSTER 命令将集群快速回退到过去某一个指定的时间点

    FLASHBACK CLUSTER 支持在 Garbage Collection (GC) life time 时间内，快速回退整个集群到指定的时间点。使用该特性可以轻松快速撤消 DML 误操作，例如，用户误执行了没有 WHERE 子句的 DELETE，FLASHBACK CLUSTER 能够在几分钟内回退原数据库集群到指点时间点。该特性不依赖于数据库备份，支持在时间线上反复回退以确定特定数据更改发生的时间。FLASHBACK CLUSTER 不能替代数据库备份。[#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303)  @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)

    [用户文档](/sql-statements/sql-statement-flashback-to-timestamp.md)


### 安全

*  TiKFlash 静态加密支持国密算法 SM4

    TiFlash 的静态加密新增 SM4 算法，用户可以修改配置文件 tiflash-learner.toml 中的 data-encryption-method 参数，设置为 sm4-ctr，以启用基于国密算法 SM4 的静态加密能力。 [#5953](https://github.com/pingcap/tiflash/issues/5953) @[lidezhu](https://github.com/lidezhu)

    [用户文档](/encryption-at-rest.md)

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

* TiDB 分区表兼容 Linear Hash 分区

    TiDB 现有的分区方式支持 Hash，Range，List 分区，在此基础上增加了对 [MySQL Linear Hash](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html) 分区的兼容行为，方便原 MySQL 用户迁移到 TiDB。
    用户现有的 MySQL Linear Hash 分区的 DDL 可以不经修改直接在 TiDB 上执行，产生一个 TiDB Hash 分区表（TiDB 内部实际不存在 Linear Hash 分区）。用户已有的查询/访问原 Linear Hash 分区的 SQL（DML）也可以不经修改，直接访问对应的 TiDB Hash 分区，得到正常结果。此功能保证了对 MySQL Linear Hash 分区的语法兼容，方便用户的应用无缝迁移到 TiDB。[#issue](https://github.com/pingcap/tidb/issues/38450) @[贡献者 GitHub ID](mjonss)

    [用户文档](/mysql-compatibility.md)

* 支持高性能、全局单调递增的 AUTO_INCREMENT 列属性

    TiDB 现有的 AUTO_INCREMENT 列属性的全局单调性和性能不可兼得，提供高性能、全局单调递增的 AUTO_INCREMENT 列属性能够更完美的兼容 MySQL AUTO_INCREMENT 的功能，降低用户从 MySQL 迁移到 TiDB 的改造成本。例如，使用该特性能够轻松解决用户的查询结果需要按照自增 ID 排序的问题。[#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao)

    [用户文档](/auto-increment.md#mysql-兼容模式)


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
| TiFlash | data-encryption-method | 修改 | 扩展可选值范围：增加 sm4-ctr。设置为 sm4-ctr 时，数据将采用国密算法 SM4 加密后进行存储。 |
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
