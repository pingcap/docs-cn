---
title: CALIBRATE RESOURCE
summary: An overview of the usage of CALIBRATE RESOURCE for the TiDB database.
---

# `CALIBRATE RESOURCE`

The `CALIBRATE RESOURCE` statement is used to estimate and output the ['Request Unit (RU)`](/tidb-resource-control#what-is-request-unit-ru) capacity of the current cluster.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

## Synopsis

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE'
```

## Examples

```sql
CALIBRATE RESOURCE;
+-------+
| QUOTA |
+-------+
| 68569 |
+-------+
1 row in set (0.03 sec)
```

> *Note:**
>
> The RU capacity of a cluster varies with the topology of the cluster and the hardware and software configuration of each component. The actual RU that each cluster consumes is also related to the actual workload. This estimation is for reference only and might have some deviation from the actual maximum value.
