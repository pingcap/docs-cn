---
title: SHOW DRAINER STATUS
summary: TiDB 数据库中 SHOW DRAINER STATUS 的使用概况。
---

# SHOW DRAINER STATUS

`SHOW DRAINER STATUS` 语句用于显示集群中所有 Drainer 的状态信息。

## 示例

{{< copyable "sql" >}}

```sql
SHOW DRAINER STATUS;
```

```sql
+----------|----------------|--------|--------------------|---------------------|
|  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+----------|----------------|--------|--------------------|---------------------|
| drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
+----------|----------------|--------|--------------------|---------------------|
| drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
+----------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [SHOW PUMP STATUS](/sql-statements/sql-statement-show-pump-status.md)
* [CHANGE PUMP STATUS](/sql-statements/sql-statement-change-pump.md)
* [CHANGE DRAINER STATUS](/sql-statements/sql-statement-change-drainer.md)
