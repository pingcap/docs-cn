---
title: ALTER PLACEMENT POLICY
summary: TiDB 数据库中 ALTER PLACEMENT POLICY 的使用概况。
---

# ALTER PLACEMENT POLICY

> **警告：**
>
> Placement Rules in SQL 是 TiDB 在 v5.3.0 中引入的实验特性，其语法在 GA 前可能会发生变化，还可能存在 bug。如果你知晓潜在的风险，可通过执行 `SET GLOBAL tidb_enable_alter_placement = 1;` 来开启该实验特性。

`ALTER PLACEMENT POLICY` 用于修改已创建的放置策略。此修改会自动更新至所有使用这些放置策略的表和分区。

## 语法图

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

## 示例

> **注意：**
>
> 如要查看所在集群中可用的区域，见 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)。如果未看到任何可用的区域，此 TiKV 集群在部署时可能未正确设置标签 (label)。

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

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
* [DROP PLACEMENT POLICY](/sql-statements/sql-statement-drop-placement-policy.md)
