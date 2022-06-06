---
title: CLUSTER_INFO
summary: 了解 TiDB 集群拓扑表 `CLUSTER_INFO`。
---

# CLUSTER_INFO

集群拓扑表 `CLUSTER_INFO` 提供集群当前的拓扑信息，以及各个节点的版本信息、版本对应的 Git Hash、各节点的启动时间、各实例的运行时间。

{{< copyable "sql" >}}

```sql
USE information_schema;
desc cluster_info;
```

```sql
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

字段解释：

* `TYPE`：节点类型，目前节点的可取值为 `tidb`，`pd` 和 `tikv`。
* `INSTANCE`：实例地址，为 `IP:PORT` 格式的字符串。
* `STATUS_ADDRESS`：HTTP API 的服务地址。部分 `tikv-ctl`、`pd-ctl` 或 `tidb-ctl` 命令会使用到 HTTP API 和该地址。用户也可以通过该地址获取一些额外的集群信息，详情可参考 [HTTP API 文档](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)。
* `VERSION`：对应节点的语义版本号。TiDB 版本为了兼容 MySQL 的版本号，以 `${mysql-version}-${tidb-version}` 的格式展示版本号。
* `GIT_HASH`：编译节点版本时的 Git Commit Hash，用于识别两个节点是否是绝对一致的版本。
* `START_TIME`：对应节点的启动时间。
* `UPTIME`：对应节点已经运行的时间。

{{< copyable "sql" >}}

```sql
SELECT * FROM cluster_info;
```

```sql
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
| TYPE | INSTANCE        | STATUS_ADDRESS  | VERSION      | GIT_HASH                                 | START_TIME                | UPTIME              |
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
| tidb | 0.0.0.0:4000    | 0.0.0.0:10080   | 4.0.0-beta.2 | 0df3b74f55f8f8fbde39bbd5d471783f49dc10f7 | 2020-07-05T09:25:53-06:00 | 26h39m4.352862693s  |
| pd   | 127.0.0.1:2379  | 127.0.0.1:2379  | 4.1.0-alpha  | 1ad59bcbf36d87082c79a1fffa3b0895234ac862 | 2020-07-05T09:25:47-06:00 | 26h39m10.352868103s |
| tikv | 127.0.0.1:20165 | 127.0.0.1:20180 | 4.1.0-alpha  | b45e052df8fb5d66aa8b3a77b5c992ddbfbb79df | 2020-07-05T09:25:50-06:00 | 26h39m7.352869963s  |
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
3 rows in set (0.00 sec)
```
