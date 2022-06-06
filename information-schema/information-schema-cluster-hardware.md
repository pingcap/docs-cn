---
title: CLUSTER_HARDWARE
summary: 了解 TiDB 集群硬件表 `CLUSTER_HARDWARE`。
---

# CLUSTER_HARDWARE

集群硬件表 `CLUSTER_HARDWARE` 提供了集群各实例所在服务器的硬件信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_hardware;
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
6 rows in set (0.00 sec)
```

字段解释：

* `TYPE`：对应集群信息表 [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) 中的 `TYPE` 字段，可取值为 `tidb`，`pd` 和 `tikv`。
* `INSTANCE`：对应于集群信息表 [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) 中的 `INSTANCE` 字段。
* `DEVICE_TYPE`：硬件类型。目前可以查询的硬件类型有 `cpu`、`memory`、`disk` 和 `net`。
* `DEVICE_NAME`：硬件名。对于不同的 `DEVICE_TYPE`，`DEVICE_NAME` 的取值不同。
    * `cpu`：硬件名为 cpu。
    * `memory`：硬件名为 memory。
    * `disk`：磁盘名。
    * `net`：网卡名。
* `NAME`：硬件不同的信息名，比如 cpu 有 `cpu-logical-cores` 和 `cpu-physical-cores` 两个信息名，表示逻辑核心数量和物理核心数量。
* `VALUE`：对应硬件信息的值。例如磁盘容量和 CPU 核数。

查询集群 CPU 信息的示例如下：

{{< copyable "sql" >}}

```sql
SELECT * FROM cluster_hardware WHERE device_type='cpu' AND device_name='cpu' AND name LIKE '%cores';
```

```sql
+------+-----------------+-------------+-------------+--------------------+-------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME               | VALUE |
+------+-----------------+-------------+-------------+--------------------+-------+
| tidb | 0.0.0.0:4000    | cpu         | cpu         | cpu-logical-cores  | 16     |
| tidb | 0.0.0.0:4000    | cpu         | cpu         | cpu-physical-cores | 8     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-logical-cores  | 16     |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | cpu-physical-cores | 8     |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | cpu-logical-cores  | 16     |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | cpu-physical-cores | 8     |
+------+-----------------+-------------+-------------+--------------------+-------+
6 rows in set (0.03 sec)
```
