---
title: SHOW CREATE RESOURCE GROUP
summary: Learn the usage of SHOW CREATE RESOURCE GROUP in TiDB.
---

# SHOW CREATE RESOURCE GROUP

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

You can use the `SHOW CREATE RESOURCE GROUP` statement to view the current definition of a resource group.

## Synopsis

```ebnf+diagram
ShowCreateResourceGroupStmt ::=
    "SHOW" "CREATE" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
```

## Examples

Create a resource group `rg1`.

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=100;
Query OK, 0 rows affected (0.10 sec)
```

View the definition of `rg1`.

```sql
SHOW CREATE RESOURCE GROUP rg1;
***************************[ 1. row ]***************************
+----------------+--------------------------------------------+
| Resource_Group | Create Resource Group                      |
+----------------+--------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=100 |
+----------------+--------------------------------------------+
1 row in set (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension for MySQL.

## See also

* [TiDB RESOURCE CONTROL](/tidb-resource-control.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
