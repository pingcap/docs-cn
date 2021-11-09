---
title: ALTER PLACEMENT POLICY
summary: The usage of ALTER PLACEMENT POLICY in TiDB.
---

# ALTER PLACEMENT POLICY

> **Warning:**
>
> Placement Rules in SQL is an experimental feature. The syntax might change before its GA, and there might also be bugs.
>
> If you understand the risks, you can enable this experiment feature by executing `SET GLOBAL tidb_enable_alter_placement = 1;`.

`ALTER PLACEMENT POLICY` is used to modify existing placement policies that have previously been created. All the tables and partitions which use the placement policy will automatically be updated.

## Synopsis

```ebnf+diagram
AlterPolicyStmt ::=
    "ALTER" "PLACEMENT" "POLICY" IfExists PolicyName PlacementOptionList

PolicyName ::=
    Identifier

PlacementOptionList ::=
    DirectPlacementOption
|   PlacementOptionList DirectPlacementOption
|   PlacementOptionList ',' DirectPlacementOption

DirectPlacementOption ::=
    "PRIMARY_REGION" EqOpt stringLit
|   "REGIONS" EqOpt stringLit
|   "FOLLOWERS" EqOpt LengthNum
|   "VOTERS" EqOpt LengthNum
|   "LEARNERS" EqOpt LengthNum
|   "SCHEDULE" EqOpt stringLit
|   "CONSTRAINTS" EqOpt stringLit
|   "LEADER_CONSTRAINTS" EqOpt stringLit
|   "FOLLOWER_CONSTRAINTS" EqOpt stringLit
|   "VOTER_CONSTRAINTS" EqOpt stringLit
|   "LEARNER_CONSTRAINTS" EqOpt stringLit
```

## Examples

> **Note:**
>
> To know which regions are available in your cluster, see [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md).
>
> If you do not see any available regions, your TiKV installation might not have labels set correctly.

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4;
SHOW CREATE PLACEMENT POLICY p1\G
```

```
Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.10 sec)

*************************** 1. row ***************************
       Policy: p1
Create Policy: CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
* [DROP PLACEMENT POLICY](/sql-statements/sql-statement-drop-placement-policy.md)