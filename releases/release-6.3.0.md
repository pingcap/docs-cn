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
- TiKV/TiFlash 静态加密支持国密算法 SM4
- TiDB 支持基于国密算法 SM3 插件的身份验证
- SQL语句CREATE USER / ALTER USER支持ACCOUNT LOCK/UNLOCK 选项
- JSON 数据类型和 JSON 函数 GA
- TiDB 支持 Null Aware Anti Join

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

* CREATE USER 支持 ACCOUNT LOCK/UNLOCK 选项

    在执行CREATE USER创建用户时，允许使用ACCOUNT LOCK / UNLOCK 选项，限定被创建的用户是否被锁定。锁定后的用户不能正常登录数据库。
    
    [用户文档]( / sql-statements/sql-statement-create-user.md),[#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf)

* ALTER USER 支持 ACCOUNT LOCK/UNLOCK 选项

    对于已存在的用户，可以通过ALTER USER 使用 ACCOUNT LOCK / UNLOCK 选项，修改用户的锁定状态。
    
    [用户文档]( /sql-statements/sql-statement-alter-user.md),[#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf)

* JSON 数据类型和 JSON 函数 GA

    JSON 是一种流行的数据格式，被大量的程序设计所采用。TiDB 在早起版本就引入了 JSON 支持， 兼容 MySQL 的 JSON 数据类型 和一部分 JSON 函数。在 v6.3.0 版本中，我们正式将这些功能 GA ，用户可以安全地在生产环境中使用 JSON 相关的功能。 JSON 功能的 GA，为 TiDB 提供了更丰富的数据类型支持，同时也进一步提升的 TiDB 对 MySQL 的兼容能力。

    [用户文档](/data-type-json.md) [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei)

### 安全

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()
    
* 静态加密 TiKV 支持国密算法SM4

    TiKV 静态加密中新增加密算法SM4，用户在配置静态加密时，支持配置 data-encryption-method 参数为 "sm4-ctr"，以启用基于国密算法SM4的静态加密能力。
    
    [用户文档](/encryption-at-rest.md) [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)
    
* 静态加密 TiFlash 支持国密算法SM4

    TiFlash 静态加密中新增加密算法SM4，用户在配置静态加密时，支持配置 data-encryption-method 参数为 "sm4-ctr"，以启用基于国密算法SM4的静态加密能力。

    [用户文档](/encryption-at-rest.md) [#5714](https://github.com/pingcap/tiflash/issues/5714) @[lidezhu](https://github.com/lidezhu)
    
* TiDB 支持国密算法 SM3 的身份验证

    TiDB 身份验证新增基于国密算法 SM3 的插件“tidb_sm3_password”，启用此插件后，用户密码将通过SM3进行加密存储和验证。
    
    [用户文档](/system-variables.md) [#36192](https://github.com/pingcap/tidb/issues/36192) @[CbcWestwolf](https://github.com/CbcWestwolf)

* JDBC 支持国密算法 SM3 的身份验证

    用户密码的身份验证需要客户端的支持，现在 JDBC 支持国密算法 SM3 的能力，用户可以通过 JDBC 连接到 TiDB 使用国密算法 SM3 的身份验证能力。

    [用户文档]() []() @[]()

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

* TiDB 支持 Null Aware Anti Join

    TiDB 在新版本中引入了新的连接类型 Null Aware Anti Join (NAAJ)。 NAAJ 在集合操作时能够感知集合是否为空，或是否有空值，优化了一部分操作比如`IN`、`= ANY` 的执行效率，提升SQL性能。 

    [用户文档](/explain-subqueries.md) [#issue]() @[贡献者 GitHub ID]()

* 增加优化器 hint 控制哈希连接的驱动端

    在新版本中，优化器引入了两个新的 hint `HASH_JOIN_BUILD()` 和 `HASH_JOIN_PROBE()` 用来指定哈希连接时的驱动端和被驱动端。 这两个新的 hint 与原有的 `LEADING()` 和 `HASH_JOIN` 兼容，可以组合使用，从而达到细粒度的执行计划控制。 在没有选到最优执行计划的情况下，提供了更丰富的干预手段。 

    [用户文档](/explain-subqueries.md) [#issue]() @[贡献者 GitHub ID]()

### 事务

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

* 悲观事务可以延迟唯一性检查

    提供变量 `tidb_constraint_check_in_place_pessimistic` 来控制悲观事务中唯一约束检查的时间点。 当变量设为 `ON` 时， TiDB 会把加锁操作和唯一约束检测推迟到必要的时候进行， 以此提升批量DML操作的性能。 

    [用户文档](/constraints.md#唯一约束) [#36579](https://github.com/pingcap/tidb/issues/36579) @[贡献者 GitHub ID]()

* 优化 Read-Committed 隔离级别中对 TSO 的获取

    在 Read-Committed 隔离级别中， 引入新的系统变量控制语句对 TSO 的获取方式。 在Plan Cache命中的情况下，通过降低对 TSO 的获取频率提升批量DML的执行效率，降低跑批类任务的执行时间。 

    [用户文档]() [#36812](https://github.com/pingcap/tidb/issues/36812) @[贡献者 GitHub ID]()  


### 稳定性

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

* 修改优化统计信息过期时的默认加载策略

    在 v5.3.0 版本时，我们引入变量 `tidb_enable_pseudo_for_outdated_stats` 控制优化器过期的加载策略，默认为 `ON`，即保持旧版本行为不变：当 SQL 涉及的对象的统计信息过期时，优化器认为该表上除总行数以外的统计信息不再可靠，转而使用 pseudo 统计信息。 经过一系列测试和用户实际场景分析， 我们在新版本中决定将  `tidb_enable_pseudo_for_outdated_stats` 的默认值改为 `OFF`, 即使统计信息过期，优化器也仍会使用该表上的统计信息，这有利于执行计划的稳定性。 

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 易用性

* 优化 TiFlash 数据同步进度的准确性

    TiDB 的 information_schema.tiflash_replica 表中的 PROGRESS 字段表示对应表 TiFlash 副本与 TiKV 数据的同步进度。在之前的版本中，PROCESS 字段只显示创建 TiFlash 副本过程中的数据同步进度。当 TiFlash 副本创建完毕，进行数据导入后，该值不会更新数据同步进度。v6.3.0 版本改进了 TiFlash 副本数据同步进度更新机制，在创建 TiFlash 副本后，进行数据导入等操作，TiFlash 副本需要和 TiKV 数据进行同步时，information_schema.tiflash_replica 表中的 PROGRESS 值将会更新，显示实际的数据同步进度。通过 TiFlash 数据同步进度的准确性优化，用户可以了解数据同步的实际进度，具有更好的使用体验。

    [用户文档](/information-schema/information-schema-tiflash-replica.md) [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen)

### MySQL 兼容性

* 功能标题

    功能描述

    [用户文档]() [#issue]() @[贡献者 GitHub ID]()

### 备份恢复

* PITR 支持以 GCS/Azure Blob Storage 作为备份存储目标。部署在 GCP 或者 Azure 上的用户，升级 TiDB 集群到 v6.3.0 后，就可以使用 PITR 功能了。
[用户文档](xxx)  @[joccau](https://github.com/joccau)

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
| default_authentication_plugin | 修改 | 扩展可选值范围：增加 tidb_sm3_password，设置为 tidb_sm3_password 时，用户密码验证的加密算法为国密算法SM3 |
|  |  |  |
|  |  |  |
|  |  |  |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiKV | data-encryption-method | 修改 | 扩展可选值范围：增加：sm4-ctr，设置为 sm4-ctr 时，数据将采用国密算法SM4加密后进行存储 |
| TiFlash | data-encryption-method | 修改 | 扩展可选值范围：增加：sm4-ctr，设置为 sm4-ctr 时，数据将采用国密算法SM4加密后进行存储 |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 其他
* 提升对 MySQL 的兼容性：修复 MySQL 兼容性不支持项 “TiDB 不支持 ACCOUNT LOCK 和 ACCOUNT UNLOCK 选项”

## 废弃功能

## 改进提升

+ TiDB

    - note [#issue]() @[贡献者 GitHub ID]()
    - 支持 ACCOUNT LOCK/UNLOCK [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf)

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
