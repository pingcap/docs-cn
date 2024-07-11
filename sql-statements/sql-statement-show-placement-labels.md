---
title: SHOW PLACEMENT LABELS
summary: TiDB 数据库中 SHOW PLACEMENT LABELS 的使用概况。
---

# SHOW PLACEMENT LABELS

`SHOW PLACEMENT LABELS` 汇总可用于放置规则 (Placement Rules) 的标签 (label) 和值。

## 语法图

```ebnf+diagram
ShowStmt ::=
    "SHOW" "PLACEMENT" "LABELS" ShowLikeOrWhere?
```

## 示例

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
