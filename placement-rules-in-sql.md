---
title: SQL 中的放置规则
summary: 了解如何使用 SQL 语句调度表和分区的数据放置。
---

# SQL 中的放置规则

SQL 中的放置规则是一项功能，可让你使用 SQL 语句指定数据在 TiKV 集群中的存储位置。通过此功能，你可以将集群、数据库、表或分区的数据调度到特定的区域、数据中心、机架或主机。

此功能可以满足以下使用场景：

- 跨多个数据中心部署数据，并配置规则以优化高可用性策略。
- 合并来自不同应用程序的多个数据库，并在物理上隔离不同用户的数据，满足实例内不同用户的隔离要求。
- 增加重要数据的副本数量，以提高应用程序可用性和数据可靠性。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 概述

通过 SQL 中的放置规则功能，你可以[创建放置策略](#创建和附加放置策略)并为不同级别的数据配置所需的放置策略，粒度从粗到细如下：

| 级别            | 描述                                                                          |
|------------------|--------------------------------------------------------------------------------------|
| 集群          | 默认情况下，TiDB 为集群配置 3 个副本的策略。你可以为集群配置全局放置策略。更多信息，请参见[为集群全局指定副本数量](#为集群全局指定副本数量)。 |
| 数据库         | 你可以为特定数据库配置放置策略。更多信息，请参见[为数据库指定默认放置策略](#为数据库指定默认放置策略)。 |
| 表            | 你可以为特定表配置放置策略。更多信息，请参见[为表指定放置策略](#为表指定放置策略)。 |
| 分区        | 你可以为表中的不同行创建分区，并为分区单独配置放置策略。更多信息，请参见[为分区表指定放置策略](#为分区表指定放置策略)。 |

> **提示：**
>
> *SQL 中的放置规则*的实现依赖于 PD 的*放置规则功能*。详情请参考[配置放置规则](https://docs.pingcap.com/tidb/stable/configure-placement-rules)。在 SQL 中的放置规则上下文中，*放置规则*可能指附加到其他对象的*放置策略*，或从 TiDB 发送到 PD 的规则。

## 限制

- 为简化维护，建议将集群内的放置策略数量限制在 10 个或更少。
- 建议将附加了放置策略的表和分区的总数限制在 10,000 个或更少。为太多表和分区附加策略会增加 PD 的计算工作负载，从而影响服务性能。
- 建议按照本文档提供的示例使用 SQL 中的放置规则功能，而不是使用其他复杂的放置策略。

## 前提条件

放置策略依赖于 TiKV 节点上的标签配置。例如，`PRIMARY_REGION` 放置选项依赖于 TiKV 中的 `region` 标签。

<CustomContent platform="tidb">

当你创建放置策略时，TiDB 不会检查策略中指定的标签是否存在。相反，TiDB 会在你附加策略时执行检查。因此，在附加放置策略之前，请确保每个 TiKV 节点都配置了正确的标签。TiDB Self-Managed 集群的配置方法如下：

```
tikv-server --labels region=<region>,zone=<zone>,host=<host>
```

有关详细配置方法，请参见以下示例：

| 部署方法 | 示例 |
| --- | --- |
| 手动部署 | [使用拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md) |
| 使用 TiUP 部署 | [跨地域部署拓扑](/geo-distributed-deployment-topology.md) |
| 使用 TiDB Operator 部署 | [在 Kubernetes 中配置 TiDB 集群](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-data-high-availability) |

> **注意：**
>
> 对于 TiDB Cloud Dedicated 集群，你可以跳过这些标签配置步骤，因为 TiDB Cloud Dedicated 集群中的 TiKV 节点上的标签是自动配置的。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于 TiDB Cloud Dedicated 集群，TiKV 节点上的标签是自动配置的。

</CustomContent>

要查看当前 TiKV 集群中的所有可用标签，你可以使用 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) 语句：

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

本节介绍如何使用 SQL 语句创建、附加、查看、修改和删除放置策略。

### 创建和附加放置策略

1. 要创建放置策略，使用 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) 语句：

    ```sql
    CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
    ```

    在此语句中：

    - `PRIMARY_REGION="us-east-1"` 选项表示将 Raft Leaders 放置在 `region` 标签为 `us-east-1` 的节点上。
    - `REGIONS="us-east-1,us-west-1"` 选项表示将 Raft Followers 放置在 `region` 标签为 `us-east-1` 和 `region` 标签为 `us-west-1` 的节点上。

    有关可配置的放置选项及其含义，请参见[放置选项参考](#放置选项参考)。

2. 要将放置策略附加到表或分区表，使用 `CREATE TABLE` 或 `ALTER TABLE` 语句为该表或分区表指定放置策略：

    ```sql
    CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
    CREATE TABLE t2 (a INT);
    ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
    ```

   `PLACEMENT POLICY` 不与任何数据库架构关联，可以在全局范围内附加。因此，使用 `CREATE TABLE` 指定放置策略不需要任何额外的权限。

### 查看放置策略

- 要查看现有的放置策略，你可以使用 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) 语句：

    ```sql
    SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
    *************************** 1. row ***************************
           Policy: myplacementpolicy
    Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
    1 row in set (0.00 sec)
    ```

- 要查看附加到特定表的放置策略，你可以使用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 语句：

    ```sql
    SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
    1 row in set (0.00 sec)
    ```

- 要查看集群中放置策略的定义，你可以查询 [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md) 系统表：

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
    SCHEDULE            |
    FOLLOWERS            | 4
    LEARNERS             | 0
    1 row in set
    ```

- 要查看集群中所有附加了放置策略的表，你可以查询 `information_schema.tables` 系统表的 `tidb_placement_policy_name` 列：

    ```sql
    SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- 要查看集群中所有附加了放置策略的分区，你可以查询 `information_schema.partitions` 系统表的 `tidb_placement_policy_name` 列：

    ```sql
    SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- 附加到所有对象的放置策略都是*异步*应用的。要检查放置策略的调度进度，你可以使用 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) 语句：

    ```sql
    SHOW PLACEMENT;
    ```

### 修改放置策略

要修改放置策略，你可以使用 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) 语句。修改将应用于附加了相应策略的所有对象。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

在此语句中，`FOLLOWERS=4` 选项表示为数据配置 5 个副本，包括 4 个 Followers 和 1 个 Leader。有关可配置的放置选项及其含义，请参见[放置选项参考](#放置选项参考)。

### 删除放置策略

要删除未附加到任何表或分区的策略，你可以使用 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) 语句：

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 放置选项参考

创建或修改放置策略时，你可以根据需要配置放置选项。

> **注意：**
>
> `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 选项不能与 `CONSTRAINTS` 选项一起指定，否则会出错。

### 常规放置选项

常规放置选项可以满足数据放置的基本要求。

| 选项名称                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | 指定将 Raft Leaders 放置在 `region` 标签与此选项值匹配的节点上。     |
| `REGIONS`                  | 指定将 Raft Followers 放置在 `region` 标签与此选项值匹配的节点上。 |
| `SCHEDULE`                 | 指定调度 Followers 放置的策略。值选项为 `EVEN`（默认）或 `MAJORITY_IN_PRIMARY`。 |
| `FOLLOWERS`                | 指定 Followers 的数量。例如，`FOLLOWERS=2` 表示数据将有 3 个副本（2 个 Followers 和 1 个 Leader）。 |

### 高级放置选项

高级配置选项为数据放置提供了更大的灵活性，以满足复杂场景的要求。但是，配置高级选项比常规选项更复杂，需要你对集群拓扑和 TiDB 数据分片有深入的了解。

| 选项名称                | 描述                                                                                    |
| --------------| ------------ |
| `CONSTRAINTS`              | 适用于所有角色的约束列表。例如，`CONSTRAINTS="[+disk=ssd]"`。 |
| `LEADER_CONSTRAINTS`       | 仅适用于 Leader 的约束列表。                                      |
| `FOLLOWER_CONSTRAINTS`     | 仅适用于 Followers 的约束列表。                                   |
| `LEARNER_CONSTRAINTS`      | 仅适用于 learners 的约束列表。                                     |
| `LEARNERS`                 | learners 的数量。 |
| `SURVIVAL_PREFERENCE`      | 根据标签的灾难容忍级别的副本放置优先级。例如，`SURVIVAL_PREFERENCE="[region, zone, host]"`。 |

### CONSTRAINTS 格式

你可以使用以下任一格式配置 `CONSTRAINTS`、`FOLLOWER_CONSTRAINTS` 和 `LEARNER_CONSTRAINTS` 放置选项：

| CONSTRAINTS 格式 | 描述 |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| 列表格式  | 如果要指定的约束适用于所有副本，你可以使用键值列表格式。每个键以 `+` 或 `-` 开头。例如：<br/><ul><li>`[+region=us-east-1]` 表示将数据放置在具有 `region` 标签为 `us-east-1` 的节点上。</li><li>`[+region=us-east-1,-type=fault]` 表示将数据放置在具有 `region` 标签为 `us-east-1` 但不具有 `type` 标签为 `fault` 的节点上。</li></ul><br/>  |
| 字典格式 | 如果需要为不同的约束指定不同数量的副本，你可以使用字典格式。例如：<br/><ul><li>`FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 表示在 `us-east-1` 中放置一个 Follower，在 `us-east-2` 中放置一个 Follower，在 `us-west-1` 中放置一个 Follower。</li><li>`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';` 表示在位于 `us-east-1` 区域且具有 `type` 标签为 `scale-node` 的节点上放置一个 Follower，在 `us-west-1` 中放置一个 Follower。</li></ul>字典格式支持每个键以 `+` 或 `-` 开头，并允许你配置特殊的 `#evict-leader` 属性。例如，`FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}'` 表示在灾难恢复期间，将尽可能驱逐 `us-west-1` 中的 Leaders。|

> **注意：**
>
> - `LEADER_CONSTRAINTS` 放置选项仅支持列表格式。
> - 列表和字典格式都基于 YAML 解析器，但在某些情况下可能会错误解析 YAML 语法。例如，`"{+region=east:1,+region=west:2}"` （`:` 后没有空格）可能会被错误解析为 `'{"+region=east:1": null, "+region=west:2": null}'`，这是意外的。但是，`"{+region=east: 1,+region=west: 2}"` （`:` 后有空格）可以被正确解析为 `'{"+region=east": 1, "+region=west": 2}'`。因此，建议在 `:` 后添加空格。
## 基本示例

### 为集群全局指定副本数量

集群初始化后，默认副本数为 `3`。如果集群需要更多副本，你可以通过配置放置策略来增加这个数量，然后使用 [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md) 在集群级别应用该策略。例如：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

注意，由于 TiDB 默认 Leaders 数量为 `1`，`five replicas` 表示 `4` 个 Followers 和 `1` 个 Leader。

### 为数据库指定默认放置策略

你可以为数据库指定默认放置策略。这类似于为数据库设置默认字符集或排序规则。如果数据库中的表或分区没有指定其他放置策略，则数据库的放置策略将应用于该表和分区。例如：

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- 创建放置策略

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- 创建表 t1，未指定任何放置策略。

ALTER DATABASE test PLACEMENT POLICY=p2;  -- 更改数据库的默认放置策略为 p2，不会应用于现有表 t1。

CREATE TABLE t2 (a INT);  -- 创建表 t2。默认放置策略 p2 应用于 t2。

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- 创建表 t3。因为此语句指定了另一个放置规则，默认放置策略 p2 不会应用于表 t3。

ALTER DATABASE test PLACEMENT POLICY=p3;  -- 再次更改数据库的默认策略，不会应用于现有表。

CREATE TABLE t4 (a INT);  -- 创建表 t4。默认放置策略 p3 应用于 t4。

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- `FOLLOWERS=3` 应用于附加了策略 p3 的表（即表 t4）。
```

注意，表到其分区的策略继承与上述示例中的策略继承不同。当你更改表的默认策略时，新策略也会应用于该表中的分区。但是，只有在创建表时未指定任何策略时，表才会从数据库继承策略。一旦表从数据库继承了策略，修改数据库的默认策略不会应用于该表。

### 为表指定放置策略

你可以为表指定默认放置策略。例如：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- 创建表 t 并将 'five_replicas' 放置策略附加到它。

ALTER TABLE t PLACEMENT POLICY=default; -- 从表 t 移除 'five_replicas' 放置策略，并重置为默认放置策略。
```

### 为分区表指定放置策略

你也可以为分区表或分区指定放置策略。例如：

```sql
CREATE PLACEMENT POLICY storageforhisotrydata CONSTRAINTS="[+node=history]";
CREATE PLACEMENT POLICY storagefornewdata CONSTRAINTS="[+node=new]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageforhisotrydata,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storagefornewdata
);
```

如果表中的分区没有指定放置策略，该分区会尝试从表继承策略（如果有）。在上述示例中：

- `p0` 分区将应用 `storageforhisotrydata` 策略。
- `p4` 分区将应用 `storagefornewdata` 策略。
- `p1`、`p2` 和 `p3` 分区将应用从表 `t1` 继承的 `companystandardpolicy` 放置策略。
- 如果没有为表 `t1` 指定放置策略，`p1`、`p2` 和 `p3` 分区将继承数据库默认策略或全局默认策略。

在这些分区附加了放置策略后，你可以像下面的示例一样更改特定分区的放置策略：

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhisotrydata;
```
## 高可用性示例

假设有一个集群具有以下拓扑结构，其中 TiKV 节点分布在 3 个区域，每个区域包含 3 个可用区：

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

如果你不特别关心具体的数据分布，但优先考虑满足灾难恢复要求，你可以使用 `SURVIVAL_PREFERENCES` 选项来指定数据生存偏好。

如上例所示，TiDB 集群分布在 3 个区域，每个区域包含 3 个可用区。在为此集群创建放置策略时，假设你按如下方式配置 `SURVIVAL_PREFERENCES`：

```sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

创建放置策略后，你可以根据需要将它们附加到相应的表：

- 对于附加了 `multiaz` 放置策略的表，数据将放置在不同区域的 3 个副本中，优先满足跨区域的数据隔离生存目标，其次是跨可用区的生存目标，最后是跨主机的生存目标。
- 对于附加了 `singleaz` 放置策略的表，数据将首先放置在 `us-east-1` 区域的 3 个副本中，然后满足跨可用区的数据隔离生存目标。

<CustomContent platform="tidb">

> **注意：**
>
> `SURVIVAL_PREFERENCES` 等同于 PD 中的 `location-labels`。更多信息，请参见[使用拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> `SURVIVAL_PREFERENCES` 等同于 PD 中的 `location-labels`。更多信息，请参见[使用拓扑 label 进行副本调度](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)。

</CustomContent>

### 指定跨多个数据中心按 2:2:1 分布的 5 副本集群

如果你需要特定的数据分布，例如按 2:2:1 的比例分布的 5 个副本，你可以通过使用[字典格式](#constraints-格式)配置这些 `CONSTRAINTS` 来为不同的约束指定不同数量的副本：

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

在为集群设置全局 `deploy221` 放置策略后，TiDB 会按照此策略分布数据：在 `us-east-1` 区域放置两个副本，在 `us-east-2` 区域放置两个副本，在 `us-west-1` 区域放置一个副本。

### 指定 Leaders 和 Followers 的分布

你可以使用约束或 `PRIMARY_REGION` 指定 Leaders 和 Followers 的特定分布。

#### 使用约束

如果你对 Raft Leaders 在节点间的分布有特定要求，可以使用以下语句指定放置策略：

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1: 1}';
```

创建此放置策略并附加到所需数据后，数据的 Raft Leader 副本将放置在 `LEADER_CONSTRAINTS` 选项指定的 `us-east-1` 区域，而其他副本将放置在 `FOLLOWER_CONSTRAINTS` 选项指定的区域。注意，如果集群发生故障，例如 `us-east-1` 区域的节点宕机，仍然会从其他区域选举新的 Leader，即使这些区域在 `FOLLOWER_CONSTRAINTS` 中指定。换句话说，确保服务可用性具有最高优先级。

如果在 `us-east-1` 区域发生故障时，你不希望在 `us-west-1` 放置新的 Leaders，你可以配置特殊的 `evict-leader` 属性来驱逐该区域中新选举的 Leaders：

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}';
```

#### 使用 `PRIMARY_REGION`

如果在集群拓扑中配置了 `region` 标签，你也可以使用 `PRIMARY_REGION` 和 `REGIONS` 选项为 Followers 指定放置策略：

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

- `PRIMARY_REGION` 指定 Leaders 的分布区域。你只能在此选项中指定一个区域。
- `SCHEDULE` 选项指定 TiDB 如何平衡 Followers 的分布。
    - 默认的 `EVEN` 调度规则确保 Followers 在所有区域中均匀分布。
    - 如果你想确保在 `PRIMARY_REGION`（即 `us-east-1`）中放置足够数量的 Follower 副本，你可以使用 `MAJORITY_IN_PRIMARY` 调度规则。此调度规则以牺牲一些可用性为代价提供较低延迟的事务。如果主要区域发生故障，`MAJORITY_IN_PRIMARY` 不提供自动故障转移。
## 数据隔离示例

如下例所示，在创建放置策略时，你可以为每个策略配置一个约束，要求将数据放置在具有指定 `app` 标签的 TiKV 节点上。

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

在此示例中，约束使用列表格式指定，如 `[+app=order]`。你也可以使用字典格式指定它们，如 `{+app=order: 3}`。

执行示例中的语句后，TiDB 将把 `app_order` 数据放置在 `app` 标签为 `order` 的 TiKV 节点上，把 `app_list` 数据放置在 `app` 标签为 `list_collection` 的 TiKV 节点上，从而在存储中实现物理数据隔离。

## 兼容性

## 与其他功能的兼容性

- 临时表不支持放置策略。
- 放置策略仅确保静态数据位于正确的 TiKV 节点上，但不保证传输中的数据（通过用户查询或内部操作）仅在特定区域中发生。
- 要为数据配置 TiFlash 副本，你需要[创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)而不是使用放置策略。
- 允许为设置 `PRIMARY_REGION` 和 `REGIONS` 使用语法糖规则。未来，我们计划为 `PRIMARY_RACK`、`PRIMARY_ZONE` 和 `PRIMARY_HOST` 添加变体。参见 [issue #18030](https://github.com/pingcap/tidb/issues/18030)。

## 与工具的兼容性

<CustomContent platform="tidb">

| 工具名称 | 最低支持版本 | 描述 |
| --- | --- | --- |
| Backup & Restore (BR) | 6.0 | 6.0 版本之前，BR 不支持备份和恢复放置策略。更多信息，请参见[为什么在恢复放置规则到集群时出错](/faq/backup-and-restore-faq.md#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster)。 |
| TiDB Lightning | 尚未兼容 | 当 TiDB Lightning 导入包含放置策略的备份数据时会报错  |
| TiCDC | 6.0 | 忽略放置策略，不会将策略复制到下游 |
| TiDB Binlog | 6.0 | 忽略放置策略，不会将策略复制到下游 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 工具名称 | 最低支持版本 | 描述 |
| --- | --- | --- |
| TiDB Lightning | 尚未兼容 | 当 TiDB Lightning 导入包含放置策略的备份数据时会报错  |
| TiCDC | 6.0 | 忽略放置策略，不会将策略复制到下游 |

</CustomContent>
