---
title: ALTER RANGE
summary: An overview of the usage of ALTER RANGE for TiDB.
---

# ALTER RANGE

Currently, the `ALTER RANGE` statement can only be used to modify the range of a specific placement policy in TiDB.

> **Note:**
>
> This feature is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

## Synopsis

```ebnf+diagram
AlterRangeStmt ::=
    'ALTER' 'RANGE' Identifier PlacementPolicyOption
```

`ALTER RANGE` supports the following two parameters:

- `global`: indicates the range of all data in a cluster.
- `meta`: indicates the range of internal metadata stored in TiDB.

## Examples

```sql
CREATE PLACEMENT POLICY `deploy111` CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 1, "+region=us-west-1": 1}';
CREATE PLACEMENT POLICY `five_replicas` FOLLOWERS=4;

ALTER RANGE global PLACEMENT POLICY = "deploy111";
ALTER RANGE meta PLACEMENT POLICY = "five_replicas";
```

The preceding example creates two placement policies (`deploy111` and `five_replicas`), specifies constraints for different regions, and then applies the `deploy111` placement policy to all data in the cluster range and the `five_replicas` placement policy to the metadata range.