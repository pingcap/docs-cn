---
title: SHOW MASTER STATUS
summary: TiDB 数据库中 SHOW MASTER STATUS 的使用概况。
---

# SHOW MASTER STATUS

`SHOW MASTER STATUS` 语句用于显示集群当前最新的 TSO 信息。

## 示例

{{< copyable "sql" >}}

```sql
SHOW MASTER STATUS;
```

```sql
+-------------+--------------------+--------------+------------------+-------------------+
| File        | Position           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------+--------------------+--------------+------------------+-------------------+
| tidb-binlog | 416916363252072450 |              |                  |                   |
+-------------+--------------------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW MASTER STATUS` 语句与 MySQL 兼容，但是执行结果有差异，在 MySQL 中执行结果为 binlog 的位置信息，而在 TiDB 中为最新的 TSO 信息。

## 另请参阅

* [SHOW PUMP STATUS](/sql-statements/sql-statement-show-pump-status.md)
* [SHOW DRAINER STATUS](/sql-statements/sql-statement-show-drainer-status.md)
* [CHANGE PUMP STATUS](/sql-statements/sql-statement-change-pump.md)
* [CHANGE DRAINER STATUS](/sql-statements/sql-statement-change-drainer.md)
