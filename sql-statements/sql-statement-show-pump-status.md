---
title: SHOW PUMP STATUS
summary: TiDB 数据库中 SHOW PUMP STATUS 的使用概况。
---

# SHOW PUMP STATUS

`SHOW PUMP STATUS` 语句用于显示集群中所有 Pump 的状态信息。

## 示例

{{< copyable "sql" >}}

```sql
SHOW PUMP STATUS;
```

```sql
+--------|----------------|--------|--------------------|---------------------|
| NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+--------|----------------|--------|--------------------|---------------------|
| pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
+--------|----------------|--------|--------------------|---------------------|
| pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
+--------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [SHOW DRAINER STATUS](/sql-statements/sql-statement-show-drainer-status.md)
* [CHANGE PUMP STATUS](/sql-statements/sql-statement-change-pump.md)
* [CHANGE DRAINER STATUS](/sql-statements/sql-statement-change-drainer.md)
