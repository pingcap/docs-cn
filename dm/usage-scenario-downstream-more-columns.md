---
title: 下游 TiDB 表结构存在更多列的数据迁移
summary: 了解如何在下游表结构比数据源存在更多列的情况下，使用 DM 对表进行迁移。
---

# 下游 TiDB 表结构有更多列的迁移场景

本文介绍如何在下游 TiDB 表结构比上游存在更多列的情况下，使用 DM 对表进行迁移。

## 数据源表

本文档示例所用的数据源实例如下所示：

| Schema | Tables |
|:------|:------|
| user  | information, log |
| store | store_bj, store_tj |
| log   | messages |

## 迁移要求

在 TiDB 中定制创建表 `log.messages`，其表结构包含数据源中 `log.messages` 表的所有列，且比数据源的表结构有更多的列。在此需求下，将数据源表 `log.messages` 迁移到 TiDB 集群的表 `log.messages`。

> **注意：**
>
> - 下游 TiDB 相比于数据源多出的列必须指定默认值或允许为 `NULL`。
> - 对于已经通过 DM 在正常迁移的表，可直接在下游 TiDB 中新增指定了默认值或允许为 `NULL` 的列而不会影响 DM 正常的数据迁移。

## 只迁移数据源增量数据到 TiDB ，并且下游 TiDB 表结构有更多列的场景问题处理

如果该迁移任务包含全量数据迁移，迁移任务可以正常运行；但是如果你使用其他方式进行了全量迁移，只是用 DM 进行增量数据复制，可以参考[只迁移数据源增量数据到 TiDB](/dm/usage-scenario-incremental-migration.md#创建同步任务)创建数据迁移任务，同时还需手动在 DM 中设置用于解析 MySQL binlog 的表结构。

否则，创建任务后，运行 `query-status` 会返回类似如下数据迁移错误：

```
"errors": [
    {
        "ErrCode": 36027,
        "ErrClass": "sync-unit",
        "ErrScope": "internal",
        "ErrLevel": "high",
        "Message": "startLocation: [position: (mysql-bin.000001, 2022), gtid-set:09bec856-ba95-11ea-850a-58f2b4af5188:1-9 ], endLocation: [position: (mysql-bin.000001, 2022), gtid-set: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9]: gen insert sqls failed, schema: log, table: messages: Column count doesn't match value count: 3 (columns) vs 2 (values)",
        "RawCause": "",
        "Workaround": ""
    }
]
```

出现以上错误的原因是 DM 迁移 binlog event 时，如果 DM 内部没有维护对应于该表的表结构，则会尝试使用下游当前的表结构来解析 binlog event 并生成相应的 DML 语句。如果 binlog event 里数据的列数与下游表结构的列数不一致时，则会产生上述错误。

此时，我们可以使用 [`operate-schema`](/dm/dm-manage-schema.md) 命令来为该表指定与 binlog event 匹配的表结构。如果你在进行分表合并的数据迁移，那么需要为每个分表按照如下步骤在 DM 中设置用于解析 MySQL binlog 的表结构。具体操作为：

1. 为数据源中需要迁移的表 `log.messages` 指定表结构，表结构需要对应 DM 将要开始同步的 binlog event 的数据。将对应的 `CREATE TABLE` 表结构语句并保存到文件，例如将以下表结构保存到 `log.messages.sql` 中。

    ```sql
    CREATE TABLE `messages` (
      `id` int(11) NOT NULL,
      `message` varchar(255) DEFAULT NULL,
      PRIMARY KEY (`id`)
    )
    ```

2. 使用 [`operate-schema`](/dm/dm-manage-schema.md) 命令设置表结构（此时 task 应该由于上述错误而处于 `Paused` 状态）。

    {{< copyable "" >}}
    
    ```bash
    tiup dmctl --master-addr <master-addr> operate-schema set -s mysql-01 task-test -d log -t message log.message.sql
    ```    

3. 使用 [`resume-task`](/dm/dm-resume-task.md) 命令恢复处于 `Paused` 状态的任务。

4. 使用 [`query-status`](/dm/dm-query-status.md) 命令确认数据迁移任务是否运行正常。
