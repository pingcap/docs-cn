---
title: SHOW BACKUP METADATA
summary: TiDB 数据库中 SHOW BACKUP METADATA 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-backup-metadata']
---

# SHOW BACKUP METADATA

> **警告：**
>
> TiDB SHOW BACKUP METADATA 语句在 v7.1.0 是实验特性，其语法或者行为表现在 GA 前可能会发生变化。


`SHOW BACKUP METADATA` 语句会打印出指定备份存储地址([备份存储 URI 格式](/br/backup-and-restore-storages.md#uri-格式))
备份文件中涉及到的数据库对象的元数据信息。

执行 `SHOW BACKUP METADATA` 任务时需要 `BACKUP_ADMIN` 或 `SUPER` 权限。

## 语法图

```ebnf+diagram
ShowBackupMetaStmt ::=
    "SHOW" "BACKUP" "METADATA" "FROM" stringLit
```

## 示例

{{< copyable "sql" >}}

```sql
SHOW BACKUP METADATA FROM 's3://example-bucket/backup-01/';
```

```sql
+----------+------------+-----------+-------------+---------------------+---------------------+
| Database | Table      | Total_kvs | Total_bytes | Time_range_start    | Time_range_end      |
+----------+------------+-----------+-------------+---------------------+---------------------+
| tpcc     | warehouse  | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | district   | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | stock      | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | orders     | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | customer   | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | new_order  | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | item       | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | history    | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
| tpcc     | order_line | 0         | 0           | 1970-01-01 08:00:00 | 2023-04-10 11:18:21 |
+----------+------------+-----------+-------------+---------------------+---------------------+
9 rows in set (0.00 sec)
```

输出结果的第一行描述如下：

| 列名               | 描述                  |
|:-----------------|:--------------------|
| `Database`       | 该备份对应的数据库名          |
| `Table`          | 该备份对应的表名            |
| `Total_kvs`       | 此表在本备份中的 kv 总数      |
| `Total_bytes`     | 此表在本备份中的总字节数        |
| `Time_range_start` | 此表在被本次备份中涉及的最老的改动时间 |
| `Time_range_end `    | 此表在被本次备份中涉及的最新的改动时间 |

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [RESTORE](/sql-statements/sql-statement-restore.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)
* [PITR](/sql-statements/sql-statement-pitr.md)
* [BR_JOB_ADMIN](/sql-statements/sql-statement-br-job-admin.md)
