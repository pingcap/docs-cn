---
title: SHOW CONFIG
summary: TiDB 数据库中 SHOW CONFIG 的使用概况。
---

# SHOW CONFIG

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

`SHOW CONFIG` 语句用于展示 TiDB 各个组件当前正在应用的配置，请注意，配置与系统变量作用于不同维度，请不要混淆，如果希望获取系统变量信息，请使用 [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md) 语法。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## 示例

显示所有配置：

{{< copyable "sql" >}}

```sql
SHOW CONFIG;
```

```
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| Type | Instance       | Name                                            | Value                                                               |
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| tidb | 127.0.0.1:4000 | advertise-address                               | 127.0.0.1                                                           |
| tidb | 127.0.0.1:4000 | binlog.binlog-socket                            |                                                                     |
| tidb | 127.0.0.1:4000 | binlog.enable                                   | false                                                               |
...
120 rows in set (0.01 sec)
```

显示 `type` 是 `tidb` 的配置：

{{< copyable "sql" >}}

```sql
SHOW CONFIG WHERE type = 'tidb' AND name = 'advertise-address';
```

```
+------+----------------+-------------------+-----------+
| Type | Instance       | Name              | Value     |
+------+----------------+-------------------+-----------+
| tidb | 127.0.0.1:4000 | advertise-address | 127.0.0.1 |
+------+----------------+-------------------+-----------+
1 row in set (0.05 sec)
```

也可以用 `LIKE` 子句来显示 `type` 是 `tidb` 的配置：

{{< copyable "sql" >}}

```sql
SHOW CONFIG LIKE 'tidb';
```

```
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| Type | Instance       | Name                                            | Value                                                               |
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| tidb | 127.0.0.1:4000 | advertise-address                               | 127.0.0.1                                                           |
| tidb | 127.0.0.1:4000 | binlog.binlog-socket                            |                                                                     |
| tidb | 127.0.0.1:4000 | binlog.enable                                   | false                                                               |
...
40 rows in set (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
