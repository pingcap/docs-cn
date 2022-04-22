---
title: 管理迁移表的表结构
summary: 了解如何管理待迁移表在 DM 内部的表结构。
---

# 管理迁移表的表结构

本文介绍如何使用 [dmctl](/dm/dmctl-introduction.md) 组件来管理通过 DM 迁移的表在 DM 内部的表结构。

## 原理介绍

DM 执行增量迁移时，首先读取上游的 binlog，然后生成 SQL 语句执行到下游。但是，上游的 binlog 中并不记录表的完整结构信息，为了生成 SQL 语句，DM 内部维护了待迁移的表的 schema 信息，即表结构信息，DM 中的 schema 信息来源包括以下几部分：

1. 执行全量数据迁移（task-mode=all）时，任务将经过 dump/load/sync （全量导出/全量导入/增量同步）三个阶段。dump 阶段将表结构信息随着数据一并导出，并自动在下游创建相关表。sync 阶段时即以该表结构作为起始的表结构信息；
2. sync 阶段中，处理 DDL 语句（如 alter table）时，DM 执行该语句的同时更新内部维护的表结构信息；
3. 如果任务是增量迁移（task-mode=incremental），下游已经将待迁移的表创建完成，DM 会从下游数据库获取该表的结构信息（此行为随版本变化而不同）。

增量迁移过程的 Schema 信息维护较为复杂，在整个数据链路中包含以下几类可能相同或不同的表结构。

![表结构](/media/dm/operate-schema.png)

- 上游当前时刻的表结构（记为 `schema-U`）。
- 当前 DM 正在消费的 binlog event 的表结构（记为 `schema-B`，其对应于上游某个历史时刻的表结构）。
- DM 内部（schema tracker 组件）当前维护的表结构（记为 `schema-I`）。
- 下游 TiDB 集群中的表结构（记为 `schema-D`）。

在大多数情况下，以上 4 类表结构一致。当上游执行 DDL 变更表结构后，`schema-U` 即会发生变更；DM 通过将该 DDL 应用于内部的 schema tracker 组件及下游 TiDB，会先后更新 `schema-I`、`schema-D` 以与 `schema-U` 保持一致，因而随后能正常消费 binlog 中在 DDL 之后对应表结构为 `schema-B` 的 binlog event。即当 DDL 被复制成功后，仍能保持 `schema-U`、`schema-B`、`schema-I` 及 `schema-D` 的一致。

需要注意以下不一致的情况：

- 在开启[乐观 shard DDL 支持](/dm/feature-shard-merge-optimistic.md) 的数据迁移过程中，下游合并表的 `schema-D` 可能与部分分表对应的 `schema-B` 及 `schema-I` 并不一致，但 DM 仍保持 `schema-I` 与 `schema-B` 的一致以确保能正常解析 DML 对应的 binlog event。

- 下游比上游多部分列，`schema-D` 也可能会与 `schema-B` 及 `schema-I` 并不一致。`task-mode=all`时 DM 会自动处理，而`task-mode=incremental`时，由于任务首次启动，内部尚无 Schema 信息，DM 将自动读取下游表结构即 `schema-D`，更新自身的`schema-I`(此行为随版本变化而不同)。之后 DM 使用`schema-I`解析`schema-B`的 binlog 将会导致`Column count doesn't match value count`错误，详情可参考：[下游存在更多列的迁移场景](/migrate-with-more-columns-downstream.md)

为了支持以上的特殊场景及处理其他可能的由于 schema 不匹配导致的迁移中断等问题，DM 提供了 `binlog-schema` 命令来获取、修改、删除 DM 内部维护的表结构 `schema-I`。

> **注意：**
>
> `binlog-schema` 命令仅在 DM v6.0 及其以后版本支持，之前版本可使用 `operate-schema` 命令。

## 命令介绍

{{< copyable "" >}}

```bash
help binlog-schema
```

```
manage or show table schema in schema tracker

Usage:
  dmctl binlog-schema [command]

Available Commands:
  delete      delete table schema structure
  list        show table schema structure
  update      update tables schema structure

Flags:
  -h, --help   help for binlog-schema

Global Flags:
  -s, --source strings   MySQL Source ID.

Use "dmctl binlog-schema [command] --help" for more information about a command.
```

> **注意：**
>
> - 由于表结构在数据迁移过程中可能会发生变更，为获取确定性的表结构，当前 `binlog-schema` 命令仅能在数据迁移任务处于 `Paused` 状态时可用。
> - 强烈建议在修改表结构前，首先获取并备份表结构，以免误操作导致数据丢失。

## 参数解释

+ `delete`：删除表结构
+ `list`：获取查看表结构
+ `update`：更新设置表结构
+ `-s` 或 `--source`:
    - 必选
    - 指定操作将应用到的 MySQL 源

## 使用示例

### 获取表结构

如需获取表结构，可使用 `binlog-schema list` 命令：

```bash
help binlog-schema list
```

```
show table schema structure

Usage:
  dmctl binlog-schema list <task-name> <database> <table> [flags]

Flags:
  -h, --help   help for list

Global Flags:
  -s, --source strings   MySQL Source ID.
```

假设要获取 `db_single` 任务对应于 `mysql-replica-01` MySQL 源的 ``` `db_single`.`t1` ``` 表的表结构，则执行如下命令：

{{< copyable "" >}}

```bash
binlog-schema list -s mysql-replica-01 task_single db_single t1
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "CREATE TABLE `t1` ( `c1` int(11) NOT NULL, `c2` int(11) DEFAULT NULL, PRIMARY KEY (`c1`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```

### 更新设置表结构

如需更新设置表结构，可使用 `binlog-schema update` 命令：

```bash
help binlog-schema update
```

```
update tables schema structure

Usage:
  dmctl binlog-schema update <task-name> <database> <table> [schema-file] [flags]

Flags:
      --flush         flush the table info and checkpoint immediately (default true)
      --from-source   use the schema from upstream database as the schema of the specified tables
      --from-target   use the schema from downstream database as the schema of the specified tables
  -h, --help          help for update
      --sync          sync the table info to master to resolve shard ddl lock, only for optimistic mode now (default true)

Global Flags:
  -s, --source strings   MySQL Source ID.
```

假设要设置 `db_single` 任务对应于 `mysql-replica-01` MySQL 源的 ``` `db_single`.`t1` ``` 表的表结构为如下所示：

```sql
CREATE TABLE `t1` (
    `c1` int(11) NOT NULL,
    `c2` bigint(11) DEFAULT NULL,
    PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin
```

则将上述 `CREATE TABLE` 语句保存为文件（如 `db_single.t1-schema.sql`）后，执行如下命令：

{{< copyable "" >}}

```bash
binlog-schema update -s mysql-replica-01 task_single db_single t1 db_single.t1-schema.sql
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```

### 删除表结构

如需删除表结构，可使用 `binlog-schema delete` 命令：

```bash
help binlog-schema delete
```

```
delete table schema structure

Usage:
  dmctl binlog-schema delete <task-name> <database> <table> [flags]

Flags:
  -h, --help   help for delete

Global Flags:
  -s, --source strings   MySQL Source ID.
```

> **注意：**
>
> 删除 DM 内部维护的表结构后，如果后续有该表的 DDL/DML 需要复制到下游，则 DM 会依次尝试从 checkpoint 表里 `table_info` 字段、乐观 shard DDL 协调中的元信息以及下游 TiDB 中对应的该表获取表结构。

假设要删除 `db_single` 任务对应于 `mysql-replica-01` MySQL 源的 ``` `db_single`.`t1` ``` 表的表结构，则执行如下命令：

{{< copyable "" >}}

```bash
binlog-schema delete -s mysql-replica-01 task_single db_single t1
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```
