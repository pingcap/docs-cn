---
title: 下游存在更多列的迁移场景
summary: 介绍下游存在更多列的迁移场景。
---

# 下游存在更多列的迁移场景

本文档介绍数据同步时，下游存在更多列的迁移场景需要的注意事项。具体迁移操作可参考已有数据迁移场景：

- [从 TiB 级以下 MySQL 迁移数据到 TiDB](/data-migration/migrate-mysql-tidb-less-tb.md)
- [从 TiB 级以上 MySQL 迁移数据到 TiDB](/data-migration/migrate-mysql-tidb-above-tb.md)
- [TB 级以下分库分表 MySQL 合并迁移数据到 TiDB](/data-migration/migrate-shared-mysql-tidb-less-tb.md)
- [TB 级以上分库分表 MySQL 合并迁移数据到 TiDB](/data-migration/migrate-shared-mysql-tidb-above-tb.md)

## 使用 DM 迁移至更多列的下游

截至当前版本，DM 同步 binlog 时，会尝试使用上游当前的表结构来解析 binlog 并生成相应的 DML 语句。如果 binlog 里数据的列数与表结构的列数不一致则会产生如下错误：

```json
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

例如上游表结构为：

```sql
# 上游表结构
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
)

# 下游表结构
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `message` varchar(255) DEFAULT NULL, # 下游比上游多出的列。
  PRIMARY KEY (`id`)
)
```

DM 尝试使用下游表结构解析上游产生的 binlog event 时，会报出上述`Column count doesn't match`错误。

此时，我们可以使用`operate-schema`命令来为该表指定与 binlog event 匹配的表结构。如果你在进行分表合并的数据迁移，那么需要为每个分表按照如下步骤在 DM 中设置用于解析 binlog event 的表结构。具体操作为：

第 1 步：为数据源中需要迁移的表指定表结构，表结构需要对应 DM 将要开始同步的 binlog event 的数据。将对应的 CREATE TABLE 表结构语句并保存到文件，例如将以下表结构保存到`log.messages.sql` 中。

```sql
# 上游表结构
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
)
```

第 2 步：使用`operate-schema`命令设置表结构（此时 task 应该由于上述错误而处于 Paused 状态）。

{{< copyable "shell-regular" >}}

```
tiup dmctl --master-addr ${advertise-addr} operate-schema set -s mysql-01 task-test -d log -t message log.message.sql
```

该命令中的参数描述如下：
|参数           |描述|
|-              |-|
|--master-addr  |dmctl 要连接的集群的任意 DM-master 节点的 {advertise-addr}，例如：172.16.10.71:8261|
|operate-schema set|手动设置 schema 信息|
|-s             |指定 source|
|-d             |指定 database|
|-t             |指定 table|

第 3 步：使用`resume-task`命令恢复处于 Paused 状态的任务。

{{< copyable "shell-regular" >}}

```
tiup dmctl --master-addr ${advertise-addr} resume-task ${task-name}
```

第 4 步：使用`query-status`命令确认数据迁移任务是否运行正常。

{{< copyable "shell-regular" >}}

```
tiup dmctl --master-addr ${advertise-addr} query-status resume-task ${task-name}
```
