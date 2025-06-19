---
title: DROP RESOURCE GROUP
summary: 了解在 TiDB 中 DROP RESOURCE GROUP 的用法。
---

# DROP RESOURCE GROUP

你可以使用 `DROP RESOURCE GROUP` 语句删除资源组。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法概要

```ebnf+diagram
DropResourceGroupStmt ::=
    "DROP" "RESOURCE" "GROUP" IfExists ResourceGroupName

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

> **注意：**
>
> - 只有当全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 设置为 `ON` 时，才能执行 `DROP RESOURCE GROUP` 语句。
> - `default` 资源组是保留的，不能被删除。

## 示例

删除名为 `rg1` 的资源组。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+-------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT |
+------+------------+----------+-----------+-------------+
| rg1  | 500        | MEDIUM   | YES       | NULL        |
+------+------------+----------+-----------+-------------+
1 row in set (0.01 sec)
```

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 1 rows affected (0.09 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
Empty set (0.00 sec)
```

## MySQL 兼容性

MySQL 也支持 [DROP RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/drop-resource-group.html)，但 TiDB 不支持 `FORCE` 参数。

## 另请参阅

* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [请求单元 (RU)](/tidb-resource-control.md#what-is-request-unit-ru)
