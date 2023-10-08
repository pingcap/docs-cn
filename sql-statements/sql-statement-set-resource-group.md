---
title: SET RESOURCE GROUP
summary: An overview of the usage of SET RESOURCE GROUP in the TiDB database.
---

# SET RESOURCE GROUP

`SET RESOURCE GROUP` is used to set the resource group for the current session.

> **Note:**
>
> This feature is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

## Synopsis

**SetResourceGroupStmt:**

```ebnf+diagram
SetResourceGroupStmt ::=
    "SET" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

## Examples

Create a user `user1`, create two resource groups `rg1` and `rg2`, and bind the user `user1` to the resource group `rg1`.

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

Use `user1` to log in and view the resource group bound to the current user.

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg1                      |
+--------------------------+
1 row in set (0.00 sec)
```

Execute `SET RESOURCE GROUP` to set the resource group for the current session to `rg2`.

```sql
SET RESOURCE GROUP `rg2`;
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg2                      |
+--------------------------+
1 row in set (0.00 sec)
```

Execute `SET RESOURCE GROUP` to specify the current session to use the default resource group.

```sql
SET RESOURCE GROUP `default`;
SELECT CURRENT_RESOURCE_GROUP();
```

```sql
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| default                  |
+--------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

MySQL also supports [SET RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/set-resource-group.html). But the accepted parameters are different from that of TiDB. They are not compatible.

## See also

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [Resource Control](/tidb-resource-control.md)