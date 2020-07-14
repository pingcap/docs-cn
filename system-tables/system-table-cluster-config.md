---
title: CLUSTER_CONFIG
summary: Learn the `CLUSTER_CONFIG` cluster configuration system table.
aliases: ['/docs/dev/system-tables/system-table-cluster-config/','/docs/dev/reference/system-databases/cluster-config/']
---

# CLUSTER_CONFIG

You can use the `CLUSTER_CONFIG` cluster configuration table to get the current configuration of all TiDB/PD/TiKV instances in the cluster. For TiDB versions earlier than 4.0, you need to access the HTTP API of each instance one by one to collect all component configurations.

{{< copyable "sql" >}}

```sql
desc information_schema.cluster_config;
```

```sql
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| TYPE     | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE | varchar(64)  | YES  |      | NULL    |       |
| KEY      | varchar(256) | YES  |      | NULL    |       |
| VALUE    | varchar(128) | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
```

Field description:

* `TYPE`: The instance type. The optional values are `tidb`, `pd`, and `tikv`.
* `INSTANCE`: The service address of the instance.
* `KEY`: The configuration item name.
* `VALUE`: The configuration item value.

The following example shows how to query the `coprocessor` configuration on the TiKV instance using the `CLUSTER_CONFIG` table:

{{< copyable "sql" >}}

```sql
select * from information_schema.cluster_config where type='tikv' and `key` like 'coprocessor%';
```

```sql
+------+-----------------+-----------------------------------+----------+
| TYPE | INSTANCE        | KEY                               | VALUE    |
+------+-----------------+-----------------------------------+----------+
| tikv | 127.0.0.1:20160 | coprocessor.batch-split-limit     | 10       |
| tikv | 127.0.0.1:20160 | coprocessor.region-max-keys       | 1.44e+06 |
| tikv | 127.0.0.1:20160 | coprocessor.region-max-size       | 144MiB   |
| tikv | 127.0.0.1:20160 | coprocessor.region-split-keys     | 960000   |
| tikv | 127.0.0.1:20160 | coprocessor.region-split-size     | 96MiB    |
| tikv | 127.0.0.1:20160 | coprocessor.split-region-on-table | false    |
+------+-----------------+-----------------------------------+----------+
```
