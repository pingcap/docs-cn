---
title: RESOURCE_GROUPS
summary: Learn the `RESOURCE_GROUPS` information_schema table.
---

# RESOURCE_GROUPS

> **Warning:**
>
> This feature is experimental and its form and usage might change in subsequent versions.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

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
CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- Create the resource group rg1
```

```sql
Query OK, 0 rows affected (0.34 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1; -- Display the definition of the rg1 resource group
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
SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg1';
```

```sql
+------+------------+----------+-----------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE |
+------+------------+----------+-----------+
| rg1  |       1000 | MEDIUM   | NO        |
+------+------------+----------+-----------+
1 row in set (0.00 sec)
```

The descriptions of the columns in the `RESOURCE_GROUPS` table are as follows:

* `NAME`: the name of the resource group.
* `RU_PER_SEC`：the backfilling speed of the resource group. The unit is RU/second, in which RU means [Request Unit](/tidb-resource-control.md#what-is-request-unit-ru).
* `PRIORITY`: the absolute priority of tasks to be processed on TiKV. Different resources are scheduled according to the `PRIORITY` setting. Tasks with high `PRIORITY` are scheduled first. For resource groups with the same `PRIORITY`, tasks will be scheduled proportionally according to the `RU_PER_SEC` configuration. If `PRIORITY` is not specified, the default priority is `MEDIUM`.
* `BURSTABLE`: whether to allow the resource group to overuse the available system resources.
