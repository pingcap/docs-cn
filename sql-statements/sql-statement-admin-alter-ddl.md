---
title: ADMIN ALTER DDL JOBS
summary: TiDB 数据库中 `ADMIN ALTER DDL JOBS` 的使用概况。
---

# ADMIN ALTER DDL JOBS

`ADMIN ALTER DDL JOBS` 语句可用于修改单个正在运行的 DDL 作业相关的参数。例如：

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
```

其中 `101` 表示 DDL 作业的 ID，该 ID 可以通过查询 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 获得。`THREAD` 表示当前 DDL 作业的并发度，其初始值由系统变量 [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt) 设置。

目前支持 `ADMIN ALTER DDL JOBS` 的 DDL 作业类型包括：`ADD INDEX`、`MODIFY COLUMN` 和 `REORGANIZE PARTITION`。对于其他 DDL 作业类型，执行 `ADMIN ALTER DDL JOBS` 会报 `unsupported DDL operation` 的错误。

以下是不同 DDL 作业类型支持的各项参数，以及它们对应的系统变量：

- `ADD INDEX`: 
    - `THREAD`: 并发度，初始值由系统变量 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`: 批大小，初始值由系统变量 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size) 设置。
    - `MAX_WRITE_SPEED`: 向每个 TiKV 导入索引记录时的最大带宽限制，初始值由系统变量 [`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-从-v850-版本开始引入) 设置。

- `MODIFY COLUMN`:
    - `THREAD`: 并发度，初始值由系统变量 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`: 批大小，初始值由系统变量 `tidb_ddl_reorg_batch_size` 设置。

- `REORGANIZE PARTITION`:
    - `THREAD`: 并发度，初始值由系统变量 `tidb_ddl_reorg_worker_cnt` 设置。
    - `BATCH_SIZE`: 批大小，初始值由系统变量 `tidb_ddl_reorg_batch_size` 设置。

参数的取值范围和系统变量的保持一致。

`ADMIN ALTER DDL JOBS` 仅对正在运行的 DDL 作业生效。如果 DDL 作业不存在或者已经结束，执行该语句会报 `ddl job ? is not running` 的错误。

以下是部分语句示例：

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
ADMIN ALTER DDL JOBS 101 BATCH_SIZE = 256;
ADMIN ALTER DDL JOBS 101 MAX_WRITE_SPEED = '200MiB';
ADMIN ALTER DDL JOBS 101 THREAD = 8, BATCH_SIZE = 256;
```

要查看某个 DDL 作业当前的参数值，可以执行 `ADMIN SHOW DDL JOBS`，结果显示在 `COMMENTS` 列：

```sql
mysql> admin show ddl jobs 1;
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE  | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE  | COMMENTS              |
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
|    124 | test    | t          | add index | public       |         2 |      122 |         3 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:08.363000 | synced | ingest, DXF, thread=8 |
+--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
1 row in set (0.01 sec)
```

## 语法图

```ebnf+diagram
AdminPauseDDLStmt ::=
    'ADMIN' 'ALTER' 'DDL' 'JOBS' Int64Num AlterJobOptionList

AlterJobOptionList ::=
    AlterJobOption ( ',' AlterJobOption )*

AlterJobOption ::=
    identifier "=" SignedLiteral
```

## MySQL 兼容性

`ADMIN ALTER DDL JOBS` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)