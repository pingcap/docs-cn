---
title: DM 执行任务时的前置检查
summary: 了解 DM 执行数据迁移任务时将进行的前置检查。
aliases: ['/docs-cn/tidb-data-migration/dev/precheck/']
---

# 任务前置检查

本文介绍了 DM 提供的任务前置检查功能，DM 会在任务启动时自动触发任务前置检查并返回检查结果。只有当前置检查通过后，DM 才开始执行该任务。此功能用于在启动数据迁移任务时提前检测出上游 MySQL 实例配置中可能存在的一些错误。

如果你想要手动触发前置检查，运行 `check-task` 命令即可。例如：

{{< copyable "" >}}

```bash
tiup dmctl check-task ./task.yaml
```

## 检查项说明

要使数据迁移任务顺利进行，上下游数据库用户必须具备相应的读写权限。在任务前置检查中，DM 会根据配置文件自动检查上游和下游数据库的用户权限和配置。

本小节列出了任务前置检查中的所有检查项，并对各检查项的检查内容进行了说明。

> **注意：**
>
> 针对前置检查中必须通过的检查项，本文在检查项名称前标注了（必须）。
>
> + 对于标注了（必须）的检查项，如果检查没有通过，DM 会在检查结束后返回错误并拒绝执行该迁移任务。此时，请依据错误信息修改配置，在满足检查项要求后重试。
> + 对于未标注（必须）的检查项，如果检查没有通过，DM 会在检查结束后返回警告。如果检查结果中只有警告没有错误，DM 将自动开始执行该迁移任务。

* 通用检查项

    - 数据库版本

        - MySQL 版本 > 5.5
        - MariaDB 版本 >= 10.1.2
        > **警告：**
        >
        > - 使用 DM 从 MySQL v8.0 迁移数据到 TiDB 目前为实验特性（从 DM v2.0 引入），不建议在生产环境下使用。
        > - 使用 DM 从 MariaDB 迁移数据到 TiDB 目前为实验特性，不建议在生产环境下使用。

    - 上游 MySQL 表结构的兼容性

        - 检查上游表是否设置了外键。TiDB 不支持外键，如果上游表设置了外键，则返回警告。
        - （必须）检查字符集是否存在兼容性差异，详见 [TiDB 支持的字符集](/character-set-and-collation.md)。
        - （必须）检查上游表中是否存在主键或唯一键约束（从 v1.0.7 版本引入）。

## 使用场景

本节介绍各场景的具体检查项。

### 全量数据迁移模式（`task-mode: full`）

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

    - 乐观协调模式下，检查所有分表结构是否满足[乐观协调兼容](https://github.com/pingcap/tiflow/blob/master/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)。

    - 如果曾经通过 `start-task` 命令成功启动任务，那么将不会对一致性进行检查。

* 分表中自增主键检查

    - 分表存在自增主键时返回警告。如果存在自增主键冲突，请参照[自增主键冲突处理](/dm/shard-merge-best-practices.md#自增主键冲突处理)解决。

### 增量数据迁移模式（ `task-mode: incremental` ）

* （必须）上游数据库的 REPLICATION 权限

    - 检查是否有 REPLICATION CLIENT 权限。
    - 检查是否有 REPLICATION SLAVE 权限。

* （必须）数据库主从配置

    - 上游数据库必须设置数据库 ID `server_id`（非 AWS Aurora 环境建议开启 GTID）。

* （必须）MySQL binlog 配置

    - 检查 binlog 是否开启（DM 要求 binlog 必须开启）。
    - 检查是否有 `binlog_format=ROW`（DM 只支持 ROW 格式的 binlog 迁移）。
    - 检查是否有 `binlog_row_image=FULL`（DM 只支持 `binlog_row_image=FULL`）。
    - 如果配置了 `binlog_do_db` 或者 `binlog_ignore_db`，那么检查需要迁移的库表，是否满足 `binlog_do_db` 和 `binlog_ignore_db` 的条件。

* （必须）检查上游是否处于 [Online-DDL](/dm/feature-online-ddl.md) 过程中，即创建了 `ghost` 表，但还未执行 `rename` 的阶段。如果处于 online-DDL 中，则检查报错，请等待 DDL 结束后重试。

### 全量加增量数据迁移模式 （ `task-mode: all` ）

对于全量加增量数据迁移模式，除了通用检查项外，前置检查还将包含全量数据迁移模式（ `task-mode: full` ）相关的检查项，以及增量数据迁移模式（ `task-mode: incremental` ）相关的检查项。

## 检查配置

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
