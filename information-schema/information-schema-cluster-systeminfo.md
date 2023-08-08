---
title: CLUSTER_SYSTEMINFO
summary: 了解 TiDB 集群负载表 `CLUSTER_SYSTEMINFO`。
---

# CLUSTER_SYSTEMINFO

内核参数表 `CLUSTER_SYSTEMINFO` 用于查询集群所有实例所在服务器的内核配置信息。目前支持查询 `sysctl` 的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_systeminfo;
```

```sql
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

* `TYPE`：对应于节点信息表 [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) 中的 `TYPE` 字段，可取值为 `tidb`，`pd` 和 `tikv`。
* `INSTANCE`：对应于节点信息表 [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) 中的 `INSTANCE` 字段。
* `SYSTEM_TYPE`：系统类型，目前可以查询的系统类型有 `system`。
* `SYSTEM_NAME`：目前可以查询的 `SYSTEM_NAME` 为 `sysctl`。
* `NAME`：`sysctl` 对应的配置名。
* `VALUE`：`sysctl` 对应配置项的值。

查询集群所有服务器的内核版本示例如下：

```sql
SELECT * FROM cluster_systeminfo WHERE name LIKE '%kernel.osrelease%'
```

```sql
+------+-------------------+-------------+-------------+------------------+----------------------------+
| TYPE | INSTANCE          | SYSTEM_TYPE | SYSTEM_NAME | NAME             | VALUE                      |
+------+-------------------+-------------+-------------+------------------+----------------------------+
| tidb | 172.16.5.40:4008  | system      | sysctl      | kernel.osrelease | 3.10.0-862.14.4.el7.x86_64 |
| pd   | 172.16.5.40:20379 | system      | sysctl      | kernel.osrelease | 3.10.0-862.14.4.el7.x86_64 |
| tikv | 172.16.5.40:21150 | system      | sysctl      | kernel.osrelease | 3.10.0-862.14.4.el7.x86_64 |
+------+-------------------+-------------+-------------+------------------+----------------------------+
```
