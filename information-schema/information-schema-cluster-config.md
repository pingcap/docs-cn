---
title: CLUSTER_CONFIG
summary: 了解 information_schema 表 `CLUSTER_CONFIG`。
aliases: ['/docs-cn/dev/system-tables/system-table-cluster-config/','/docs-cn/dev/reference/system-databases/cluster-config/','/zh/tidb/dev/system-table-cluster-config/','/docs-cn/dev/information-schema/information-schema-cluster-config/']
---

# CLUSTER_CONFIG

`CLUSTER_CONFIG` 表用于获取集群当前所有组件实例的配置。在 TiDB 早期的版本，用户需要逐个访问各个实例的 HTTP API 才能收集到所有组件配置。TiDB v4.0 后，该表的引入提高了易用性。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_config;
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
SELECT * FROM cluster_config WHERE type='tikv' AND `key` LIKE 'coprocessor%';
```

```sql
+------+-----------------+-----------------------------------+---------+
| TYPE | INSTANCE        | KEY                               | VALUE   |
+------+-----------------+-----------------------------------+---------+
| tikv | 127.0.0.1:20165 | coprocessor.batch-split-limit     | 10      |
| tikv | 127.0.0.1:20165 | coprocessor.region-max-keys       | 1440000 |
| tikv | 127.0.0.1:20165 | coprocessor.region-max-size       | 144MiB  |
| tikv | 127.0.0.1:20165 | coprocessor.region-split-keys     | 960000  |
| tikv | 127.0.0.1:20165 | coprocessor.region-split-size     | 96MiB   |
| tikv | 127.0.0.1:20165 | coprocessor.split-region-on-table | false   |
+------+-----------------+-----------------------------------+---------+
6 rows in set (0.00 sec)
```
