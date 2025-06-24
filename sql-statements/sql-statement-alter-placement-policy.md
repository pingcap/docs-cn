---
title: ALTER PLACEMENT POLICY
summary: TiDB 中 ALTER PLACEMENT POLICY 的使用方法。
---

# ALTER PLACEMENT POLICY

`ALTER PLACEMENT POLICY` 用于修改先前创建的放置策略。使用该放置策略的所有表和分区都将自动更新。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

`ALTER PLACEMENT POLICY` 用新定义_替换_之前的策略。它不会将旧策略与新策略_合并_。在以下示例中，执行 `ALTER PLACEMENT POLICY` 时，`FOLLOWERS=4` 会丢失：

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=4;
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

## 语法

```ebnf+diagram
AlterPolicyStmt ::=
    "ALTER" "PLACEMENT" "POLICY" IfExists PolicyName PlacementOptionList

PolicyName ::=
    Identifier

PlacementOptionList ::=
    PlacementOption
|   PlacementOptionList PlacementOption
|   PlacementOptionList ',' PlacementOption

PlacementOption ::=
    CommonPlacementOption
|   SugarPlacementOption
|   AdvancedPlacementOption

CommonPlacementOption ::=
    "FOLLOWERS" EqOpt LengthNum

SugarPlacementOption ::=
    "PRIMARY_REGION" EqOpt stringLit
|   "REGIONS" EqOpt stringLit
|   "SCHEDULE" EqOpt stringLit

AdvancedPlacementOption ::=
    "LEARNERS" EqOpt LengthNum
|   "CONSTRAINTS" EqOpt stringLit
|   "LEADER_CONSTRAINTS" EqOpt stringLit
|   "FOLLOWER_CONSTRAINTS" EqOpt stringLit
|   "LEARNER_CONSTRAINTS" EqOpt stringLit
|   "SURVIVAL_PREFERENCES" EqOpt stringLit
```

## 示例

> **注意：**
>
> 要了解集群中有哪些可用区域，请参见 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)。
>
> 如果你没有看到任何可用区域，你的 TiKV 安装可能没有正确设置标签。

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE TABLE t1 (i INT) PLACEMENT POLICY=p1; -- 将策略 p1 分配给表 t1
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4; -- t1 的规则将自动更新。
SHOW CREATE PLACEMENT POLICY p1\G
```

```
Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.10 sec)

***************************[ 1. row ]***************************
Policy        | p1
Create Policy | CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [SQL 中的放置规则](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
* [DROP PLACEMENT POLICY](/sql-statements/sql-statement-drop-placement-policy.md)
