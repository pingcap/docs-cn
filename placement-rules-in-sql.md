---
title: Placement Rules in SQL
summary: 了解如何通过 SQL 接口调度表和分区的放置位置。
---

# Placement Rules in SQL

Placement Rules in SQL 特性用于通过 SQL 语句配置数据在 TiKV 集群中的放置位置。通过该功能，你可以将集群、数据库、表、或分区的数据部署到不同的地域、机房、机柜、主机。

该功能可以实现以下业务场景：

- 多数据中心部署，配置规则优化数据高可用策略
- 合并多个不同业务的数据库，物理隔离不同用户的数据，满足实例内部不同用户的隔离需求
- 增加重要数据的副本数，提高业务可用性和数据可靠性

## 功能概述

通过 Placement Rules in SQL 功能, 你可以[创建放置策略 (placement policy)](#创建并绑定放置策略)，并为不同的数据级别配置所需的放置策略，粒度从粗到细为：

| 级别                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| 集群          | TiDB 默认为集群配置 3 副本的策略。你可以为集群配置全局放置策略，参考[集群配置](#为集群指定全局的副本数)。  |
| 数据库        | 你可以为指定的 Database 配置放置策略，参考[为数据库指定默认的放置策略](#为数据库指定默认的放置策略)。 |
| 表            | 你可以为指定的 Table 配置放置策略，参考[为表指定放置策略](#为表指定放置策略)。  |
| 分区          | 你可以为表中不同的 Row 创建分区，并单独对分区配置放置策略，参考[为分区表指定放置策略](#为分区表指定放置策略)。 |

> **建议：**
>
> Placement Rules in SQL 底层的实现依赖 PD 提供的放置规则 (placement rules) 功能，参考 [Placement Rules 使用文档](/configure-placement-rules.md)。在 Placement Rules in SQL 语境下，放置规则既可以代指绑定对象的放置策略 (placement policy)，也可以代指 TiDB 发给 PD 的放置规则。

## 使用限制

- 为了降低运维难度，建议将一个集群的 placement policy 数量限制在 10 个以内。
- 建议将绑定了 placement policy 的表和分区数的总数限制在 10000 以内。为过多的表和分区绑定 policy，会增加 PD 上规则计算的负担，从而影响服务性能。
- 建议按照本文中提到的示例场景使用 Placement Rules in SQL 功能，不建议使用复杂的放置策略。

## 前提条件

放置策略依赖于 TiKV 节点标签 (label) 的配置。例如，放置选项 `PRIMARY_REGION` 依赖 TiKV 中的 `region` 标签。

创建放置策略时，TiDB 不会检查标签是否存在，而是在绑定放置策略的时候进行检查。因此，在绑定放置策略前，请确保各个 TiKV 节点已配置正确的标签。配置方法为：

```
tikv-server --labels region=<region>,zone=<zone>,host=<host>
```

详细配置方法可参考以下示例:

| 方式 | 示例 |
| --- | --- |
| 手动部署 | [通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md) |
| TiUP 部署 | [跨机房部署拓扑结构](/geo-distributed-deployment-topology.md) |
| Operator 部署| [在 Kubernetes 中配置 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster#数据的高可用) |

如需查看当前 TiKV 集群中所有可用的标签，可以使用 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) 语句：

```sql
SHOW PLACEMENT LABELS;
+--------+----------------+
| Key    | Values         |
+--------+----------------+
| disk   | ["ssd"]        |
| region | ["us-east-1"]  |
| zone   | ["us-east-1a"] |
+--------+----------------+
3 rows in set (0.00 sec)
```

## 使用方法

本节介绍如何通过 SQL 语句创建、绑定、查看、修改、删除放置策略。

### 创建并绑定放置策略

1. 使用 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) 语句创建放置策略：

    ```sql
    CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
    ```

    在该语句中：

    - `PRIMARY_REGION="us-east-1"` 选项代表 Raft leader 被放置在 `region` 标签为 `us-east-1` 的节点上。
    - `REGIONS="us-east-1,us-west-1"` 选项代表 Raft followers 被放置在 `region` 标签为 `us-east-1` 和 `region` 标签为 `us-west-1` 的节点上。

    更多可配置的放置选项和对应的含义，请参考[放置选项](#放置选项参考)。

2. 使用 `CREATE TABLE` 或者 `ALTER TABLE` 将放置策略绑定至表或分区表，这样就在表或分区上指定了放置策略：

    ```sql
    CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
    CREATE TABLE t2 (a INT);
    ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
    ```

    `PLACEMENT POLICY` 为全局作用域，不与任何数据库表结构相关联。因此，通过 `CREATE TABLE` 指定放置策略时，无需任何额外的权限。

### 查看放置策略

- 要查看某条已创建的放置策略，可以使用 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) 语句：

    ```sql
    SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
    *************************** 1. row ***************************
           Policy: myplacementpolicy
    Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
    1 row in set (0.00 sec)
    ```

- 要查看某张表绑定的放置策略，可以使用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 语句：

    ```sql
    SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
    1 row in set (0.00 sec)
    ```

- 要查看集群中所有放置策略的定义，可以查询 [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md) 系统表：

    ```sql
    SELECT * FROM information_schema.placement_policies\G
    ***************************[ 1. row ]***************************
    POLICY_ID            | 1
    CATALOG_NAME         | def
    POLICY_NAME          | p1
    PRIMARY_REGION       | us-east-1
    REGIONS              | us-east-1,us-west-1
    CONSTRAINTS          |
    LEADER_CONSTRAINTS   |
    FOLLOWER_CONSTRAINTS |
    LEARNER_CONSTRAINTS  |
    SCHEDULE             |
    FOLLOWERS            | 4
    LEARNERS             | 0
    1 row in set
    ```

- 要查看集群中所有绑定了放置策略的表，可以查询 `information_schema.tables` 系统表的 `tidb_placement_policy_name` 列：

    ```sql
    SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- 要查看集群中所有绑定了放置策略的分区，可以查询 `information_schema.partitions` 系统表的 `tidb_placement_policy_name` 列：

    ```sql
    SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- 所有绑定放置策略的对象都是异步调度的。要查看放置策略的调度进度，可以使用 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) 语句。

    ```sql
    SHOW PLACEMENT;
    ```

### 修改放置策略

要修改放置策略，可以使用 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) 语句。该修改将应用于所有绑定了此放置策略的对象。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

在该语句中，`FOLLOWERS=4` 选项代表数据有 5 个副本，包括 4 个 follower 和 1 个 leader。更多可配置的放置选项和对应的含义，请参考[放置选项](#放置选项参考)。

### 删除放置策略

要删除没有绑定任何表或分区的放置策略，可以使用 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) 语句：

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 放置选项参考

在创建和修改放置策略时，你可以按需配置放置选项。

> **注意：**
>
> `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 选项不可与 `CONSTRAINTS` 选项同时指定，否则会报错。

### 常规放置选项

常规放置选项可以满足数据放置的基本需求。

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | Raft leader 被放置在有 `region` 标签的节点上，且这些 `region` 标签匹配本选项的值。     |
| `REGIONS`                  | Raft followers 被放置在有 `region` 标签的节点上，且这些 `region` 标签匹配本选项的值。 |
| `SCHEDULE`                 |  用于调度 follower 放置位置的策略。可选值为 `EVEN`（默认值）或 `MAJORITY_IN_PRIMARY`。 |
| `FOLLOWERS`                |  Follower 的数量。例如 `FOLLOWERS=2` 表示数据有 3 个副本（2 个 follower 和 1 个 leader）。 |

### 高级放置选项

高级配置选项可以更灵活地放置数据，满足复杂的场景需求，但其配置方法相对常规配置选项更复杂一些，需要你对集群拓扑和 TiDB 数据分片有深入的了解。

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `CONSTRAINTS`              | 适用于所有角色 (role) 的约束列表。例如，`CONSTRAINTS="[+disk=ssd]"`。|
| `LEADER_CONSTRAINTS`       | 仅适用于 leader 的约束列表。                                         |
| `FOLLOWER_CONSTRAINTS`     | 仅适用于 follower 的约束列表。                                           |
| `LEARNER_CONSTRAINTS`      | 仅适用于 learner 的约束列表。                                           |
| `LEARNERS`                 | 指定 learner 的数量。     |
| `SURVIVAL_PREFERENCE`      | 指定按 label 容灾等级的优先级放置副本。例如 `SURVIVAL_PREFERENCE="[region, zone, host]"`。    |

### CONSTRAINTS 格式

`CONSTRAINTS`、`FOLLOWER_CONSTRAINTS`、`LEARNER_CONSTRAINTS` 放置选项支持以下两种配置格式:

| CONSTRAINTS 格式 | 描述 |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| 列表格式  | 如果指定的约束适用于所有副本，可以使用键值对列表格式。键以 `+` 或 `-` 开头。例如：<br/> <ul><li>`[+region=us-east-1]` 表示放置数据在 `region` 标签为 `us-east-1` 的节点上。</li><li>`[+region=us-east-1,-type=fault]` 表示放置数据在 `region` 标签为 `us-east-1` 且 `type` 标签不为 `fault` 的节点上。</li></ul><br/>  |
| 字典格式 | 如果需要为不同的约束指定不同数量的副本，可以使用字典格式。例如：<br/> <ul><li>`FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 表示 1 个 follower 位于 `us-east-1`，1 个 follower 位于 `us-east-2`，1 个 follower 位于 `us-west-1`。</li><li>`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';` 表示 1 个 follower 位于 `us-east-1` 区域中有标签 `type` 为 `scale-node` 的节点上，1 个 follower 位于 `us-west-1`。</li></ul>字典格式支持以 `+` 或 `-` 开头的键，并支持配置特殊的 `#evict-leader` 属性。例如，`FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}'` 表示当进行容灾时，`us-west-1` 上尽可能驱逐当选的 leader。|

> **注意：**
>
> - `LEADER_CONSTRAINTS` 放置选项只支持列表格式。
> - 字典和列表格式都基于 YAML 解析，但 YAML 语法有时不能被正常解析。例如 YAML 会把 `"{+region=east:1,+region=west:2}"`（`:` 后无空格）错误地解析成 `'{"+region=east:1": null, "+region=west:2": null}'`，不符合预期。但 `"{+region=east: 1,+region=west: 2}"`（`:` 后有空格）能被正确解析成 `'{"+region=east": 1, "+region=west": 2}'`。因此建议 `:` 后加上空格。
>

## 基础示例

### 为集群指定全局的副本数

集群初始化后，副本数默认值为 `3`。集群如需更多的副本数，可使用配置策略调大该值，应用到集群级别，可以使用 [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md)。示例如下：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

注意，TiDB 默认 leader 个数是 1。因此，5 个副本为 4 个 follower 和 1 个 leader。

### 为数据库指定默认的放置策略

你可以为某个数据库指定默认的放置策略，类似于为数据库设置默认字符集或排序规则。如果数据库中的表或分区没有单独指定其他放置策略，就会使用数据库上指定的放置策略。示例如下：

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- 创建放置策略

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- 创建表 t1，且未指定放置策略。

ALTER DATABASE test PLACEMENT POLICY=p2;  -- 更改数据库默认的放置策略为 p2，但更改不影响已有的表 t1。

CREATE TABLE t2 (a INT);  -- 创建表 t2，默认的放置策略 p2 在 t2 上生效。

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- 创建表 t3。因为语句中已经指定了其他放置策略，默认的 p2 策略在 t3 上不生效。

ALTER DATABASE test PLACEMENT POLICY=p3;  -- 再次更改数据库默认的放置策略，此更改不影响已有的表。

CREATE TABLE t4 (a INT);  -- 创建表 t4，默认的放置策略 p3 在 t4 生效。

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- 绑定策略 p3 的表，也就是 t4，会采用 FOLLOWERS=3。
```

注意分区与表之间的继承和这里的继承不同。改变表的默认放置策略，也会让分区应用新的策略。但是只有建表时没有指定放置策略，表才会从数据库继承放置策略，且之后再改变数据库的默认放置策略也不影响已经继承的表。

### 为表指定放置策略

你可以为某个表指定默认的放置策略。示例如下：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- 创建表 t。绑定放置策略为 five_replicas。

ALTER TABLE t PLACEMENT POLICY=default; -- 删除表 t 已绑定的放置策略 five_replicas，重置为默认的放置策略。
```

### 为分区表指定放置策略

你还可以给表分区指定放置策略。示例如下：

```sql
CREATE PLACEMENT POLICY storageforhistorydata CONSTRAINTS="[+node=history]";
CREATE PLACEMENT POLICY storagefornewdata CONSTRAINTS="[+node=new]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE, UNIQUE INDEX idx(id) GLOBAL)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageforhistorydata,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storagefornewdata
);
```

如果没有为表中的某个分区指定任何放置策略，该分区将尝试继承表上可能存在的策略。如果该表有[全局索引](/partitioned-table.md#全局索引)，索引将应用与该表相同的放置策略。在上面示例中：

- `p0` 分区将会应用 `storageforhistorydata` 策略
- `p4` 分区将会应用 `storagefornewdata` 策略
- `p1`、`p2`、`p3` 分区将会应用表 `t1` 的放置策略 `companystandardpolicy`
- 全局索引 `idx` 将应用与表 `t1` 相同的 `companystandardpolicy` 放置策略
- 如果没有为表 `t1` 指定放置策略，`p1`、`p2` 和 `p3` 分区以及全局索引 `idx` 将继承数据库默认策略或全局默认策略

给分区绑定放置策略后，你可以更改指定分区的放置策略。示例如下：

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhistorydata;
```

## 高可用场景示例

假设集群的拓扑结构如下，集群的 TiKV 节点分布在 3 个 `region`（区域），每个 `region` 有 3 个可用的 `zone` （可用区）：

```sql
SELECT store_id,address,label from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
| store_id | address         | label                                                                                                                    |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
|        1 | 127.0.0.1:20163 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1a"}, {"key": "host", "value": "host1"}]     |
|        2 | 127.0.0.1:20162 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1b"}, {"key": "host", "value": "host2"}]     |
|        3 | 127.0.0.1:20164 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1c"}, {"key": "host", "value": "host3"}]     |
|        4 | 127.0.0.1:20160 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2a"}, {"key": "host", "value": "host4"}]     |
|        5 | 127.0.0.1:20161 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2b"}, {"key": "host", "value": "host5"}]     |
|        6 | 127.0.0.1:20165 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2c"}, {"key": "host", "value": "host6"}]     |
|        7 | 127.0.0.1:20166 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1a"}, {"key": "host", "value": "host7"}]     |
|        8 | 127.0.0.1:20167 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1b"}, {"key": "host", "value": "host8"}]     |
|        9 | 127.0.0.1:20168 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1c"}, {"key": "host", "value": "host9"}]     |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+

```

### 指定生存偏好

如果你不特别在意数据的具体分布，只希望能满足容灾生存要求，可以使用 `SURVIVAL_PREFERENCES` 选项设置数据的生存能力偏好。

在上面的例子中，TiDB 集群分布在 3 个 `region`，且每个区域有 3 个 `zone`。在为该集群创建放置策略时，假设 `SURVIVAL_PREFERENCES` 的设置如下：

``` sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

创建好放置策略后，你可以按需将放置策略绑定到对应的表上：

- 对于绑定了 `multiaz` 放置策略的表，数据将以 3 副本的形式放置在不同的 `region` 里，优先满足跨 `region` 级别的生存目标，再满足跨 `zone` 级别的生存目标，最后再满足跨 `host` 级别的生存目标。
- 对于绑定了 `singleaz` 放置策略的表，数据会优先以 3 副本的形式全部放置在 `us-east-1` 这个 `region` 里，再满足跨 `zone` 级别的数据隔离的生存目标。

> **注意：**
>
> `SURVIVAL_PREFERENCES` 和 PD 中的 `location-labels` 是等价的，更多信息可以参考[通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md)。

### 指定集群多数据中心 5 副本 2:2:1 分布

如需特定的数据分布（如 5 副本 2:2:1 分布），可以配置[字典格式](#constraints-格式)的 `CONSTRAINTS` 为不同的约束指定不同数量的副本：

```sql
CREATE PLACEMENT POLICY `deploy221` CONSTRAINTS='{"+region=us-east-1":2, "+region=us-east-2": 2, "+region=us-west-1": 1}';

ALTER RANGE global PLACEMENT POLICY = "deploy221";

SHOW PLACEMENT;
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| Target            | Placement                                                                                   | Scheduling_State |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| POLICY deploy221  | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | NULL             |
| RANGE TiDB_GLOBAL | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | SCHEDULED        |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
```

通过为集群全局设置 `deploy221` 放置策略后，TiDB 会根据该策略来分布数据：`us-east-1` 区域放置两个副本，`us-east-2` 区域放置两个副本，`us-west-1` 区域放置一个副本。

### 指定 Leader/Follower 分布

你可以通过 Constraints 或 PRIMARY_REGION 指定特殊的 Leader/Follower 的分布。

#### 使用 Constraints 指定

如果你对 Raft Leader 的分布节点有要求，可以使用如下语句指定：

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1": 1}';
```

该放置策略创建好并绑定到所需的数据后，这些数据的 Raft Leader 副本将会放置在 `LEADER_CONSTRAINTS` 选项指定的 `us-east-1` 区域中，其他副本将会放置在`FOLLOWER_CONSTRAINTS` 选项指定的区域。需要注意的是，如果集群发生故障，比如 Leader 所在区域 `us-east-1` 的节点宕机，这时候即使其他区域设置的都是 `FOLLOWER_CONSTRAINTS`, 也会从中选举出一个新的 Leader，也就是说保证服务可用的优先级是最高的。

在 `us-east-1` 区域故障发生时，如果希望新的 Leader 不要放置在 `us-west-1`，可以配置特殊的 `evict-leader` 属性，驱逐上面新的 Leader:

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}';
```

#### 使用 PRIMARY_REGION 指定

如果你的集群拓扑配置了 `region` label，你还可以使用 `PRIMARY_REGION` 和 `REGIONS` 选项来指定 follower 的放置策略：

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

- `PRIMARY_REGION` 为 Leader 分布的区域，只能指定一个。
- `SCHEDULE` 选项指定 TiDB 如何平衡 follower 的分布。
    - 该选项默认的 `EVEN` 调度规则确保 follower 在所有区域内分布平衡。
    - 如需保证在 `PRIMARY_REGION`（即 `us-east-1`）内放置足够多的 follower 副本，你可以使用 `MAJORITY_IN_PRIMARY` 调度规则来使该区域的 follower 达到指定数量。该调度牺牲一些可用性来换取更低的事务延迟。如果主区域宕机，`MAJORITY_IN_PRIMARY` 无法提供自动故障转移。

## 数据隔离场景示例

以下示例在创建放置策略时，设置了一个约束，要求数据必须放置在配置了指定的 `app` 标签的 TiKV 节点：

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

在该示例中，约束是通过列表格式 (`[+app=order]`) 指定的。你也可以使用字典格式指定，例如 (`{+app=order: 3}`)。

执行示例中的语句后，TiDB 会将 `app_order` 的数据放置在配置了 `app` 标签为 `order` 的 TiKV 节点上，将 `app_list` 的数据放置在配置了 `app` 标签为 `list_collection` 的 TiKV 节点上，从而在存储上达到了物理隔离的效果。

## 兼容性说明

### 功能兼容性

- 临时表不支持放置策略。
- 放置策略仅保证静态数据被放置在正确的 TiKV 节点上。该策略不保证传输中的数据（通过用户查询或内部操作）只出现在特定区域内。
- 设置数据的 TiFlash 副本需要通过[构建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)的方式创建，不能使用该特性。
- 设置 `PRIMARY_REGION` 和 `REGIONS` 时允许存在语法糖。但在未来版本中，我们计划为 `PRIMARY_RACK`、`PRIMARY_ZONE` 和 `PRIMARY_HOST` 添加变体支持，见 [issue #18030](https://github.com/pingcap/tidb/issues/18030)。

### 工具兼容性

| 工具名称 | 最低兼容版本 | 说明 |
| --- | --- | --- |
| Backup & Restore (BR) | 6.0 | BR 在 v6.0 之前不支持放置策略的备份与恢复，请参见[恢复 Placement Rule 到集群时为什么会报错？](/faq/backup-and-restore-faq.md#恢复-placement-rule-到集群时为什么会报错) |
| TiDB Lightning | 暂时不兼容 | 导入包含放置策略的数据时会报错 |
| TiCDC | 6.0 | 忽略放置策略，不同步策略到下游集群 |
