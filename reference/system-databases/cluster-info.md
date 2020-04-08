---
title: CLUSTER_INFO
summary: Learn the `CLUSTER_INFO` cluster topology information table.
category: reference
---

# CLUSTER_INFO

The `CLUSTER_INFO` cluster topology table provides the current topology information of the cluster, the version information of each node, the Git Hash corresponding to the node version, the starting time of each node, and the running time of each node.

{{< copyable "sql" >}}

```sql
desc cluster_info;
```

```
+----------------+-------------+------+------+---------+-------+
| Field          | Type        | Null | Key  | Default | Extra |
+----------------+-------------+------+------+---------+-------+
| TYPE           | varchar(64) | YES  |      | NULL    |       |
| INSTANCE       | varchar(64) | YES  |      | NULL    |       |
| STATUS_ADDRESS | varchar(64) | YES  |      | NULL    |       |
| VERSION        | varchar(64) | YES  |      | NULL    |       |
| GIT_HASH       | varchar(64) | YES  |      | NULL    |       |
| START_TIME     | varchar(32) | YES  |      | NULL    |       |
| UPTIME         | varchar(32) | YES  |      | NULL    |       |
+----------------+-------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

Field description:

* `TYPE`: The node type. The optional values are `tidb`, `pd`, and `tikv`.
* `INSTANCE`: The instance address, which is a string in the format of `IP:PORT`.
* `STATUS_ADDRESS`: The service address of HTTP API. Some commands in tikv-ctl, pd-ctl, or tidb-ctl might use this API and this address. You can also get more cluster information via this address. Refer to [TiDB HTTP API document](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md) for details.
* `VERSION`: The semantic version number of the corresponding node. To be compatible with the MySQL version number, the TiDB version is displayed in the format of `${mysql-version}-${tidb-version}`.
* `GIT_HASH`: The Git Commit Hash when compiling the node version, which is used to identify whether two nodes are of the absolutely consistent version.
* `START_TIME`: The starting time of the corresponding node.
* `UPTIME`: The uptime of the corresponding node.

{{< copyable "sql" >}}

```sql
select * from cluster_info;
```

```
+------+-----------------+-----------------+----------------------------------------+------------------------------------------+---------------------------+--------------+
| TYPE | INSTANCE        | STATUS_ADDRESS  | VERSION                                | GIT_HASH                                 | START_TIME                | UPTIME       |
+------+-----------------+-----------------+----------------------------------------+------------------------------------------+---------------------------+--------------+
| tidb | 127.0.0.1:4000  | 127.0.0.1:10080 | 5.7.25-TiDB-v4.0.0-beta-195-gb5ea3232a | b5ea3232afa970f00db7a0fb13ed10857db1912e | 2020-03-02T16:27:28+08:00 | 4m18.845924s |
| pd   | 127.0.0.1:2379  | 127.0.0.1:2379  | 4.1.0-alpha                            | 4b9bcbc1425c96848042b6d700eb63f84e72b338 | 2020-03-02T16:27:17+08:00 | 4m29.845928s |
| tikv | 127.0.0.1:20160 | 127.0.0.1:20180 | 4.1.0-alpha                            | 7c4202a1c8faf60eda659dfe0e64e31972488e78 | 2020-03-02T16:27:28+08:00 | 4m18.845929s |
+------+-----------------+-----------------+----------------------------------------+------------------------------------------+---------------------------+--------------+
```
