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
+------------+-------------+------+------+---------+-------+
| Field      | Type        | Null | Key  | Default | Extra |
+------------+-------------+------+------+---------+-------+
| NAME       | varchar(32) | NO   |      | NULL    |       |
| RU_PER_SEC | bigint(21)  | YES  |      | NULL    |       |
| RU_TOKENS  | bigint(21)  | YES  |      | NULL    |       |
| BURSTABLE  | varchar(3)  | YES  |      | NULL    |       |
+------------+-------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

## 示例

{{< copyable "sql" >}}

```sql
mysql> CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- 创建资源组 rg1
Query OK, 0 rows affected (0.34 sec)
mysql> SHOW CREATE RESOURCE GROUP rg1; -- 显示 rg1 资源组的定义。
+----------------+---------------------------------------------+
| Resource_Group | Create Resource Group                       |
+----------------+---------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=1000 |
+----------------+---------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg1';
+------+------------+-----------+-----------+
| NAME | RU_PER_SEC | RU_TOKENS | BURSTABLE |
+------+------------+-----------+-----------+
| rg1  |       1000 |    100000 | NO        |
+------+------------+-----------+-----------+
1 row in set (0.00 sec)
```
