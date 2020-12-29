---
title: CLUSTER_LOAD
summary: 了解 information_schema 表 `CLUSTER_LOAD`。
---

# CLUSTER_LOAD

集群负载表 `CLUSTER_LOAD` 提供集群各个实例所在服务器的的当前负载信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_load;
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

* `TYPE`：对应于节点信息表 [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) 中的 `TYPE` 字段，可取值为 `tidb`，`pd` 和 `tikv`。
* `INSTANCE`：对应于节点信息表 [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) 中的 `INSTANCE` 字段。
* `DEVICE_TYPE`：硬件类型，目前可以查询的硬件类型有 `cpu`、`memory`、`disk` 和 `net`。
* `DEVICE_NAME`：硬件名。对于不同的 `DEVICE_TYPE`，`DEVICE_NAME` 取值不同。
    * `cpu`：硬件名为 cpu。
    * `disk`：磁盘名。
    * `net`：网卡名。
    * `memory`：硬件名为 memory。
* `NAME`：不同的负载类型。例如 cpu 有 `load1`/`load5`/`load15` 三个负载类型，分别表示 cpu 在 1min/5min/15min 内的平均负载。
* `VALUE`：硬件负载的值，例如 cpu 在 1min/5min/15min 内的平均负载。

查询集群当前的 CPU 负载信息示例如下：

{{< copyable "sql" >}}

```sql
SELECT * FROM cluster_load WHERE device_type='cpu' AND device_name='cpu';
```

```sql
+------+-----------------+-------------+-------------+--------+-------+
| TYPE | INSTANCE        | DEVICE_TYPE | DEVICE_NAME | NAME   | VALUE |
+------+-----------------+-------------+-------------+--------+-------+
| tidb | 0.0.0.0:4000    | cpu         | cpu         | load1  | 0.13  |
| tidb | 0.0.0.0:4000    | cpu         | cpu         | load5  | 0.25  |
| tidb | 0.0.0.0:4000    | cpu         | cpu         | load15 | 0.31  |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load1  | 0.13  |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load5  | 0.25  |
| pd   | 127.0.0.1:2379  | cpu         | cpu         | load15 | 0.31  |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | load1  | 0.13  |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | load5  | 0.25  |
| tikv | 127.0.0.1:20165 | cpu         | cpu         | load15 | 0.31  |
+------+-----------------+-------------+-------------+--------+-------+
9 rows in set (1.50 sec)
```