---
title: CLUSTER_SYSTEMINFO
summary: Learn the `CLUSTER_SYSTEMINFO` kernel parameter table.
aliases: ['/docs/dev/system-tables/system-table-cluster-systeminfo/','/docs/dev/reference/system-databases/cluster-systeminfo/','/tidb/dev/system-table-cluster-systeminfo/']
---

# CLUSTER_SYSTEMINFO

You can use the `CLUSTER_SYSTEMINFO` kernel parameter table to query the kernel configuration information of the server where all instances of the cluster are located. Currently, you can query the information of the `sysctl` system.

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

Field description:

* `TYPE`: Corresponds to the `TYPE` field in the [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) table. The optional values are `tidb`, `pd`, and `tikv`.
* `INSTANCE`: Corresponds to the `INSTANCE` field in the [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md) cluster information table.
* `SYSTEM_TYPE`: The system type. Currently, you can query the `system` system type.
* `SYSTEM_NAME`: The system name. Currently, you can query the `sysctl` system name.
* `NAME`: The configuration name corresponding to `sysctl`.
* `VALUE`: The value of the configuration item corresponding to `sysctl`.

The following example shows how to query the kernel version of all servers in the cluster using the `CLUSTER_SYSTEMINFO` system information table.

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
