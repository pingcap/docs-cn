---
title: ALTER RANGE
summary: TiDB 数据库中 ALTER RANGE 的使用概况。
---

# ALTER RANGE

`ALTER RANGE` 语句目前仅用于修改 TiDB 数据库中指定范围的放置策略。

## 语法图

```ebnf+diagram
AlterRangeStmt ::=
    'ALTER' 'RANGE' Identifier PlacementPolicyOption
```

目前 `ALTER RANGE` 能起作用的有 `global` 和 `meta` 两个参数：

- `global`: 表示集群内全域数据的范围
- `meta`: 表示 TiDB 内部存储的元信息的数据范围

## 示例

```sql
CREATE PLACEMENT POLICY `deploy221` CONSTRAINTS='{"+region=us-east-1":2, "+region=us-east-2": 2, "+region=us-west-1": 1}';

ALTER RANGE global PLACEMENT POLICY = "deploy221";
```

上述示例创建了一个名为 `deploy221` 的放置策略，为不同的区域指定了约束条件。然后，将该放置策略应用到了整个集群范围内的数据。