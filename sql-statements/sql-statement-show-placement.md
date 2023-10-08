---
title: SHOW PLACEMENT
summary: The usage of SHOW PLACEMENT in TiDB.
---

# SHOW PLACEMENT

`SHOW PLACEMENT` summarizes all placement options from placement policies, and presents them in canonical form.

> **Note:**
>
> This feature is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

The statement returns a result set in which the `Scheduling_State` field indicates the current progress that the Placement Driver (PD) has made in scheduling the placement:

* `PENDING`: The PD has not yet started scheduling the placement. This might indicate that that the placement rules are semantically correct, but cannot currently be satisfied by the cluster. For example, if `FOLLOWERS=4` but there are only 3 TiKV stores which are candidates for followers.
* `INPROGRESS`: The PD is currently scheduling the placement.
* `SCHEDULED`: The PD has successfully scheduled the placement.

## Synopsis

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT"
```

## Examples

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW PLACEMENT;
```

```
Query OK, 0 rows affected (0.01 sec)

Query OK, 0 rows affected (0.00 sec)

+---------------+----------------------------------------------------------------------+------------------+
| Target        | Placement                                                            | Scheduling_State |
+---------------+----------------------------------------------------------------------+------------------+
| POLICY p1     | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | NULL             |
| DATABASE test | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
| TABLE test.t1 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+---------------+----------------------------------------------------------------------+------------------+
4 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT FOR](/sql-statements/sql-statement-show-placement-for.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
