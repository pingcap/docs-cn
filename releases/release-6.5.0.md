---
title: TiDB 6.5.0 Release Notes
---

# TiDB 6.5.0 Release Notes

发版日期：2022 年 xx 月 xx 日

TiDB 版本：6.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/)

TiDB 6.5.0 为长期支持版本 (Long-Term Support Releases, LTS)。

相比于前一个 LTS (即 6.1.0 版本)，6.5.0 版本包含 [6.2.0-DMR](/releases/release-6.2.0.md)、[6.3.0-DMR](/releases/release-6.3.0.md)、[6.4.0-DMR](/releases/release-6.4.0.md) 中已发布的新功能、提升改进和错误修复，并引入了以下关键特性：

- 关键特性 1
- 关键特性 2
- 关键特性 3
- ......

## 新功能

### SQL

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiFlash 支持 `INSERT SELECT` 语句 [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi)

    用户可以指定 TiFlash 执行 `INSERT SELECT` 中的 `SELECT` 子句（分析查询），并将结果在此事务中写回到 TIDB 表中:
    ```sql
    insert into t2 select mod(x,y) from t1;
    ```
    用户可以方便地保存（物化）TiFlash 的计算结果以供下游步骤使用，可以起到结果缓存（物化）的效果。适用于以下场景：使用 TiFlash 做复杂分析，需重复使用计算结果或响应高并发的在线请求，计算性质本身聚合性好（相对输入数据，计算得出的结果集比较小，推荐 100MB 以内）。作为写入对象的 结果表本身没有特别限制，可以任意选择是否添加 TiFlash 副本。（实验功能）
    更多信息，请参考[用户文档](/tiflash/tiflash-results-materialization.md)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 完整支持索引合并[INDEX MERGE](/glossary.md#index-merge)功能 [#3933](https://github.com/pingcap/tidb/issues/39333) @[guo-shaoge](https://github.com/guo-shaoge) 

    新增了对在 WHERE 语句中使用 `AND` 联结的过滤条件的索引合并能力（v6.5 之前的版本只支持 `OR` 连接词的情况），TiDB 的索引合并至此可以覆盖更一般的查询过滤条件组合，不再限定于并集（`OR`）关系。用户可以通过使用 使用 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) Hint 来开启对于 AND 联结的索引合并。关于“索引合并”功能的介绍请参阅 [v5.4 release note](/release-5.4.0#性能), 以及优化器相关的[用户文档](/explain-index-merge.md)

* 新增支持下推[JSON 函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#39458](https://github.com/pingcap/tidb/issues/39458) @[yibin87](https://github.com/yibin87)

    * `->`
    * `->>`
    * `JSON_EXTRACT()`

* 新增支持下推[字符串函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008)

    * `regexp_like`
    * `regexp_instr`
    * `regexp_substr`

* 新增全局 hint 指定[视图](/develop/dev-guide-use-views.md)内查询的优化器行为 [#37887](https://github.com/pingcap/tidb/issues/37887) @[Reminiscent](https://github.com/Reminiscent)

    [视图](/develop/dev-guide-use-views.md)是数据库常见的建模方式。 当 SQL 语句中包含对视图的访问时，部分情况下需要用 hint 对视图内查询的执行计划进行干预，以获得最佳性能。 在 v6.5.0 中， TiDB 允许针对视图内的查询块添加全局 hint 。 全局 hint 由 “查询块命名” 和 “ hint 引用” 两部分组成，为包含复杂视图嵌套的 SQL 提供 hint 的注入手段， 增强了执行计划控制能力， 进而稳定复杂 SQL 的执行性能。

    更多信息，请参考[用户文档](/optimizer-hints.md#全局生效的-Hint)。

* [分区表](/partitioned-table.md)的排序操作下推至 TiKV [#26166](https://github.com/pingcap/tidb/issues/26166) @[winoros](https://github.com/winoros)

    [分区表](/partitioned-table.md)在 v6.1.0 正式 GA， TiDB 持续提升分区表相关的性能。 在 v6.5.0 中， 排序操作如 `ORDER BY`, `LIMIT` 能够下推至 TiKV 进行计算和过滤，降低网络 I/O 的开销，提升了使用分区表时 SQL 的性能。 
    

### 事务

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 易用性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 完善 EXPLAIN ANALYZE 输出的 TiFlash 的 TableFullScan 算子的统计信息 [#5926](https://github.com/pingcap/tiflash/issues/5926) @[hongyunyan](https://github.com/hongyunyan)

    [`EXPLAIN ANALYZE`] 语句可以输出执行计划及运行时的统计信息。现有版本的统计信息中，TiFlash 的 TableFullScan 算子统计信息不完善。v6.5.0 版本对 TableFullScan 算子的统计信息进行完善，补充了 dmfile 相关的执行信息，可以更加清晰的展示 TiFlash 的数据扫描状态信息，方便进行性能分析。

    更多信息，请参考[用户文档](sql-statements/sql-statement-explain-analyze.md)。

* 执行计划支持 JSON 格式的打印 [#39261](https://github.com/pingcap/tidb/issues/39261) @[fzzf678](https://github.com/fzzf678)

    在新版本中，TiDB 扩展了执行计划的打印格式。 通过 `explain format = json <SQL语句> ` 能够将 SQL 的执行计划以 JSON 格式输出。 借助这个能力，SQL 调试工具和诊断工具能够更方便准确地解读执行计划，进而提升 SQL 诊断调优的易用性。

    更多信息，请参考[用户文档](/sql-statements/sql-statement-explain.md)。

### MySQL 兼容性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 支持导出和导入压缩后的 CSV、SQL 文件 [#38514](https://github.com/pingcap/tidb/issues/38514) @[lichunzhu](https://github.com/lichunzhu)

功能描述：支持导出和导入压缩后的 CSV 文件
        功能简介：Dumpling 支持将数据导出为 SQL、CSV 的压缩文件，支持 gzip/snappy/zstd 三种压缩格式。Lightning 支持导入压缩后的 SQL、CSV 文件，支持gzip/snappy/zstd 三种压缩格式。
        功能价值：之前用户导出数据或者导入数据都需要提供较大的存储空间，用于存储导出或者即将导入的非压缩后的 csv 、sql文件，导致存储成本增加。该功能发布后，通过压缩存储空间，可以大大降低用户的存储成本。
        如何使用：参考用户文档
    更多信息，请参考[用户文档](https://github.com/pingcap/tidb/issues/38514)。


* 优化了 binlog 解析能力 [#无](无) @[gmhdbjd](https://github.com/GMHDBJD)

功能描述：优化了 binlog 解析能力
        功能简介： 可将不在迁移任务里的库、表对象的 binlog event 过滤掉不做解析，从而提升解析效率和稳定性。 
        功能价值： 原先用户仅迁移少数几张表，也需要解析上游整个 binlog 文件，即仍需要解析该 binlog 文件中不需要迁移的表的 binlog event，效率会比较低，同时如果不在迁移任务里的库表的 binlog event 不支持解析，还会导致任务失败。通过只解析在迁移任务里的库表对象的 binlog event 可以大大提升 binlog 解析效率，提升任务稳定性。
        如何使用：该策略在 6.5 版本默认生效，用户不感知。

* Lightning 支持  disk quota 特性 GA，可避免 Lightning 任务写满本地磁盘 [#无](无) @[buchuitoudegou](https://github.com/buchuitoudegou)
功能描述：Lightning 支持  disk quota 特性 GA，可避免写 Lightning 任务满本地磁盘
        功能简介：你可以为 TiDB Lightning 配置磁盘配额 (disk quota)。当磁盘配额不足时，TiDB Lightning 会暂停读取源数据以及写入临时文件的过程，优先将已经完成排序的 key-value 写入到 TiKV，TiDB Lightning 删除本地临时文件后，再继续导入过程。
        功能价值： 没有这个功能之前，TiDB Lightning 在使用物理模式导入数据时，会在本地磁盘创建大量的临时文件，用来对原始数据进行编码、排序、分割。当用户本地磁盘空间不足时，TiDB Lightning 会由于写入文件失败而报错退出。 
        如何使用：参考用户文档
    更多信息，请参考[用户文档]( https://docs.pingcap.com/tidb/v6.4/tidb-lightning-physical-import-mode-usage#configure-disk-quota-new-in-v620)。


* GA DM 增量数据校验的功能 [#4426](https://github.com/pingcap/tiflow/issues/4426) @[[D3Hunter](https://github.com/D3Hunter)
功能描述： GA DM 增量数据校验的功能
        功能简介： 在将增量数据从上游迁移到下游数据库的过程中，数据的流转有小概率导致错误或者丢失的情况。对于需要依赖于强数据一致的场景，如信贷、证券等业务，你可以在数据迁移完成之后对数据进行全量校验，确保数据的一致性。然而，在某些增量复制的业务场景下，上游和下游的写入是持续的、不会中断的，因为上下游的数据在不断变化，导致用户难以对表里面的全部数据进行一致性校验。
        功能价值： 过去，需要中断业务，做全量数据校验，会影响用户业务。现在推出该功能后，在一些不可中断的业务场景，无需中断业务，通过该功能就可以实现增量数据校验。
        如何使用：参考用户文档
    更多信息，请参考[用户文档]( https://docs.pingcap.com/tidb/v6.4/dm-continuous-data-validation)。

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据共享与订阅

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 部署及运维

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

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

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 改进持续对特定行只加锁但不更新情况下的读写性能 [#13694](https://github.com/tikv/tikv/issues/13694) [@sticnarf](https://github.com/sticnarf)
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

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID](链接)