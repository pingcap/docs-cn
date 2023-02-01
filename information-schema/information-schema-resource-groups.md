---
title: RESOURCE_GROUPS
summary: 了解 information_schema 表 `RESOURCE_GROUPS`。
---

`RESOURCE_GROUPS` 表展示所有资源组 (resource group) 的信息，见[使用资源管控 (Resource Control) 实现资源隔离](/tidb-resource-control.md)。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC resource_groups;
```

```sql
+-----------------+-------------+------+------+---------+-------+
| Field           | Type        | Null | Key  | Default | Extra |
+-----------------+-------------+------+------+---------+-------+
| NAME            | varchar(32) | NO   |      | NULL    |       |
| MODE            | varchar(12) | NO   |      | NULL    |       |
| RRU             | bigint(21)  | YES  |      | NULL    |       |
| RRU_TOKEN       | bigint(21)  | YES  |      | NULL    |       |
| WRU             | bigint(21)  | YES  |      | NULL    |       |
| WRU_TOKEN       | bigint(21)  | YES  |      | NULL    |       |
| CPU             | bigint(21)  | YES  |      | NULL    |       |
| READ_BANDWIDTH  | bigint(21)  | YES  |      | NULL    |       |
| WRITE_BANDWIDTH | bigint(21)  | YES  |      | NULL    |       |
+-----------------+-------------+------+------+---------+-------+
9 rows in set (0.08 sec)
```

## 示例

{{< copyable "sql" >}}

```sql
mysql> CREATE RESOURCE GROUP my_rg1 RRU_PER_SEC=1000 WRU_PER_SEC=2000 ; -- 使用 RU_MODE 创建资源组 my_rg1
Query OK, 0 rows affected (0.34 sec)
mysql> SHOW CREATE RESOURCE GROUP my_rg1; -- 显示 my_rg1 资源组的定义。
+----------------+------------------------------------------------------------------+
| Resource_Group | Create Resource Group                                            |
+----------------+------------------------------------------------------------------+
| my_rg1         | CREATE RESOURCE GROUP `my_rg1` RRU_PER_SEC=1000 WRU_PER_SEC=2000 |
+----------------+------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT * FROM information_schema.placement_policies WHERE NAME = 'my_rg1'; -- 显示资源组 my_rg1 运行时状态。
+--------+---------+------+-----------+------+-----------+------+----------------+-----------------+
| NAME   | MODE    | RRU  | RRU_TOKEN | WRU  | WRU_TOKEN | CPU  | READ_BANDWIDTH | WRITE_BANDWIDTH |
+--------+---------+------+-----------+------+-----------+------+----------------+-----------------+
| my_rg1 | RU_MODE | 1000 |    168999 | 2000 |    249999 | NULL |           NULL |            NULL |
+--------+---------+------+-----------+------+-----------+------+----------------+-----------------+
1 row in set (0.02 sec)
```

```sql
mysql> CREATE RESOURCE GROUP my_rg2 CPU="8" IO_READ_BANDWIDTH="1000Mi" IO_WRITE_BANDWIDTH="1000Mi"; -- 使用 RAW_MODE 创建资源组 my_rg2
Query OK, 0 rows affected (0.20 sec)
mysql> show create resource group my_rg2; -- 显示 my_rg2 资源组的定义。
+----------------+-----------------------------------------------------------------------------------------------+
| Resource_Group | Create Resource Group                                                                         |
+----------------+-----------------------------------------------------------------------------------------------+
| my_rg2         | CREATE RESOURCE GROUP `my_rg2` CPU="8" IO_READ_BANDWIDTH="1000Mi" IO_WRITE_BANDWIDTH="1000Mi" |
+----------------+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME = 'my_rg2'; -- 显示资源组 my_rg2 运行时状态。
+--------+----------+------+-----------+------+-----------+------+----------------+-----------------+
| NAME   | MODE     | RRU  | RRU_TOKEN | WRU  | WRU_TOKEN | CPU  | READ_BANDWIDTH | WRITE_BANDWIDTH |
+--------+----------+------+-----------+------+-----------+------+----------------+-----------------+
| my_rg2 | RAW_MODE | NULL |      NULL | NULL |      NULL | 8000 |     1048576000 |      1048576000 |
+--------+----------+------+-----------+------+-----------+------+----------------+-----------------+
1 row in set (0.00 sec)
```
