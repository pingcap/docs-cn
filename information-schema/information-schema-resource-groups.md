---
title: RESOURCE_GROUPS
summary: Learn the `RESOURCE_GROUPS` information_schema table.
---

# RESOURCE_GROUPS

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [TiDB Serverless clusters](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

</CustomContent>

The `RESOURCE_GROUPS` table shows the information about all resource groups. For more information, see [Use Resource Control to Achieve Resource Isolation](/tidb-resource-control.md).

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
| PRIORITY   | varchar(6)  | YES  |      | NULL    |       |
| BURSTABLE  | varchar(3)  | YES  |      | NULL    |       |
+------------+-------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

## Examples

```sql
SELECT * FROM information_schema.resource_groups; -- View all resource groups. TiDB has a `default` resource group.
```

```sql
+---------+------------+----------+-----------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE |
+---------+------------+----------+-----------+
| default | UNLIMITED  | MEDIUM   | YES       |
+---------+------------+----------+-----------+
```

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- Create a resource group `rg1`
```

```sql
Query OK, 0 rows affected (0.34 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1; -- Show the definition of the `rg1` resource group
```

```sql
+----------------+---------------------------------------------------------------+
| Resource_Group | Create Resource Group                                         |
+----------------+---------------------------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=1000 PRIORITY="MEDIUM" |
+----------------+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg1'; -- View the resource groups `rg1`
```

```sql
+------+------------+----------+-----------+-------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT |
+------+------------+----------+-----------+-------------+
| rg1  | 1000       | MEDIUM   | NO        | NULL        |
+------+------------+----------+-----------+-------------+
1 row in set (0.00 sec)
```

The descriptions of the columns in the `RESOURCE_GROUPS` table are as follows:

* `NAME`: the name of the resource group.
* `RU_PER_SEC`: the backfilling speed of the resource group. The unit is RU/second, in which RU means [Request Unit](/tidb-resource-control.md#what-is-request-unit-ru).
* `PRIORITY`: the absolute priority of tasks to be processed on TiKV. Different resources are scheduled according to the `PRIORITY` setting. Tasks with high `PRIORITY` are scheduled first. For resource groups with the same `PRIORITY`, tasks will be scheduled proportionally according to the `RU_PER_SEC` configuration. If `PRIORITY` is not specified, the default priority is `MEDIUM`.
* `BURSTABLE`: whether to allow the resource group to overuse the available system resources.

> **Note:**
>
> TiDB automatically creates a `default` resource group during cluster initialization. For this resource group, the default value of `RU_PER_SEC` is `UNLIMITED` (equivalent to the maximum value of the `INT` type, that is, `2147483647`) and it is in `BURSTABLE` mode. All requests that are not bound to any resource group are automatically bound to this `default` resource group. When you create a new configuration for another resource group, it is recommended to modify the `default` resource group configuration as needed.
