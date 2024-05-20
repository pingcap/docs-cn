---
title: TiDB Data Migration 任务前置检查
summary: 了解 DM 执行数据迁移任务时将进行的前置检查。
---

# TiDB Data Migration 任务前置检查

本文介绍了 TiDB Data Migration (DM) 的任务前置检查功能。此功能用于提前检测出上游 MySQL 实例配置中可能存在的一些错误。

## 使用场景

为了使数据迁移任务顺利进行，DM 在启动迁移任务时会自动触发任务前置检查，并返回检查结果。只有当前置检查通过后，DM 才开始执行迁移任务。

如果你想要手动触发前置检查，运行 `check-task` 命令即可。

例如：

{{< copyable "" >}}

```bash
tiup dmctl check-task ./task.yaml
```

## 检查项说明

当任务前置检查被触发时，DM 会按照配置的迁移模式对相应的检查项进行检查。

本小节列出了前置检查中的所有检查项。

> **注意：**
>
> 针对前置检查中必须通过的检查项，本文在检查项名称前标注了（必须）。
>
> + 对于标注了（必须）的检查项，如果检查没有通过，DM 会在检查结束后返回错误并拒绝执行该迁移任务。此时，请依据错误信息修改配置，在满足检查项要求后重试。
> + 对于未标注（必须）的检查项，如果检查没有通过，DM 会在检查结束后返回警告。如果检查结果中只有警告没有错误，DM 将自动开始执行该迁移任务。

### 通用检查项

对于任何一种迁移模式，前置检查都会包含以下通用检查项：

- 数据库版本

    - MySQL 版本 > 5.5
    - MariaDB 版本 >= 10.1.2

    > **警告：**
    >
    > - 使用 DM 从 MySQL v8.0 迁移数据到 TiDB 目前为实验特性（从 DM v2.0 引入），不建议在生产环境下使用。
    > - 使用 DM 从 MariaDB 迁移数据到 TiDB 目前为实验特性，不建议在生产环境下使用。

- 上游 MySQL 表结构的兼容性

    - 检查上游表是否设置了外键。TiDB 不支持外键，如果上游表设置了外键，则返回警告。
    - 检查上游字符集是否与 TiDB 兼容，详见 [TiDB 支持的字符集](/character-set-and-collation.md)。
    - 检查上游表中是否存在主键或唯一键约束（从 v1.0.7 版本引入）。

    > **警告：**
    >
    > - 上游使用不兼容的字符集时，下游可以使用 utf8mb4 字符集建表兼容同步，但不建议这样做。建议调整上游的字符集，使用下游支持的字符集。
    > - 上游表不存在主键或唯一键约束时，可能出现单行数据在下游被重复同步多次的情况，同步性能也会降低，不建议在生产环境下使用。

### 全量数据迁移检查项

对于全量数据迁移模式（`task-mode: full`），除了[通用检查项](#通用检查项)，前置检查还会包含以下检查项：

* （必须）上游数据库的 dump 权限

    - 检查是否有 INFORMATION_SCHEMA 和 dump 表的 SELECT 权限。
    - 如果 consistency=flush，将检查是否有 RELOAD 权限。
    - 如果 consistency=flush/lock，将检查是否有 dump 表的 LOCK TABLES 权限。

* （必须）上游 MySQL 多实例分库分表的一致性

    - 悲观协调模式下，检查所有分表的表结构是否一致，检查内容包括：

        - Column 数量
        - Column 名称
        - Column 顺序
        - Column 类型
        - 主键
        - 唯一索引

    - 乐观协调模式下，检查所有分表结构是否满足[乐观协调兼容](https://github.com/pingcap/tiflow/blob/release-8.1/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)。

    - 如果曾经通过 `start-task` 命令成功启动任务，那么将不会对一致性进行检查。

* 分表中自增主键检查

    - 分表存在自增主键时返回警告。如果存在自增主键冲突，请参照[自增主键冲突处理](/dm/shard-merge-best-practices.md#自增主键冲突处理)解决。

#### Physical Import 检查项

在任务配置中使用 `import-mode: "physical"` 后，会增加如下的前置检查项以保证[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)正常运行。如果参照提示后仍然难以完成这些前置检查，你可以尝试使用[逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)进行导入。

* 下游数据库中的空 Region

    - 如果空 Region 的数量大于 `max(1000, 表的数量 * 3)`，即大于“1000”和“3 倍表数量”二者中的较大者，前置检查会向用户返回警告。可以调整 PD 相关参数加快空 Region 的合并速度，并等待空 Region 数量下降以解除警告。参见 [PD 调度策略最佳实践 - Region Merge 速度慢](/best-practices/pd-scheduling-best-practices.md#region-merge-速度慢)

* 下游数据库中的 Region 分布

    - 统计不同的 TiKV 上的 Region 数目。假设 Region 数最少的 TiKV 节点上拥有 `a` 个 Region，Region 数最多的 TiKV 节点上拥有 `b` 个 Region，如果 a/b 小于 0.75，则前置检查会向用户返回警告。可以调整 PD 相关参数加快 Region 调度速度，并等待 Region 数目变化以解除警告。参见 [PD 调度策略最佳实践 - Leader/Region 分布不均衡](/best-practices/pd-scheduling-best-practices.md#leaderregion-分布不均衡)
    
* 下游数据库 TiDB、PD、TiKV 组件的版本

    - 物理导入模式需要调用 TiDB、PD、TiKV 接口，如果版本不符合要求，会返回错误。
    
* 下游数据库的剩余空间

    - 估算上游数据库所有白名单表的大小之和 (`source_size`)，如果下游数据库剩余空间小于 `source_size`，前置检查会返回错误；如果下游数据库剩余空间小于 TiKV 副本数 \* `source_size` \* 2，前置检查会返回警告。
    
* 下游数据库是否在运行与 Physical Import 不兼容的任务

    - 目前物理导入模式不兼容 [TiCDC](/ticdc/ticdc-overview.md)、[PITR](/br/br-pitr-guide.md) 任务，如果发现下游数据库正在运行这些任务，前置检查会返回错误。

### 增量数据迁移检查项

对于增量数据迁移模式（`task-mode: incremental`），除了[通用检查项](#通用检查项)，前置检查还会包含以下检查项：

* （必须）上游数据库的 REPLICATION 权限

    - 检查是否有 REPLICATION CLIENT 权限。
    - 检查是否有 REPLICATION SLAVE 权限。

* 数据库主从配置

    - 建议上游数据库设置数据库 ID `server_id`（非 AWS Aurora 环境建议开启 GTID），防止主从复制切换出错。

* （必须）MySQL binlog 配置

    - 检查 binlog 是否开启（DM 要求 binlog 必须开启）。
    - 检查是否有 `binlog_format=ROW`（DM 只支持 ROW 格式的 binlog 迁移）。
    - 检查是否有 `binlog_row_image=FULL`（DM 只支持 `binlog_row_image=FULL`）。
    - 如果配置了 `binlog_do_db` 或者 `binlog_ignore_db`，那么检查需要迁移的库表，是否满足 `binlog_do_db` 和 `binlog_ignore_db` 的条件。

* （必须）检查上游是否处于 [Online-DDL](/dm/feature-online-ddl.md) 过程中，即创建了 `ghost` 表，但还未执行 `rename` 的阶段。如果处于 online-DDL 中，则检查报错，请等待 DDL 结束后重试。

### 全量加增量数据迁移检查项

对于全量加增量数据迁移模式（`task-mode: all`），除了[通用检查项](#通用检查项)，前置检查还会包含[全量数据迁移检查项](#全量数据迁移检查项)，以及[增量数据迁移检查项](#增量数据迁移检查项)。

### 可忽略检查项

一般情况下前置检查项用于提前发现环境中可能存在的风险，不建议忽略。如果你的数据迁移任务面临特殊场景，你可以通过 [`ignore-checking-items` 配置项](/dm/task-configuration-file-full.md#完整配置文件示例)来跳过部分检查项。

|值|含义|
|-|-|
|dump_privilege|检查上游 MySQL 实例用户的 dump 相关权限|
|replication_privilege|检查上游 MySQL 实例用户的 replication 相关权限|
|version|检查上游数据库版本|
|server_id|检查上游数据库是否设置 server_id|
|binlog_enable|检查上游数据库是否已启用 binlog|
|table_schema|检查上游 MySQL 表结构的兼容性|
|schema_of_shard_tables|检查上游 MySQL 多实例分库分表的表结构一致性|
|auto_increment_ID|检查上游 MySQL 多实例分库分表的自增主键冲突|
|online_ddl|检查上游是否处于 [Online-DDL](/dm/feature-online-ddl.md) 过程中|
|empty_region|物理导入模式检查空 Region 的数目|
|region_distribution|物理导入模式检查 Region 的分布|
|downstream_version|检查下游数据库 TiDB、PD、TiKV 的版本|
|free_space|检查下游数据库的剩余空间|
|downstream_mutex_features|检查下游数据库是否存在与物理导入模式不兼容的任务|

> **注意：**
>
> 6.0 之前的版本支持忽略更多的检查项，但诸如 `binlog_row_image` 等参数，若配置错误可能导致同步时丢失数据，因此在 6.0 版本中移除了部分与数据安全相关的检查项。

## 配置检查参数

任务前置检查支持多线程并行。即使分表数目达到万级别，检查也可以在分钟级完成。

你可以通过数据迁移任务配置文件里 `mydumpers` 字段中的 `threads` 参数指定线程的数量。

```yaml
mydumpers:                           # dump 处理单元的运行配置参数
  global:                            # 配置名称
    threads: 4                       # dump 处理单元从上游数据库实例导出数据和执行前置检查时访问上游的线程数量，默认值为 4
    chunk-filesize: 64               # dump 处理单元生成的数据文件大小，默认值为 64，单位为 MB
    extra-args: "--consistency none" # dump 处理单元的其他参数，不需要在 extra-args 中配置 table-list，DM 会自动生成
```

> **注意：**
>
> `threads` 参数的值决定了上游和 DM 之间的物理连接数。过大的 `threads` 可能会加大上游的负载，请注意控制 `threads` 大小。
