---
title: SHOW PLACEMENT
summary: TiDB 中 SHOW PLACEMENT 的使用。
---

# SHOW PLACEMENT

`SHOW PLACEMENT` 汇总了来自放置策略的所有放置选项，并以规范形式呈现它们。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

该语句返回一个结果集，其中 `Scheduling_State` 字段指示 Placement Driver (PD) 在调度放置时的当前进度：

* `PENDING`：PD 尚未开始调度放置。这可能表明放置规则在语义上是正确的，但当前集群无法满足。例如，如果设置 `FOLLOWERS=4` 但只有 3 个 TiKV 存储节点可作为从节点的候选者。
* `INPROGRESS`：PD 当前正在调度放置。
* `SCHEDULED`：PD 已成功调度放置。

## 语法图

```ebnf+diagram
ShowStmt ::=
    "SHOW" "PLACEMENT" ShowLikeOrWhere?
```

## 示例

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

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [SQL 中的放置规则](/placement-rules-in-sql.md)
* [SHOW PLACEMENT FOR](/sql-statements/sql-statement-show-placement-for.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
