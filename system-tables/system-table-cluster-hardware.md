---
title: CLUSTER_HARDWARE
summary: Learn the `CLUSTER_HARDWARE` cluster hardware system table.
aliases: ['/docs/dev/system-tables/system-table-cluster-hardware/','/docs/dev/reference/system-databases/cluster-hardware/']
---

# CLUSTER_HARDWARE

The `CLUSTER_HARDWARE` hardware system table provides the hardware information of the server where each instance of the cluster is located.

{{< copyable "sql" >}}

```sql
desc information_schema.cluster_hardware;
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

* `TYPE`: Corresponds to the `TYPE` field in the [`information_schema.cluster_info`](/system-tables/system-table-cluster-info.md) table. The optional values are `tidb`, `pd`, and `tikv`.
* `INSTANCE`: Corresponds to the `INSTANCE` field in the [`information_schema.cluster_info`](/system-tables/system-table-cluster-info.md) cluster information table.
* `DEVICE_TYPE`: Hardware type. Currently, you can query the `cpu`, `memory`, `disk`, and `net` types.
* `DEVICE_NAME`: Hardware name. The value of `DEVICE_NAME` varies with `DEVICE_TYPE`.
    * `cpu`: The hardware name is cpu.
    * `memory`: The hardware name is memory.
    * `disk`: The disk name.
    * `net`: The network card name.
* `NAME`: The different information names of the hardware. For example, cpu has two information names: `cpu-logical-cores` and `cpu-physical-cores`, which respectively mean logical core numbers and physical core numbers.
* `VALUE`: The value of the corresponding hardware information, such as the disk volume and CPU core numbers.

The following example shows how to query the CPU information using the `CLUSTER_HARDWARE` table:

{{< copyable "sql" >}}

```sql
select * from information_schema.cluster_hardware where device_type='cpu' and device_name='cpu' and name like '%cores';
```

```sql
+------+-----------------+-------------+-------------+--------------------+-------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME               | VALUE |
+------+-----------------+-------------+-------------+--------------------+-------+
| tidb | 0.0.0.0:4000    | cpu         | cpu         | cpu-logical-cores  | 8     |
| tidb | 0.0.0.0:4000    | cpu         | cpu         | cpu-physical-cores | 4     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-logical-cores  | 8     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-physical-cores | 4     |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | cpu-logical-cores  | 8     |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | cpu-physical-cores | 4     |
+------+-----------------+-------------+-------------+--------------------+-------+
```
