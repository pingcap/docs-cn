---
title: CLUSTER_CONFIG
aliases: ['/docs-cn/dev/system-tables/system-table-cluster-config/','/docs-cn/dev/reference/system-databases/cluster-config/']
summary: 了解 TiDB 集群配置表 `CLUSTER_CONFIG`。
---

# CLUSTER_CONFIG

集群配置表 `CLUSTER_CONFIG` 用于获取集群当前所有 TiDB/PD/TiKV 实例的配置。对于 TiDB 4.0 以前的版本，用户需要逐个访问各个实例的 HTTP API 才能收集到所有组件配置。

{{< copyable "sql" >}}

```sql
desc information_schema.cluster_config;
```

```sql
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| TYPE     | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE | varchar(64)  | YES  |      | NULL    |       |
| KEY      | varchar(256) | YES  |      | NULL    |       |
| VALUE    | varchar(128) | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
```

字段解释：

* `TYPE`：节点的类型，可取值为 `tidb`，`pd` 和 `tikv`。
* `INSTANCE`：节点的服务地址。
* `KEY`：配置项名。
* `VALUE`：配置项值。

以下示例查询 TiKV 实例的 `coprocessor` 相关配置：

{{< copyable "sql" >}}

```sql
select * from information_schema.cluster_config where type='tikv' and `key` like 'coprocessor%';
```

```sql
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
```
