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

- `global`：表示集群内全域数据的范围
- `meta`：表示 TiDB 内部存储的元信息的数据范围

## 示例

```sql
CREATE PLACEMENT POLICY `deploy111` CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 1, "+region=us-west-1": 1}';
CREATE PLACEMENT POLICY `five_replicas` FOLLOWERS=4;

ALTER RANGE global PLACEMENT POLICY = "deploy111";
ALTER RANGE meta PLACEMENT POLICY = "five_replicas";
```

上述示例创建了一个名为 `deploy111` 和 `five_replicas` 的放置策略，为不同的区域指定了约束条件。然后将 `deploy111` 放置策略应用到了整个集群范围内的数据，将 `five_replicas` 放置策略应用到元数据范围内。