---
title: SHOW PROFILES
summary: TiDB 数据库中 SHOW PROFILES 的使用概况。
---

# SHOW PROFILES

`SHOW PROFILES` 语句目前只会返回空结果。

## 语法图

```ebnf+diagram
ShowProfilesStmt ::=
    "SHOW" "PROFILES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW PROFILES
```

```
Empty set (0.00 sec)
```

## MySQL 兼容性

该语句仅与 MySQL 兼容，无其他作用。执行 `SHOW PROFILES` 始终返回空结果。

作为替代方案，TiDB 提供了 [Statement Summary Tables](/statement-summary-tables.md)，以帮助理解 SQL 性能问题。