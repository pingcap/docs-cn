---
title: SHOW MASTER STATUS
summary: TiDB 数据库中 SHOW MASTER STATUS 的使用概述。
---

# SHOW MASTER STATUS

`SHOW MASTER STATUS` 语句显示集群中的最新 TSO。

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

`SHOW MASTER STATUS` 的输出格式设计为与 MySQL 匹配。但是，执行结果不同，MySQL 的结果是 binlog 位置信息，而 TiDB 的结果是最新的 TSO 信息。

`SHOW BINARY LOG STATUS` 语句作为 `SHOW MASTER STATUS` 的别名被添加到 TiDB 中，而 `SHOW MASTER STATUS` 在 MySQL 8.2.0 及更新版本中已被弃用。

## 另请参阅

<CustomContent platform="tidb">

* [SHOW PUMP STATUS](/sql-statements/sql-statement-show-pump-status.md)
* [SHOW DRAINER STATUS](/sql-statements/sql-statement-show-drainer-status.md)
* [CHANGE PUMP STATUS](/sql-statements/sql-statement-change-pump.md)
* [CHANGE DRAINER STATUS](/sql-statements/sql-statement-change-drainer.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md)

</CustomContent>
