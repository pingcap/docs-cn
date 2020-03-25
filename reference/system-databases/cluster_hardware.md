---
title: CLUSTER_HARDWARE
category: reference
---

# CLUSTER_HARDWARE

集群硬件表 `CLUSTER_HARDWARE` 提供了集群各节点实例的硬件信息。

{{< copyable "sql" >}}

```sql
desc cluster_hardware;
```

```
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
6 rows in set (0.00 sec)
```

字段解释：

* TYPE：对应于节点信息表 `information_schema.cluster_info`  中的 TYPE 字段，可取值为 tidb/pd/tikv，且均为小写
* INSTANCE：对应于节点信息表 `information_schema.cluster_info`  中的 STATUS_ADDRESS 字段
* DEVICE_TYPE：硬件类型，目前可以查询的硬件类型有 cpu/memory/disk/net
* DEVICE_NAME：硬件名，对于不同的 DEVICE_TYPE，取值不同
    * cpu：硬件名为 cpu
    * memory：硬件名为 memory
    * disk：磁盘名
    * `net`：NIC 名。
* NAME：硬件不同的信息名，比如 cpu 有 `cpu-logical-cores`/`cpu-physical-cores`，可以通过 `select name from cluster_hardware where device_type='cpu' group by name` 来查询不同硬件类型支持的 NAME
* VALUE：对应硬件信息的值，比如磁盘容量，CPU 核数

具体示例，查询集群的 CPU 信息：

{{< copyable "sql" >}}

```sql
select * from cluster_hardware where device_type='cpu' and device_name='cpu' and name like '%cores';
```

```
+------+-----------------+-------------+-------------+--------------------+-------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME               | VALUE |
+------+-----------------+-------------+-------------+--------------------+-------+
| tidb | 127.0.0.1:10080 | cpu         | cpu         | cpu-logical-cores  | 8     |
| tidb | 127.0.0.1:10080 | cpu         | cpu         | cpu-physical-cores | 4     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-logical-cores  | 8     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-physical-cores | 4     |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | cpu-logical-cores  | 8     |
| tikv | 127.0.0.1:20160 | cpu         | cpu         | cpu-physical-cores | 4     |
+------+-----------------+-------------+-------------+--------------------+-------+
6 rows in set (0.26 sec)
```
