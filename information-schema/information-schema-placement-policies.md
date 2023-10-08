---
title: PLACEMENT_POLICIES
summary: Learn the `PLACEMENT_POLICIES` information_schema table.
aliases: ['/tidb/dev/information-schema-placement-rules']
---

# PLACEMENT_POLICIES

The `PLACEMENT_POLICIES` table provides information on all placement policies. For details, refer to [Placement Rules in SQL](/placement-rules-in-sql.md).

> **Note:**
>
> This table is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC placement_policies;
```

```sql
+----------------------+---------------+------+-----+---------+-------+
| Field                | Type          | Null | Key | Default | Extra |
+----------------------+---------------+------+-----+---------+-------+
| POLICY_ID            | bigint(64)    | NO   |     | <null>  |       |
| CATALOG_NAME         | varchar(512)  | NO   |     | <null>  |       |
| POLICY_NAME          | varchar(64)   | NO   |     | <null>  |       |
| PRIMARY_REGION       | varchar(1024) | YES  |     | <null>  |       |
| REGIONS              | varchar(1024) | YES  |     | <null>  |       |
| CONSTRAINTS          | varchar(1024) | YES  |     | <null>  |       |
| LEADER_CONSTRAINTS   | varchar(1024) | YES  |     | <null>  |       |
| FOLLOWER_CONSTRAINTS | varchar(1024) | YES  |     | <null>  |       |
| LEARNER_CONSTRAINTS  | varchar(1024) | YES  |     | <null>  |       |
| SCHEDULE             | varchar(20)   | YES  |     | <null>  |       |
| FOLLOWERS            | bigint(64)    | YES  |     | <null>  |       |
| LEARNERS             | bigint(64)    | YES  |     | <null>  |       |
+----------------------+---------------+------+-----+---------+-------+
12 rows in set (0.00 sec)
```

## Examples

The `PLACEMENT_POLICIES` table only shows all placement policies. To view the canonical version of placement rules (including all placement policies and objects assigned placement policies), use the statement `SHOW PLACEMENT` instead:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT); 
CREATE PLACEMENT POLICY p1 primary_region="us-east-1" regions="us-east-1";
CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;
SHOW PLACEMENT; -- Shows all information, including table t3.
SELECT * FROM information_schema.placement_policies; -- Only shows placement policies, excluding t3.
```

```sql
Query OK, 0 rows affected (0.09 sec)

Query OK, 0 rows affected (0.11 sec)

Query OK, 0 rows affected (0.08 sec)

+---------------+------------------------------------------------+------------------+
| Target        | Placement                                      | Scheduling_State |
+---------------+------------------------------------------------+------------------+
| POLICY p1     | PRIMARY_REGION="us-east-1" REGIONS="us-east-1" | NULL             |
| TABLE test.t3 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1" | PENDING          |
+---------------+------------------------------------------------+------------------+
2 rows in set (0.00 sec)

+-----------+--------------+-------------+----------------+-----------+-------------+--------------------+----------------------+---------------------+----------+-----------+----------+
| POLICY_ID | CATALOG_NAME | POLICY_NAME | PRIMARY_REGION | REGIONS   | CONSTRAINTS | LEADER_CONSTRAINTS | FOLLOWER_CONSTRAINTS | LEARNER_CONSTRAINTS | SCHEDULE | FOLLOWERS | LEARNERS |
+-----------+--------------+-------------+----------------+-----------+-------------+--------------------+----------------------+---------------------+----------+-----------+----------+
| 1         | def          | p1          | us-east-1      | us-east-1 |             |                    |                      |                     |          | 2         | 0        |
+-----------+--------------+-------------+----------------+-----------+-------------+--------------------+----------------------+---------------------+----------+-----------+----------+
1 rows in set (0.00 sec)
```
