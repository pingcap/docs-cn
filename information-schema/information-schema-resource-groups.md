---
title: RESOURCE_GROUPS
summary: 了解 `RESOURCE_GROUPS` information_schema 表。
---

# RESOURCE_GROUPS

`RESOURCE_GROUPS` 表显示了所有资源组的信息。更多信息，请参见[使用资源控制实现资源隔离](/tidb-resource-control.md)。

> **注意：**
>
> 此表在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

```sql
USE information_schema;
DESC resource_groups;
```

```sql
+------------+-------------+------+------+---------+-------+
| Field      | Type        | Null | Key  | Default | Extra |
+------------+-------------+------+------+---------+-------+
| NAME       | varchar(32) | NO   |      | NULL    |       |
| RU_PER_SEC | bigint(21)  | YES  |      | NULL    |       |
| PRIORITY   | varchar(6)  | YES  |      | NULL    |       |
| BURSTABLE  | varchar(3)  | YES  |      | NULL    |       |
+------------+-------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

## 示例

```sql
SELECT * FROM information_schema.resource_groups; -- 查看所有资源组。TiDB 有一个 `default` 资源组。
```

```sql
+---------+------------+----------+-----------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE |
+---------+------------+----------+-----------+
| default | UNLIMITED  | MEDIUM   | YES       |
+---------+------------+----------+-----------+
```

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- 创建资源组 `rg1`
```

```sql
Query OK, 0 rows affected (0.34 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1; -- 显示资源组 `rg1` 的定义
```

```sql
+----------------+---------------------------------------------------------------+
| Resource_Group | Create Resource Group                                         |
+----------------+---------------------------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=1000 PRIORITY="MEDIUM" |
+----------------+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg1'; -- 查看资源组 `rg1`
```

```sql
+------+------------+----------+-----------+-------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT |
+------+------------+----------+-----------+-------------+
| rg1  | 1000       | MEDIUM   | NO        | NULL        |
+------+------------+----------+-----------+-------------+
1 row in set (0.00 sec)
```

`RESOURCE_GROUPS` 表中各列的描述如下：

* `NAME`：资源组的名称。
* `RU_PER_SEC`：资源组的回填速度。单位为 RU/秒，其中 RU 表示[请求单元（Request Unit）](/tidb-resource-control.md#what-is-request-unit-ru)。
* `PRIORITY`：在 TiKV 上处理任务的绝对优先级。不同资源按照 `PRIORITY` 设置进行调度。高 `PRIORITY` 的任务优先调度。对于具有相同 `PRIORITY` 的资源组，将根据 `RU_PER_SEC` 配置按比例调度任务。如果未指定 `PRIORITY`，默认优先级为 `MEDIUM`。
* `BURSTABLE`：是否允许资源组超用可用的系统资源。

> **注意：**
>
> TiDB 在集群初始化时会自动创建一个 `default` 资源组。对于该资源组，`RU_PER_SEC` 的默认值为 `UNLIMITED`（相当于 `INT` 类型的最大值，即 `2147483647`），并且处于 `BURSTABLE` 模式。所有未绑定到任何资源组的请求都会自动绑定到这个 `default` 资源组。当你为其他资源组创建新配置时，建议根据需要修改 `default` 资源组配置。
