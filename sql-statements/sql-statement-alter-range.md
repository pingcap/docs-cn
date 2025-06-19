---
title: ALTER RANGE
summary: TiDB 中 ALTER RANGE 的使用概述。
---

# ALTER RANGE

目前，`ALTER RANGE` 语句只能用于修改 TiDB 中特定放置策略的范围。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法图

```ebnf+diagram
AlterRangeStmt ::=
    'ALTER' 'RANGE' Identifier PlacementPolicyOption
```

`ALTER RANGE` 支持以下两个参数：

- `global`：表示集群中所有数据的范围。
- `meta`：表示存储在 TiDB 中的内部元数据的范围。

## 示例

```sql
CREATE PLACEMENT POLICY `deploy111` CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 1, "+region=us-west-1": 1}';
CREATE PLACEMENT POLICY `five_replicas` FOLLOWERS=4;

ALTER RANGE global PLACEMENT POLICY = "deploy111";
ALTER RANGE meta PLACEMENT POLICY = "five_replicas";
```

上述示例创建了两个放置策略（`deploy111` 和 `five_replicas`），为不同区域指定了约束条件，然后将 `deploy111` 放置策略应用于集群范围内的所有数据，将 `five_replicas` 放置策略应用于元数据范围。
