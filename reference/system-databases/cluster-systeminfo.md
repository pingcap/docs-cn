---
title: CLUSTER_SYSTEMINFO
category: reference
---

# CLUSTER_SYSTEMINFO

集群负载表 `CLUSTER_SYSTEMINFO` 用于查询集群不同节点的内核配置信息。目前支持查询 `sysctl` 的信息。

{{< copyable "sql" >}}

```sql
desc cluster_systeminfo;
```

```
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE    | varchar(64)  | YES  |      | NULL    |       |
| SYSTEM_TYPE | varchar(64)  | YES  |      | NULL    |       |
| SYSTEM_NAME | varchar(64)  | YES  |      | NULL    |       |
| NAME        | varchar(256) | YES  |      | NULL    |       |
| VALUE       | varchar(128) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

字段解释：

* `TYPE`：对应于节点信息表 `information_schema.cluster_info` 中的 `TYPE` 字段，可取值为 `tidb`，`pd` 或 `tikv`。
* `INSTANCE`：对应于节点信息表 `information_schema.cluster_info` 中的 `INSTANCE` 字段。
* `SYSTEM_TYPE`：系统类型，目前可以查询的系统类型有 `system`。
* `SYSTEM_NAME`：目前可以查询的 `SYSTEM_NAME` 为 `sysctl`。
* `NAME`：`sysctl` 对应的配置名。
* `VALUE`：`sysctl` 对应配置项的值。

```sql
select * from cluster_systeminfo where name like '%fd%';
```

```
+------+-----------------+-------------+-------------+-------------------------------+-------+
| TYPE | INSTANCE        | SYSTEM_TYPE | SYSTEM_NAME | NAME                          | VALUE |
+------+-----------------+-------------+-------------+-------------------------------+-------+
| tidb | 127.0.0.1:10080 | system      | sysctl      | net.inet6.ip6.maxifdefrouters | 16    |
| tidb | 127.0.0.1:10080 | system      | sysctl      | net.necp.client_fd_count      | 98    |
| tidb | 127.0.0.1:10080 | system      | sysctl      | net.necp.observer_fd_count    | 0     |
| pd   | 127.0.0.1:2379  | system      | sysctl      | net.inet6.ip6.maxifdefrouters | 16    |
| pd   | 127.0.0.1:2379  | system      | sysctl      | net.necp.client_fd_count      | 98    |
| pd   | 127.0.0.1:2379  | system      | sysctl      | net.necp.observer_fd_count    | 0     |
+------+-----------------+-------------+-------------+-------------------------------+-------+
6 rows in set (0.04 sec)
```