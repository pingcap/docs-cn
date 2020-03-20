---
title: CLUSTER_INFO
category: reference
---

# CLUSTER_INFO

集群拓扑表 `CLUSTER_INFO` 提供了集群当前的拓扑信息，以及各个节点的版本、版本对应的 Git Hash、启动时间、运行时间信息。

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

字段解释：

* TYPE：节点类型，目前节点的类型为 pd/tikv/tidb，节点类型始终为小写
* INSTANCE：实例地址，始终为 IP:PORT 格式的字符串
* STATUS_ADDRESS：HTTP API 服务地址，部分 tikv-ctl / pd-ctl / tidb-ctl 命令会使用到 HTTP API，会使用这个地址，用户也可以通过这个地址获取一些额外的集群信息，具体 HTTP API 参考官方文档
* VERSION：对应节点的语义版本号，TiDB 版本为了兼容 MySQL 的版本号，以 ${mysql-version}-${tidb-version} 方式展示
* GIT_HASH：对应节点版本编译时的 git commit hash，主要用于识别两个节点是否是绝对一致的版本
* START_TIME：对应节点的启动时间
* UPTIME：对应节点已经运行的时间

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
3 rows in set (0.01 sec)
```