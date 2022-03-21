---
title: 下游存在更多列的迁移场景
summary: 介绍下游存在更多列的迁移场景。
aliases: ['zh/tidb/dev/usage-scenario-downstream-more-columns/']
---

# 下游存在更多列的迁移场景

本文档介绍数据同步时，下游存在更多列的迁移场景需要的注意事项。具体迁移操作可参考已有数据迁移场景：

- [从小数据量 MySQL 迁移数据到 TiDB](/migrate-small-mysql-to-tidb.md)
- [从大数据量 MySQL 迁移数据到 TiDB](/migrate-large-mysql-to-tidb.md)
- [从小数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [从大数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-large-mysql-shards-to-tidb.md)

## 使用 DM 迁移至存在更多列的下游

DM 同步上游的 binlog 时，会尝试使用下游当前的表结构来解析 binlog 并生成相应的 DML 语句。如果上游的 binlog 里数据表的列数与下游表结构的列数不一致，则会产生如下错误：

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
```

例如下游表结构为：

```sql
# 下游表结构
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `message` varchar(255) DEFAULT NULL, # 下游比上游多出的列。
  PRIMARY KEY (`id`)
)
```

当 DM 尝试使用下游表结构解析上游产生的 binlog event 时，DM 会报出上述 `Column count doesn't match` 错误。

此时，你可以使用 `binlog-schema` 命令来为数据源中需要迁移的表指定表结构，表结构需要对应 DM 将要开始同步的 binlog event 的数据。如果你在进行分表合并的数据迁移，那么需要为每个分表按照如下步骤在 DM 中设置用于解析 binlog event 的表结构。具体操作为：

1. 在 DM 中，新建一个 `.sql` 文件，并将上游表结构对应的 `CREATE TABLE` 语句添加到该文件。例如，将以下表结构保存到 `log.messages.sql` 中。

    ```sql
    # 上游表结构
    CREATE TABLE `messages` (
    `id` int(11) NOT NULL,
    PRIMARY KEY (`id`)
    )
    ```

2. 使用 `binlog-schema` 命令为数据源中需要迁移的表设置表结构（此时数据迁移任务应该由于上述 `Column count doesn't match` 错误而处于 Paused 状态）。

    {{< copyable "shell-regular" >}}

    ```
    tiup dmctl --master-addr ${advertise-addr} binlog-schema update -s ${source-id} ${task-name} ${database-name} ${table-name} ${schema-file}
    ```

    该命令中的参数描述如下：

    | 参数            |  描述 |
    | :---           | :--- |
    | --master-addr  | 指定 dmctl 要连接的集群的任意 DM-master 节点的 `${advertise-addr}`。`${advertise-addr}` 表示 DM-master 向外界宣告的地址。 |
    | binlog-schema update| 手动更新 schema 信息 |
    | -s             | 指定 source。`${source-id}` 表示 MySQL 数据源 ID。 |
    | `${task-name}` | 指定 task。表示数据同步任务配置文件 `task.yaml` 中定义的同步任务名称。|
    | `${database-name}` | 指定 database。表示上游数据库名。 |
    | `${table-name}` | 指定 table。表示上游数据表名。表示将被设置的表结构文件。 |
    | `${schema-file}` | 指定表的 schema 文件。表示将被设置的表结构文件。 |
    
    例如：

    {{< copyable "shell-regular" >}}

    ```
    tiup dmctl --master-addr 172.16.10.71:8261 binlog-schema update -s mysql-01 task-test -d log -t message log.message.sql
    ```

3. 使用 `resume-task` 命令恢复处于 Paused 状态的同步任务。

    {{< copyable "shell-regular" >}}

    ```
    tiup dmctl --master-addr ${advertise-addr} resume-task ${task-name}
    ```

4. 使用 `query-status` 命令确认数据迁移任务是否运行正常。

    {{< copyable "shell-regular" >}}

    ```
    tiup dmctl --master-addr ${advertise-addr} query-status resume-task ${task-name}
    ```
