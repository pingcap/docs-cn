---
title: SHOW PLACEMENT LABELS
summary: TiDB 数据库中 SHOW PLACEMENT LABELS 的使用概况。
---

# SHOW PLACEMENT LABELS

> **警告：**
>
> Placement Rules in SQL 是 TiDB 在 v5.3.0 中引入的实验特性，其语法在 GA 前可能会发生变化，还可能存在 bug。如果你知晓潜在的风险，可通过执行 `SET GLOBAL tidb_enable_alter_placement = 1;` 来开启该实验特性。

`SHOW PLACEMENT LABELS` 汇总可用于放置规则 (Placement Rules) 的标签 (label) 和值。

## 语法图

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT" "LABELS"
```

## 示例

{{< copyable "sql" >}}

```sql
SHOW PLACEMENT LABELS;
```

```sql
+--------+----------------+
| Key    | Values         |
+--------+----------------+
| region | ["us-east-1"]  |
| zone   | ["us-east-1a"] |
+--------+----------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
