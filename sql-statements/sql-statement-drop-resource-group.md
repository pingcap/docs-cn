---
title: DROP RESOURCE GROUP
summary: Learn the usage of DROP RESOURCE GROUP in TiDB.
---

# DROP RESOURCE GROUP

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

You can use the `DROP RESOURCE GROUP` statement to drop a resource group.

## Synopsis

```ebnf+diagram
DropResourceGroupStmt:
    "DROP" "RESOURCE" "GROUP" IfExists ResourceGroupName

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName:
    Identifier
```

> **Note:**
>
> The `DROP RESOURCE GROUP` statement can only be executed when the global variable [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) is set to `ON`.

## Examples

Drop a resource group named `rg1`.

```sql
mysql> DROP RESOURCE GROUP IF EXISTS rg1;
Query OK, 0 rows affected (0.22 sec)
mysql> CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+------------+-----------+
| NAME | RU_PER_SEC | BURSTABLE |
+------+------------+-----------+
| rg1  |        500 | YES       |
+------+------------+-----------+
1 row in set (0.01 sec)

mysql> DROP RESOURCE GROUP IF EXISTS rg1;
Query OK, 1 rows affected (0.09 sec)

mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
Empty set (0.00 sec)
```

## MySQL compatibility

MySQL also supports [DROP RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/drop-resource-group.html), but TiDB does not support the `FORCE` parameter.

## See also

* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru)