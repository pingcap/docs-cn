---
title: CLUSTER_CONFIG
category: reference
---

# CLUSTER_CONFIG

集群配置表 `CLUSTER_CONFIG` 用于获取集群当前所有节点的配置，而 TiDB 4.0 之前的版本必须通过逐个访问各个节点的 HTTP API 的形式才能收集到所有节点配置。

```sql
mysql> desc cluster_config;
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| TYPE     | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE | varchar(64)  | YES  |      | NULL    |       |
| KEY      | varchar(256) | YES  |      | NULL    |       |
| VALUE    | varchar(128) | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

字段解释：

* TYPE：对应于节点信息表 `information_schema.cluster_info`  中的 TYPE 字段，可取值为 tidb/pd/tikv，且均为小写
* INSTANCE：对应于节点信息表 `information_schema.cluster_info`  中的 STATUS_ADDRESS 字段
* KEY：配置项名
* VALUE：配置项值

具体示例，查询 TiKV 节点的 `coprocessor` 相关配置：

```sql
mysql> select * from cluster_config where type='tikv' and `key` like 'coprocessor%';
+------+-----------------+-----------------------------------+----------+
| TYPE | INSTANCE        | KEY                               | VALUE    |
+------+-----------------+-----------------------------------+----------+
| tikv | 127.0.0.1:20160 | coprocessor.batch-split-limit     | 10       |
| tikv | 127.0.0.1:20160 | coprocessor.region-max-keys       | 1.44e+06 |
| tikv | 127.0.0.1:20160 | coprocessor.region-max-size       | 144MiB   |
| tikv | 127.0.0.1:20160 | coprocessor.region-split-keys     | 960000   |
| tikv | 127.0.0.1:20160 | coprocessor.region-split-size     | 96MiB    |
| tikv | 127.0.0.1:20160 | coprocessor.split-region-on-table | false    |
+------+-----------------+-----------------------------------+----------+
6 rows in set (1.04 sec)
```