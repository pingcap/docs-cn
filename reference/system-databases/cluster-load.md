---
title: CLUSTER_LOAD
summary: Learn the `CLUSTER_LOAD` cluster load table.
category: reference
---

# CLUSTER_LOAD

The `CLUSTER_LOAD` cluster load table provides the current load information of the server where each instance of the TiDB cluster is located.

{{< copyable "sql" >}}

```sql
desc cluster_load;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE    | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| DEVICE_NAME | varchar(64)  | YES  |      | NULL    |       |
| NAME        | varchar(256) | YES  |      | NULL    |       |
| VALUE       | varchar(128) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
```

Field description:

* `TYPE`: Corresponds to the `TYPE` field in the [`information_schema.cluster_info`](/reference/system-databases/cluster-info.md) table. The optional values are `tidb`, `pd`, and `tikv`.
* `INSTANCE`: Corresponds to the `INSTANCE` field in the [`information_schema.cluster_info`](/reference/system-databases/cluster-info.md) cluster information table.
* `DEVICE_TYPE`: Hardware type. Currently, you can query the `cpu`, `memory`, `disk`, and `net` types.
* `DEVICE_NAME`: Hardware name. The value of `DEVICE_NAME` varies with `DEVICE_TYPE`.
    * `cpu`: The hardware name is cpu.
    * `disk`: The disk name.
    * `net`: The network card name.
    * `memory`: The hardware name is memory.
* `NAME`: Different load types. For example, cpu has three load types: `load1`, `load5`, and `load15`, which respectively mean the average load of cpu within 1 minute, 5 minutes, and 15 minutes.
* `VALUE`: The value of the hardware load. For example, `1min`, `5min`, and `15min` respectively mean the average load of the hardware within 1 minute, 5 minutes, and 15 minutes.

The following example shows how to query the current load information of cpu using the `CLUSTER_LOAD` table:

{{< copyable "sql" >}}

```sql
select * from cluster_load where device_type='cpu' and device_name='cpu';
```

```sql
+------+-----------------+-------------+-------------+--------+---------------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME   | VALUE         |
+------+-----------------+-------------+-------------+--------+---------------+
| tidb | 127.0.0.1:10080 | cpu         | cpu         | load1  | 1.94          |
| tidb | 127.0.0.1:10080 | cpu         | cpu         | load5  | 2.16          |
| tidb | 127.0.0.1:10080 | cpu         | cpu         | load15 | 2.24          |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load1  | 1.94          |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load5  | 2.16          |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load15 | 2.24          |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | load1  | 1.94287109375 |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | load5  | 2.15576171875 |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | load15 | 2.2421875     |
+------+-----------------+-------------+-------------+--------+---------------+
```
