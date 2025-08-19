---
title: RESOURCE_GROUPS
summary: 了解 information_schema 表 `RESOURCE_GROUPS`。
---

# RESOURCE_GROUPS

`RESOURCE_GROUPS` 表展示所有资源组 (resource group) 的信息，见[使用资源管控 (Resource Control) 实现资源组限制和流控](/tidb-resource-control-ru-groups.md)。

```sql
USE information_schema;
DESC resource_groups;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| NAME        | varchar(32)  | NO   |      | NULL    |       |
| RU_PER_SEC  | varchar(21)  | YES  |      | NULL    |       |
| PRIORITY    | varchar(6)   | YES  |      | NULL    |       |
| BURSTABLE   | varchar(3)   | YES  |      | NULL    |       |
| QUERY_LIMIT | varchar(256) | YES  |      | NULL    |       |
| BACKGROUND  | varchar(256) | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

## 示例

```sql
SELECT * FROM information_schema.resource_groups; -- 查看资源组，TiDB 默认预置 `default` 资源组
```

```sql
+---------+------------+----------+-----------+-------------+------------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND |
+---------+------------+----------+-----------+-------------+------------+
| default | UNLIMITED  | MEDIUM   | UNLIMITED | NULL        | NULL       |
+---------+------------+----------+-----------+-------------+------------+
```

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- 创建资源组 `rg1`
```

```sql
Query OK, 0 rows affected (0.34 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1; -- 显示 `rg1` 资源组的定义
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
+------+------------+----------+-----------+-------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND |
+------+------------+----------+-----------+-------------+------------+
| rg1  | 1000       | MEDIUM   | OFF       | NULL        | NULL       |
+------+------------+----------+-----------+-------------+------------+
1 row in set (0.00 sec)
```

`RESOURCE_GROUPS` 表中列的含义如下：

* `NAME`：资源组名称。
* `RU_PER_SEC`：资源组的回填速度，单位为每秒回填的 [Request Unit (RU)](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 数量。
* `PRIORITY`：任务在 TiKV 上处理的绝对优先级。不同的资源按照 `PRIORITY` 的设置进行调度，`PRIORITY` 高的任务会被优先调度。如果资源组的 `PRIORITY` 相同，则会根据 `RU_PER_SEC` 的配置按比例调度。如果不指定 `PRIORITY`，资源组的默认优先级为 `MEDIUM`。
* `BURSTABLE`：是否允许此资源组超额使用剩余的系统资源。从 v9.0.0 开始，支持以下三种模式，如果没有为 `BURSTABLE` 指定目标值，将默认启用 `MODERATED` 模式。
    - `OFF`：表示不允许此资源组超额使用剩余的系统资源；
    - `MODERATED`：表示**有限度**地允许此资源组超额使用剩余的系统资源，优先保证资源组限额内的资源得到分配；
    - `UNLIMITED`：表示**无限度**地允许此资源组超额使用剩余的系统资源，与限额内资源同等竞争。

> **注意：**
>
> TiDB 集群在初始化时会自动创建 `default` 资源组，其 `RU_PER_SEC` 的默认值为 `UNLIMITED` (等同于 `INT` 类型最大值，即 `2147483647`)，且 `BURSTABLE` 为 `UNLIMITED` 模式。所有未绑定资源组的语句将自动绑定至该资源组。`default` 资源组不支持删除，但支持修改其 RU 配置。
